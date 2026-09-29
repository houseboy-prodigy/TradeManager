"""Manual trade desk storage.

Telegram used to turn a chat message into a trade object. This module does that
for the web form and stores the trade in Postgres, without calling KuCoin.
"""

import json
import sys

import psycopg2
from psycopg2.extras import RealDictCursor

import messageProcess

DATABASE_DSN = "host=127.0.0.1 port=5432 dbname=postgres user=postgres password=p1a9v6a3n"


def connect():
    return psycopg2.connect(DATABASE_DSN)


def ensure_table(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS "TradeDetails" (
              "tradeId" SERIAL PRIMARY KEY,
              currency TEXT,
              "TP" DOUBLE PRECISION[],
              "SL" DOUBLE PRECISION,
              entry DOUBLE PRECISION[],
              side TEXT,
              profit DOUBLE PRECISION,
              "TP_hit" INTEGER,
              done BOOLEAN,
              "TP_len" INTEGER
            )
            """
        )
    conn.commit()


def _as_float(value):
    return float(str(value).replace(",", "").strip())


def derive_side(take_profits):
    if len(take_profits) < 2:
        raise ValueError("At least two take-profit levels are required.")
    return "buy" if take_profits[0] < take_profits[1] else "sell"


def normalize_trade(data):
    if not isinstance(data, dict):
        raise ValueError("Trade must be an object.")

    curr = str(data.get("curr") or data.get("Curr") or "").strip().upper()
    if "/" in curr:
        curr = curr.split("/", 1)[0]
    if "BTC" in curr:
        curr = "XBT"
    if not curr:
        raise ValueError("Pair is required.")

    entry_values = data.get("entry") or data.get("Entry") or []
    tp_values = data.get("tp") or data.get("TP") or []
    if not isinstance(entry_values, (list, tuple)) or not isinstance(tp_values, (list, tuple)):
        raise ValueError("Entry and take-profit must be lists of prices.")

    entry = [_as_float(value) for value in entry_values if str(value).strip()]
    take_profits = [_as_float(value) for value in tp_values if str(value).strip()]
    if len(entry) < 2:
        raise ValueError("Entry zone needs a low and a high price.")
    stop_loss = _as_float(data.get("sl") if data.get("sl") is not None else data.get("SL"))

    requested_side = str(data.get("side") or "").strip().lower()
    side = requested_side or derive_side(take_profits)
    if side not in ("buy", "sell"):
        raise ValueError("Side must be buy or sell.")

    return {
        "curr": curr,
        "entry": entry,
        "tp": take_profits,
        "sl": stop_loss,
        "side": side,
    }


def parse_signal(message):
    if not isinstance(message, str) or not message.strip():
        raise ValueError("Paste a signal first.")
    parsed = messageProcess.processMessage(message)
    return normalize_trade(
        {
            "curr": parsed.get("Curr"),
            "entry": parsed.get("entry"),
            "tp": parsed.get("TP"),
            "sl": parsed.get("SL"),
            "side": parsed.get("side"),
        }
    )


def row_to_trade(row):
    return {
        "tradeId": row["tradeId"],
        "curr": row["currency"],
        "entry": list(row["entry"] or []),
        "tp": list(row["TP"] or []),
        "sl": row["SL"],
        "side": row["side"],
        "done": row["done"],
    }


def list_trades():
    with connect() as conn:
        ensure_table(conn)
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT "tradeId", currency, "TP", "SL", entry, side, done
                FROM "TradeDetails"
                WHERE done IS NOT TRUE
                ORDER BY "tradeId" DESC
                """
            )
            return [row_to_trade(row) for row in cur.fetchall()]


def put_trade(data):
    trade = normalize_trade(data)
    with connect() as conn:
        ensure_table(conn)
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO "TradeDetails"
                  (currency, "TP", "SL", entry, side, profit, "TP_hit", done, "TP_len")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING "tradeId", currency, "TP", "SL", entry, side, done
                """,
                (
                    trade["curr"],
                    trade["tp"],
                    trade["sl"],
                    trade["entry"],
                    trade["side"],
                    0,
                    0,
                    False,
                    len(trade["tp"]),
                ),
            )
            saved = row_to_trade(cur.fetchone())
        conn.commit()
    return saved


def main(argv):
    command = argv[1] if len(argv) > 1 else ""
    raw = sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}

    if command == "list":
        result = {"trades": list_trades()}
    elif command == "put":
        result = put_trade(payload)
    elif command == "parse":
        result = parse_signal(payload.get("message", ""))
    else:
        raise ValueError("Unknown command.")

    print(json.dumps(result))


if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as exc:
        print(json.dumps({"status": "error", "message": str(exc)}))
        sys.exit(1)

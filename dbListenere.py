import time
import threading
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.sql import text
from sqlalchemy import create_engine, Column, Integer, String, select, update, Boolean, Float, ARRAY
from controlCenter import dreamerEntryBotManual
# DB Connection: create_engine(DBMS_name+driver://<username>:Password@619@<hostname>/<database_name>)
engine = create_engine('postgresql+psycopg2://postgres:p1a9v6a3n\
@localhost:5432/postgres')
from dbOps import TradeDetails
def dbListener():
    last_processed_id = -1

    while True:
        with Session(engine) as session:
            # Fetch the latest row from the database
            result = session.query(TradeDetails).order_by(TradeDetails.tradeId.desc()).first()


        if result and result.tradeId > last_processed_id:
            # Process the row and create a tradeObj
            tradeObj = createTradeObjFromRow(result)

            # Call the same operations as in dreamerEntryBot
            handle_trade(tradeObj)

            # Update the last_processed_id
            last_processed_id = result.tradeId

        # Wait for a certain period before checking for new rows again
        time.sleep(10)

def createTradeObjFromRow(row):
    # Convert the row data to a tradeObj dictionary
    #{'Curr': 'XRP ', 'TP': ['0.4640', '0.4594', '0.4546', '0.4476', '0.4406', '0.4313'], 'SL': '0.4920','entry': ['0.4688 ', ' 0.4780'], 'side': 'sell'}
    tradeObj = {
        'Curr': row.currency,
        'TP': row.TP,
        'SL': row.SL,
        'entry': row.entry,
        'side': row.side
        # Add other fields as required
    }
    return tradeObj

def handle_trade(tradeObj):
    # Your existing dreamerEntryBot operations here
    thread = threading.Thread(target=dreamerEntryBotManual, args=(tradeObj,))
    thread.start()


dbListener()
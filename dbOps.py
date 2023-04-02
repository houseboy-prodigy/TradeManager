# my_module.py

# NOTE: Drop the address & user_account tables before running this script

from sqlalchemy import create_engine, Column, Integer, String, select, update, Boolean, Float
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import sessionmaker
import controlCenter
from sqlalchemy.engine import reflection

# DB Connection: create_engine(DBMS_name+driver://<username>:Password@619@<hostname>/<database_name>)
engine = create_engine('postgresql+psycopg2://postgres:p1a9v6a3n\
@localhost:5432/postgres')
base = declarative_base()

def testFunction(arg1):
    return arg1
def getTrade(pair):
    # Your function implementation here
    # Simple Queries Query 1 and Query 2
    session = Session(engine)
    stmt = select(TradeDetails).where(TradeDetails.currency==pair)
    # Execute the query and fetch the single result
    curr = session.execute(stmt).one_or_none()
    trade = curr[0]
    if trade:
        trade_dict = trade.as_dict()
        return trade_dict

    else:
        return 'none'

    session.close()


'''
def putTradeintoDB(curr, entry, tp, sl, side):
    print('called')
    # Your function implementation here
    try:
        with Session(engine) as session:

            trade = TradeDetails(
                currency=curr,
                entry=entry,
                TP=tp,
                SL=sl,
                side=side,
                profit=0,
                TP_hit="",
                done=False
            )
            session.add_all([trade])
            session.commit()
        print('done')
        session.close()
        return {"status": "success"}
    except Exception as e:
        session.rollback()
        session.close()
        return {"status": "error", "message": str(e)}

'''
'''
# Define a function to update a customer
def updateTrade(id, email):
    try:
        Session = sessionmaker(bind=engine)
        with Session() as session:
            # Create an update statement for the Customers table
            stmt = update(Customer).where(Customer.CustomerID == id).values(cEmail=email)

            # Execute the statement
            session.execute(stmt)

            # Commit the transaction
            session.commit()
            return {"status": "success", "CustomerID": id}
    except Exception as e:

        return {"status": "error", "message": str(e)}
        
'''
def getAllTrades():
    # Create a session to interact with the database
    session = Session(engine)

    # Define the query to select all TradeDetails where done is False
    stmt = select(TradeDetails).where(TradeDetails.done == False)

    # Execute the query and fetch all results
    trades = session.execute(stmt).fetchall()

    # Create a list to store the trade dictionaries
    trades_list = []

    # Iterate through the trades and convert them to dictionaries
    for trade_row in trades:
        trade = trade_row[0]
        trade_dict = trade.as_dict()
        trades_list.append(trade_dict)

    # Close the session
    session.close()

    # Return the list of trade dictionaries
    return trades_list


# Define Classes/Tables
class TradeDetails(base):
    __tablename__ = 'TradeDetails'
    tradeId = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String)
    TP = Column(ARRAY(Float))
    SL = Column(Float)
    entry = Column(ARRAY(Float))
    side = Column(String)
    profit = Column(Float)
    TP_hit = Column(Integer)
    done = Column(Boolean)
    TP_len = Column(Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def putTrad(curr, entry, tp, sl, side):
    # Your function implementation here
    try:
        with Session(engine) as session:
            C12 = TradeDetails(
                currency=curr,
                entry=entry,
                TP=tp,
                SL=sl,
                side=side,
                profit=0,
                TP_hit=0,
                done=False,
                TP_len=len(tp)
            )
            session.add_all([C12])
            session.commit()
            return {"status": "success", "CustomerID": C12.currency}
    except Exception as e:
        return {"status": "error", "message": str(e)}
'''
with Session(engine) as session:

    C12 = Customer(
        CustomerID="C31",
        cName="Jose",
        cEmail="Jose44@outlook.com",
        cAddress="8112 Skokie Blvd",
        cPassword="Arcade786"
    )
    session.add_all([C12])
    session.commit()
'''
#print(getTrade('C01'))
#print(updateTrade('C01','Jose43@outlook.com'))
#print(getTrade('C01'))
#print(putTrade("Cuu", "a", "b", "c", "buy"))

#tradeObj = {'Curr': 'ART', 'TP': [0.941, 0.950, 0.959, 0.978, 1.006], 'SL': 0.904, 'entry': [0.932,0.920], 'side': 'buy'}
#print(putTrad(tradeObj['Curr'], tradeObj['entry'], tradeObj['TP'], tradeObj['SL'], tradeObj['side']))

#print(getAllTrades())
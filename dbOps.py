# my_module.py

# NOTE: Drop the address & user_account tables before running this script

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, select, Float, update
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.orm import sessionmaker
from controlCenter import dreamerEntryBotManual
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
    stmt = select(Customer).where(Customer.CustomerID==pair)
    # Execute the query and fetch the single result
    user = session.execute(stmt).one_or_none()
    customer = user[0]
    if user:
        user_dict = customer.as_dict()
        return user_dict

    else:
        return 'none'

    session.close()

def putTradeintoDB(curr, entry, tp, sl, side):
    # Your function implementation here
    try:
        with Session(engine) as session:
            C12 = Customer(
                CustomerID="C77",
                cName=curr,
                cEmail=entry,
                cAddress=tp,
                cPassword=sl
            )
            session.add_all([C12])
            session.commit()
            return {"status": "success", "CustomerID": C12.CustomerID}
    except Exception as e:
        return {"status": "error", "message": str(e)}


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
# Define Classes/Tables
class Customer(base):
    __tablename__ = "Customers"
    CustomerID = Column(String(10), primary_key=True)
    cName = Column(String(40))
    cEmail = Column(String(50))
    cAddress = Column(String(50))
    cPassword = Column(String(40))

    def __repr__(self):
        return "Customer(CustomerID={!r}, cName={!r}, cEmail={!r}, cAddress={!r}, cPassword={!r})".format(
            self.CustomerID, self.cName, self.cEmail, self.cAddress, self.cPassword
        )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

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
tradeObj = {
    'Curr': 'ARB',
    'TP': ['0.941', '0.950', '0.959', '0.978', '1.006'],
    'SL': '0.904',
    'entry': ['0.922', '0.920'],
    'side': 'buy'
}

#dreamerEntryBotManual(tradeObj)
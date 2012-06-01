from sqlalchemy import Column, Integer, String, create_engine, DATE, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey

engine = create_engine('sqlite:///test.sqlite', echo=True)

Base = declarative_base()

class Fund(Base):
    __tablename__ = 'funds'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    name = Column(String)

    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return "<Fund('%s = %s')>" % (self.symbol, self.name)

class HistoricalPrice(Base):
    __tablename__ = 'historicalprices'
    id = Column(Integer, primary_key=True)
    date = Column(DATE) 
    price = Column(Float)
    fund_id = Column(Integer, ForeignKey('funds.id'))
    fund = relationship('Fund', backref=backref('historicalprices', order_by=id))

    def __init__(self, date, price)
        self.date = date
        self.price = price

    def __repr__(self):
        return "<HistoricalPrice(%s - %s)>" % (self.date, self.price)

Base.metadata.create_all(engine)

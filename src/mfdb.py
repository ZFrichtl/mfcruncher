import sqlalchemy
import sqlalchemy.ext.declarative

engine = sqlalchemy.create_engine('sqlite:///test.sqlite', echo=True)

Base = sqlalchemy.ext.declarative.declarative_base()

class Fund(Base):
    __tablename__ = 'funds'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    symbol = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return "<Fund('%s = %s')>" % (self.symbol, self.name)

class HistoricalPrice(Base):
    __tablename__ = 'historicalprices'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    date = sqlalchemy.Column(sqlalchemy.DATE) 
    price = sqlalchemy.Column(sqlalchemy.Float)
    fund_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('funds.id'))
    fund = sqlalchemy.orm.relationship('Fund', backref=sqlalchemy.orm.backref('historicalprices', order_by=id))

    def __init__(self, date, price):
        self.date = date
        self.price = price

    def __repr__(self):
        return "<HistoricalPrice(%s - %s)>" % (self.date, self.price)

Base.metadata.create_all(engine)

import urllib
import re
import sys
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

__Base = sqlalchemy.ext.declarative.declarative_base()
class Fund(__Base):
    __tablename__ = 'Funds'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    symbol = sqlalchemy.Column(sqlalchemy.String, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name

    def __repr__(self):
        return "<Fund('%s = %s')>" % (self.symbol, self.name)

class FundTable(object):
    def __init__(self, session):
        self.session = session
    def add(self, fund):
        if not isinstance(fund, Fund):
            raise TypeError
        if self.session.query(Fund).filter_by(symbol=fund.symbol).count() == 0:
            self.session.add(fund)
    def getFunds(self):
        return self.session.query(Fund)


class FundDataSource(__Base):
    __tablename__ = 'FundDataSources'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    fund_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Funds.id'))
    fund = sqlalchemy.orm.relationship('Fund', backref=sqlalchemy.orm.backref('FundDataSources', order_by=id))
    url = sqlalchemy.Column(sqlalchemy.String)
    def __init__(self, url):
        self.url = url

class HistoricalPrice(__Base):
    __tablename__ = 'HistoricalPrices'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    date = sqlalchemy.Column(sqlalchemy.Date, unique=True)
    price = sqlalchemy.Column(sqlalchemy.Float)
    fund_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Funds.id'))
    fund = sqlalchemy.orm.relationship('Fund', backref=sqlalchemy.orm.backref('HistoricalPrices', order_by=id))
    def __init__(self, date, price):
        self.date = date
        self.price = price


class Availability(__Base):
    __tablename__ = 'Availability'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
    fund_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Funds.id'))
    fund = sqlalchemy.orm.relationship('Fund', backref=sqlalchemy.orm.backref('Availability', order_by=id))
    name = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, name):
        self.name = name

def createFundTable(filename):
    engine = sqlalchemy.create_engine('sqlite:///' + filename, echo=True)
    __Base.metadata.create_all(engine)
    return engine

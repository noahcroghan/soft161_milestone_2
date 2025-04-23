from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Persisted = declarative_base()


class User(Persisted):
    __tablename__ = 'users'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(String(256), nullable=False)


class Portfolio(Persisted):
    __tablename__ = 'portfolios'
    portfolio_id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    crypto_id = Column(Integer, ForeignKey('cryptocurrencies.crypto_id'), nullable=False)
    coin_amount = Column(Float, nullable=False)
    purchase_date = Column(Date, nullable=False)
    initial_investment_amount = Column(Float, nullable=False)


class Cryptocurrency(Persisted):
    __tablename__ = 'cryptocurrencies'
    crypto_id = Column(Integer, autoincrement=True, primary_key=True)
    crypto_name = Column(String(256), nullable=False)
    crypto_symbol = Column(String(256), nullable=False)
    crypto_value = Column(Float, nullable=False)


class PortfolioTrackerDatabase(object):
    @staticmethod
    def construct_mysql_url(authority, port, database, username, password):
        return f'mysql+mysqlconnector://{username}:{password}@{authority}:{port}/{database}'

    @staticmethod
    def construct_in_memory_url():
        return 'sqlite:///'

    def __init__(self, url):
        self.engine = create_engine(url)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    def ensure_tables_exist(self):
        Persisted.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()

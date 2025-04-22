from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, Date, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker

from config import password, port, username

Persisted = declarative_base()


class User(Persisted):
    __tablename__ = 'users'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(String(30), nullable=False)


class Portfolio(Persisted):
    __tablename__ = 'portfolios'
    portfolio_id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    crypto_id = Column(Integer, ForeignKey('cryptocurrencies.crypto_id'), nullable=False)
    coin_amount = Column(Numeric(20, 8), nullable=False)
    purchase_date = Column(Date, nullable=False)
    initial_investment_amount = Column(Numeric(20, 8), nullable=False)


class Cryptocurrency(Persisted):
    __tablename__ = 'cryptocurrencies'
    crypto_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    symbol = Column(String(15), nullable=False)
    current_price = Column(Numeric(20, 8), nullable=False)
    percent_change_24h = Column(Numeric(20, 8))


class HistoricalPrice(Persisted):
    __tablename__ = 'historical_prices'
    id = Column(Integer, primary_key=True)
    crypto_id = Column(Integer, ForeignKey('cryptocurrencies.crypto_id'), nullable=False)
    date = Column(Date, nullable=False)
    price = Column(Numeric(20, 8), nullable=False)


class CryptoDatabase(object):
    @staticmethod
    def construct_mysql_url(authority, database):
        return f'mysql+mysqlconnector://{username}:{password}@{authority}:{port}/{database}'

    @staticmethod
    def construct_in_memory_url():
        return 'sqlite:///'

    @staticmethod
    def get_session():
        url = CryptoDatabase.construct_mysql_url('localhost', 'crypto')
        crypto_database = CryptoDatabase(url)
        return crypto_database.create_session()

    def __init__(self, url):
        self.engine = create_engine(url)
        self.Session = sessionmaker(bind=self.engine)

    def ensure_tables_exist(self):
        Persisted.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()

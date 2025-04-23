from sqlalchemy import Integer, Column, String, Double, Date, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from config import password, port, username

Persisted = declarative_base()


class Cryptocurrency(Persisted):
    __tablename__ = 'cryptocurrencies'
    coingecko_id = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    symbol = Column(String(15), nullable=False)
    current_price = Column(Double, nullable=False)
    percent_change_24h = Column(Double)
    historical_prices = relationship("HistoricalPrice", back_populates="cryptocurrency")


class HistoricalPrice(Persisted):
    __tablename__ = 'historical_prices'
    id = Column(Integer, primary_key=True)
    coingecko_id = Column(String(50), ForeignKey('cryptocurrencies.coingecko_id'), nullable=False)
    date = Column(Date, nullable=False)
    price = Column(Double, nullable=False)
    cryptocurrency = relationship("Cryptocurrency", back_populates="historical_prices")


class CryptoDatabase(object):
    @staticmethod
    def construct_mysql_url(authority, port, database, username, password):
        return f'mysql+mysqlconnector://{username}:{password}@{authority}:{port}/{database}'

    @staticmethod
    def construct_in_memory_url():
        return 'sqlite:///'

    @staticmethod
    def get_session():
        url = CryptoDatabase.construct_mysql_url('localhost', port, 'crypto', username, password)
        crypto_database = CryptoDatabase(url)
        return crypto_database.create_session()

    def __init__(self, url):
        self.engine = create_engine(url)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

    def ensure_tables_exist(self):
        Persisted.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()

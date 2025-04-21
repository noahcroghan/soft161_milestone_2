from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Symbol(Base):
    __tablename__ = 'symbols'
    symbol_id = Column(String(10), primary_key=True)
    crypto_id = Column(String(256), ForeignKey('watchlist.crypto_id'))


class Watchlist(Base):
    __tablename__ = 'watchlist'
    crypto_id = Column(String(256), primary_key=True)
    symbol_id = Column(String(10), ForeignKey('symbols.crypto_id'))
    price = Column(Integer)


class CryptoDatabase(object):
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
        Base.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()

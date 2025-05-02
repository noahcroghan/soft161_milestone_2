from urllib.parse import quote_plus

from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, Date, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker

try:
    from config import username, password, port
except ImportError:
    print(
        "Failed to get values from config.py. Please follow the instructions in the README. Ensure all values are set.")
    username = None
    password = None
    port = None
    exit(1)

Persisted = declarative_base()


class User(Persisted):
    __tablename__ = 'users'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(String(30), nullable=False, unique=True)


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
    coingecko_id = Column(String(50), nullable=False)


class HistoricalPrice(Persisted):
    __tablename__ = 'historical_prices'
    historical_price_id = Column(Integer, primary_key=True)
    crypto_id = Column(Integer, ForeignKey('cryptocurrencies.crypto_id'), nullable=False)
    date = Column(Date, nullable=False)
    open_price = Column(Numeric(20, 8), nullable=False)
    high_price = Column(Numeric(20, 8), nullable=False)
    low_price = Column(Numeric(20, 8), nullable=False)
    close_price = Column(Numeric(20, 8), nullable=False)


class CryptoDatabase(object):
    @staticmethod
    def construct_mysql_url():
        password_encoded = quote_plus(password)
        return f'mysql+mysqlconnector://{username}:{password_encoded}@localhost:{port}/crypto'

    @staticmethod
    def construct_in_memory_url():
        return 'sqlite:///'

    @staticmethod
    def get_session():
        url = CryptoDatabase.construct_mysql_url()
        crypto_database = CryptoDatabase(url)
        return crypto_database.create_session()

    def __init__(self, url):
        self.engine = create_engine(url)
        self.Session = sessionmaker(bind=self.engine)

    def ensure_tables_exist(self):
        # --- BEGIN: Drop and recreate the database for testing only ---
        print('Dropping and recreating database.')
        from sqlalchemy import text
        password_encoded = quote_plus(password)
        temp_engine = create_engine(f'mysql+mysqlconnector://{username}:{password_encoded}@localhost:{port}',
                                    isolation_level="AUTOCOMMIT")
        with temp_engine.connect() as conn:
            conn.execute(text("DROP DATABASE IF EXISTS crypto"))
            conn.execute(text("CREATE DATABASE crypto"))
        self.engine = create_engine(self.construct_mysql_url())
        self.Session = sessionmaker(bind=self.engine)
        # --- END: Drop and recreate the database for testing only ---

        Persisted.metadata.create_all(self.engine)

    def create_session(self):
        return self.Session()

    def create_user(self, new_username):
        if not new_username:
            return None

        session = self.create_session()
        existing_user = session.query(User).filter(User.user_name == new_username).first()
        if existing_user:
            return None
        user = User(user_name=new_username)
        session.add(user)
        session.commit()
        return user.user_name

    @staticmethod
    def get_all_usernames():
        session = CryptoDatabase.get_session()
        users = session.query(User).all()
        return [user.user_name for user in users]

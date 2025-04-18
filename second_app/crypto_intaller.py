from datetime import date
from sys import stderr

from sqlalchemy.exc import SQLAlchemyError

from config import port, password, username
from cryptocurrencies import CryptoDatabase, Cryptocurrency, HistoricalPrice


def add_starter_data(session):
    session.add_all([Cryptocurrency(coingecko_id='bitcoin', name='Bitcoin', symbol='BTC', current_price=50000.00,
                                    percent_change_24h=-2.5),
                     Cryptocurrency(coingecko_id='ethereum', name='Ethereum', symbol='ETH', current_price=4000.00,
                                    percent_change_24h=3.1),
                     Cryptocurrency(coingecko_id='cardano', name='Cardano', symbol='ADA', current_price=1.25,
                                    percent_change_24h=0.8),
                     Cryptocurrency(coingecko_id='solana', name='Solana', symbol='SOL', current_price=150.00,
                                    percent_change_24h=-1.2),
                     Cryptocurrency(coingecko_id='dogecoin', name='Dogecoin', symbol='DOGE', current_price=0.30,
                                    percent_change_24h=5.0),

                     HistoricalPrice(coingecko_id='bitcoin', date=date(2025, 4, 14), price=51000.00),
                     HistoricalPrice(coingecko_id='bitcoin', date=date(2025, 4, 13), price=51500.00),
                     HistoricalPrice(coingecko_id='ethereum', date=date(2025, 4, 14), price=3950.00),
                     HistoricalPrice(coingecko_id='ethereum', date=date(2025, 4, 13), price=3900.00),
                     HistoricalPrice(coingecko_id='cardano', date=date(2025, 4, 14), price=1.20),
                     HistoricalPrice(coingecko_id='cardano', date=date(2025, 4, 13), price=1.22),
                     HistoricalPrice(coingecko_id='solana', date=date(2025, 4, 14), price=152.00),
                     HistoricalPrice(coingecko_id='solana', date=date(2025, 4, 13), price=155.00),
                     HistoricalPrice(coingecko_id='dogecoin', date=date(2025, 4, 14), price=0.28),
                     HistoricalPrice(coingecko_id='dogecoin', date=date(2025, 4, 13), price=0.27)])


def main():
    try:
        url = CryptoDatabase.construct_mysql_url('localhost', port, 'crypto', username, password)
        crypto_database = CryptoDatabase(url)
        crypto_database.ensure_tables_exist()
        print('Tables created.')
        session = crypto_database.create_session()
        add_starter_data(session)
        session.commit()
        print('Records created.')
    except SQLAlchemyError as exception:
        print('Database setup failed!', file=stderr)
        print(f'Cause: {exception}', file=stderr)
        exit(1)


if __name__ == "__main__":
    main()
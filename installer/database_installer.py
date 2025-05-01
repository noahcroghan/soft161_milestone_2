from datetime import date
from sys import stderr

from pycoingecko import CoinGeckoAPI
from sqlalchemy.exc import SQLAlchemyError

from installer.database import CryptoDatabase, Cryptocurrency, HistoricalPrice, User

coin_gecko_api = CoinGeckoAPI()
coins_list = coin_gecko_api.get_coins_markets(vs_currency='usd')


def add_starter_data(session):
    # TODO: This is incomplete. It should get starter data from the API.
    for coin_details in coins_list:
        session.add(Cryptocurrency(name=coin_details['name'], symbol=coin_details['symbol'].upper(),
                                   current_price=coin_details['current_price'],
                                   percent_change_24h=coin_details['price_change_percentage_24h']))

    session.add_all([HistoricalPrice(crypto_id=1, date=date(2025, 4, 14), open_price=50500.00, high_price=51500.00,
                                     low_price=50000.00, close_price=51000.00),
                     HistoricalPrice(crypto_id=1, date=date(2025, 4, 13), open_price=51000.00, high_price=52000.00,
                                     low_price=50500.00, close_price=51500.00),
                     HistoricalPrice(crypto_id=2, date=date(2025, 4, 14), open_price=3900.00, high_price=4000.00,
                                     low_price=3850.00, close_price=3950.00),
                     HistoricalPrice(crypto_id=2, date=date(2025, 4, 13), open_price=3850.00, high_price=3950.00,
                                     low_price=3800.00, close_price=3900.00),
                     HistoricalPrice(crypto_id=3, date=date(2025, 4, 14), open_price=1.18, high_price=1.22,
                                     low_price=1.15, close_price=1.20),
                     HistoricalPrice(crypto_id=3, date=date(2025, 4, 13), open_price=1.20, high_price=1.25,
                                     low_price=1.18, close_price=1.22),
                     HistoricalPrice(crypto_id=4, date=date(2025, 4, 14), open_price=150.00, high_price=155.00,
                                     low_price=149.00, close_price=152.00),
                     HistoricalPrice(crypto_id=4, date=date(2025, 4, 13), open_price=153.00, high_price=158.00,
                                     low_price=151.00, close_price=155.00),
                     HistoricalPrice(crypto_id=5, date=date(2025, 4, 14), open_price=0.26, high_price=0.29,
                                     low_price=0.25, close_price=0.28),
                     HistoricalPrice(crypto_id=5, date=date(2025, 4, 13), open_price=0.25, high_price=0.28,
                                     low_price=0.24, close_price=0.27)])

    session.add_all([User(user_name='Ben'), User(user_name='Jake'), User(user_name='Chan')])


def main():
    try:
        url = CryptoDatabase.construct_mysql_url()
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


if __name__ == '__main__':
    main()

from sys import stderr

from pycoingecko import CoinGeckoAPI
from sqlalchemy.exc import SQLAlchemyError

from installer.database import CryptoDatabase, Cryptocurrency, User

coin_gecko_api = CoinGeckoAPI()
coins_list = coin_gecko_api.get_coins_markets(vs_currency='usd')


def add_starter_data(session):
    for coin_details in coins_list:
        session.add(Cryptocurrency(name=coin_details['name'], symbol=coin_details['symbol'].upper(),
                                   current_price=coin_details['current_price'],
                                   percent_change_24h=coin_details['price_change_percentage_24h']))

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

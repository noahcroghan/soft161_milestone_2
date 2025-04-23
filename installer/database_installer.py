from sys import stderr

from sqlalchemy.exc import SQLAlchemyError

from installer.database import CryptoDatabase, Cryptocurrency


def add_starter_data(session):
    # This is incomplete. Add more data as needed.
    crypto = Cryptocurrency(crypto_id=1, name='Bitcoin', symbol='BTC', current_price=50000.00, percent_change_24h=-2.5)
    session.add(crypto)


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

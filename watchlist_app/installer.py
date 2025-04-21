from sys import stderr

from datetime import date

from sqlalchemy.exc import SQLAlchemyError

from table_creater import CryptoDatabase, Symbol, Watchlist


def add_starter_data(session):
    symbol = Symbol(symbol_id=input())
    name = Watchlist(crypto_id=input())
    session.add(symbol)
    session.add(name)


def main():
    try:
        url = CryptoDatabase.construct_mysql_url('localhost', 3306, 'crypto_watchlist', 'root', 'Blet21306!')
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

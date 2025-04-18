from sys import stderr

from sqlalchemy.exc import SQLAlchemyError

from portfoliotracker import PortfolioTrackerDatabase, User, Portfolio, Cryptocurrency


def add_starter_data(session):
    user_name = User(user_name='username')
    session.add(user_name)


def main():
    try:
        url = PortfolioTrackerDatabase.construct_mysql_url('localhost', 3306, 'portfoliotracker', 'username', 'password')
        portfoliotracker_database = PortfolioTrackerDatabase(url)
        portfoliotracker_database.ensure_tables_exist()
        print('Tables created.')
        session = portfoliotracker_database.create_session()
        add_starter_data(session)
        session.commit()
        print('Records created.')
    except SQLAlchemyError as exception:
        print('Database setup failed!', file=stderr)
        print(f'Cause: {exception}', file=stderr)
        exit(1)


if __name__ == '__main__':
    main()

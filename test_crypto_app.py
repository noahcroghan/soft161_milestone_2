from datetime import datetime
from unittest import TestCase

from installer.database import CryptoDatabase, Persisted, User, Cryptocurrency, Portfolio
from portfolio_tracker_app.main import add_crypto_to_database, add_portfolio_to_database


class TestCryptoApp(TestCase):
    def setUp(self):
        self.db = CryptoDatabase(CryptoDatabase.construct_in_memory_url())
        Persisted.metadata.create_all(self.db.engine)
        self.session = self.db.create_session()

    # Test for getting all the usernames method from the database
    def test_get_all_usernames_returns_multiple_users(self):
        self.db.create_user('Kenny', self.session)
        self.db.create_user('Austin', self.session)
        usernames = self.db.get_all_usernames(self.session)
        self.assertIn('Kenny', usernames)
        self.assertIn('Austin', usernames)

    # Test for creating new users method to the database
    def test_create_user_and_insert_in_database(self):
        self.db.create_user('Deku', self.session)
        user = self.session.query(User).filter(User.user_name == 'Deku').one()
        self.assertEqual(user.user_name, 'Deku')

    # Test inserting adding new crypto to the database
    def test_add_crypto_to_database_successfully(self):
        example_crypto = add_crypto_to_database(
            session=self.session,
            name="Capstone",
            symbol="CSC",
            price=98.45,
            percent_change_24h=6.8
        )
        self.assertTrue(example_crypto)

        inserted = self.session.query(Cryptocurrency).filter_by(symbol='CSC').one()
        self.assertEqual(inserted.name, "Capstone")

    def test_add_crypto_to_database_validates_all_fields(self):
        name = "CheckCoin"
        symbol = "CC"
        price = 123.12
        percent_change_24h = 9.99

        crypto = add_crypto_to_database(
            session=self.session,
            name=name,
            symbol=symbol,
            price=price,
            percent_change_24h=percent_change_24h
        )
        self.assertTrue(crypto)
        inserted = self.session.query(Cryptocurrency).filter_by(symbol=symbol).one()
        self.assertEqual(inserted.name, name)
        self.assertEqual(float(inserted.current_price), price)
        self.assertEqual(float(inserted.percent_change_24h), percent_change_24h)

    def test_add_portfolio_to_database_successfully(self):
        example_portfolio = add_portfolio_to_database(
            session=self.session,
            user_id=1,
            crypto_id=1,
            coin_amount=24,
            purchase_date=datetime(2025, 2, 6).date(),
            initial_investment_amount=28
        )
        self.assertTrue(example_portfolio)
        inserted = self.session.query(Portfolio).filter_by(purchase_date=datetime(2025, 2, 6).date()).one()
        self.assertEqual(inserted.coin_amount, 24)

    def tearDown(self):
        self.session.close()

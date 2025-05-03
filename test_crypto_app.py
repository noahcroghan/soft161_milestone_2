from unittest import TestCase

from historical_prices_app.remove_me.config import username
from installer.database import CryptoDatabase, Persisted, User


class TestCryptoApp(TestCase):
    def setUp(self):
        self.db = CryptoDatabase(CryptoDatabase.construct_in_memory_url())
        Persisted.metadata.create_all(self.db.engine)
        self.session = self.db.create_session()

    #Test for getting all the usernames method from the database
    def test_get_all_usernames_returns_multiple_users(self):
        self.db.create_user('Kenny',self.session)
        self.db.create_user('Austin',self.session)
        usernames = self.db.get_all_usernames(self.session)
        self.assertIn('Kenny',usernames)
        self.assertIn('Austin',usernames)

    #Test for creating new users method to the database
    def test_create_user_and_insert_in_database(self):
        self.db.create_user('Deku',self.session)
        user = self.session.query(User).filter(User.user_name=='Deku').one()
        self.assertEqual(user.user_name,'Deku')


    def tearDown(self):
        self.session.close()




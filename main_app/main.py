import webbrowser
from sys import stderr

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError

from historical_prices_app.main import SelectCoinScreen, ViewHistoryScreen
from installer.database import CryptoDatabase
from portfolio_tracker_app.main import NewCryptoScreen, UpdateCryptoScreen, NewPortfolioScreen, CheckPortfolioScreen, UpdateEntryScreen


class LoginScreen(Screen):

    def update_spinner_values(self):
        db = CryptoDatabase(CryptoDatabase.construct_mysql_url())
        session = db.create_session()
        usernames = db.get_all_usernames(session)
        self.ids.existing_users_spinner.values = usernames
        session.close()

    def on_enter(self):
        self.update_spinner_values()

    def create_username(self, target_screen=None):
        new_username = self.ids.new_username_input.text if not target_screen else target_screen.ids.new_username_input.text
        if not new_username:
            if target_screen:
                self.ids.login_message.text = "Username cannot be empty. Please enter a username."
            else:
                self.ids.login_message.text = "Username cannot be empty. Please enter a username."
            return
        try:
            db = CryptoDatabase(CryptoDatabase.construct_mysql_url())
            session = db.create_session()
            added_username = db.create_user(new_username, session)
            session.close()

            if added_username:
                if target_screen:
                    if added_username not in target_screen.ids.existing_users_spinner.values:
                        target_screen.ids.existing_users_spinner.values.append(added_username)
                    target_screen.ids.new_username_input.text = ''
                    target_screen.ids.login_message.text = f"User {added_username} created successfully. Click on existing users"
                else:
                    if added_username not in self.ids.existing_users_spinner.values:
                        self.ids.existing_users_spinner.values.append(added_username)
                    self.ids.new_username_input.text = ''
                    self.ids.login_message.text = f"User {added_username} created successfully. Click on existing users"

                App.get_running_app().current_user = added_username
            else:
                print("Failed to add username. The username was not created.")
                if target_screen:
                    target_screen.ids.login_message.text = f"Username {added_username} already exists."
                else:
                    self.ids.login_message.text = f"Username {added_username} already exists."
        except SQLAlchemyError:
            self.ids.login_message.text = "Database connection failed. Make sure to run the installer first."

    def login_selected_user(self):
        selected_user = self.ids.existing_users_spinner.text

        if selected_user and selected_user != "Select Existing User":
            App.get_running_app().current_user = selected_user
            self.manager.current = "MainScreen"
        else:
            self.ids.login_message.text = "Please select a user before logging in."


class HelpScreen(Screen):
    @staticmethod
    def open_link():
        webbrowser.open_new_tab('https://docs.coingecko.com/reference/introduction')


class MainScreen(Screen):
    pass


# TODO: Proper error message like LoginScreen when username is empty.
#  Also if the user tries to add a new profile the spinner isn't updated.
#  Maybe refactor since both screens do similar things
class SwitchUserScreen(Screen):
    def update_spinner(self):
        db = CryptoDatabase(CryptoDatabase.construct_mysql_url())
        session = db.create_session()
        usernames = db.get_all_usernames(session)
        session.close()
        self.ids.existing_users_spinner.values = usernames

        current_user = App.get_running_app().current_user
        if current_user in self.ids.existing_users_spinner.values:
            self.ids.existing_users_spinner.text = current_user
        else:
            self.ids.existing_users_spinner.text = 'Select Existing User'

    def get_new_user(self):

        if self.ids.new_username_input.focus:
            login_screen = self.manager.get_screen('LoginScreen')
            login_screen.create_username(self)

        self.update_spinner()

    def on_enter(self):
        self.update_spinner()

    def confirm_user_switch(self):
        selected_user = self.ids.existing_users_spinner.text
        if selected_user and selected_user != "Select Existing User":
            App.get_running_app().current_user = selected_user
            self.manager.current = "MainScreen"
        else:
            self.ids.login_message.text = "Please select a user before switching."


class MainApp(App):
    current_user = StringProperty('')

    def build(self):
        Window.size = (420, 720)
        self.title = 'Cryptocurrency App'

        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen())
        screen_manager.add_widget(MainScreen())
        screen_manager.add_widget(HelpScreen())
        screen_manager.add_widget(SelectCoinScreen())
        screen_manager.add_widget(ViewHistoryScreen())
        screen_manager.add_widget(SwitchUserScreen())
        screen_manager.add_widget(NewCryptoScreen())
        screen_manager.add_widget(UpdateCryptoScreen())
        screen_manager.add_widget(NewPortfolioScreen())
        screen_manager.add_widget(CheckPortfolioScreen())
        screen_manager.add_widget(UpdateEntryScreen())

        return screen_manager


if __name__ == '__main__':
    try:
        MainApp().run()
    except ProgrammingError:
        print('Database connection failed! Make sure to follow the instructions in the README.', file=stderr)
        exit(1)

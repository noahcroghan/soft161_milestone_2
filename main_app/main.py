import webbrowser
from sys import stderr

from kivy.app import App
from kivy.modules import inspector  # For Inspection
from kivy.core.window import Window
from kivy.modules import inspector  # For Inspection
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from sqlalchemy.exc import SQLAlchemyError

from historical_prices_app.main import SelectCoinScreen, ViewHistoryScreen
from installer.database import CryptoDatabase, User
from historical_prices_app.remove_me.config import username
from portfolio_tracker_app.main import NewCryptoScreen, NewPortfolioScreen, CheckPortfolioScreen
from installer.database import CryptoDatabase, User  # Adjust path if needed




class LoginScreen(Screen):

    def update_spinner_values(self):
        db = CryptoDatabase(CryptoDatabase.construct_mysql_url())
        usernames = db.get_all_usernames()
        self.ids.existing_users_spinner.values = usernames

    def on_enter(self):
        self.update_spinner_values()

    def create_username(self):
        new_username = self.ids.new_username_input.text
        if not new_username:
            return

        db = CryptoDatabase.construct_mysql_url()
        db_session = CryptoDatabase(db)

        added_username = db_session.create_user(new_username)

        if added_username:
            if added_username not in self.ids.existing_users_spinner.values:
                self.ids.existing_users_spinner.values.append(added_username)
            self.ids.new_username_input.text = ''
            self.ids.login_message.text = f"User {added_username} created successfully. Click on existing users"
            App.get_running_app().current_user = added_username
        else:
            print("Failed to add username. The username was not created.")
            self.ids.login_message.text = f"Username {added_username} already exists."

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


class SwitchUserScreen(Screen):
    def update_spinner(self):
        db = CryptoDatabase(CryptoDatabase.construct_mysql_url())
        usernames = db.get_all_usernames()
        self.ids.existing_users_spinner.values = usernames

        if self.ids.existing_users_spinner.values:
            self.ids.existing_users_spinner.text = self.ids.existing_users_spinner.values[0]
        else:
            self.ids.existing_users_spinner.text = 'Select Existing User'

    def get_new_user(self):
        login_screen = self.manager.get_screen('LoginScreen')
        login_screen.create_username()

        self.update_spinner()

    def on_enter(self):
        self.update_spinner()
        selected_user = self.ids.existing_users_spinner.text
        if selected_user and selected_user != "Select Existing User":
            App.get_running_app().current_user = selected_user

            main_screen = self.manager.get_screen('MainScreen')
            main_screen.on_enter()


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
        screen_manager.add_widget(NewPortfolioScreen())
        screen_manager.add_widget(CheckPortfolioScreen())

        inspector.create_inspector(Window, screen_manager)  # For Inspection

        return screen_manager


if __name__ == '__main__':
    try:
        MainApp().run()
    except SQLAlchemyError as exception:
        print('Database connection failed!', file=stderr)
        print(f'Cause: {exception}', file=stderr)
        exit(1)

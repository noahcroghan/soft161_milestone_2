from kivy.app import App
from kivy.modules import inspector # For Inspection
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

from historical_prices_app.main import SelectCoinScreen, ViewHistoryScreen
from portfolio_tracker_app.main import NewCryptoScreen, NewPortfolioScreen, CheckPortfolioScreen
from installer.database import CryptoDatabase  # Adjust path if needed


class LoginScreen(Screen):

    def on_pre_enter(self):
        db = CryptoDatabase('mysql+mysqlconnector://username:password@localhost:3306/crypto')
        usernames = db.get_all_users()
        self.ids.existing_users_spinner.values = usernames


    def create_username(self):
        new_username = self.ids.new_username_input.text.strip()
        if not new_username:
            return


        db = CryptoDatabase('mysql+mysqlconnector://username:password@localhost:3306/crypto')


        added_username = db.create_user(new_username)


        if added_username:
            self.ids.existing_users_spinner.values += [added_username]
            self.ids.new_username_input.text = ''


class HelpScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class SwitchUserScreen(Screen):
    pass

class MainApp(App):
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

        inspector.create_inspector(Window, screen_manager) # For Inspection

        return screen_manager


if __name__ == '__main__':

    MainApp().run()

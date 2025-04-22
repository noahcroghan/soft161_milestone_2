from kivy.app import App
from kivy.modules import inspector # For Inspection
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

from historical_prices_app.main import ViewHistoryScreen, SelectCoinScreen

class LoginScreen(Screen):
    pass


class HelpScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class MainApp(App):
    def build(self):
        Window.size = (420, 720)
        self.title = 'Cryptocurrency App'

        screen_manager = ScreenManager()
        # screen_manager.add_widget(LoginScreen())
        screen_manager.add_widget(MainScreen())
        screen_manager.add_widget(HelpScreen())

        inspector.create_inspector(Window, screen_manager) # For Inspection

        return screen_manager


if __name__ == '__main__':
    MainApp().run()

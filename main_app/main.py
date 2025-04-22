from kivy.app import App
from kivy.modules import inspector # For Inspection
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from historical_prices_app.main import MenuScreen, ViewHistoryScreen, SelectCoinScreen


class MainApp(App):
    def build(self):
        Window.size = (420, 720)
        self.title = 'Cryptocurrency App'

        screen_manager = ScreenManager()
        screen_manager.add_widget(MenuScreen(name='MenuScreen'))
        screen_manager.add_widget(SelectCoinScreen(name='SelectCoinScreen'))
        screen_manager.add_widget(ViewHistoryScreen(name='ViewHistoryScreen'))

        inspector.create_inspector(Window, screen_manager) # For Inspection

        return screen_manager


if __name__ == '__main__':
    MainApp().run()

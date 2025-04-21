from kivy.app import App
from kivy.modules import inspector  # For inspection.
from kivy.core.window import Window  # For inspection.
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput


class MenuScreen(Screen):
    pass

class WatchlistMain(Screen):
    pass

class NewWatchlist(Screen):
    pass

class ViewWatchlist(Screen):
    pass

class CryptoApp(App):
    def __init__(self, **kwargs):
        super(CryptoApp, self).__init__(**kwargs)
        url = CryptoDatabase.construct_mysql_url('localhost', 3306, 'sql_lab', 'root', 'Blet21306!')
        self.movie_database = MovieDatabase(url)
        self.session = self.movie_database.create_session()

class Milestone_1App(App):
    def build(self):
        sm = ScreenManager()
        inspector.create_inspector(Window, self)
        sm.add_widget(MenuScreen(name="Menu"))
        sm.add_widget(WatchlistMain(name="Watchlist_Main"))
        sm.add_widget(NewWatchlist(name="New_Watchlist"))
        sm.add_widget(ViewWatchlist(name="View_Watchlist"))
        return sm

if __name__ == '__main__':
    app = Milestone_1App()
    app.run()
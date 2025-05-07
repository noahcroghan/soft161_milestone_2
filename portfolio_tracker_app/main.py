# from kivy.app import App
# from kivy.modules import inspector
# from kivy.core.window import Window
# from kivy.properties import NumericProperty, StringProperty
#
#
# class PortfolioTrackerApp(App):
#     crypto_price = StringProperty("")
#     portfolio_value = StringProperty("")
#     portfolio_value_change = StringProperty("")
#     input_text = StringProperty("")
#
#     def check_value(self, input_id, message_id):
#         if input_id.text != '':
#             message_id.text = ""
#             self.crypto_price = "$#.##"
#             self.portfolio_value = "$###.##"
#             self.portfolio_value_change = "+ ##.##%"
#         else:
#             self.crypto_price = ""
#             self.portfolio_value = ""
#             self.portfolio_value_change = ""
#             message_id.text = "Portfolio ID is Required"
#
#     def go_to_home(self, message_id):
#         self.crypto_price = ""
#         self.portfolio_value = ""
#         self.portfolio_value_change = ""
#         self.input_text = " "
#         self.input_text = ""
#         message_id.text = ""
#
#     def submit_data(self, message_id, id1, id2, id3, message_pass, message_fail):
#         if id1.text != '' and id2.text != '' and id3.text != '':
#             message_id.text = message_pass
#             id1.text = ""
#             id2.text = ""
#             id3.text = ""
#         else:
#            message_id.text = message_fail
#
#     def build(self):
#         inspector.create_inspector(Window, self)
#
#
# if __name__ == '__main__':
#     Window.size = (420, 720)
#     app = PortfolioTrackerApp()
#     app.run()
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import Screen
from installer.database import CryptoDatabase, User, Cryptocurrency, Portfolio  # Adjust path if needed
from installer.database_installer import coin_gecko_api


def get_all_cryptocurrencies():
    db_session = CryptoDatabase.get_session()
    return [crypto.name for crypto in db_session.query(Cryptocurrency).all()]

class NewCryptoScreen(Screen):
    pass

class NewPortfolioScreen(Screen):

    def update_spinner_values(self):
        cryptocurrencies = get_all_cryptocurrencies()
        self.ids.new_portfolio_crypto.values = cryptocurrencies

    def show_error(self, message, font_size):
        self.ids.new_portfolio_message.text = message
        self.ids.new_portfolio_message.color = (1, 0, 0, 1)
        self.ids.new_portfolio_message.font_size = font_size

    def show_message(self, message, font_size):
        self.ids.new_portfolio_message.text = message
        self.ids.new_portfolio_message.color = ((50/256), (222/256), (153/256), 1.0)
        self.ids.new_portfolio_message.font_size = font_size

    def go_home(self):
        self.ids.new_portfolio_message.text = ""
        self.ids.new_portfolio_message.color = ((50/256), (222/256), (153/256), 1.0)
        self.ids.new_portfolio_message.font_size = 50
        self.ids.new_portfolio_crypto.text = ""
        self.ids.new_portfolio_quantity.text = ""
        self.ids.new_portfolio_date.text = ""


    def on_enter(self):
        self.update_spinner_values()

    def create_new_portfolio(self):
        db_session = CryptoDatabase.get_session()
        selected_crypto = self.ids.new_portfolio_crypto.text
        coin_quantity = float(self.ids.new_portfolio_quantity.text)
        purchase_date = self.ids.new_portfolio_date.text
        selected_user = App.get_running_app().current_user

        try:
            purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
        except ValueError:
            self.show_error("Invalid date format. Use YYYY-MM-DD.", 25)
            return

        if not selected_crypto or not coin_quantity or not purchase_date or not selected_user:
            self.show_error("Missing required data", 30)
            return

        selected_crypto_id = [crypto.crypto_id for crypto in db_session.query(Cryptocurrency).all() if crypto.name == selected_crypto]

        if len(selected_crypto_id) != 1:
            self.show_error("Invalid cryptocurrency selected", 30)
            return

        selected_user_id = [user.user_id for user in db_session.query(User).all() if user.user_name == selected_user]

        if len(selected_user_id) != 1:
            self.show_error("Invalid user selected", 30)
            return

        selected_coin_gecko_id = [crypto.coingecko_id for crypto in db_session.query(Cryptocurrency).all() if crypto.name == selected_crypto]

        if len(selected_coin_gecko_id) != 1:
            self.show_error("Invalid coingecko cryptocurrency selected", 25)
            return
        else:
            selected_coin_gecko_id = selected_coin_gecko_id[0]

        try:
            gecko_purchase_date = datetime.strftime(purchase_date, "%d-%m-%Y")
        except ValueError:
            self.show_error("Invalid date format. Use DD-MM-YYYY.", 25)
            return

        self.show_message("Connecting to Coingecko...", 25)

        try:
            price_at_purchase = coin_gecko_api.get_coin_history_by_id(selected_coin_gecko_id, localization='false' ,vs_currencies="usd", date=gecko_purchase_date)['market_data']['current_price']['usd']
        except ValueError:
            self.show_error("Purchase date must be within last 365 days", 25)
            return

        initial_investment = price_at_purchase * coin_quantity

        db_session.add(Portfolio(user_id=selected_user_id[0], crypto_id=selected_crypto_id[0], coin_amount=coin_quantity, purchase_date=purchase_date, initial_investment_amount=initial_investment))
        db_session.commit()
        self.show_message("Submitted", 50)

class CheckPortfolioScreen(Screen):
    pass
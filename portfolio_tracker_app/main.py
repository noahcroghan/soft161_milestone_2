from kivy.uix.screenmanager import Screen

from installer.database import CryptoDatabase, Cryptocurrency


def get_all_cryptocurrencies():
    db_session = CryptoDatabase.get_session()
    return [crypto.name for crypto in db_session.query(Cryptocurrency).all()]


class NewCryptoScreen(Screen):
    def submit_new_crypto(self):
        name = self.ids.new_crypto_name_input.text
        symbol = self.ids.new_crypto_symbol_input.text
        price = self.ids.new_crypto_price_input.text
        if not name or len(name) > 50:
            self.show_error("Name field is required and must be less than 50 characters long.")
            return
        if not symbol or len(symbol) > 15:
            self.show_error("Symbol field is required and must be less than 15 characters long.")
            return
        try:
            price = float(price)
        except ValueError:
            self.show_error("Price field is required.")

        else:
            self.show_success("Success!")
            # TODO: Add new crypto to database

    def show_error(self, message):
        self.ids.new_crypto_message.text = message
        self.ids.new_crypto_message.color = ((214/256), (69/256), (69/256), 1.0)

    def show_success(self, message):
        self.ids.new_crypto_message.text = message
        self.ids.new_crypto_message.color = ((50/256), (222/256), (153/256), 1.0)


class NewPortfolioScreen(Screen):

    def update_spinner_values(self):
        cryptocurrencies = get_all_cryptocurrencies()
        self.ids.new_portfolio_crypto.values = cryptocurrencies

    def on_enter(self):
        self.update_spinner_values()


class CheckPortfolioScreen(Screen):
    pass

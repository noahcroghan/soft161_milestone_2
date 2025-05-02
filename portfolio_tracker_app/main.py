from kivy.uix.screenmanager import Screen
from sqlalchemy.exc import SQLAlchemyError

from installer.database import CryptoDatabase, Cryptocurrency


def get_all_cryptocurrencies():
    db_session = CryptoDatabase.get_session()
    return [crypto.name for crypto in db_session.query(Cryptocurrency).all()]


class NewCryptoScreen(Screen):
    def submit_new_crypto(self):
        name = self.ids.new_crypto_name_input.text.strip().capitalize()
        symbol = self.ids.new_crypto_symbol_input.text.strip().upper()
        price = self.ids.new_crypto_price_input.text
        percent_change_24h = self.ids.new_crypto_percent_change_24h_input.text
        if not name or len(name) > 50:
            self.show_error("Name field is required and must be less than 50 characters long.")
            return
        if not symbol or len(symbol) > 15:
            self.show_error("Symbol field is required and must be less than 15 characters long.")
            return
        if " " in symbol:
            self.show_error("Symbol field cannot contain spaces.")
            return
        try:
            price = float(price)
            if price < 0:
                self.show_error("Price cannot be negative.")
                return
            elif price > 1000000000000:
                self.show_error("Price cannot be greater than $10,000,000,000.")
                return
        except ValueError:
            self.show_error("Price field is required.")
            return

        try:
            percent_change_24h = float(percent_change_24h)
            if percent_change_24h < -100 or percent_change_24h > 1000:
                self.show_error("Percent change must be between -100% and 1000%.")
                return
        except ValueError:
            self.show_error("Percent change field is required.")
            return

        try:
            session = CryptoDatabase.get_session()
            crypto_exists = session.query(Cryptocurrency).filter(
                (Cryptocurrency.symbol == symbol) | (Cryptocurrency.name == name)).first()

            if crypto_exists:
                self.show_error("Submitted crypto already exists.")
                return

            new_crypto = Cryptocurrency(name=name, symbol=symbol, current_price=price,
                                        percent_change_24h=percent_change_24h, coingecko_id=symbol)
            session.add(new_crypto)
            session.commit()

            self.show_success(f"New crypto '{name}' [i]({symbol})[/i] added successfully.")
        except SQLAlchemyError as sql_alchemy_error:
            self.show_error(f'General Database error:\n{sql_alchemy_error}')
        except Exception as exception:
            self.show_error(f'General error occurred:\n{exception}')

    def show_error(self, message):
        self.ids.new_crypto_message.text = message
        self.ids.new_crypto_message.color = ((214 / 256), (69 / 256), (69 / 256), 1.0)

    def show_success(self, message):
        self.ids.new_crypto_message.text = message
        self.ids.new_crypto_message.color = ((50 / 256), (222 / 256), (153 / 256), 1.0)

    def on_leave(self):
        self.ids.new_crypto_message.text = ""
        self.ids.new_crypto_name_input.text = ""
        self.ids.new_crypto_symbol_input.text = ""
        self.ids.new_crypto_price_input.text = ""
        self.ids.new_crypto_percent_change_24h_input.text = ""


class NewPortfolioScreen(Screen):

    def update_spinner_values(self):
        cryptocurrencies = get_all_cryptocurrencies()
        self.ids.new_portfolio_crypto.values = cryptocurrencies

    def on_enter(self):
        self.update_spinner_values()


class CheckPortfolioScreen(Screen):
    pass

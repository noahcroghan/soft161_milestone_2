from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import Screen
from sqlalchemy.exc import SQLAlchemyError

from installer.database import CryptoDatabase, User, Cryptocurrency, Portfolio  # Adjust path if needed
from installer.database_installer import coin_gecko_api

from matplotlib import pyplot as plt

@staticmethod
def add_crypto_to_database(session,name,symbol,price,percent_change_24h):
    crypto_exists = session.query(Cryptocurrency).filter(
        (Cryptocurrency.symbol==symbol)|(Cryptocurrency.name==name)).first()
    if crypto_exists:
        return False
    new_crypto = Cryptocurrency(name=name,
                                symbol=symbol,
                                current_price=price,
                                percent_change_24h=percent_change_24h,
                                coingecko_id=symbol
                                )
    session.add(new_crypto)
    session.commit()
    return True
@staticmethod
def add_portfolio_to_database(session, user_id,crypto_id,coin_amount,purchase_date,initial_investment_amount):
    new_portfolio = Portfolio(user_id=user_id,
                              crypto_id = crypto_id,
                              coin_amount=coin_amount,
                              purchase_date=purchase_date,
                              initial_investment_amount=initial_investment_amount)
    session.add(new_portfolio)
    session.commit()
    return True

def get_all_cryptocurrencies():
    db_session = CryptoDatabase.get_session()
    return [crypto.name for crypto in db_session.query(Cryptocurrency).all()]

def get_all_portfolios():
    db_session = CryptoDatabase.get_session()
    int_list = [portfolios.portfolio_id for portfolios in db_session.query(Portfolio).all()]
    str_list = []
    for portfolio_id in int_list:
        str_list.append(str(portfolio_id))
    return str_list



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
            add_crypto_to_database(session,name,symbol,price,percent_change_24h)

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
        self.ids.new_portfolio_crypto.text = "Crypto Name"
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
            purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d").date()
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
        user_id =selected_user_id[0]
        crypto_id =selected_crypto_id[0]
        coin_amount= coin_quantity
        initial_investment_amount = initial_investment
        session = db_session
        add_portfolio_to_database(session,user_id,crypto_id,coin_amount,purchase_date,initial_investment_amount)
        self.show_message("Submitted", 50)

class CheckPortfolioScreen(Screen):
    def update_spinner_values(self):
        portfolios = get_all_portfolios()
        self.ids.check_portfolio_ids.values = portfolios

    def show_error(self, message, font_size):
        self.ids.check_portfolio_message.text = message
        self.ids.check_portfolio_message.color = (1, 0, 0, 1)
        self.ids.check_portfolio_message.font_size = font_size

    def show_message(self, message, font_size):
        self.ids.check_portfolio_message.text = message
        self.ids.check_portfolio_message.color = ((50/256), (222/256), (153/256), 1.0)
        self.ids.check_portfolio_message.font_size = font_size

    def go_home(self):
        self.ids.check_portfolio_message.text = ""
        self.ids.check_portfolio_message.color = ((50/256), (222/256), (153/256), 1.0)
        self.ids.check_portfolio_message.font_size = 50
        self.ids.check_portfolio_ids.text = "Portfolio ID"
        self.ids.check_investment_amount.text = ""
        self.ids.check_portfolio_value.text = ""
        self.ids.check_value_change.text = ""
        self.ids.portfolio_chart.source = ''

    def on_enter(self):
        self.update_spinner_values()

    def get_user(self, db_session):
        selected_user = App.get_running_app().current_user
        selected_user = [users.user_id for users in db_session.query(User).all() if users.user_name == selected_user]

        if len(selected_user) != 1:
            self.show_error("Invalid user selected", 25)
            return
        else:
            selected_user = selected_user[0]

        return selected_user

    def initial_investment(self):
        self.show_message("Calculating Initial Investment Amount...", 25)
        db_session = CryptoDatabase.get_session()
        portfolios = get_all_portfolios()
        initial_investment = float(0.0)
        selected_user = self.get_user(db_session)

        for portfolio in portfolios:
            portfolio = int(portfolio)
            portfolio_user = [portfolios.user_id for portfolios in db_session.query(Portfolio).all() if portfolios.portfolio_id == portfolio]

            if len(portfolio_user) != 1:
                self.show_error("Invalid user selected", 25)
                return
            else:
                portfolio_user = portfolio_user[0]

            if portfolio_user == selected_user:
                portfolio_investment = [portfolios.initial_investment_amount for portfolios in db_session.query(Portfolio).all() if portfolios.portfolio_id == portfolio]
                if len(portfolio_investment) != 1:
                    self.show_error("Invalid portfolio selected", 30)
                else:
                    portfolio_investment = portfolio_investment[0]
                initial_investment += float(portfolio_investment)
                print(portfolio_investment)
                print(initial_investment)

        return initial_investment

    def check_portfolio_entry(self, portfolio, db_session, selected_user):
        portfolio = int(portfolio)
        portfolio_user = [portfolios.user_id for portfolios in db_session.query(Portfolio).all() if portfolios.portfolio_id == portfolio]

        if len(portfolio_user) != 1:
            self.show_error("Invalid user selected", 25)
            return
        else:
            portfolio_user = portfolio_user[0]

        if portfolio_user == selected_user:
            selected_crypto_id = [portfolios.crypto_id for portfolios in db_session.query(Portfolio).all() if
                                  portfolios.portfolio_id == portfolio]

            if len(selected_crypto_id) != 1:
                self.show_error("Invalid cryptocurrency selected", 25)
                return
            else:
                selected_crypto_id = selected_crypto_id[0]

            selected_crypto_name = [crypto.name for crypto in db_session.query(Cryptocurrency).all() if
                                    crypto.crypto_id == selected_crypto_id]
            selected_coin_gecko_id = [crypto.coingecko_id for crypto in db_session.query(Cryptocurrency).all() if
                                      crypto.crypto_id == selected_crypto_id]

            if len(selected_crypto_name) != 1 or len(selected_coin_gecko_id) != 1:
                self.show_error("Invalid coingecko cryptocurrency selected", 25)
                return
            else:
                selected_coin_gecko_id = selected_coin_gecko_id[0]

            current_price = coin_gecko_api.get_price(selected_coin_gecko_id, vs_currencies="usd")
            print(current_price)
            print(selected_coin_gecko_id)
            print(current_price[selected_coin_gecko_id]["usd"])

            coin_quantity = [portfolios.coin_amount for portfolios in db_session.query(Portfolio).all() if portfolios.portfolio_id == portfolio]

            if len(coin_quantity) != 1:
                self.show_error("Invalid cryptocurrency selected", 25)
                return
            else:
                coin_quantity = coin_quantity[0]

            return current_price[selected_coin_gecko_id]["usd"] * float(coin_quantity)
        else:
            return

    def current_total_value(self):
        db_session = CryptoDatabase.get_session()
        self.show_message("Calculating Current Total Value...", 25)
        portfolios = get_all_portfolios()
        current_total = float(0.0)
        selected_user = self.get_user(db_session)

        for portfolio in portfolios:

            entry_value = self.check_portfolio_entry(portfolio, db_session, selected_user)
            current_total += entry_value
            print(current_total)

        return current_total

    def view_portfolio_summary(self):
        initial_investment = self.initial_investment()
        print(initial_investment)
        current_total_value = self.current_total_value()
        self.show_message("", 30)
        print(current_total_value)

        try:
            value_change = ((current_total_value - initial_investment) / initial_investment)*100
        except ZeroDivisionError:
            self.show_error("Initial Investment Amount Not Found", 25)
            return

        if value_change < 0:
            self.ids.check_value_change.color = (1, 0, 0, 1)
        else:
            self.ids.check_value_change.color = ((50/256), (222/256), (153/256), 1.0)

        self.ids.check_investment_amount.text = "$" + str(initial_investment)
        self.ids.check_portfolio_value.text = "$" + str(current_total_value)
        self.ids.check_value_change.text = str(value_change) + "%"
        self.show_message("Complete", 30)

    def create_portfolio_chart(self):
        db_session = CryptoDatabase.get_session()
        portfolios = get_all_portfolios()
        user_entries = []
        current_values = []
        selected_user = self.get_user(db_session)

        for portfolio in portfolios:
            portfolio = int(portfolio)
            portfolio_user = [portfolios.user_id for portfolios in db_session.query(Portfolio).all() if portfolios.portfolio_id == portfolio]

            if len(portfolio_user) != 1:
                self.show_error("Invalid user selected", 25)
                return
            else:
                portfolio_user = portfolio_user[0]

            if portfolio_user == selected_user:
                user_entries.append(str(portfolio))

            entry_value = self.check_portfolio_entry(portfolio, db_session, selected_user)
            if entry_value:
                current_values.append(entry_value)
            print(current_values)

        plt.figure(figsize=(4, 4))

        plt.pie(current_values, labels = user_entries)

        plt.title("Portfolio Entry Values")
        plt.tight_layout()

        chart_file = "portfolio_chart.png"
        plt.savefig(chart_file)
        plt.close()

        self.ids.portfolio_chart.source = chart_file
        self.ids.portfolio_chart.reload()
        self.show_message("Portfolio chart loaded successfully.", 25)
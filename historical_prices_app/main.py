from datetime import datetime

from kivy.metrics import dp
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from matplotlib import pyplot as plt
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError

from installer.database import CryptoDatabase, Cryptocurrency, HistoricalPrice


class ClickableLabel(ButtonBehavior, Label):
    pass  # behavior defined elsewhere


class SelectCoinScreen(Screen):
    def on_enter(self):
        search_text = self.ids.search_input.text.strip()
        self.load_coins(search_text)

    def load_coins(self, search_query=None):
        try:
            session = CryptoDatabase.get_session()

            query = session.query(Cryptocurrency)
            if search_query:
                query = query.filter((Cryptocurrency.name.ilike(f"%{search_query}%")) | (
                    Cryptocurrency.symbol.ilike(f"%{search_query}%")))

            coins = query.all()

            self.ids.coin_container.clear_widgets()

            if not coins:
                raise ValueError

            for coin in coins:
                self.add_coin_to_ui(coin)

            self.ids.select_coin_message.opacity = 0

        except ValueError:
            self.show_error('No coins found matching search criteria')
        except ProgrammingError:
            self.show_error('Database not initialized. Run installer first!')
        except SQLAlchemyError as sql_alchemy_error:
            self.show_error(f'General Database error:\n{sql_alchemy_error}')
        except Exception as exception:
            self.show_error(f'General error occurred:\n{exception}')

    def show_error(self, message):
        self.ids.select_coin_message.text = message
        self.ids.select_coin_message.color = (1, 0, 0, 1)
        self.ids.select_coin_message.opacity = 1

    def add_coin_to_ui(self, coin):
        box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10), padding=[dp(10), 0])

        coin_label = ClickableLabel(text=f"{coin.name} [i]({coin.symbol})[/i]", markup=True)
        coin_label.coin = coin
        coin_label.bind(on_press=self.go_to_history_from_label)

        box.add_widget(coin_label)

        box.add_widget(Label(text=f"${coin.current_price:,.2f}"))

        change_text = f"{coin.percent_change_24h:.2f}%"
        change_color = (0, 0, 0, 1)
        if coin.percent_change_24h < 0:
            change_color = (1, 0, 0, 1)
        elif coin.percent_change_24h > 0:
            change_color = (0, 1, 0, 1)
        box.add_widget(Label(text=change_text, color=change_color))

        self.ids.coin_container.add_widget(box)

    def go_to_history_from_label(self, instance):
        coin = instance.coin
        history_screen = self.manager.get_screen('ViewHistoryScreen')
        history_screen.ids.coin_symbol_input.text = coin.symbol
        history_screen.came_from_select_coin = True
        self.manager.current = 'ViewHistoryScreen'
        self.manager.transition.direction = 'left'

    def search_coins(self):
        search_text = self.ids.search_input.text.strip()
        self.load_coins(search_text)


class ViewHistoryScreen(Screen):
    came_from_select_coin = BooleanProperty(False)

    def submit_history(self):
        self.ids.history_message.text = ''
        self.ids.chart.source = ''
        self.ids.chart.reload()

        coin_symbol = self.ids.coin_symbol_input.text.strip().upper()
        start_date_str = self.ids.start_date_input.text.strip()
        end_date_str = self.ids.end_date_input.text.strip()

        if not coin_symbol:
            self.show_error("Please enter a coin symbol (i.e. BTC).")
            return

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            self.show_error("Invalid date format. Use YYYY-MM-DD.")
            return

        if start_date > end_date:
            self.show_error("Start date must be before or equal to end date.")
            return

        date_range = 90
        if (end_date - start_date).days > date_range:
            self.show_error(f"Date range cannot exceed {date_range} days.")
            return

        try:
            session = CryptoDatabase.get_session()

            historical_prices = (session.query(HistoricalPrice).join(Cryptocurrency,
                                                                     HistoricalPrice.crypto_id == Cryptocurrency.crypto_id).filter(
                Cryptocurrency.symbol == coin_symbol, HistoricalPrice.date >= start_date,
                HistoricalPrice.date <= end_date).order_by(HistoricalPrice.date.asc()).all())

            if not historical_prices:
                self.show_error("No historical data found for selected coin and date range.")
                return

            dates = [record.date for record in historical_prices]
            price_values = [record.price for record in historical_prices]

            plt.figure(figsize=(6, 4))
            plt.plot(dates, price_values, marker='o', linestyle='-')
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.title(f"{coin_symbol} Price History")
            plt.xticks(rotation=45)
            plt.tight_layout()

            chart_file = "chart.png"
            plt.savefig(chart_file)
            plt.close()

            self.ids.chart.source = chart_file
            self.ids.chart.reload()
            self.show_success("Price history loaded successfully.")

        except Exception as exception:
            self.show_error(f'General error occurred:\n{exception}')

    def show_error(self, message):
        self.ids.history_message.text = message
        self.ids.history_message.color = (1, 0, 0, 1)
        self.ids.history_message.opacity = 1

    def show_success(self, message):
        self.ids.history_message.text = message
        self.ids.history_message.color = (0, 1, 0, 1)
        self.ids.history_message.opacity = 1

    def on_leave(self):
        self.ids.coin_symbol_input.text = ''
        self.ids.start_date_input.text = ''
        self.ids.end_date_input.text = ''
        self.ids.history_message.text = ''
        self.ids.chart.source = ''
        self.came_from_select_coin = False

from datetime import datetime, timezone, timedelta

import mplfinance as mpf
import pandas as pd
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from matplotlib import pyplot as plt
from pycoingecko import CoinGeckoAPI
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError

from installer.database import CryptoDatabase, Cryptocurrency


class ClickableLabel(ButtonBehavior, Label):
    pass  # behavior defined elsewhere


# TODO: Make this screen get from the API instead of DB
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
        self.ids.select_coin_message.color = ((214 / 256), (69 / 256), (69 / 256), 1.0)
        self.ids.select_coin_message.opacity = 1

    def add_coin_to_ui(self, coin):
        box = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10), padding=dp(10))

        coin_label = ClickableLabel(text=f"{coin.name} [i]({coin.symbol})[/i]", markup=True, text_size=(dp(115), None),
                                    shorten=False, halign="center", valign="middle")
        coin_label.coin = coin
        coin_label.bind(on_press=self.go_to_history_from_label)

        box.add_widget(coin_label)

        box.add_widget(Label(text=f"${coin.current_price:,.2f}"))

        change_text = f"{coin.percent_change_24h:.2f}%"
        change_color = (1, 1, 1, 1)
        if coin.percent_change_24h < 0:
            change_color = ((214 / 256), (69 / 256), (69 / 256), 1.0)
        elif coin.percent_change_24h > 0:
            change_color = ((50 / 256), (222 / 256), (153 / 256), 1.0)
        box.add_widget(Label(text=change_text, color=change_color))

        self.ids.coin_container.add_widget(box)

    def go_to_history_from_label(self, instance):
        coin = instance.coin
        history_screen = self.manager.get_screen('ViewHistoryScreen')
        history_screen.ids.coin_name_spinner.text = coin.name
        history_screen.came_from_select_coin = True
        self.manager.current = 'ViewHistoryScreen'
        self.manager.transition.direction = 'left'

    def search_coins(self):
        search_text = self.ids.search_input.text.strip()
        self.load_coins(search_text)


class ViewHistoryScreen(Screen):
    came_from_select_coin = BooleanProperty(False)
    is_historical_data_generated = BooleanProperty(False)

    def on_enter(self):
        try:
            session = CryptoDatabase.get_session()
            cryptocurrencies = [crypto.name for crypto in session.query(Cryptocurrency).all()]
            self.ids.coin_name_spinner.values = cryptocurrencies

        except Exception as exception:
            self.show_error(f'General error occurred:\n{exception}')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.export_df = None

    def submit_history(self):
        self.ids.view_history_submit_button.disabled = True
        Clock.schedule_once(lambda dt: self.process_submission())  # Try to block the API request (doesn't always work)

    def process_submission(self):
        try:
            self.ids.history_message.text = ''
            self.ids.chart.source = ''
            self.ids.chart.reload()

            coin_name = self.ids.coin_name_spinner.text
            if coin_name == 'Select Coin':
                self.show_error("Please select a coin (i.e. Bitcoin).")
                return

            start_date_str = self.ids.start_date_input.text.strip()
            end_date_str = self.ids.end_date_input.text.strip()

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
            days_difference = (end_date - start_date).days
            if days_difference < 1 or days_difference > date_range:
                self.show_error(f"Date range must be between 1 and {date_range}.")
                return

            current_date = datetime.now()
            days_ago = (current_date - start_date).days
            if days_ago > 365:
                self.show_error("Historical data queries cannot further than 365 days ago.")
                return

            chart_type = self.ids.historical_price_chart_spinner.text
            if chart_type == "Select Chart Type":
                self.show_error("Please select a chart type.")
                return

            session = CryptoDatabase.get_session()

            crypto = session.query(Cryptocurrency).filter(Cryptocurrency.name == coin_name).first()
            if not crypto:
                self.show_error(f"No coin found with symbol '{coin_name}'.")
                return

            coingecko = CoinGeckoAPI()

            from_timestamp = int(start_date.replace(tzinfo=timezone.utc).timestamp())
            to_timestamp = int(
                (end_date + timedelta(days=1) - timedelta(seconds=1)).replace(tzinfo=timezone.utc).timestamp())

            data = coingecko.get_coin_market_chart_range_by_id(id=crypto.coingecko_id, vs_currency='usd',
                                                               from_timestamp=from_timestamp, to_timestamp=to_timestamp)
            prices = data.get('prices', [])

            if not prices:
                self.show_error("No data for that window.")
                return

            df = pd.DataFrame(prices, columns=['timestamp', 'price'])
            df['Date'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('Date', inplace=True)

            ohlc = df['price'].resample('D').agg(
                {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'}).dropna().reset_index()

            date_list = [row for row in ohlc['Date']]
            open_prices = [row for row in ohlc['Open']]
            high_prices = [row for row in ohlc['High']]
            low_prices = [row for row in ohlc['Low']]
            close_prices = [row for row in ohlc['Close']]

            self.export_df = pd.DataFrame(
                {'Date': date_list, 'Open': open_prices, 'High': high_prices, 'Low': low_prices, 'Close': close_prices})

            plt.figure(figsize=(6, 4))

            if chart_type == "Line Chart":
                plt.plot(date_list, close_prices, linestyle='-')
            elif chart_type == "Bar Chart":
                plt.bar(date_list, close_prices)
            elif chart_type == "Candlestick Chart":
                ohlc_dataframe = pd.DataFrame(
                    {'Open': open_prices, 'High': high_prices, 'Low': low_prices, 'Close': close_prices, },
                    index=date_list)
                ohlc_dataframe.index = pd.DatetimeIndex(ohlc_dataframe.index)

                axis = plt.gca()

                mpf.plot(ohlc_dataframe, type='candle', ax=axis, datetime_format='%Y-%m-%d', tight_layout=True,
                         show_nontrading=True)

            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.title(f"{coin_name} Price History")
            plt.xticks(rotation=45)
            plt.tight_layout()

            chart_file = "chart.png"
            plt.savefig(chart_file)
            plt.close()

            self.ids.chart.source = chart_file
            self.ids.chart.reload()
            self.show_success("Price history loaded successfully.")
            self.is_historical_data_generated = True
        except Exception as exception:
            self.show_error(f'General error occurred:\n{exception}')
        finally:
            self.ids.view_history_submit_button.disabled = False

    def export_to_csv(self):
        try:
            self.export_df.to_csv("historical_data.csv", index=False)
            self.show_success("Successfully exported CSV.")
        except Exception as exception:
            self.show_error(f'Error occurred while exporting to CSV:\n{exception}')

    def show_error(self, message):
        self.ids.history_message.text = message
        self.ids.history_message.color = ((214 / 256), (69 / 256), (69 / 256), 1.0)
        self.ids.history_message.opacity = 1

    def show_success(self, message):
        self.ids.history_message.text = message
        self.ids.history_message.color = ((50 / 256), (222 / 256), (153 / 256), 1.0)
        self.ids.history_message.opacity = 1

    def on_leave(self):
        self.ids.coin_name_spinner.text = 'Select Coin'
        self.ids.start_date_input.text = ''
        self.ids.end_date_input.text = ''
        self.ids.history_message.text = ''
        self.ids.chart.source = ''
        self.came_from_select_coin = False
        self.ids.historical_price_chart_spinner.text = 'Select Chart Type'

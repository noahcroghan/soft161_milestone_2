# Cryptocurrency App

- `main_app/main.py` Primary GUI Application
- `installer/database_installer.py` Creates tables and records in the database
- `historical_prices_app/main.py` Code for the Historical Price Viewer App
- `portfolio_tracker_app/main.py` Code for the Portfolio Tracker App

# Completeness

- The API is known to sometimes be slow when fetching OHLC data.
  This causes the app to occasionally stall or crash on
  the View History Screen.
  If you are trying to get data for the full 90-day range or press submit multiple times,
  expect the app to stall.
  A solution could not be found.
- No other known bugs at this time.

# Instructions

1. Clone the repository
2. Change into the cloned directory i.e `cd soft161_milestone_2` or import the directory into your IDE
3. Install Python 3.12
4. Install PIP package dependencies `pycoingecko`, `mplfinance`, `matplotlib`, `sqlalchemy`, and `kivy`
5. Install MySQL Server Community Edition
6. Make a file in the project ***root directory*** called `config.py` with the following contents

```python
username = 'root'  # Change username if applicable
port = 3306  # Change port if applicable
password = ""  # Enter password between quotes
```

7. Enter a MySQL shell, typically by running `mysql` from a terminal
8. In the MySQL shell, run the following commands (only need to run these on the first installation)
    - `DROP DATABASE IF EXISTS crypto;`
    - `CREATE DATABASE crypto;`
9. Run `installer/database_installer.py`
    - This will populate the database. You can verify it worked with the following commands:
        - `USE crypto;` (Will select the database)
        - `SELECT * FROM cryptocurrencies;` (Will get all cryptocurrency coins in the database)
10. Run the main application from the root directory with `python -m main_app.main` in a terminal or from your IDE.
    (or use `python3` if necessary)
# Cryptocurrency App

- `main_app/main.py` Primary GUI Application
- `historical_prices_app/main.py` Code for the Historical Price Viewer App
- `portfolio_tracker_app/main.py` Code for the Portfolio Tracker App
- `installer/database_installer.py` Creates tables and records in the database

# Completeness

[//]: # (TODO: The status of the apps in terms of completeness and correctness &#40;list any known issues or bugs&#41;)

# Instructions

1. Clone the repository
2. Install Python 3.12
3. Install dependencies `pycoingecko`, `mplfinance`, `matplotlib`, `sqlalchemy`, and `kivy`
4. Install MySQL Server Community Edition
5. Make a file in the project root directory called `config.py` with the following contents

```python
username = 'root'  # Change username if applicable
port = 3306  # Change port if applicable
password = ""  # Enter password between quotes
```

6. Enter a MySQL shell, typically by running `mysql` from a terminal
7. In the MySQL shell, run the following commands
    - `DROP DATABASE IF EXISTS crypto;`
    - `CREATE DATABASE crypto;`
8. Run `installer/database_installer.py`
    - This will populate the database. You can verify it worked with the following commands:
        - `USE crypto;` Will select the database
        - `SELECT * FROM cryptocurrencies;` Will get all cryptocurrency coins in the database.

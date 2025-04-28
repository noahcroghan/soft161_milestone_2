# Cryptocurrency App

- `main_app/main.py` Primary GUI Application
- `historical_prices_app/main.py` Code for the Historical Price Viewer App
- `portfolio_tracker_app/main.py` Code for the Portfolio Tracker App
- `installer/database_installer.py` Creates tables and records in the database

# Completeness

The status of the apps in terms of completeness and correctness (list any known issues or bugs)

# Instructions

[//]: # (Instructions for building and running the apps, including any required dependencies and commands to create the database)

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

In here, set your password and change your port and username if necessary.

Continue more instructions below...
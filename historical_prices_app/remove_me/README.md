# Historical Price Viewer App

- `main.py` Primary GUI application
- `crypto_installer.py`: Creates tables and records in database

# Completeness

Does not currently get accurate and up-to-date data from the CoinGecko API. It instead uses sample placeholder data.
Should otherwise be fully feature complete, and requirement meeting. No known bugs at this time.

# Instructions

1. Clone the repository
2. Install Python 3.12
3. Install dependencies Kivy, Matplotlib and SQLAlchemy using your IDE or however you prefer to install packages (e.g.
   `pip`)
4. Install MySQL Server Community Edition
    - By default, the program assumes you have no password. If you choose to set a password, make sure to set it in `config.py` (and don't accidentally commit this file with
      Git).
    - You can also set your port and username in this file if necessary.
5. Enter a MySQL shell, typically by running `mysql` from a terminal
6. In the MySQL shell, ensure the database doesn't already exist with `show databases;`
    - If it already exists, drop it with `drop database crypto;`
7. Create the database with `create database crypto;`
    - Note that `crypto_installer.py` will error if you do not complete this step!
    - After running this, you can verify data has been added by first selecting the database (`use crypto;`) and running
      any query on the data. (e.g. `select * from cryptocurrencies;`)

# CoinGecko Endpoints

Not currently used in implementation, may be helpful once the API has been implemented

- Getting market data with query parameters for ordering and filtering: `/coins/markets`
- Getting coin icon: `/coins/{id}`
- Getting a line chart: `/coins/{id}/market_chart`
- Fetching current prices: `/simple/price`
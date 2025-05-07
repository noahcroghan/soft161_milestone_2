# Cryptocurrency App

File Structure

- `main_app/main.py` Primary GUI Application
- `installer/database_installer.py` Creates tables and records in the database
- `historical_prices_app/main.py` Code for the Historical Price Viewer App
- `portfolio_tracker_app/main.py` Code for the Portfolio Tracker App

# Applications

- Main App: Includes the Login Screen, Switch User Screen, Help Screen, and Main Screen
- Portfolio Tracker App: Includes the New Cryptocurrency Screen, New Portfolio Screen, and Check Portfolio Screen
- Historical Prices App: Includes the Select Coin Screen and View History Screen

# Completeness

- There is a known issue with fetching OHLC data from CoinGecko that causes the View History Screen to stall or crash.
  This is due to the way
- No other known bugs at this time.
- App fully meets requirements.

# Instructions

1. Install Git.
    - Set up your [personal access token](https://docs.gitlab.com/user/profile/personal_access_tokens/) if you haven't
      already.
2. Clone the repository with:
    - `git clone git@git.unl.edu:bchebefuh2/soft161_milestone_2.git` or
    - `git clone https://git.unl.edu/bchebefuh2/soft161_milestone_2.git`
    - Provide the personal access token when asked for a username/password

3. Change into the cloned directory with `cd soft161_milestone_2` or import the directory into your IDE
4. Install and use [Python 3.12](https://www.python.org/downloads/), do so in
   a [virtual environment](https://wiki.archlinux.org/title/Python/Virtual_environment) if necessary.
    - Newer or older versions of Python are not guaranteed to work
5. Install package dependencies with `pip install pycoingecko mplfinance matplotlib sqlalchemy kivy`
    - You can alternatively install these in your IDE
6. Install [MySQL Server Community Edition](https://dev.mysql.com/downloads/mysql/).
7. Make a file in the project **root directory** called `config.py` with the following contents:

```python
username = 'root'  # Change username if applicable
port = 3306  # Change port if applicable
password = ""  # Enter MySQL server password between quotes or leave blank
```

8. Enter a MySQL shell, typically by running `mysql` from a terminal.
    - If the command isn't found, ensure MySQL is added to your system PATH variable or use the terminal included with
      your MySQL installation
9. In the MySQL shell, run the following commands (only need to run these on the first installation).
    - `DROP DATABASE IF EXISTS crypto;`
    - `CREATE DATABASE crypto;`
10. Run `installer/database_installer.py`.
    - This will populate the database. You can verify it worked with the following commands:
        - `USE crypto;` (Will select the database)
        - `SELECT * FROM cryptocurrencies;` (Will get all cryptocurrency coins in the database)
11. Run the main application from the root directory with `python -m main_app.main` in a terminal or from your IDE.
    (replace `python` with `python3` if necessary)
# _**Alijah Alfieri Milestone 1**_
Portfolio Tracker App

### Files
* Crypto App: main.py
* Database Installer: portfoliotrackerinstaller.py
* GUI Kivy File: portfoliotracker.kv
* Additional Information for the Installer: portfoliotracker.py

### Completenes
* To my knowledge, the app is fully complete and correct.

### Instructions
* Crypto App:
  * Run main.py
  * The home screen is the first screen opened.
  * Clicking on any of the buttons on the home screen will take you to that correlating screen.
  * Clicking the "HOME" button on the non-home screens will bring you back to the home screen.
  * New Cryptocurrency:
    * Clicking the "SUBMIT" button with text in all the TextInputs will clear the TextInputs and display the message "New Crypto Added".
    * Clicking the "SUBMIT" button without text in all the TextInputs will display the message "Error: Invalid Data".
    * Clicking the "HOME" button will clear all TextInputs and messages.
  * New Portfolio Entry:
    * Clicking the "SUBMIT" button with text in all the TextInputs will clear the TextInputs and display the message "New Portfolio Added".
    * Clicking the "SUBMIT" button without text in all the TextInputs will display the message "Error: Invalid Data".
    * Clicking the "HOME" button will clear all TextInputs and messages.
  * Check Portfolio Value:
    * Clicking the "CHECK" button with text in the "Portfolio ID" TextInput will display text under "Crypto Current Price:", "Current Portfolio Value:", and "Portfolio Value Change:".
    * Clicking the "CHECK" button without text in the "Portfolio ID" TextInput will display the message "Portfolio ID is Required".
    * Clicking the "HOME" button will clear the TextInput and message.
* Databse Installer:
  * Create a database called 'portfoliotracker' in your session of MySQL.
  * Change the authority, port, username, and password variables on line 15 of portfoliotrackerinstaller.py to reflect your session of MySQL.
  * Change the String (currently 'username') being set to = user_name on line 9 of portfoliotrackerinstaller.py to your username.
  * Run portfoliotrackerinstaller.py
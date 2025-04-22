import os
from dotenv import load_dotenv

load_dotenv('config.env')

if not os.path.exists('config.env'):
    raise FileNotFoundError("config.env file is missing. Please create it and define USERNAME and PORT inside, according to the README")

username = os.getenv('USERNAME')
port_string = os.getenv('PORT')
password = os.getenv('PASSWORD')

if not username:
    raise ValueError("USERNAME must be set in config.env")

if not port_string:
    raise ValueError("PORT must be set in config.env")

try:
    port = int(port_string)
except ValueError:
    raise ValueError("PORT must be a valid integer")
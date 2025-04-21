import os
from dotenv import load_dotenv

load_dotenv('config.env')

username = os.getenv('USERNAME')
port = int(os.getenv('PORT'))
password = os.getenv('PASSWORD')

if not username or not password or not port:
    raise Exception('Please set USERNAME, PASSWORD and PORT in config.env')
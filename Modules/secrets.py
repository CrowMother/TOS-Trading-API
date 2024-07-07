import os
from dotenv import load_dotenv

APP_KEY = ""
SECRET = ""

def set_secrets():
    global APP_KEY, SECRET
    load_dotenv()

    APP_KEY = os.getenv('APP_KEY')
    SECRET = os.getenv('SECRET')

def get_app_key():
    global APP_KEY
    if_empty(APP_KEY)
    return APP_KEY

def get_secret():
    global SECRET
    if_empty(SECRET)
    return SECRET

def if_empty(key):
    if (key == ""):
        set_secrets()
    else:
        return
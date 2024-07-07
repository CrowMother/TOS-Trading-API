import os
from dotenv import load_dotenv
from Modules import universal

APP_KEY = ""
SECRET = ""

def set_secrets():
    dotenv_path = os.path.join('config', '.env')
    global APP_KEY, SECRET
    load_dotenv(dotenv_path)

    APP_KEY = os.getenv('APP_KEY')
    SECRET = os.getenv('SECRET')
    check_set()


def get_app_key():
    if_empty()
    global APP_KEY
    return APP_KEY

def get_secret():
    if_empty()
    global SECRET
    return SECRET

def if_empty():
    global APP_KEY, SECRET
    if( APP_KEY or SECRET == ""):
        set_secrets()

def check_set():
    global APP_KEY, SECRET
    if( APP_KEY or SECRET == ""):
        universal.error_code("APP_KEY or SECRET not set from .env file. (check config folder for proper env file)")
    else:
        universal.okay_code("APP_KEY and SECRET set!")
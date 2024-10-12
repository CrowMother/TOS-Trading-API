from Modules import universal as u

import traceback
import datetime



#this is a file for enabling debugger level logging for trades tracker

def debugger_level():
    #configuration for debugging level
    return

def log_trade(data):
    """
    Logs a trade to trades.txt with a timestamp.

    Args:
        data (str): The trade data to be logged.
    """
    try:
        # Open the file in append mode to log errors without overwriting
        with open('trades.txt', 'a') as schwabDataFile:
            # Write the timestamp and the trade data
            schwabDataFile.write(f"[{u.get_time()}] {data}\n")
    except Exception as e:
        # Handle any exceptions that occur while logging the trade
        handle_exception(e, data)


def handle_exception(exception, extraData=""):
    """Handles an exception by logging the traceback to errors.txt."""
    try:
        # Get the full exception traceback
        error_message = traceback.format_exc()
        
        # Log the exception using the log_error function
        log_error(f": {extraData}: {error_message} ")
    except Exception as e:
        print(f"Failed to handle exception: {e}")

def log_error(error_message):
    """Logs an error message to errors.txt with a timestamp."""
    try:
        print(f"[{u.get_time()}]\n{error_message}\n")
        # Open the file in append mode to log errors without overwriting
        with open('errors.txt', 'a') as error_file:
            # Write the timestamp and the error message
            error_file.write(f"[{u.get_time()}] {error_message}\n")
    except Exception as e:
        print(f"Failed to log error: {e}")

def customPrint(message):
    
    print(message)
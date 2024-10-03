from Modules import universal as u

import traceback
import datetime



#this is a file for enabling debugger level logging for trades tracker


def log_trade(data):
    try:
        # Open the file in append mode to log errors without overwriting
        with open('trades.txt', 'a') as schwabDataFile:
            schwabDataFile.write(f"[{u.get_time}] {data}\n")
    except Exception as e:
        handle_exception(e, data)


def handle_exception(exception, extraData=""):
    """Handles an exception by logging the traceback to errors.txt."""
    try:
        # Get the full exception traceback
        error_message = traceback.format_exc()
        
        # Log the exception using the log_error function
        log_error(f"{error_message} : {extraData}")
    except Exception as e:
        print(f"Failed to handle exception: {e}")

def log_error(error_message):
    """Logs an error message to errors.txt with a timestamp."""
    try:
        # Open the file in append mode to log errors without overwriting
        with open('errors.txt', 'a') as error_file:
            # Write the timestamp and the error message
            error_file.write(f"[{u.get_time()}] {error_message}\n")
    except Exception as e:
        print(f"Failed to log error: {e}")
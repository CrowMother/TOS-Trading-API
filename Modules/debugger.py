from Modules import universal as u
from Modules import streamer
import traceback


class debugger:
    def __init__(self):
        #smaller number is less verbose logs and error codes
        self.debugLevel = 2


#this is a file for enabling debugger level logging for trades tracker


    def log_trade(self, data):
        """
        Logs a trade to trades.txt with a timestamp.

        Args:
            data (str): The trade data to be logged.
        """
        try:
            isTrade = streamer.contains_acct_activity(data)
           
           #check if it is a trade and the debug level is high enough
            if not isTrade and not(self.debugLevel < 2):
                #print if the debug level is high enough
                if self.debugLevel >= 2:
                    print(f"[{u.get_time()}]$\n {data}")
                #return if the debug level is not high enough
                return
            

 # Open the file in append mode to log errors without overwriting
            with open('trades.txt', 'a') as schwabDataFile:
                # Write the timestamp and the trade data
                schwabDataFile.write(f"[{u.get_time()}]$\n {data}\n")
                print(f"Trade logged at[{u.get_time()}]$\n{data}")
        except Exception as e:
            # Handle any exceptions that occur while logging the trade
            self.handle_exception(e, data)


    def handle_exception(self, exception, extraData=""):
        """Handles an exception by logging the traceback to errors.txt."""
        try:
            # Get the full exception traceback
            error_message = traceback.format_exc()
            
            # Log the exception using the log_error function
            self.log_error(f": {extraData}: {error_message} ")
        except Exception as e:
            print(f"Failed to handle exception: {e}")

    def log_error(self, error_message):
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
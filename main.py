import schwabdev #import the package
from Modules import secretkeys
from Modules import universal
from Modules import streamer
from Modules import test_data
import time
import threading



print("welcome to the Schwab API test Suite")
#links the bot to the client for placing and pulling information
client = schwabdev.Client(secretkeys.get_app_key(), secretkeys.get_secret())  #create a client

#grab the if it it is BTO CTO or other

#start of the main close
def main():
    #send test data
    #test_data.send_test_trade_order()
    
    streamer.set_streamer(client)
    # #streaming of real time account data with 
    isCrit_error = streamer.start_account_tracking(client)

    # Keep the main program alive indefinitely
    time.sleep(5)


main()
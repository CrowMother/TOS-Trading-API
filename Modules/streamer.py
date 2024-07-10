import schwabdev
from Modules import universal
from Modules import logger
import time

streamer = None

def set_streamer(client):
    global streamer
    streamer = client.stream
    

def my_handler(message):
    print(message)
    logger.write_to_log(message)

#tracking for stock pricing of AMD
def start_level_one_equity_stream(client):
    streamer.start(my_handler)
    client.stream.send(client.stream.level_one_equities("AMD,INTC", "0,1,2,3,4,5,6,7,8"))
    time.sleep(60)

#tracking of account data 
def start_account_tracking(client):
    streamer.start(my_handler)
    client.stream.send(client.stream.account_activity("Account Activity", "0,1,2,3,4,5,6,7,8"))
    time.sleep(60)
    
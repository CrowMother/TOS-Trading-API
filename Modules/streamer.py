
from Modules import universal
from Modules import logger
from Modules import secretkeys
from Modules import trade_processing 
from Modules import debugger
from Modules import JsonParser
import time
from flask import Flask, request, jsonify
import requests
import json




#main handler for new data coming in
def my_handler(data):
    if isinstance(data, dict):
        data_string = json.dumps(data)
    else:
        data_string = str(data)

    debugger.log_trade(data_string)
    print(f"{data_string}\n\n")
    
    # Sort out heartbeats and login responses
    isValidTrade = contains_acct_activity(data)
    if isValidTrade:
        #parse the incoming data
        dataDict = JsonParser.custom_json_parser(data_string)
        trade = trade_processing.Trade()


        #get current ID
        tradeID = dataDict.get('LifecycleSchwabOrderID')
        if tradeID is not None:
            #pull trade off ID
            oldData = trade_processing.load_trade_by_SchwabOrderID(tradeID)
            #if trade exists load into trade
            if oldData is not None:
                trade.load_from_json(oldData)
        #function to get older trades for the 2 parts to combine
        #new trade if not found
        
        #load new / current data to the trade
        trade.load_trade(dataDict)

        #other logic to format and post to server
        trade.send_trade()

        #store the trade
        trade.store_trade()


    return





def set_streamer(client):
    global streamer
    streamer = client.stream




# # Tracking for stock pricing of AMD and intel
# def start_level_one_equity_stream(client):
#     streamer.start(my_handler)
#     client.stream.send(client.stream.level_one_equities("AMD,INTC", "0,1,2,3,4,5,6,7,8"))
#     streamer.stop()

# Tracking of account data 
def start_account_tracking(client):
    if client is None:
        universal.error_code("Error Client is a None Type")
    else:
        streamer.start(my_handler)
        client.stream.send(client.stream.account_activity("Account Activity", "0,1,2,3"))

    

def contains_acct_activity(message):
    """Checks if the string contains '"service":"ACCT_ACTIVITY"'."""
    # Check if the substring '"service":"ACCT_ACTIVITY"' is in the message
    if '"response":[{"service":"ACCT_ACTIVITY"' in message:
        return False
    if 'SUBSCRIBED' in message:
        return False
    if '"service":"ACCT_ACTIVITY"' in message:
        return True
    
    return False
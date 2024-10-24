
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

db = debugger.debugger()


#main handler for new data coming in
def my_handler(data):
    """Handle incoming data from the streamer.

    Args:
        data: The incoming data from the streamer.
    """
    
    if isinstance(data, dict):
        data_string = json.dumps(data)
    else:
        data_string = str(data)
    
    db.log_trade(data_string)
    
    # Sort out heartbeats and login responses
    isValidTrade = contains_acct_activity(data)
    if isValidTrade:
        
        LoadedTradeData = None

        # Parse the incoming data
        dataDict = JsonParser.custom_json_parser(data_string)

        #create trade object
        trade = trade_processing.Trade()
        trade.load_trade(dataDict)

        #fill in first and second execution prices if executionPrice exists


        print(trade.SchwabOrderID)

        #load trades from json with matching SchwabOrderID if exists in trade_data.json
        #if not found, create new trade
        if trade.SchwabOrderID is not None:
            tradeID = (trade.SchwabOrderID)
            #check if trade exists in trade_data.json
            LoadedTradeData = trade_processing.load_trade_by_SchwabOrderID(tradeID)
            if LoadedTradeData is not None:
                LoadedTrade = trade_processing.Trade()
                LoadedTrade.load_from_json(LoadedTradeData)

                #combine trade and loaded trade objects
                trade = combine_trades(trade, LoadedTrade)

        #check if trade is placed
        trade.check_if_placed()

        #check if trade is complete






        #send the trade
        try:
            # Other logic to format and post to server
            trade.send_trade()
        except Exception as e:
            db.handle_exception(e, "Error sending trade")

        try:
            # Store the trade
            trade.store_trade()
        except Exception as e:
            db.handle_exception(e, "Error storing trade")

    return




def set_streamer(client):
    global streamer
    streamer = client.stream

def combine_trades(trade, LoadedTrade):
    """Combine the trade and loaded trade objects replacing loadedTrade data with the new trade data.

    Args:
        trade (Trade): The new trade object.
        LoadedTrade (Trade): The loaded trade object.
    Returns:
        Trade: The combined trade object.
    """
    for key in LoadedTrade.__dict__:
        setattr(LoadedTrade, key, getattr(trade, key) if getattr(trade, key) is not None else getattr(LoadedTrade, key))
    return LoadedTrade


# # Tracking for stock pricing of AMD and intel
# def start_level_one_equity_stream(client):
#     streamer.start(my_handler)
#     client.stream.send(client.stream.level_one_equities("AMD,INTC", "0,1,2,3,4,5,6,7,8"))
#     streamer.stop()

# Tracking of account data 
def start_account_tracking(client):
    try:
        if client is None:
            universal.error_code("Error Client is a None Type")
        else:
            #look into turning tracker off during market close
            streamer.start(my_handler)
            client.stream.send(client.stream.account_activity("Account Activity", "0,1,2,3"))
            return False
    except Exception as e:
        db.handle_exception(e, "Error in account tracking!!!!!!!!!!")
        return True
    

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
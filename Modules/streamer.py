
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
        data (dict or str): The incoming data from the streamer.
    """
    try:
        data_string = json.dumps(data) if isinstance(data, dict) else str(data)
        
        db.log_trade(data_string)

        # Sort out heartbeats and login responses
        if not contains_acct_activity(data):
            return

        # Parse the incoming data
        data_dict = JsonParser.custom_json_parser(data_string)

        # Create trade object
        trade = trade_processing.Trade()
        trade.load_trade(data_dict)

        # Load trades from json with matching SchwabOrderID if exists in trade_data.json
        # If not found, create new trade
        if trade.SchwabOrderID is not None:
            trade_id = trade.SchwabOrderID
            loaded_trade_data = trade_processing.load_trade_by_SchwabOrderID(trade_id)
            if loaded_trade_data is not None:
                loaded_trade = trade_processing.Trade()
                loaded_trade.load_from_json(loaded_trade_data)

                # Combine trade and loaded trade objects
                #trade = combine_trades(trade, loaded_trade)

        # Check if trade is placed
        trade.check_if_placed()

        # Check if trade is complete

        # Send the trade
        try:
            # Other logic to format and post to server
            trade.send_trade()
        except Exception as e:
            db.handle_exception(e, "Error sending trade")

        # Store the trade
        try:
            trade.store_trade()
        except Exception as e:
            db.handle_exception(e, "Error storing trade")

    except Exception as e:
        db.handle_exception(e, "Error in my_handler")
        streamer.stop()




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
            streamer = client.stream
            streamer.start(my_handler, daemon=False)
            streamer.send(streamer.account_activity("Account Activity", "0,1,2,3"))

    except Exception as e:
        db.handle_exception(e, "Error in account tracking!!!!!!!!!!")
        
        
    

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
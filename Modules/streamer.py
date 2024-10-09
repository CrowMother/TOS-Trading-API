
from Modules import universal
from Modules import logger
from Modules import secretkeys
from Modules import data as Data
from Modules import debugger
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
        # Since Data.Parse_data expects a JSON string, pass data_string
        parsed_data = Data.Parse_data(data_string)
        # universal.okay_code(parsed_data)
        
        logger.write_to_log(parsed_data)
        
        # Parse data that we need
        processed_data = Data.data_in(parsed_data)

    # Ensure that send_trade is called correctly within the application context
    return



def remove_specific_characters(input_string, characters_to_remove):
    return ''.join([char for char in input_string if char not in characters_to_remove])

def parse_message(message):
    try:
        chars_to_remove = "\[]}{\"\'"
        message = remove_specific_characters(message, chars_to_remove)
        mes_parts = message.split(",")
        #print(f"\nparts\n{mes_parts}")
        return mes_parts
    except Exception as e:
        print(f"can't parse: {e}")

def datafy(parsed_message):

    data = {'time': universal.time_stamp()}

    # Process each string in the parsed message
    for item in parsed_message:
        try:
            # Split on ':' and strip the quotes and whitespace
            key, value = item.split(':')
            key = key.strip().strip('"')
            value = value.strip().strip('"')
            data[key] = value
        except ValueError as e:
            universal.error_code(f"Skipping invalid format: {item}. Error: {str(e)}")
    
    return data


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
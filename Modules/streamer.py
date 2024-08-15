import schwabdev
from Modules import universal
from Modules import logger
import time
from flask import Flask, request, jsonify
import requests
import datetime
import json

app = Flask(__name__)
streamer = None

def remove_specific_characters(input_string, characters_to_remove):
    return ''.join([char for char in input_string if char not in characters_to_remove])

def parse_message(message):
    try:
        chars_to_remove = "\[]{\}\"\'"
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

def my_handler(message):
    #call a function to convert raw message to a data format similar to below
    #data = {'time': universal.time_stamp() ,
    #        'data': message}
    #{"response":[{"service":"ADMIN","command":"LOGIN","requestid":"0","SchwabClientCorrelId":"369e8458-2d9d-0d84-828a-03a694c658ca","timestamp":1722003493339,"content":{"code":0,"msg":"server=s0635dc6-4;status=NP"}}]}

    universal.okay_code(message)
    logger.write_to_log(message)
    
    # message_parsed = parse_message(message)
    # data = datafy(message_parsed)
    # print(data)
    # Ensure that send_trade is called correctly within the application context
    
    with app.app_context():
        send_trade(message)

# Tracking for stock pricing of AMD and intel
def start_level_one_equity_stream(client):
    streamer.start(my_handler)
    client.stream.send(client.stream.level_one_equities("AMD,INTC", "0,1,2,3,4,5,6,7,8"))
    time.sleep(60)
    streamer.stop()

# Tracking of account data 
def start_account_tracking(client):
    streamer.start(my_handler)
    client.stream.send(client.stream.account_activity("Account Activity", "0,1,2,3,4"))
    
    

# Get request to server to tell server we have new data to send
@app.route('/send-trade', methods=["GET"])
def send_trade(data):
    # Data to be sent to the other server

    # Post request to the other server
    try:
        response = requests.post('http://localhost:5000/receive-trade', json=data)
        # Return the response from the other server
        return jsonify({'status': 'data sent', 'response': response.json()})
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the POST request
        universal.error_code("connection with server lost!")
        
        #after error code figure out design for what to do with the data that can't be sent
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True)
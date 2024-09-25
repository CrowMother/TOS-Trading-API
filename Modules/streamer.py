
from Modules import universal
from Modules import logger
from Modules import secretkeys
from Modules import data as Data
import time
from flask import Flask, request, jsonify
import requests


app = Flask(__name__)
streamer = None
SERVER_URL = secretkeys.get_url()
print(SERVER_URL)

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

def my_handler(data):
    #universal.okay_code(data)
    logger.write_to_log(data)
    
    #parse data that we need
    data = Data.data_in(data)

    logger.write_to_log(f"Post data Processing: {data}")
    # Ensure that send_trade is called correctly within the application context\
    return


# Tracking for stock pricing of AMD and intel
def start_level_one_equity_stream(client):
    streamer.start(my_handler)
    client.stream.send(client.stream.level_one_equities("AMD,INTC", "0,1,2,3,4,5,6,7,8"))
    streamer.stop()

# Tracking of account data 
def start_account_tracking(client):
    if client is None:
        universal.error_code("Error Client is a None Type")
    else:
        streamer.start(my_handler)
        client.stream.send(client.stream.account_activity("Account Activity", "0,1,2,3,4"))
    
    
def send_trade_data_in_background(data):
    with app.app_context():
        try:

            print(f"sending data to: {SERVER_URL}")
            response = requests.post(f"{SERVER_URL}", json=data)
            response.raise_for_status()  # Handle HTTP errors
            return {'status': 'data sent', 'response': response.json()}
        except requests.exceptions.RequestException as e:
            universal.error_code(f"Connection with server lost! {str(e)}")
            return {'status': 'error', 'message': str(e)}

    
#send heart beat notification to server
@app.route('/send-heart', methods=["GET"])
def send_heart(data):
    global SERVER_URL
    # Post request to the other server
    try:
        
        time.sleep(30)
        response = requests.post(SERVER_URL, json=data)
        # Return the response from the other server
        return jsonify({'status': 'data sent', 'response': response.json()})
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the POST request
        universal.error_code("connection with server lost!")
        
        #after error code figure out design for what to do with the data that can't be sent
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    # Start the Flask app
     app.run(host="0.0.0.0", port=80, debug=True)
     


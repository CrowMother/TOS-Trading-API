import schwabdev
from Modules import universal
from Modules import logger
import time
from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)
streamer = None

def set_streamer(client):
    global streamer
    streamer = client.stream

def my_handler(message):
    #call a function to convert raw message to a data format similar to below
    #data = {'time': universal.time_stamp() ,
    #        'data': message}

    universal.okay_code(message)
    logger.write_to_log(message)
    # Ensure that send_trade is called correctly within the application context
    with app.app_context():
        send_trade(message)

# Tracking for stock pricing of AMD
def start_level_one_equity_stream(client):
    streamer.start(my_handler)
    client.stream.send(client.stream.level_one_equities("AMD,INTC", "0,1,2,3,4,5,6,7,8"))
    time.sleep(60)
    streamer.stop()

# Tracking of account data 
def start_account_tracking(client):
    streamer.start(my_handler)
    client.stream.send(client.stream.account_activity("Account Activity", "0,1,2,3,4,5,6,7,8"))
    
    

# Get request to server to tell server we have new data to send
@app.route('/send-trade', methods=["GET"])
def send_trade(message):
    # Data to be sent to the other server
    data = {'time': universal.time_stamp() ,
            'data': message}

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
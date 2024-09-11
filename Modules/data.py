import json
from Modules import streamer

order_data_map = {}

REQUIRED_FIELDS = [
    "SchwabOrderID", "AccountNumber", "UnderlyingSymbol", "StrikePrice",
    "OptionsQuote", "OptionExpiryDate", "ExecutionPrice", "OpenClosePositionCode"
]

def data_in(data):
    global order_data_map
    #print(data)
    """ #check if the heartbeat exists
    heartBeat = check_heart_beat(data)
    #if heartbeat then return
    
    #check if there is a heartbeat
    if heartBeat is not None:
        print(f"heartBeat: {heartBeat}")
        return heartBeat """
    
    #if not heart beat parse for data
    data = parse_json(data)
    #grab data needed to add to order data map


    completeOrders = check_data_map_completeness(order_data_map) 
    return completeOrders

def check_heart_beat(json_data):
    data = json.loads(json_data)
    for entry in data.get('notify', []):
            heartbeat = entry.get('heartbeat', 'N/A')
            return heartbeat

def update_order_data_map(json_data):
    SchwabOrderID = json_data.get("")


""" def parse_json(json_data):
    global order_data_map
    try:
        # Load the outer JSON data
        data = json.loads(json_data)

        for item in data.get('data', []):
            for content in item.get('content', []):
                # The '3' field contains a JSON string, so we need to parse it
                content_data = json.loads(content.get('3', '{}'))  # Parse the JSON string into a dictionary
                
                #parse into the nested json section
                nested_json_string = data['data'][0]['content'][0]['3']
                nested_data = json.loads(nested_json_string)  # Parse the nested JSON string

            # Extract values from the parsed JSON
                #Extract Order ID
                schwab_order_id = content_data.get('SchwabOrderID', 'N/A')
                #Extract Account Number
                account_number = content_data.get('AccountNumber', 'N/A')
                # Extract the symbol
                symbol = nested_data['BaseEvent']['OrderCreatedEventEquityOrder']['Order']['Order']['AssetOrderEquityOrderLeg']['OrderLegs'][0]['Security']['Symbol']
                # Extract the Strike
                strike_price = nested_data['BaseEvent']['OrderCreatedEventEquityOrder']['Order']['Order']['AssetOrderEquityOrderLeg']['OrderLegs'][0]['Security']['OptionsSecurityInfo']['StrikePrice']['lo']
                # Extract options quote (Call or Put)
                options_quote = nested_data['BaseEvent']['OrderCreatedEventEquityOrder']['Order']['Order']['AssetOrderEquityOrderLeg']['OrderLegs'][0]['QuoteOnOrderAcceptance']['OptionsQuote']['PutCallCode']
                # Extract Option Expiry Date
                option_expiry_date = nested_data['BaseEvent']['OrderCreatedEventEquityOrder']['Order']['Order']['AssetOrderEquityOrderLeg']['OrderLegs'][0]['Security']['OptionsSecurityInfo']['OptionExpiryDate']['DateTimeString']
                # Extract Execution Price
                #find this value
                execution_price = "N/A"
                # Extract OpenClosePositionCode
                open_close_position_code = nested_data['BaseEvent']['OrderCreatedEventEquityOrder']['Order']['Order']['AssetOrderEquityOrderLeg']['OrderLegs'][0]['EquityOrderLeg']['EquityOptionsOrderLeg']['OpenClosePositionCode']



                # Store or update the data in order_data_map
                if schwab_order_id not in order_data_map:
                    order_data_map[schwab_order_id] = {
                        "SchwabOrderID": schwab_order_id,
                        "AccountNumber": account_number,
                        "Symbol": symbol,
                        "strikePrice": strike_price,
                        "OptionsQuote": options_quote,
                        "OptionExpiryDate": option_expiry_date,
                        "ExecutionPrice": execution_price,
                        "OpenClosePositionCode": open_close_position_code
                    }
                else:
                    # Update only if new data is provided
                    order_data_map[schwab_order_id].update({
                        "Symbol": symbol if symbol != 'N/A' else order_data_map[schwab_order_id]["Symbol"],
                        "strikePrice": strike_price if strike_price != 'N/A' else order_data_map[schwab_order_id]["strikePrice"],
                        "OptionsQuote": options_quote if options_quote != 'N/A' else order_data_map[schwab_order_id]["OptionsQuote"],
                        "OptionExpiryDate": option_expiry_date if option_expiry_date != 'N/A' else order_data_map[schwab_order_id]["OptionExpiryDate"],
                        "ExecutionPrice": execution_price if execution_price != 'N/A' else order_data_map[schwab_order_id]["ExecutionPrice"],
                        "OpenClosePositionCode": open_close_position_code if open_close_position_code != 'N/A' else order_data_map[schwab_order_id]["OpenClosePositionCode"]
                    })

        return order_data_map
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return "" """

def parse_json(json_data):
    json_data = remove_specific_characters(json_data, "\"][}{\\//")
    manual_json_parse(json_data)
    return json_data



    
# Function to check if an order has all required fields
def is_order_complete(order):
    return all(order.get(field, None) is not None and order[field] != 'N/A' for field in REQUIRED_FIELDS)

# Function to check completeness of all orders in the data map
def check_data_map_completeness(order_data_map):
    complete_orders = []
    for order_id, order in order_data_map.items():
        if is_order_complete(order):
            complete_orders.append(order_id)
    return complete_orders


def datapoint_get(context, key):
    return context.get(key, 'N/A')

def manual_json_parse(json_data):
    parsed_json = {}
    
    # Remove leading/trailing whitespace and escape characters
    cleaned_data = json_data.replace('\\"', '"').replace("\\", "")
    
    # Split data into segments for each key-value pair
    sections = cleaned_data.split('{')
    
    # Traverse each section
    for section in sections:
        terms = section.split(",")
        for term in terms:
            # Further split on ':' to get key-value pairs
            if ":" in term:
                key, value = term.split(":", 1)
                key = key.strip().replace('"', '')  # Clean key
                value = value.strip().replace('"', '')  # Clean value
                
                # Check if the key matches any of the required fields
                if any(required_field in key for required_field in REQUIRED_FIELDS):
                    print(f"Found field: {key} -> {value}")
                    parsed_json[key] = value
    
    print("_________________________________________________________")
    return parsed_json

def is_useful_key(key):
    if key in REQUIRED_FIELDS:
        return True
    else:
        return False


def remove_specific_characters(json_data, chars):
    for char in chars:
       json_data = json_data.replace(char, "")
    return json_data
    
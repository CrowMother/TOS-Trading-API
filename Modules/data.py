import json
from Modules import streamer
from Modules import universal

ORDER_DATA_MAP = {}

REQUIRED_FIELDS = [
    "SchwabOrderID", "AccountNumber", "UnderlyingSymbol", "StrikePrice",
    "OptionsQuote", "OptionExpiryDate", "ExecutionPrice", "OpenClosePositionCode"
]

def data_in(data):
    
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
    #format out un-needed data
    data = format_data(data)
    Load_order_data_map(data)
    check_and_send_all_orders()


def check_and_send_all_orders():
    # Iterate through all SchwabOrderIDs in ORDER_DATA_MAP
    for schwabOrderID, order_data in list(ORDER_DATA_MAP.items()):
        # Check if all required fields are present for each order
        if all(field in order_data and order_data[field] is not None and order_data[field] != "" for field in REQUIRED_FIELDS):
            # All required fields are present, call the send function
    #change this line to the send function for sending the data to the server
            print(order_data)
            
            # After sending, delete the entry from ORDER_DATA_MAP
            del ORDER_DATA_MAP[schwabOrderID]
            print(f"Data sent and deleted for SchwabOrderID: {schwabOrderID}")
        else:
            # Some fields are still missing
            missing_fields = [field for field in REQUIRED_FIELDS if field not in order_data or order_data[field] is None]
            print(f"Missing fields for SchwabOrderID {schwabOrderID}: {missing_fields}")



def Load_order_data_map(data):
    # Extract SchwabOrderID first to use as the key
    schwabOrderID = data.get('SchwabOrderID')
    
    if not schwabOrderID:
        print("Missing SchwabOrderID, cannot store data.")
        return
    
    # If the order ID already exists in the map, fetch existing data, else create a new dictionary
    order_data = ORDER_DATA_MAP.get(schwabOrderID, {})
    
    # Update the existing data with any new fields provided in this data batch
    for field in REQUIRED_FIELDS:
        # Only update the field if it's provided and not None
        if field in data and data[field] is not None:
            order_data[field] = data[field]
    
    # Store or update the order data in the map
    ORDER_DATA_MAP[schwabOrderID] = order_data



#checks for heart beat for updating status of applications
def check_heart_beat(json_data):
    try:
        data = json.loads(json_data)
        for entry in data.get('notify', []):
                heartbeat = entry.get('heartbeat', 'N/A')
                return heartbeat
    except:
        return None



def format_data(data):
    print(data)
    data['AccountNumber'] = integerize(data.get('AccountNumber'))
    data['LifecycleSchwabOrderID'] = integerize(data.get('LifecycleSchwabOrderID'))
    data['StrikePrice'] = integerize(data.get('StrikePrice'))
    data['OptionExpiryDate'] = format_date(data.get('OptionExpiryDate'))
    data['SchwabOrderID'] = integerize(data.get('SchwabOrderID'))
    data['OptionsQuote'] = data.get('OptionsQuote').split(":", 1)[1]
    print("data parsed Correctly")
    return data

def parse_json(json_data):
    json_data = remove_specific_characters(json_data, "\"][}{\\//")
    json_data = manual_json_parse(json_data)
    return json_data
    
# Function to check if an order has all required fields


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
    
#converts strings to integer values
def integerize(string_data):
    if string_data is not None:
        filtered_string = ''.join(filter(str.isdigit, string_data))
        return int(filtered_string) if filtered_string else None
    return ""

def format_date(input):
    #2024-07-19 00
    if input is not None:
        universal.okay_code(input)
        #remove hours
        date = universal.split_string_at_char(input, " ", 0)
        
        #sperate the time stamp
        year = universal.split_string_at_char(date, "-", 0)
        month = universal.split_string_at_char(date, "-", 1)
        day = universal.split_string_at_char(date, "-", 2)
        #this is the lazy approach so fix in the future if needed
        year = universal.split_string_at_char(date, "0", 1)
        year = remove_specific_characters(year, "-")
        return(f"{month}/{day}/{year}")
    return ""




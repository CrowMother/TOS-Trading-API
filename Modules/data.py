import json
from Modules import streamer
from Modules import universal

ORDER_DATA_MAP = {}

REQUIRED_FIELDS = [
    "SchwabOrderID", "AccountNumber", "UnderlyingSymbol", "StrikePrice",
    "OptionsQuote", "OptionExpiryDate", "ExecutionPrice", "OpenClosePositionCode", "Quantity"
]

def data_in(data):
    #rework heartbeat detection and remove heartbeats or print in a single statement 
    
    #if not heart beat parse for data
    data = parse_json(data)
    #check for heart beat and login
    if len(data) < 3:
        #send a heartbeat
        print("heart Beat")
        return
    
    #format out un-needed data
    data = format_data(data)
    Load_order_data_map(data)
    check_and_send_all_orders()


def check_and_send_all_orders():
    # Iterate through all SchwabOrderIDs in ORDER_DATA_MAP
    for schwabOrderID, order_data in list(ORDER_DATA_MAP.items()):
        # Check if all required fields are present and non-empty
        missing_fields = [field for field in REQUIRED_FIELDS 
                          if field not in order_data or order_data[field] is None or order_data[field] == ""]
        
        if not missing_fields:
            # All required fields are present, call the send function
            # Replace with your actual function to send data
            print(order_data)
            streamer.send_trade_data_in_background(order_data)
            # After sending, delete the entry from ORDER_DATA_MAP
            del ORDER_DATA_MAP[schwabOrderID]
            print(f"Data sent and deleted for SchwabOrderID: {schwabOrderID}")
        else:
            # Some fields are still missing, print them
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
        if field in data and data[field] is not None and data[field] != "":
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
    #print(data)
    data['AccountNumber'] = integerize(data.get('AccountNumber'))
    data['LifecycleSchwabOrderID'] = integerize(data.get('LifecycleSchwabOrderID'))
    data['StrikePrice'] = integerize(data.get('StrikePrice'))
    data['OptionExpiryDate'] = format_date(data.get('OptionExpiryDate'))
    data['SchwabOrderID'] = integerize(data.get('SchwabOrderID'))
    data['Quantity'] = integerize(data.get('Quantity'))
    data['ExecutionPrice'] = integerize(data.get('ExecutionPrice'))
    
    if 'OptionsQuote' in data and data['OptionsQuote'] is not None:
        # Check if the split works correctly (and avoid IndexError)
        if ":" in data['OptionsQuote']:
            data['OptionsQuote'] = data.get('OptionsQuote').split(":", 1)[1]

    if 'OpenClosePositionCode' in data and data['OpenClosePositionCode'] is not None:
        # Check if the split works correctly (and avoid IndexError)
        equity_order_leg_parts = data['OpenClosePositionCode'].split(":")
        if len(equity_order_leg_parts) >= 3:
            data['OpenClosePositionCode'] = equity_order_leg_parts[2]

    print("data parsed Correctly")
    return data

def parse_json(json_data):
    json_data = remove_specific_characters(json_data, "\"][}{\\//")
    json_data = manual_json_parse(json_data)
    return json_data
    


# Function to check if an order has all required fields

def manual_json_parse(json_data):
    parsed_json = {}

    # Step 1: Clean the data (ensure the JSON-like string is workable)
    cleaned_data = json_data.replace('\\"', '"').replace("\\", "")
    
    # Step 2: Manually search for each required field
    for required_field in REQUIRED_FIELDS:
        field_position = cleaned_data.find(required_field)
        if field_position != -1:
            # Extract the value for the found required field
            # Assume the value follows after ':' and is either followed by a comma or a closing brace
            start_index = field_position + len(required_field) + 1  # move past the key and the colon
            end_index = cleaned_data.find(',', start_index)
            if end_index == -1:
                end_index = cleaned_data.find('}', start_index)
            value = cleaned_data[start_index:end_index].strip()

            # Clean the extracted value further
            value = value.replace('"', '').strip()
            parsed_json[required_field] = value
            print(f"{required_field} -> {value}")
    
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
    if string_data is not None and string_data != "":
        filtered_string = ''.join(filter(str.isdigit, string_data))
        return int(filtered_string) if filtered_string else None
    return ""

def format_date(input):
    #2024-07-19 00
    if input is not None and input != "":
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


def calculate_price(value, quantity):
    return (value / quantity)


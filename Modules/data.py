import json
from Modules import streamer
from Modules import universal

ORDER_DATA_MAP = {}

#"signScale\":12 create a code to find the signScale or a similar value

REQUIRED_FIELDS = [
    "SchwabOrderID", "AccountNumber", "UnderlyingSymbol", "StrikePrice",
    "OptionsQuote", "OptionExpiryDate", "ExecutionPrice", "OpenClosePositionCode", 
    "Quantity", "signScale"

]

def data_in(data):

    





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

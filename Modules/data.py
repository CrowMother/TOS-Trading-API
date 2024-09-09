import json

order_data_map = {}

def data_in(data):
    global order_data_map
    print(data)
    #check if the heartbeat exists
    heartBeat = check_heart_beat(data)
    #if heartbeat then return
    if heartBeat is not None:
        print(f"heartBeat: {heartBeat}")
        return heartBeat
    
    order_data_map = parse_json(data)
    if order_data_map is not None:
        print(order_data_map)

def check_heart_beat(json_data):
    data = json.loads(json_data)
    for entry in data.get('notify', []):
            heartbeat = entry.get('heartbeat', 'N/A')
            return heartbeat

def parse_json(json_data):
    global order_data_map
    data = json.loads(json_data)
    try:

        for item in data.get('data', []):
            for content in item.get('content', []):
                schwab_order_id = content.get('3', {}).get('SchwabOrderID', 'N/A')
                account_number = content.get('3', {}).get('AccountNumber', 'N/A')
                quote = content.get('3', {}).get('BaseEvent', {}).get('ExecutionRequestedEventRoutedInfo', {}).get('RouteInfo', {}).get('Quote', {})
                symbol = quote.get('Symbol', 'N/A')
                options_quote = quote.get('OptionsQuote', {}).get('PutCallCode', 'N/A')
                strike_price = quote.get('strikePrice', 'N/A')
                option_expiry_date = quote.get('OptionExpiryDate', {}).get('DateTimeString', 'N/A')
                execution_price = content.get('3', {}).get('BaseEvent', {}).get('ExecutionRequestedEventRoutedInfo', {}).get('RouteInfo', {}).get('RoutedPrice', {}).get('lo', 'N/A')
                open_close_position_code = content.get('3', {}).get('BaseEvent', {}).get('ExecutionRequestedEventRoutedInfo', {}).get('RouteInfo', {}).get('OptionsQuote', {}).get('OpenClosePositionCode', 'N/A')

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
                    # Update existing data if new values are available
                    order_data_map[schwab_order_id].update({
                        "Symbol": symbol if symbol != 'N/A' else order_data_map[schwab_order_id]["Symbol"],
                        "strikePrice": strike_price if strike_price != 'N/A' else order_data_map[schwab_order_id]["strikePrice"],
                        "OptionsQuote": options_quote if options_quote != 'N/A' else order_data_map[schwab_order_id]["OptionsQuote"],
                        "OptionExpiryDate": option_expiry_date if option_expiry_date != 'N/A' else order_data_map[schwab_order_id]["OptionExpiryDate"],
                        "ExecutionPrice": execution_price if execution_price != 'N/A' else order_data_map[schwab_order_id]["ExecutionPrice"],
                        "OpenClosePositionCode": open_close_position_code if open_close_position_code != 'N/A' else order_data_map[schwab_order_id]["OpenClosePositionCode"]
                    })

        return order_data_map
    except:
        print("error in parsing")
        return ""


    

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
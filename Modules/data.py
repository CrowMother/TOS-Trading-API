import json
from Modules import streamer
from Modules import universal
from Modules import webhook
from Modules import debugger
from functools import reduce
import jmespath



TRADES_DICT = {}



#tracks the whole trade
class Trade:
    def __init__(self):
        self.schwabOrderID = ""
        self.tradeType = ""
        self.processingStep = "" #Based off the furthest along step in the trade
        self.tradeStatus = "" #Order completed (opening), working(position is open), close() , used for checking if trade is complete to calcualte win loss rate

        self.openExecutionPrice = ""
        self.closeExecutionPrice = ""

        self.subTrades = [] #binds all subtrades of this 

        


    # Method to check for unique tradeStatus
    def add_sub_trade(self, sub_trade):
        # Check if tradeStatus is unique among subTrades
        if any(trade.tradeStatus == sub_trade.tradeStatus for trade in self.subTrades):
            print(f"Error: Duplicate tradeStatus '{sub_trade.tradeStatus}' found in Trade '{self.schwabOrderID}'.")
        #add the duplicate trade no matter what for now, look into how often if ever this happens and if it is an issue in the future
        self.subTrades.append(sub_trade)

    #function to check what kind of trade this will be
    # Method for checking for standard or multiLeg positions
    def check_trade_type(self):
        # Assuming all subTrades should have the same multiLegStrategyType in a trade
        for sub_trade in self.subTrades:
            print(sub_trade.multiLegStrategyType)
            if sub_trade.multiLegStrategyType:  # Check if multiLegStrategyType is not empty
                # Identify the strategy type based on multiLegStrategyType
                strategy_type = sub_trade.multiLegStrategyType
                if strategy_type == "VerticalSpread":
                    print(f"Trade {self.schwabOrderID} is a Vertical Spread.")
                    tradeType =  "Vertical Spread"
                elif strategy_type == "CalendarSpread":
                    print(f"Trade {self.schwabOrderID} is a Calendar Spread.")
                    tradeType = "Calendar Spread"
                elif strategy_type == "IronCondor":
                    print(f"Trade {self.schwabOrderID} is an Iron Condor.")
                    tradeType = "Iron Condor"
                # Add more strategies here as needed
                elif strategy_type == "N/F":
                    print(f"Trade {self.schwabOrderID} is a Regular Trade.")
                    tradeType = "Regular"
                    return "Regular"
                else:
                    print(f"Trade {self.schwabOrderID} has an unknown multi-leg strategy: {strategy_type}")
                    tradeType = "Unknown Strategy"
            else:
                print(f"Trade {self.schwabOrderID} is not found.")
                tradeType = "N/F"

        self.tradeType = tradeType

    def update_processing_step(self, order_steps):
        # Create a mapping of tradeStatus to its index in order_steps
        step_index = {step: index for index, step in enumerate(order_steps)}

        # Find the highest index of tradeStatus in subTrades
        highest_index = -1
        for sub_trade in self.subTrades:
            if sub_trade.tradeStatus in step_index:
                index = step_index[sub_trade.tradeStatus]
                if index > highest_index:
                    highest_index = index

        # Set the processingStep to the latest step if found
        if highest_index != -1:
            self.processingStep = order_steps[highest_index]
        else:
            self.processingStep = "Not Started"  # Default if no valid status found


               
    #tracks parts of the trade based on status of the trade
class SubTrade():
    def __init__(self):
        tradeStatus = ""

        shortDescriptionText = ""
        executionPrice = ""
        executionSignScale = ""
        underlyingSymbol = ""
        buySellCode = ""
        routedAmount = "" #figure out what the acutal value for multilegs are for this
        multiLegLimitPriceType = ""
        multiLegStrategyType = ""

    def get_sub_trade(self):

        self.tradeStatus


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#start of the data processing pipeline
def data_in(data):
    #sort out non-trades and heartbeats
    
    
    #create a trade object and store the subtrades within it
    trade = load_trade(data)

    #store the trade object
    schwabOrderID = trade.schwabOrderID
    
    if schwabOrderID in TRADES_DICT:
        # If the SchwabOrderID already exists in TRADES_DICT, combine the subTrades
        existing_trade = TRADES_DICT[schwabOrderID]
        # Merge subTrades
        existing_trade.subTrades.extend(trade.subTrades)
    else:
        # If it's a new trade, add it to TRADES_DICT
        TRADES_DICT[schwabOrderID] = trade

    #transfer over to the Global variable
    trade = TRADES_DICT[schwabOrderID]

    #get the type of trade to check for multiLeg
    trade.tradeType = trade.check_trade_type()
    
    

    if trade.tradeType == "Regular":
        tradeData = regularTrade(trade)
        if tradeData is not None:
            webhook.webhookout(tradeData)

            

def regularTrade(trade):
    #steps for each of the sub trade
        #put in the order of first to complete
        order_steps = [
            "orderCreated",
            "orderAccepted",
            "changeCreated",
            "ExecutionRequested",
            "ExecutionRequestCreated",
            "ExecutionRequestCompleted",
            "OrderFillCompleted"  # Last one being found should send the data
        ]
        #look and load the important data

        #update trade status
        trade.update_processing_step(order_steps)
        print(f"trade processing step: {trade.processingStep}")
        #if the trade is last in the process then send the data

        if trade.processingStep == order_steps[len(order_steps) - 1]: #calculating highest index
            print("prep data to send")
            trade_data = {}
            #get subTrade Data
            #grab the data needed for sending it to discord
            trade_data = {}
            for subTrade in trade.subTrades:
                #be able to store the data long term and prevent over writes of empty data
                trade_data = extract_sub_trade_data(subTrade, trade_data)
                #print(trade_data)
            return(trade_data)
        else:
            return(None)
            
        

    #function to check if all data needed for that trade is present



    


#load data into the sub trades and subtrades into the trade class and return the current trade loaded
def load_trade(data):
    try:
         
        if not data or not isinstance(data, list) or len(data) == 0:
            print("Error: Data is empty or invalid.")
            return None
        trade = Trade()
        # Stores the SchwabOrderID from the first set of data
        if data != "" or not None:
            trade.schwabOrderID = recursive_search(data[0], "SchwabOrderID")
        print(f"SchwabOrderID: {trade.schwabOrderID}")

        
        # Loop for each of the subtrades
        for json_data in data:
            sub_trade = SubTrade()
            #print(f"Processing subtrade: {json_data}")

            # Recursively search for keys
            sub_trade.tradeStatus = recursive_search(json_data, "EventType")
            print(f"Trade Status: {sub_trade.tradeStatus}")

            sub_trade.shortDescriptionText = recursive_search(json_data, "ShortDescriptionText")
            print(f"Short Description: {sub_trade.shortDescriptionText}")

            sub_trade.executionPrice = recursive_search(json_data, "ExecutionPrice")
            print(f"Execution Price: {sub_trade.executionPrice}")

            sub_trade.executionSignScale = recursive_search(json_data, "signScale")
            print(f"Execution Sign Scale: {sub_trade.executionSignScale}")

            sub_trade.underlyingSymbol = recursive_search(json_data, "UnderlyingSymbol")
            print(f"Underlying Symbol: {sub_trade.underlyingSymbol}")


            sub_trade.buySellCode = recursive_search(json_data, "BuySellCode")
            print(f"BuySellCode : {sub_trade.buySellCode}")
            #add recursive search for loading multileg positions as well 
            sub_trade.multiLegStrategyType = "N/F"

            # Add the subtrade to the trade that is being tracked 
            trade.add_sub_trade(sub_trade)
        
        # Return the trade
        return trade
    except Exception as e:
        print(f"Data: {data}")
        debugger.handle_exception(e)
        return None



def recursive_search(data, target_key):
    """Recursively search for a key in a nested dictionary or list."""
    try:
        if isinstance(data, dict):
            # Iterate over dictionary keys and values
            for key, value in data.items():
                if key == target_key:
                    return value  # Key found, return the value
                elif isinstance(value, (dict, list)):
                    # Recursively search nested structures
                    result = recursive_search(value, target_key)
                    if result is not None:
                        return result  # Return the result if found
        elif isinstance(data, list):
            # Iterate over items if the current level is a list
            for item in data:
                result = recursive_search(item, target_key)
                if result is not None:
                    return result
        return None  # If not found
    except Exception as e:
        debugger.handle_exception(e, data)





def pull_json_data(json_data, path, default_value="N/F"):
    """Safely extract a field from nested JSON data using jmespath."""
    try:
        result = jmespath.search(path, json_data)
        return result if result is not None else default_value
    except Exception as e:
        print(f"Error accessing path '{path}': {e}")
        return default_value


    


def Parse_data(json_string):
    start_search = 0
    jsonData = []

    #loop through the data set looking for the fields needed
    while True:
        # Find the start and end index of the "3" field
        startIndex, endIndex = find_end_of_field(json_string, "3", start_search)

        if startIndex is None or endIndex is None:
            break  # No more fields found

        # Extract the content within the brackets
        content = json_string[startIndex:endIndex]

        # Count open and closing braces
        openBrackets = content.count('{')
        closeBrackets = content.count('}')

        # If there are unbalanced brackets, calculate how many closing braces are missing
        if openBrackets > closeBrackets:
            missing = openBrackets - closeBrackets
            content = content + '}' * missing  # Append missing closing brackets

        # Check if the content is now balanced
        if check_balanced_brackets(content):
            try:
                # Parse the balanced content as JSON
                data = json.loads(content[content.find('{'):])  # Parsing only the JSON part
                #print(f"\n\nParsed Data: {data}")
                jsonData.append(data)
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}")
        else:
            print(f"Unbalanced Brackets in data set")

        # Update the starting search index for the next field to end of current field
        start_search = endIndex
    return jsonData      
                


def extract_sub_trade_data(sub_trade, trade_data):
    # Initialize an empty dictionary to store valid data or "N/F"

    # Define fields to extract and check
    fields_to_check = {
        "tradeStatus": pull_sub_trade_field(sub_trade, "tradeStatus"),
        "shortDescriptionText": pull_sub_trade_field(sub_trade, "shortDescriptionText"),
        "executionPrice": pull_sub_trade_field(sub_trade, "executionPrice"),
        "executionSignScale": pull_sub_trade_field(sub_trade, "executionSignScale"),
        "underlyingSymbol": pull_sub_trade_field(sub_trade, "underlyingSymbol"),
        "buySellCode": pull_sub_trade_field(sub_trade, "buySellCode"),
        "routedAmount": pull_sub_trade_field(sub_trade, "routedAmount"),
        "multiLegLimitPriceType": pull_sub_trade_field(sub_trade, "multiLegLimitPriceType"),
        "multiLegStrategyType": pull_sub_trade_field(sub_trade, "multiLegStrategyType")
    }

    # Store all fields, including those with "N/F"
    for key, value in fields_to_check.items():
        # Only store "N/F" if the field is missing or empty in the trade_data dictionary
        if key not in trade_data or trade_data[key] in [None, "", "N/F"]:
            trade_data[key] = value  # Store the new value, whether valid or "N/F"

    return trade_data


def pull_sub_trade_field(sub_trade, field_name):
    """Safely extract a field from sub_trade or return 'N/F' if missing."""
    try:
        # Use getattr to safely access the field
        value = getattr(sub_trade, field_name, None)
        # Return the value if it exists, or "N/F" if it's None
        return value if value is not None else "N/F"
    except Exception as e:
        # Log the error and return "N/F" if any exception occurs
        debugger.handle_exception(e)
        print(f"Error accessing {field_name}: {e}")
        return "N/F"


def check_balanced_brackets(string):
    stack = []
    
    for char in string:
        if char == '{':
            stack.append(char)  # Push to stack when an open bracket is found
        elif char == '}':
            if not stack:
                return False  # More closing brackets than opening
            stack.pop()  # Pop from stack when a closing bracket is found
    
    # If the stack is empty, all brackets are balanced
    return len(stack) == 0


def find_end_of_field(json_string, field, start_search=0):
    # Find the position of the field starting from the given index
    field_pos = json_string.find(f'"{field}":', start_search)
    if field_pos == -1:
        return None, None  # Field not found
    
    start_pos = json_string.find('{', field_pos)
    if start_pos == -1:
        return None, None  # Opening curly brace not found

    # Track opening and closing braces to find the end of the field
    open_braces = 1  # Count the first open brace
    end_pos = start_pos + 1
    while open_braces > 0 and end_pos < len(json_string):
        if json_string[end_pos] == '{':
            open_braces += 1
        elif json_string[end_pos] == '}':
            open_braces -= 1
        end_pos += 1
    
    # Return the start and end positions
    return field_pos, end_pos
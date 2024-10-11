import json
import os
import re
import math
from Modules import webhook
from Modules import debugger

#if some strikes are too high while others look at rounding method

TRADES_DICT = {}

class Trade:
    def __init__(self):
        # Declaring instance attributes using self
        self.SchwabOrderID = None           
        self.openClosePositionCode = None       
        self.buySellCode = None                
        self.shortDescriptionText = None         
        self.executionPrice = None              
        self.executionSignScale = None  
        self.orderStatus = None  
        self.underLyingSymbol = None


        self.firstExecutionPrice = None
        self.secondExecutionPrice = None


    

    def load_trade(self, dataDict):
        # Only load data if the attribute is currently None (or its initial value)
        if self.SchwabOrderID is None:
            schwabOrderID = dataDict.get('3')
            if schwabOrderID is not None:
                if len(schwabOrderID) > 1:
                    self.SchwabOrderID = schwabOrderID[1]
        
        if self.openClosePositionCode is None:
            self.openClosePositionCode = dataDict.get('OpenClosePositionCode')
        
        if self.buySellCode is None:
            self.buySellCode = dataDict.get('BuySellCode')
        
        if self.shortDescriptionText is None:
            self.shortDescriptionText = dataDict.get('ShortDescriptionText')
        
        #Execution needs both signScale and the price
        if self.executionPrice is None:
            limit_price = dataDict.get('ExecutionPrice')
            if limit_price is not None:
                if len(limit_price) > 1:
                    self.executionPrice = limit_price[1]  # Assuming second value is the price
        
        if self.executionSignScale is None:
            self.executionSignScale = dataDict.get('signScale')

        if self.underLyingSymbol is None:
            self.underLyingSymbol = dataDict.get('UnderlyingSymbol')
        
        if self.orderStatus is None:
            self.orderStatus = dataDict.get('2')

    def to_dict(self):
        # Converts the Trade object into a dictionary for easy comparison and storage
        return {
            "SchwabOrderID": self.SchwabOrderID,
            "OpenClosePositionCode": self.openClosePositionCode,
            "BuySellCode": self.buySellCode,
            "ShortDescriptionText": self.shortDescriptionText,
            "ExecutionPrice": self.executionPrice,
            "ExecutionSignScale": self.executionSignScale,
            "OrderStatus": self.orderStatus,
            "UnderLyingSymbol": self.underLyingSymbol,
            "FirstExecutionPrice": self.firstExecutionPrice,
            "SecondExecutionPrice": self.secondExecutionPrice
            
        }

    def store_trade(self, file_name="trade_data.json"):
        # Convert the current trade to a dictionary
        trade_data = self.to_dict()

        # Load existing trades from the JSON file, if the file exists
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                try:
                    existing_trades = json.load(file)
                    # Ensure it's a list
                    if not isinstance(existing_trades, list):
                        existing_trades = []
                except json.JSONDecodeError:
                    existing_trades = []
        else:
            existing_trades = []

        # Append the new trade to the list of existing trades
        existing_trades.append(trade_data)

        # Write the updated list of trades back to the file
        with open(file_name, 'w') as file:
            json.dump(existing_trades, file, indent=4)

        print(f"New trade data appended to {file_name}")

    def format_message(self):
        msgJSON = {}

        date, strike, callOrPut = split_short_description(self.shortDescriptionText)

        executionPrice = self.calculateExecution()
        msgJSON['message'] = f"{self.underLyingSymbol} ${strike} {callOrPut} {date} @ ${executionPrice}: {self.openClosePositionCode}"
        return msgJSON

    def send_trade(self):
        # Check if all the required fields are filled
        if all([self.SchwabOrderID, 
                self.openClosePositionCode, 
                self.buySellCode, 
                self.shortDescriptionText, 
                self.executionPrice, 
                self.executionSignScale, 
                self.orderStatus,
                self.underLyingSymbol]):
            # format data into a message
            msgJSON = self.format_message()

            self.firstExecutionPrice = self.executionPrice

            #send the data via webhook
            webhook.webhookout(msgJSON)
        else:
            # Do nothing if any field is missing
            print("Some required fields are missing, trade not sent.")
        
    

       
    def load_from_json(self, dataDict):
            """
            This function loads trade data from a dictionary (like the one parsed from a JSON file).
            """
            # Load data from the JSON structure, checking for None values
            self.SchwabOrderID = dataDict.get("SchwabOrderID", self.SchwabOrderID)
            self.openClosePositionCode = dataDict.get("OpenClosePositionCode", self.openClosePositionCode)
            self.buySellCode = dataDict.get("BuySellCode", self.buySellCode)
            self.shortDescriptionText = dataDict.get("ShortDescriptionText", self.shortDescriptionText)
            self.underLyingSymbol = dataDict.get("UnderLyingSymbol", self.underLyingSymbol)
            self.firstExecutionPrice = dataDict.get("FirstExecutionPrice")
            self.secondExecutionPrice = dataDict.get("SecondExecutionPrice")

            # Handling None values, in case the ExecutionPrice is missing in the JSON
            if dataDict.get("ExecutionPrice") is not None:
                self.executionPrice = dataDict.get("ExecutionPrice", self.executionPrice)
            


            self.executionSignScale = dataDict.get("ExecutionSignScale", self.executionSignScale)
            self.orderStatus = dataDict.get("OrderStatus", self.orderStatus)


    def calculateExecution(self):
        dividor = 10 ** math.floor(int(self.executionSignScale) / 2)
        return (float(self.executionPrice) / dividor)



def load_trade_by_SchwabOrderID(SchwabOrderID, file_name="trade_data.json"):
        # Load the JSON data from the file
        if not os.path.exists(file_name):
            print(f"File {file_name} not found.")
            return None

        try:
            with open(file_name, 'r') as file:
                trades = json.load(file)

                # Ensure trades is a list
                if not isinstance(trades, list):
                    print("Invalid data format: Expected a list of trades.")
                    return None

                # Iterate over each trade dictionary in the list
                for trade in trades:
                    if trade.get("SchwabOrderID") == SchwabOrderID:
                        return trade  # Return the matching trade

                # If no match is found
                print(f"No trade found with SchwabOrderID: {SchwabOrderID}")
                return None

        except json.JSONDecodeError:
            print("Error decoding the JSON file.")
            return None

 
def get_trade_ID(dataDict):
    orderID = dataDict.get('3')
    if orderID is not None:
        if len(orderID) > 1:
            SchwabOrderID = orderID[1]
            return SchwabOrderID

def split_short_description(inputString):
    try:
        # Regular expression to find the date (MM/DD/YYYY)
        pattern = r'(\d{2}/\d{2}/\d{4})'

        # Use re.split to split the string at the date
        split_values = re.split(pattern, inputString)
        date = split_values[1]
        strikeCorP = split_values[2]
        strike, callOrPut = strikeCorP.split()

        return date, strike, callOrPut
    except Exception as e:
        debugger.handle_exception(e, "Error in split_short_description")
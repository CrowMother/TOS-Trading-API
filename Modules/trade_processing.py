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
        """
        Loads the trade data from the given dictionary, overwriting any existing data only if it is None.
        """
        self._load_field('SchwabOrderID', dataDict.get('3'))
        self._load_field('openClosePositionCode', dataDict.get('OpenClosePositionCode'))
        self._load_field('buySellCode', dataDict.get('BuySellCode'))
        self._load_field('shortDescriptionText', dataDict.get('ShortDescriptionText'))
        self._load_field('executionPrice', dataDict.get('ExecutionPrice')[1] if dataDict.get('ExecutionPrice') else None)
        self._load_field('executionSignScale', dataDict.get('signScale'))
        self._load_field('underLyingSymbol', dataDict.get('UnderlyingSymbol'))
        self._load_field('orderStatus', dataDict.get('2'))

    def _load_field(self, field_name, value):
        """
        Helper function to load a field of the Trade object from the given dictionary, overwriting only if the field is currently None.
        """
        if getattr(self, field_name) is None:
            setattr(self, field_name, value)

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
        """
        Stores the current trade to a JSON file. If the file already contains
        a trade with the same SchwabOrderID, it is replaced with the new trade.
        Otherwise, the new trade is appended to the list of existing trades.
        """
        trade_data = self.to_dict()

        try:
            with open(file_name, 'r') as file:
                existing_trades = json.load(file)
        except FileNotFoundError:
            existing_trades = []
        except json.JSONDecodeError:
            existing_trades = []

        if not isinstance(existing_trades, list):
            existing_trades = []

        for i, existing_trade in enumerate(existing_trades):
            if existing_trade["SchwabOrderID"] == self.SchwabOrderID:
                existing_trades[i] = trade_data
                break
        else:
            existing_trades.append(trade_data)

        with open(file_name, 'w') as file:
            json.dump(existing_trades, file, indent=4)

    def format_message(self):
        msgJSON = {}

        date, strike, callOrPut = split_short_description(self.shortDescriptionText)

        openClosePosition = open_close_position(self.openClosePositionCode)

        executionPrice = self.calculateExecution()

        msgJSON['message'] = f"{self.underLyingSymbol} ${strike} {callOrPut} {date} @ ${executionPrice}: {openClosePosition}"
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

            # if first execution, set first execution price
            if self.firstExecutionPrice is None or self.openClosePositionCode == "PCOpen":
                self.firstExecutionPrice = self.executionPrice
                self.executionPrice = None
            # if second execution, set second execution price
            else:
                self.secondExecutionPrice = self.executionPrice
                self.executionPrice = None

            # if second execution, calculate gains/loss
            if self.firstExecutionPrice is not None and self.secondExecutionPrice is not None:
                # calculate gains/loss
                gainLoss = self.calculateGainsLoss()
                # append gain/loss to message
                # find solution to fix to 2 decimal points
                msgJSON['message'] += f" ({gainLoss}%)"

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


    def calculateGainsLoss(self):
        gainLoss = float(self.secondExecutionPrice) / float(self.firstExecutionPrice)
        gainLossPercentage = (gainLoss - 1) * 100
        return gainLossPercentage

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

def open_close_position(openClosePositionCode):
    if openClosePositionCode == "PCOpen":
        return "Open Position"
    if openClosePositionCode == "PCClose":
        return "Close Position"
    else:
        return openClosePositionCode
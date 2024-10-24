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
        self.underLyingSymbol = None
        
        self.date = None
        self.orderStatus = None  

        self.isPlaced = False
        self.isCompleted = False
        self.isMultiLeg = False


        self.firstExecutionPrice = None
        self.secondExecutionPrice = None

    

    def load_trade(self, dataDict):
        """
        Loads the trade data from the given dictionary, overwriting any existing data only if it is None.
        """
        self.load_field('SchwabOrderID', dataDict.get('3')[1] if dataDict.get('3') else None)
        self.load_field('openClosePositionCode', dataDict.get('EquityOrderLeg')[2] if dataDict.get('EquityOrderLeg') else None)
        self.load_field('buySellCode', dataDict.get('BuySellCode'))
        self.load_field('shortDescriptionText', dataDict.get('ShortDescriptionText'))
        self.load_field('executionPrice', dataDict.get('ExecutionPrice')[1] if dataDict.get('ExecutionPrice') else None)
        #look for execution sign scale on data set with it
        self.load_field('executionSignScale', dataDict.get('ExecutionPrice-signScale'))
        self.load_field('underLyingSymbol', dataDict.get('UnderlyingSymbol'))
        self.load_field('orderStatus', dataDict.get('2'))

    def load_field(self, field_name, value):
        """
        Helper function to load a field of the Trade object from the given dictionary, overwriting only if the field is currently None.
        """
        if getattr(self, field_name) is None:
            setattr(self, field_name, value)



    def store_trade(self, file_name="trade_data.json"):
        """
        Stores the current trade to a JSON file. If the file already contains
        a trade with the same SchwabOrderID, it is replaced with the new trade.
        Otherwise, the new trade is appended to the list of existing trades.
        """
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
                existing_trades[i] = self.__dict__
                break
        else:
            existing_trades.append(self.__dict__)

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

            self.isPlaced = True
            self.combine_completed_trades()

            # if first and second executions exist, calculate gains/loss
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
    

       
    def load_from_json(self, trade):
        """
        This function loads trade data from a Trade Dictionary
        """
        for key in trade:
            setattr(self, key, trade[key])


    def calculateExecution(self):
        dividor = 10 ** math.floor(int(self.executionSignScale) / 2)
        return (float(self.executionPrice) / dividor)


    def calculateGainsLoss(self):
        date, strike, callOrPut = split_short_description(self.shortDescriptionText)
        gainLoss = float(self.secondExecutionPrice) / float(self.firstExecutionPrice)
        gainLossPercentage = round((gainLoss - 1) * 100, 2)
        return gainLossPercentage
    

    def check_if_placed(self):
        if self.orderStatus == "OrderAccepted" or self.orderStatus == "ExecutionRequestCreated":
            self.isPlaced = True
        else:
            self.isPlaced = False

        
    def combine_completed_trades(self):
        if self.isPlaced == False:
            return None
        
        firstTrade = load_trade_by_short_description(self.shortDescriptionText)
        if firstTrade is None:  
            return None

        
        # set the first execution price to first trade
        self.firstExecutionPrice = firstTrade.executionPrice
        # set the second execution price to second  trade
        self.secondExecutionPrice = self.executionPrice
        self.isCompleted = True


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
        
def load_trade_by_short_description(short_description, file_name="trade_data.json"):
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
                if trade.get("shortDescriptionText") == short_description:
                    tradeObject = Trade()
                    tradeObject.load_from_json(trade)
                    #check if it is has an execution price
                    print(tradeObject.executionPrice)
                    if tradeObject.executionPrice is not None:
                        return tradeObject  # Return the matching trade

            # If no match is found
            print(f"No trade found with shortDescriptionText: {short_description}")
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
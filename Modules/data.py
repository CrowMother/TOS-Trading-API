import json
from Modules import streamer
from Modules import universal
from functools import reduce
import operator

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
        routedAmount = "" #figure out what the acutal value for multilegs are for this
        multiLegLimitPriceType = ""
        multiLegStrategyType = ""

    def get_sub_trade(self):

        self.tradeStatus



def extract_sub_trade_data(sub_trade):
    # Initialize an empty dictionary to store valid data
    trade_data = {}

    # Define fields to extract and check
    fields_to_check = {
        "tradeStatus": sub_trade.tradeStatus,
        "shortDescriptionText": sub_trade.shortDescriptionText,
        "executionPrice": sub_trade.executionPrice,
        "executionSignScale": sub_trade.executionSignScale,
        "underlyingSymbol": sub_trade.underlyingSymbol,
        "routedAmount": sub_trade.routedAmount,
        "multiLegLimitPriceType": sub_trade.multiLegLimitPriceType,
        "multiLegStrategyType": sub_trade.multiLegStrategyType
    }

    # Loop through the fields and store data only if it's not "N/F"
    for key, value in fields_to_check.items():
        if value != "N/F" and value:  # Check if value is not "N/F" and is not empty
            trade_data[key] = value

    return trade_data

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#start of the data processing pipeline
def data_in(data):
    
    trade = load_trade(data)

    #get the type of trade to check for multiLeg
    trade.check_trade_type()
    
    

    
    #regular trades, check if data is ready to send then send
    if trade.tradeType == "Regular":
        regularTrade(trade)

            

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
            
            #get subTrade Data
            for subTrade in trade.subTrades:
                extract_sub_trade_data(subTrade)
            #grab the data needed for sending it to discord
        

    #function to check if all data needed for that trade is present



    


#load data into the sub trades and subtrades into the trade class and return the current trade loaded
def load_trade(data):
    try:
        #stores the SchwabOrderID from the first set of data
        schwabOrderID = data[0]['SchwabOrderID']


        # If this SchwabOrderID is not in the trades_dict, create a new Trade
        if schwabOrderID not in TRADES_DICT:
            trade = Trade()
            trade.schwabOrderID = schwabOrderID
            TRADES_DICT[schwabOrderID] = trade
        else:
            #If the ID is in the trades_dict pull that trade
            trade = TRADES_DICT[schwabOrderID]

        #loop here for each of the subtrades
        for json_data in data:

            #either way create a subtrade to store the important data from the trade
            sub_trade = SubTrade()
            sub_trade.tradeStatus = pull_json_data(json_data, "BaseEvent.EventType")
            sub_trade.shortDescriptionText = pull_json_data(json_data, "BaseEvent.OrderCreatedEventEquityOrder.Order.AssetOrderEquityOrderLeg.OrderLegs.0.Security.ShortDescriptionText")
            sub_trade.executionPrice = pull_json_data(json_data, "BaseEvent.OrderFillCompletedEventOrderLegQuantityInfo.ExecutionInfo.ExecutionPrice.lo")
            sub_trade.executionSignScale = pull_json_data(json_data, "BaseEvent.OrderFillCompletedEventOrderLegQuantityInfo.ExecutionInfo.ExecutionPrice.signScale")
            sub_trade.multiLegLimitPriceType = pull_json_data(json_data, "BaseEvent.OrderCreatedEventEquityOrder.Order.EquityOrder.OptionsInfo.EquityOptionsInfo.MultiLegLimitPriceType")
            sub_trade.multiLegStrategyType = pull_json_data(json_data, "BaseEvent.OrderCreatedEventEquityOrder.Order.EquityOrder.MultiLegStrategyType")
            sub_trade.underlyingSymbol = pull_json_data(json_data, "BaseEvent.OrderCreatedEventEquityOrder.Order.AssetOrderEquityOrderLeg.OrderLegs.0.Security.UnderlyingSymbol")

            #add the subtrade to the trade that is being tracked 
            trade.add_sub_trade(sub_trade)

            #move important data to the trade

        #save the trade and subtrades to the dict
        TRADES_DICT[schwabOrderID] = trade
        #return the trade
        return trade
    except Exception as e:
        #look into making an error handler, something to either restart or partially restart the program
        print(f"Error in load_trade: {e}")
        return None






def pull_json_data(json_data, location):
    try:
        # Split the location string by '.' to access nested fields
        keys = location.split('.')
        # Use reduce to traverse the nested dictionary
        outputData = reduce(operator.getitem, keys, json_data)
        return outputData
    except KeyError as e:
        #print(f"KeyError: {e} is missing in the JSON data.")
        return "N/F"
    except Exception as e:
        print(f"An error occurred in pull_json_data: {str(e)}")
        return "error"
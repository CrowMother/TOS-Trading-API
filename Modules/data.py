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
        self.subTrades = []

    # Method to check for unique tradeStatus
    def add_sub_trade(self, sub_trade):
        # Check if tradeStatus is unique among subTrades
        if any(trade.tradeStatus == sub_trade.tradeStatus for trade in self.subTrades):
            print(f"Error: Duplicate tradeStatus '{sub_trade.tradeStatus}' found in Trade '{self.schwabOrderID}'.")
        #add the duplicate trade no matter what for now, look into how often if ever this happens and if it is an issue in the future
        self.subTrades.append(sub_trade)
               
    #tracks parts of the trade based on status of the trade
class SubTrade():
    def __init__(self):
        tradeStatus = ""

        shortDescriptionText = ""
        executionPrice = ""
        executionSignScale = ""
        routedAmount = "" #figure out what the acutal value for multilegs are for this
        multiLegLimitPriceType = ""
        multiLegStrategyType = ""
        


#start of the data processing pipeline
def data_in(data):
    
    load_trade(data)

    #function to check what kind of trade this will be
    #assuming basic trade for this test

    #function to check if all data needed for that trade is present





#load data into the sub trades and subtrades into the trade class and return the current trade loaded
def load_trade(data):
    
    #store and load the data into objects
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

        #add the subtrade to the trade that is being tracked 
        trade.add_sub_trade(sub_trade)
    
    #save the trade and subtrades to the dict
    TRADES_DICT[schwabOrderID] = trade
    #return the trade
    return trade






def pull_json_data(json_data, location):
    try:
        # Split the location string by '.' to access nested fields
        keys = location.split('.')
        # Use reduce to traverse the nested dictionary
        outputData = reduce(operator.getitem, keys, json_data)
        return outputData
    except KeyError as e:
        print(f"KeyError: {e} is missing in the JSON data.")
        return "N/F"
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "error"
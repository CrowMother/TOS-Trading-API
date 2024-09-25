import json
from Modules import streamer
from Modules import universal

ORDER_DATA_MAP = {}


class Trade:
    def __init__(self):
        schwabOrderID = ""
        shortDescriptionText = ""
        executionPrice = ""
        routedAmount = "" #figure out what the acutal value for multilegs are for this
        multiLegLimitPriceType = ""
        multiLegStrategyType = ""
        rollPrice = ""

        tradeStatus = ""

#start of the data processing pipeline
def data_in(data):
    print(f"First Order ID: {data[0]['SchwabOrderID']}")



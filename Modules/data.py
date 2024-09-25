import json
from Modules import streamer
from Modules import universal

ORDER_DATA_MAP = {}


#start of the data processing pipeline
def data_in(data):
    print(data)
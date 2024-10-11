from Modules import debugger

import re

#add more error catching to simplify debugging

def split_at_comma(data):
    #split the json for each comma that exists
    data = data.split(',')
    return data

def split_at_colon(data):
    dataDict = {}
    for entry in data:
        key, value = entry.split(':', 1)

        key = clean_string(key)
        value = clean_string(value)

        value = split_extra(value)
        #print(f"{key} : {value}")
        dataDict[key] = value
    return dataDict

def split_extra(value, splitVal=':'):
    if splitVal in value:
        return value.split(splitVal)
    else:
        return value


def clean_string(s):
    cleaned_string = re.sub(r'[^a-zA-Z0-9,.!?;:/ ]+', '', s)
    return cleaned_string
        

def custom_json_parser(s):
    try:
        data = split_at_comma(s)
        dataDict = split_at_colon(data)

    except Exception as e:
        debugger.handle_exception(e, "Error in custom_json_parser")
    return dataDict
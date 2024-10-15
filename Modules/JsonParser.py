from Modules import debugger

import re

#add more error catching to simplify debugging

def split_at_comma(data):
    #split the json for each comma that exists
    data = data.split(',')
    return data

def split_at_colon(data):
    dataDict = {}
    previousKey = ''
    for entry in data:
        key, value = entry.split(':', 1)


        key = clean_string(key)
        value = clean_string(value)
        #check if key is in dataDict and modify name if it is
        if key in dataDict:
            #key gets position number added to end
            key = f'{previousKey}-{key}'


        value = split_extra(value)
        #print(f"{key} : {value}")
        dataDict[key] = value

        previousKey = key
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

    #reorder dataDict in aplhabetical order for readability
    keys = list(dataDict.keys())
    keys.sort()
    sortedDataDict = {k: dataDict[k] for k in keys}
    return sortedDataDict
import schwabdev
import datetime
from Modules import universal
from Modules import logger
from Modules import secretkeys
from Modules import data as Data
import time
from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)
streamer = None
SERVER_URL = secretkeys.get_url()
print(SERVER_URL)

def remove_specific_characters(input_string, characters_to_remove):
    return ''.join([char for char in input_string if char not in characters_to_remove])

def parse_message(message):
    try:
        chars_to_remove = "\[]{\}\"\'"
        message = remove_specific_characters(message, chars_to_remove)
        mes_parts = message.split(",")
        #print(f"\nparts\n{mes_parts}")
        return mes_parts
    except Exception as e:
        print(f"can't parse: {e}")

def datafy(parsed_message):

    data = {'time': universal.time_stamp()}

    # Process each string in the parsed message
    for item in parsed_message:
        try:
            # Split on ':' and strip the quotes and whitespace
            key, value = item.split(':')
            key = key.strip().strip('"')
            value = value.strip().strip('"')
            data[key] = value
        except ValueError as e:
            universal.error_code(f"Skipping invalid format: {item}. Error: {str(e)}")
    
    return data


def set_streamer(client):
    global streamer
    streamer = client.stream

def my_handler(data):
    #call a function to convert raw message to a data format similar to below
    #data = {'time': universal.time_stamp() ,
    #        'data': message}
    #{"response":[{"service":"ADMIN","command":"LOGIN","requestid":"0","SchwabClientCorrelId":"369e8458-2d9d-0d84-828a-03a694c658ca","timestamp":1722003493339,"content":{"code":0,"msg":"server=s0635dc6-4;status=NP"}}]}

    #universal.okay_code(message)
    logger.write_to_log(data)
    
    #parse data that we need
    data = Data.data_in(data)

    logger.write_to_log(f"Post data Processing: {data}")
    # Ensure that send_trade is called correctly within the application context\

#uncomment to send to server
    # if data is not None:
    #     with app.app_context():
    #         send_trade(data)

# Tracking for stock pricing of AMD and intel
def start_level_one_equity_stream(client):
    streamer.start(my_handler)
    client.stream.send(client.stream.level_one_equities("AMD,INTC", "0,1,2,3,4,5,6,7,8"))
    time.sleep(60)
    streamer.stop()

# Tracking of account data 
def start_account_tracking(client):
    streamer.start(my_handler)
    #move to the following to preserve data streaming, figure out custom handling of data
    #streamer.start_automatic(receiver=print, after_hours=False, pre_hours=False)
    client.stream.send(client.stream.account_activity("Account Activity", "0,1,2,3"))
    
    

# send data to the server
@app.route('/send-trade', methods=["GET"])
def send_trade(data):
    global SERVER_URL
    # Post request to the other server
    try:
        response = requests.post(SERVER_URL, json=data)
        # Return the response from the other server
        return jsonify({'status': 'data sent', 'response': response.json()})
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the POST request
        universal.error_code("connection with server lost!")
        
        #after error code figure out design for what to do with the data that can't be sent
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True)




def send_test_trade_order():
    testList = [
    '[2024-08-26 09:39:50] {"data":[{"service":"ACCT_ACTIVITY", "timestamp":1724683189449,"command":"SUBS","content":[{"seq":33,"key":"Account Activity","1":"54661285","2":"OrderCreated","3":{"SchwabOrderID":"1001416563737","AccountNumber":"54661285","BaseEvent":{"EventType":"OrderCreated","OrderCreatedEventEquityOrder":{"EventType":"OrderCreated","Order":{"SchwabOrderID":"1001416563737","AccountNumber":"54661285","Order":{"AccountInfo":{"AccountNumber":"54661285","AccountBranch":"WT","CustomerOrFirmCode":"CustomerOrFirmCode_Customer","OrderPlacementCustomerID":"353286754","AccountState":"MO","AccountTypeCode":"Customer"},"ClientChannelInfo":{"ClientProductCode":"M1","EventUserID":"O1XX","EventUserType":"Client"},"LifecycleCreatedTimestamp":{"DateTimeString":"2024-08-26 10:39:49.327"},"LifecycleSchwabOrderID":"1001416563737","EntryTimestamp":{"DateTimeString":"2024-08-26 10:39:49.327"},"ExpiryTimeStamp":{"DateTimeString":"2024-08-26"},"AutoConfirm":true,"PlanSubmitDate":{"DateTimeString":"2024-08-26"},"SourceOMS":"ngOMS","FirmID":"CHAS","OrderAccount":"TDAAccount","AssetOrderEquityOrderLeg":{"OrderInstruction":{"HandlingInstructionCode":"AutomatedExecutionNoIntervention","ExecutionStrategy":{"Type":"ES_Limit","LimitExecutionStrategy":{"Type":"ES_Limit","LimitPrice":{"lo":"3300000","signScale":12},"LimitPriceUnitCode":"Units"}},"PreferredRoute":{},"EquityOrderInstruction":{}},"CommissionInfo":{"EstimatedOrderQuantity":{"lo":"1000000","signScale":12},"EstimatedPrincipalAmount":{"lo":"330000000","signScale":13},"EstimatedCommissionAmount":{"lo":"650000","signScale":12}},"AssetType":"MajorAssetType_EquityOption","TimeInForce":"Day","OrderTypeCode":"Limit","OrderLegs":[{"LegID":"1001416563737","LegParentSchwabOrderID":"1001416563737","Quantity":{"lo":"1000000","signScale":12},"QuantityUnitCodeType":"SharesOrUnits","LeavesQuantity":{"lo":"1000000","signScale":12},"BuySellCode":"Buy","Security":{"SchwabSecurityID":"102232207","Symbol":"QQQ  240828P00471000","UnderlyingSymbol":"QQQ","MajorAssetType":"MajorAssetType_EquityOption","PrimaryMarketSymbol":"QQQ  240828P00471000","ShortDescriptionText":"INVESCO QQQ TR 08/28/2024 $471 Put","ShortName":"INVESCO QQQ TR 08/28/2024 $471 Put","CUSIP":"0QQQ..TS40471000","OptionsSecurityInfo":{"PutCallCode":"Put","UnderlyingSchwabSecurityID":"48644470","StrikePrice":{"lo":"471000000","signScale":12},"OptionExpiryDate":{"DateTimeString":"2024-08-28 00:00:00.000"}}},"QuoteOnOrderAcceptance":{"Ask":{"lo":"3290000","signScale":12},"AskSize":{"lo":"16"},"Bid":{"lo":"3260000","signScale":12},"BidSize":{"lo":"15"},"QuoteTimestamp":{"DateTimeString":"2024-08-26 10:39:49.327"},"Symbol":"QQQ  240828P00471000","QuoteTypeCode":"Mark","Mid":{"lo":"3275000","signScale":12},"SchwabOrderID":"1001416563737","OptionsQuote":{"PutCallCode":"Put"}},"LegClientRequestInfo":{"SecurityId":"QQQ  240828P00471000","SecurityIdTypeCd":"Symbol"},"AccountingRuleCode":"Cash","EstimatedNetAmount":{"lo":"330650000","signScale":13},"EstimatedPrincipalAmnt":{"lo":"330000000","signScale":13},"EquityOrderLeg":{"EquityOptionsOrderLeg":{"OpenClosePositionCode":"PC_Open"}}}],"OrderCapacityCode":"OC_Agency","SettlementType":"SettlementType_Regular","Rule80ACode":73,"SolicitedCode":"Unsolicited","TradeTag":"API_TOS:TRADE_ALL","EquityOrder":{"TradingSessionCodeOnOrder":"REG"}}}}}}]}]}'
    ]

    for message in testList:
        # Extract the JSON part by removing the timestamp
        json_data = message[message.index('{'):]  # Starts from the first '{'
        
        # Now parse the valid JSON
        try:
            parsed_data = json.loads(json_data)
            print(parsed_data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
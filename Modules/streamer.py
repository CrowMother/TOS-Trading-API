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
        chars_to_remove = "\[]}{\"\'"
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

    universal.okay_code(data)
    logger.write_to_log(data)
    
    #parse data that we need
    data = Data.data_in(data)

    logger.write_to_log(f"Post data Processing: {data}")
    # Ensure that send_trade is called correctly within the application context\
    return
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
    if client is None:
        universal.error_code("Error Client is a None Type")
    else:
        streamer.start(my_handler)
        client.stream.send(client.stream.account_activity("Account Activity", "0,1,2,3,4"))
    
    
def send_trade_data_in_background(data):
    with app.app_context():
        try:
            print(f"sending data to: {SERVER_URL}")
            response = requests.post(f"{SERVER_URL}", json=data)
            response.raise_for_status()  # Handle HTTP errors
            return {'status': 'data sent', 'response': response.json()}
        except requests.exceptions.RequestException as e:
            universal.error_code(f"Connection with server lost! {str(e)}")
            return {'status': 'error', 'message': str(e)}

# flask function to send data to the server
@app.route('/send-trade-data', methods=["POST"])
def send_trade_data():
    # Extract the JSON data sent with the request
    data = request.get_json()  # This gets the data from the request body

    if not data:
        return jsonify({'status': 'error', 'message': 'No data received'}), 400
    
    try:
        print(f"Data to be sent: {data}")
        # Post request to the other server
        response = requests.post(SERVER_URL, json=data)
        response.raise_for_status()  # Ensure any HTTP errors are raised
        
        # Return the response from the other server
        return jsonify({'status': 'data sent', 'response': response.json()}), 200
    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the POST request
        universal.error_code("Connection with server lost!")
        
        # Design handling for what to do with data that couldn't be sent
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
#send heart beat notification to server
@app.route('/send-heart', methods=["GET"])
def send_heart(data):
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
        '{"data":[{"service":"ACCT_ACTIVITY", "timestamp":1726499530728,"command":"SUBS","content":[{"seq":74,"key":"Account Activity","1":"54661285","2":"OrderCreated","3":"{\"SchwabOrderID\":\"1001602704574\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"OrderCreated\",\"OrderCreatedEventEquityOrder\":{\"EventType\":\"OrderCreated\",\"Order\":{\"SchwabOrderID\":\"1001602704574\",\"AccountNumber\":\"54661285\",\"Order\":{\"AccountInfo\":{\"AccountNumber\":\"54661285\",\"AccountBranch\":\"WT\",\"CustomerOrFirmCode\":\"CustomerOrFirmCode_Customer\",\"OrderPlacementCustomerID\":\"353286754\",\"AccountState\":\"MO\",\"AccountTypeCode\":\"Customer\"},\"ClientChannelInfo\":{\"ClientProductCode\":\"M1\",\"EventUserID\":\"O1XX\",\"EventUserType\":\"Client\"},\"LifecycleCreatedTimestamp\":{\"DateTimeString\":\"2024-09-16 11:12:10.632\"},\"LifecycleSchwabOrderID\":\"1001602704574\",\"EntryTimestamp\":{\"DateTimeString\":\"2024-09-16 11:12:10.632\"},\"ExpiryTimeStamp\":{\"DateTimeString\":\"2024-09-16\"},\"AutoConfirm\":true,\"PlanSubmitDate\":{\"DateTimeString\":\"2024-09-16\"},\"SourceOMS\":\"ngOMS\",\"FirmID\":\"CHAS\",\"OrderAccount\":\"TDAAccount\",\"AssetOrderEquityOrderLeg\":{\"OrderInstruction\":{\"HandlingInstructionCode\":\"AutomatedExecutionNoIntervention\",\"ExecutionStrategy\":{\"Type\":\"ES_Limit\",\"LimitExecutionStrategy\":{\"Type\":\"ES_Limit\",\"LimitPrice\":{\"lo\":\"1570000\",\"signScale\":12},\"LimitPriceUnitCode\":\"Units\"}},\"PreferredRoute\":{},\"EquityOrderInstruction\":{}},\"CommissionInfo\":{\"EstimatedOrderQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"EstimatedPrincipalAmount\":{\"lo\":\"157000000\",\"signScale\":12},\"EstimatedCommissionAmount\":{\"lo\":\"650000\",\"signScale\":12}},\"AssetType\":\"MajorAssetType_EquityOption\",\"TimeInForce\":\"Day\",\"OrderTypeCode\":\"Limit\",\"OrderLegs\":[{\"LegID\":\"1001602704574\",\"LegParentSchwabOrderID\":\"1001602704574\",\"Quantity\":{\"lo\":\"1000000\",\"signScale\":12},\"QuantityUnitCodeType\":\"SharesOrUnits\",\"LeavesQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"BuySellCode\":\"Sell\",\"Security\":{\"SchwabSecurityID\":\"93257851\",\"Symbol\":\"BA    240920P00150000\",\"UnderlyingSymbol\":\"BA\",\"MajorAssetType\":\"MajorAssetType_EquityOption\",\"PrimaryMarketSymbol\":\"BA    240920P00150000\",\"ShortDescriptionText\":\"Boeing Co 09\/20\/2024 $150 Put\",\"ShortName\":\"Boeing Co 09\/20\/2024 $150 Put\",\"CUSIP\":\"0BA...UK40150000\",\"OptionsSecurityInfo\":{\"PutCallCode\":\"Put\",\"UnderlyingSchwabSecurityID\":\"1890758598\",\"StrikePrice\":{\"lo\":\"150000000\",\"signScale\":12},\"OptionExpiryDate\":{\"DateTimeString\":\"2024-09-20 00:00:00.000\"}}},\"QuoteOnOrderAcceptance\":{\"Ask\":{\"lo\":\"1580000\",\"signScale\":12},\"AskSize\":{\"lo\":\"21\"},\"Bid\":{\"lo\":\"1540000\",\"signScale\":12},\"BidSize\":{\"lo\":\"250\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-09-16 11:12:10.632\"},\"Symbol\":\"BA    240920P00150000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"1560000\",\"signScale\":13},\"SchwabOrderID\":\"1001602704574\",\"OptionsQuote\":{\"PutCallCode\":\"Put\"}},\"LegClientRequestInfo\":{\"SecurityId\":\"BA    240920P00150000\",\"SecurityIdTypeCd\":\"Symbol\"},\"AccountingRuleCode\":\"Cash\",\"EstimatedNetAmount\":{\"lo\":\"156350000\",\"signScale\":12},\"EstimatedPrincipalAmnt\":{\"lo\":\"157000000\",\"signScale\":12},\"EquityOrderLeg\":{\"EquityOptionsOrderLeg\":{\"OpenClosePositionCode\":\"PC_Close\"}}}],\"OrderCapacityCode\":\"OC_Agency\",\"SettlementType\":\"SettlementType_Regular\",\"Rule80ACode\":73,\"SolicitedCode\":\"Unsolicited\",\"TradeTag\":\"API_TOS:TRADE_ALL\",\"EquityOrder\":{\"TradingSessionCodeOnOrder\":\"REG\"}}}}}}}"}]}]}',
        '{"data":[{"service":"ACCT_ACTIVITY", "timestamp":1726499531736,"command":"SUBS","content":[{"seq":75,"key":"Account Activity","1":"54661285","2":"OrderAccepted","3":"{\"SchwabOrderID\":\"1001602704574\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"OrderAccepted\",\"OrderAcceptedEvent\":{\"EventType\":\"OrderAccepted\",\"CreatedTimeStamp\":{\"DateTimeString\":\"2024-09-16 11:12:10.632\"},\"ExpiryTimeStamp\":{\"DateTimeString\":\"2024-09-16\"},\"Status\":\"Open\",\"TradingSessionCodeOnOrderEntry\":\"REG\",\"QuoteOnOrderEntry\":[{\"Ask\":{\"lo\":\"1580000\",\"signScale\":12},\"AskSize\":{\"lo\":\"21\"},\"Bid\":{\"lo\":\"1540000\",\"signScale\":12},\"BidSize\":{\"lo\":\"250\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-09-16 11:12:10.632\"},\"Symbol\":\"BA    240920P00150000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"1560000\",\"signScale\":13},\"SchwabOrderID\":\"1001602704574\",\"OptionsQuote\":{\"PutCallCode\":\"Put\"}}]}}}"},{"seq":76,"key":"Account Activity","1":"54661285","2":"ExecutionRequested","3":"{\"SchwabOrderID\":\"1001602704574\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequested\",\"ExecutionRequestedEventRoutedInfo\":{\"EventType\":\"ExecutionRequested\",\"RouteSequenceNumber\":1,\"RouteInfo\":{\"RouteName\":\"DASH_OPT_F1_J1\",\"RouteSequenceNumber\":1,\"RoutedExecutionTimestamp\":{\"DateTimeString\":\"2024-09-16 11:12:10.667\"},\"Quote\":{\"Ask\":{\"lo\":\"1580000\",\"signScale\":12},\"AskSize\":{\"lo\":\"21\"},\"Bid\":{\"lo\":\"1540000\",\"signScale\":12},\"BidSize\":{\"lo\":\"250\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-09-16 11:12:10.632\"},\"Symbol\":\"BA    240920P00150000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"1560000\",\"signScale\":13},\"SchwabOrderID\":\"1001602704574\",\"OptionsQuote\":{\"PutCallCode\":\"Put\"}},\"RouteRequestedType\":\"New\",\"RoutedQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"RoutedPrice\":{\"lo\":\"1570000\",\"signScale\":12},\"RouteStatus\":\"RouteCreated\",\"ClientOrderID\":\"1001602704574.1\",\"RoutedTime\":{\"DateTimeString\":\"2024-09-16 11:12:10.667\"},\"RouteTimeInForce\":\"Day\",\"RouteAcknowledgmentTimeStamp\":{}},\"RouteRequestedBy\":\"RR_Broker\",\"LegId\":\"1001602704574\"}}}"},{"seq":77,"key":"Account Activity","1":"54661285","2":"ExecutionRequestCreated","3":"{\"SchwabOrderID\":\"1001602704574\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequestCreated\",\"ExecutionRequestCreatedEvent\":{\"EventType\":\"ExecutionRequestCreated\",\"LegId\":\"1001602704574\",\"RouteName\":\"DASH_OPT_F1_J1\",\"RouteRequestType\":\"New\",\"RouteSequenceNumber\":1,\"RouteRequestedBy\":\"RR_Broker\",\"RouteStatus\":\"RouteFixAcknowledged\",\"SenderCompID\":\"SCHWABTDAMOFP1\",\"RoutedTime\":{\"DateTimeString\":\"2024-09-16 11:12:10.692\"},\"ClientOrderID\":\"1001602704574.1\"}}}"},{"seq":78,"key":"Account Activity","1":"54661285","2":"ExecutionRequestCompleted","3":"{\"SchwabOrderID\":\"1001602704574\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequestCompleted\",\"ExecutionRequestCompletedEvent\":{\"EventType\":\"ExecutionRequestCompleted\",\"LegId\":\"1001602704574\",\"ResponseType\":\"Accepted\",\"ExchangeOrderID\":\"7700108138668\",\"ExecutionTime\":{\"DateTimeString\":\"2024-09-16 11:12:10.803\"},\"RouteSequenceNumber\":1,\"RouteStatus\":\"RouteVenueAccepted\",\"RouteAcknowledgmentTimeStamp\":{\"DateTimeString\":\"2024-09-16 11:12:10.770\"},\"ClientOrderID\":\"1001602704574.1\"}}}"}]}]}',
        '{"data":[{"service":"ACCT_ACTIVITY", "timestamp":1726499534897,"command":"SUBS","content":[{"seq":79,"key":"Account Activity","1":"54661285","2":"OrderFillCompleted","3":"{\"SchwabOrderID\":\"1001602704574\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"OrderFillCompleted\",\"OrderFillCompletedEventOrderLegQuantityInfo\":{\"EventType\":\"OrderFillCompleted\",\"LegId\":\"1001602704574\",\"LegStatus\":\"LegClosed\",\"QuantityInfo\":{\"ExecutionID\":\"20240916-EST-ngOMS-13276896900\",\"CumulativeQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"LeavesQuantity\":{\"signScale\":12},\"AveragePrice\":{\"lo\":\"1570000\",\"signScale\":12}},\"PriceImprovement\":{\"signScale\":12},\"LegSubStatus\":\"LegSubStatusFilled\",\"ExecutionInfo\":{\"ExecutionSequenceNumber\":1,\"ExecutionId\":\"20240916-EST-ngOMS-13276896900\",\"VenueExecutionID\":\"7700633770743\",\"Exchange\":\"CBOE\",\"ExecutionQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"ExecutionPrice\":{\"lo\":\"1570000\",\"signScale\":12},\"ExecutionTimeStamp\":{\"DateTimeString\":\"2024-09-16 11:12:14.819\"},\"ExecutionTransType\":\"Fill\",\"ExecutionCapacityCode\":\"Agency\",\"RouteName\":\"DASH_OPT_F1_J1\",\"RouteSequenceNumber\":1,\"VenuExecutionTimeStamp\":{\"DateTimeString\":\"2024-09-16 11:12:14.787\"},\"ReportingCapacityCode\":\"RC_Agency\",\"ActualChargedCommissionAmount\":{\"lo\":\"650000\",\"signScale\":12},\"AsOfTimeStamp\":{},\"ActualChargedFeesCommissionAndTax\":{\"StateTaxWithholding\":{\"signScale\":12},\"FederalTaxWithholding\":{\"signScale\":12},\"SECFees\":{\"signScale\":12},\"ORF\":{\"lo\":\"10000\",\"signScale\":12},\"FTT\":{\"signScale\":12},\"TaxWithholding1446\":{\"signScale\":12},\"GoodsAndServicesTax\":{\"signScale\":12},\"IOF\":{\"signScale\":12},\"TAF\":{\"signScale\":12},\"CommissionAmount\":{\"lo\":\"650000\",\"signScale\":12}},\"ClientOrderID\":\"1001602704574.1\"},\"OrderInfoForTransactionPosting\":{\"LimitPrice\":{\"lo\":\"1570000\",\"signScale\":12},\"OrderTypeCode\":\"Limit\",\"OpenClosePositionCode\":\"PC_Close\",\"BuySellCode\":\"Sell\",\"Quantity\":{\"lo\":\"1000000\",\"signScale\":12},\"StopPrice\":{},\"Symbol\":\"BA    240920P00150000\",\"SchwabSecurityID\":\"93257851\",\"SolicitedCode\":\"Unsolicited\",\"AccountingRuleCode\":\"Cash\",\"SettlementType\":\"SettlementType_Regular\",\"OrderCreatedUserID\":\"O1XX\",\"OrderCreatedUserType\":\"Venue\",\"ClientProductCode\":\"N1\"}}}}"}]}]}'
    ]
    
    for message in testList:
        time.sleep(1)
        # Extract the JSON part by removing the timestamp
        my_handler(message)
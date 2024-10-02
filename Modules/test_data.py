from Modules import streamer
from Modules import data as Data
import json
import re



def send_test_trade_order():
    testList = [
        '{"service":"ACCT_ACTIVITY","timestamp":1727879999737,"command":"SUBS","content":[{"1":"54661285","2":"OrderCreated","3":"{\"SchwabOrderID\":\"1001763245039\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"OrderCreated\",\"OrderCreatedEventEquityOrder\":{\"EventType\":\"OrderCreated\",\"Order\":{\"SchwabOrderID\":\"1001763245039\",\"AccountNumber\":\"54661285\",\"Order\":{\"AccountInfo\":{\"AccountNumber\":\"54661285\",\"AccountBranch\":\"WT\",\"CustomerOrFirmCode\":\"CustomerOrFirmCode_Customer\",\"OrderPlacementCustomerID\":\"353286754\",\"AccountState\":\"MO\",\"AccountTypeCode\":\"Customer\"},\"ClientChannelInfo\":{\"ClientProductCode\":\"M1\",\"EventUserID\":\"O1XX\",\"EventUserType\":\"Client\"},\"LifecycleCreatedTimestamp\":{\"DateTimeString\":\"2024-10-02 10:39:59.632\"},\"LifecycleSchwabOrderID\":\"1001763245039\",\"EntryTimestamp\":{\"DateTimeString\":\"2024-10-02 10:39:59.632\"},\"ExpiryTimeStamp\":{\"DateTimeString\":\"2024-10-02\"},\"AutoConfirm\":true,\"PlanSubmitDate\":{\"DateTimeString\":\"2024-10-02\"},\"SourceOMS\":\"ngOMS\",\"FirmID\":\"CHAS\",\"OrderAccount\":\"TDAAccount\",\"AssetOrderEquityOrderLeg\":{\"OrderInstruction\":{\"HandlingInstructionCode\":\"AutomatedExecutionNoIntervention\",\"ExecutionStrategy\":{\"Type\":\"ES_Limit\",\"LimitExecutionStrategy\":{\"Type\":\"ES_Limit\",\"LimitPrice\":{\"lo\":\"3050000\",\"signScale\":12},\"LimitPriceUnitCode\":\"Units\"}},\"PreferredRoute\":{},\"EquityOrderInstruction\":{}},\"CommissionInfo\":{\"EstimatedOrderQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"EstimatedPrincipalAmount\":{\"lo\":\"305000000\",\"signScale\":13},\"EstimatedCommissionAmount\":{\"lo\":\"650000\",\"signScale\":12}},\"AssetType\":\"MajorAssetType_EquityOption\",\"TimeInForce\":\"Day\",\"OrderTypeCode\":\"Limit\",\"OrderLegs\":[{\"LegID\":\"1001763245039\",\"LegParentSchwabOrderID\":\"1001763245039\",\"Quantity\":{\"lo\":\"1000000\",\"signScale\":12},\"QuantityUnitCodeType\":\"SharesOrUnits\",\"LeavesQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"BuySellCode\":\"Buy\",\"Security\":{\"SchwabSecurityID\":\"102642089\",\"Symbol\":\"BABA  241011C00120000\",\"UnderlyingSymbol\":\"BABA\",\"MajorAssetType\":\"MajorAssetType_EquityOption\",\"PrimaryMarketSymbol\":\"BABA  241011C00120000\",\"ShortDescriptionText\":\"ALIBABA GROUP HLDG LTD 10/11/2024 $120 Call\",\"ShortName\":\"ALIBABA GROUP HLDG LTD 10/11/2024 $120 Call\",\"CUSIP\":\"0BABA.JB40120000\",\"OptionsSecurityInfo\":{\"PutCallCode\":\"Call\",\"UnderlyingSchwabSecurityID\":\"1737167066\",\"StrikePrice\":{\"lo\":\"120000000\",\"signScale\":12},\"OptionExpiryDate\":{\"DateTimeString\":\"2024-10-11 00:00:00.000\"}}},\"QuoteOnOrderAcceptance\":{\"Ask\":{\"lo\":\"3000000\",\"signScale\":12},\"AskSize\":{\"lo\":\"9\"},\"Bid\":{\"lo\":\"2930000\",\"signScale\":12},\"BidSize\":{\"lo\":\"3\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-10-02 10:39:59.632\"},\"Symbol\":\"BABA  241011C00120000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"2965000\",\"signScale\":12},\"SchwabOrderID\":\"1001763245039\",\"OptionsQuote\":{\"PutCallCode\":\"Call\"}},\"LegClientRequestInfo\":{\"SecurityId\":\"BABA  241011C00120000\",\"SecurityIdTypeCd\":\"Symbol\"},\"AccountingRuleCode\":\"Cash\",\"EstimatedNetAmount\":{\"lo\":\"305650000\",\"signScale\":13},\"EstimatedPrincipalAmnt\":{\"lo\":\"305000000\",\"signScale\":13},\"EquityOrderLeg\":{\"EquityOptionsOrderLeg\":{\"OpenClosePositionCode\":\"PC_Open\"}}}],\"OrderCapacityCode\":\"OC_Agency\",\"SettlementType\":\"SettlementType_Regular\",\"Rule80ACode\":73,\"SolicitedCode\":\"Unsolicited\",\"TradeTag\":\"API_TOS:TRADE_ALL\",\"EquityOrder\":{\"TradingSessionCodeOnOrder\":\"REG\"}}}}}}}","seq":1,"key":"Account Activity"}]}',
        '{"service":"ACCT_ACTIVITY","timestamp":1727880000752,"command":"SUBS","content":[{"1":"54661285","2":"OrderAccepted","3":"{\"SchwabOrderID\":\"1001763245039\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"OrderAccepted\",\"OrderAcceptedEvent\":{\"EventType\":\"OrderAccepted\",\"CreatedTimeStamp\":{\"DateTimeString\":\"2024-10-02 10:39:59.632\"},\"ExpiryTimeStamp\":{\"DateTimeString\":\"2024-10-02\"},\"Status\":\"Open\",\"TradingSessionCodeOnOrderEntry\":\"REG\",\"QuoteOnOrderEntry\":[{\"Ask\":{\"lo\":\"3000000\",\"signScale\":12},\"AskSize\":{\"lo\":\"9\"},\"Bid\":{\"lo\":\"2930000\",\"signScale\":12},\"BidSize\":{\"lo\":\"3\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-10-02 10:39:59.632\"},\"Symbol\":\"BABA  241011C00120000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"2965000\",\"signScale\":12},\"SchwabOrderID\":\"1001763245039\",\"OptionsQuote\":{\"PutCallCode\":\"Call\"}}]}}}","seq":2,"key":"Account Activity"},{"1":"54661285","2":"ExecutionRequested","3":"{\"SchwabOrderID\":\"1001763245039\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequested\",\"ExecutionRequestedEventRoutedInfo\":{\"EventType\":\"ExecutionRequested\",\"RouteSequenceNumber\":1,\"RouteInfo\":{\"RouteName\":\"DASH_OPT_F1_J1\",\"RouteSequenceNumber\":1,\"RoutedExecutionTimestamp\":{\"DateTimeString\":\"2024-10-02 10:39:59.669\"},\"Quote\":{\"Ask\":{\"lo\":\"3000000\",\"signScale\":12},\"AskSize\":{\"lo\":\"9\"},\"Bid\":{\"lo\":\"2930000\",\"signScale\":12},\"BidSize\":{\"lo\":\"3\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-10-02 10:39:59.632\"},\"Symbol\":\"BABA  241011C00120000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"2965000\",\"signScale\":12},\"SchwabOrderID\":\"1001763245039\",\"OptionsQuote\":{\"PutCallCode\":\"Call\"}},\"RouteRequestedType\":\"New\",\"RoutedQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"RoutedPrice\":{\"lo\":\"3050000\",\"signScale\":12},\"RouteStatus\":\"RouteCreated\",\"ClientOrderID\":\"1001763245039.1\",\"RoutedTime\":{\"DateTimeString\":\"2024-10-02 10:39:59.669\"},\"RouteTimeInForce\":\"Day\",\"RouteAcknowledgmentTimeStamp\":{}},\"RouteRequestedBy\":\"RR_Broker\",\"LegId\":\"1001763245039\"}}}","seq":3,"key":"Account Activity"},{"1":"54661285","2":"ExecutionRequestCreated","3":"{\"SchwabOrderID\":\"1001763245039\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequestCreated\",\"ExecutionRequestCreatedEvent\":{\"EventType\":\"ExecutionRequestCreated\",\"LegId\":\"1001763245039\",\"RouteName\":\"DASH_OPT_F1_J1\",\"RouteRequestType\":\"New\",\"RouteSequenceNumber\":1,\"RouteRequestedBy\":\"RR_Broker\",\"RouteStatus\":\"RouteFixAcknowledged\",\"SenderCompID\":\"SCHWABTDAMOFP1\",\"RoutedTime\":{\"DateTimeString\":\"2024-10-02 10:39:59.697\"},\"ClientOrderID\":\"1001763245039.1\"}}}","seq":4,"key":"Account Activity"},{"1":"54661285","2":"ExecutionRequestCompleted","3":"{\"SchwabOrderID\":\"1001763245039\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequestCompleted\",\"ExecutionRequestCompletedEvent\":{\"EventType\":\"ExecutionRequestCompleted\",\"LegId\":\"1001763245039\",\"ResponseType\":\"Accepted\",\"ExchangeOrderID\":\"7800114321537\",\"ExecutionTime\":{\"DateTimeString\":\"2024-10-02 10:39:59.771\"},\"RouteSequenceNumber\":1,\"RouteStatus\":\"RouteVenueAccepted\",\"RouteAcknowledgmentTimeStamp\":{\"DateTimeString\":\"2024-10-02 10:39:59.739\"},\"ClientOrderID\":\"1001763245039.1\"}}}","seq":5,"key":"Account Activity"},{"1":"54661285","2":"OrderFillCompleted","3":"{\"SchwabOrderID\":\"1001763245039\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"OrderFillCompleted\",\"OrderFillCompletedEventOrderLegQuantityInfo\":{\"EventType\":\"OrderFillCompleted\",\"LegId\":\"1001763245039\",\"LegStatus\":\"LegClosed\",\"QuantityInfo\":{\"ExecutionID\":\"20241002-EST-ngOMS-13352530990\",\"CumulativeQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"LeavesQuantity\":{\"signScale\":12},\"AveragePrice\":{\"lo\":\"2960000\",\"signScale\":12}},\"PriceImprovement\":{\"lo\":\"4000000\",\"signScale\":12},\"LegSubStatus\":\"LegSubStatusFilled\",\"ExecutionInfo\":{\"ExecutionSequenceNumber\":1,\"ExecutionId\":\"20241002-EST-ngOMS-13352530990\",\"VenueExecutionID\":\"7800667068096\",\"Exchange\":\"CBOE\",\"ExecutionQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"ExecutionPrice\":{\"lo\":\"2960000\",\"signScale\":12},\"ExecutionTimeStamp\":{\"DateTimeString\":\"2024-10-02 10:39:59.943\"},\"ExecutionTransType\":\"Fill\",\"ExecutionCapacityCode\":\"Agency\",\"RouteName\":\"DASH_OPT_F1_J1\",\"RouteSequenceNumber\":1,\"VenuExecutionTimeStamp\":{\"DateTimeString\":\"2024-10-02 10:39:59.911\"},\"ReportingCapacityCode\":\"RC_Agency\",\"ActualChargedCommissionAmount\":{\"lo\":\"650000\",\"signScale\":12},\"AsOfTimeStamp\":{},\"ActualChargedFeesCommissionAndTax\":{\"StateTaxWithholding\":{\"signScale\":12},\"FederalTaxWithholding\":{\"signScale\":12},\"SECFees\":{\"signScale\":12},\"ORF\":{\"lo\":\"10000\",\"signScale\":12},\"FTT\":{\"signScale\":12},\"TaxWithholding1446\":{\"signScale\":12},\"GoodsAndServicesTax\":{\"signScale\":12},\"IOF\":{\"signScale\":12},\"TAF\":{\"signScale\":12},\"CommissionAmount\":{\"lo\":\"650000\",\"signScale\":12}},\"ClientOrderID\":\"1001763245039.1\"},\"OrderInfoForTransactionPosting\":{\"LimitPrice\":{\"lo\":\"3050000\",\"signScale\":12},\"OrderTypeCode\":\"Limit\",\"OpenClosePositionCode\":\"PC_Open\",\"BuySellCode\":\"Buy\",\"Quantity\":{\"lo\":\"1000000\",\"signScale\":12},\"StopPrice\":{},\"Symbol\":\"BABA  241011C00120000\",\"SchwabSecurityID\":\"102642089\",\"SolicitedCode\":\"Unsolicited\",\"AccountingRuleCode\":\"Cash\",\"SettlementType\":\"SettlementType_Regular\",\"OrderCreatedUserID\":\"O1XX\",\"OrderCreatedUserType\":\"Venue\",\"ClientProductCode\":\"N1\"}}}}","seq":6,"key":"Account Activity"}]}'
    ]
    
    for trade in testList:
        streamer.my_handler(trade)



from Modules import streamer
import json
import re



def send_test_trade_order():
    testList = [
        '{"data":[{"service":"ACCT_ACTIVITY","timestamp":1725979265562,"command":"SUBS","content":[{"1":"54661285","2":"OrderCreated","3":"{\"SchwabOrderID\":\"1001546948468\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"OrderCreated\",\"OrderCreatedEventEquityOrder\":{\"EventType\":\"OrderCreated\",\"Order\":{\"SchwabOrderID\":\"1001546948468\",\"AccountNumber\":\"54661285\",\"Order\":{\"AccountInfo\":{\"AccountNumber\":\"54661285\",\"AccountBranch\":\"WT\",\"CustomerOrFirmCode\":\"CustomerOrFirmCode_Customer\",\"OrderPlacementCustomerID\":\"353286754\",\"AccountState\":\"MO\",\"AccountTypeCode\":\"Customer\"},\"ClientChannelInfo\":{\"ClientProductCode\":\"M1\",\"EventUserID\":\"O1XX\",\"EventUserType\":\"Client\"},\"LifecycleCreatedTimestamp\":{\"DateTimeString\":\"2024-09-10 10:41:05.457\"},\"LifecycleSchwabOrderID\":\"1001546948468\",\"EntryTimestamp\":{\"DateTimeString\":\"2024-09-10 10:41:05.457\"},\"ExpiryTimeStamp\":{\"DateTimeString\":\"2024-09-10\"},\"AutoConfirm\":true,\"PlanSubmitDate\":{\"DateTimeString\":\"2024-09-10\"},\"SourceOMS\":\"ngOMS\",\"FirmID\":\"CHAS\",\"OrderAccount\":\"TDAAccount\",\"AssetOrderEquityOrderLeg\":{\"OrderInstruction\":{\"HandlingInstructionCode\":\"AutomatedExecutionNoIntervention\",\"ExecutionStrategy\":{\"Type\":\"ES_Limit\",\"LimitExecutionStrategy\":{\"Type\":\"ES_Limit\",\"LimitPrice\":{\"lo\":\"500000\",\"signScale\":12},\"LimitPriceUnitCode\":\"Units\"}},\"PreferredRoute\":{},\"EquityOrderInstruction\":{}},\"CommissionInfo\":{\"EstimatedOrderQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"EstimatedPrincipalAmount\":{\"lo\":\"50000000\",\"signScale\":13},\"EstimatedCommissionAmount\":{\"lo\":\"650000\",\"signScale\":12}},\"AssetType\":\"MajorAssetType_EquityOption\",\"TimeInForce\":\"Day\",\"OrderTypeCode\":\"Limit\",\"OrderLegs\":[{\"LegID\":\"1001546948468\",\"LegParentSchwabOrderID\":\"1001546948468\",\"Quantity\":{\"lo\":\"1000000\",\"signScale\":12},\"QuantityUnitCodeType\":\"SharesOrUnits\",\"LeavesQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"BuySellCode\":\"Buy\",\"Security\":{\"SchwabSecurityID\":\"96332598\",\"Symbol\":\"DJT   240920C00030000\",\"UnderlyingSymbol\":\"DJT\",\"MajorAssetType\":\"MajorAssetType_EquityOption\",\"PrimaryMarketSymbol\":\"DJT   240920C00030000\",\"ShortDescriptionText\":\"TRUMP MEDIA \u0026 TECHNO 09\/20\/2024 $30 Call\",\"ShortName\":\"TRUMP MEDIA \u0026 TECHNO 09\/20\/2024 $30 Call\",\"CUSIP\":\"0DJT..IK40030000\",\"OptionsSecurityInfo\":{\"PutCallCode\":\"Call\",\"UnderlyingSchwabSecurityID\":\"72840365\",\"StrikePrice\":{\"lo\":\"30000000\",\"signScale\":12},\"OptionExpiryDate\":{\"DateTimeString\":\"2024-09-20 00:00:00.000\"}}},\"QuoteOnOrderAcceptance\":{\"Ask\":{\"lo\":\"520000\",\"signScale\":12},\"AskSize\":{\"lo\":\"20\"},\"Bid\":{\"lo\":\"480000\",\"signScale\":12},\"BidSize\":{\"lo\":\"27\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-09-10 10:41:05.457\"},\"Symbol\":\"DJT   240920C00030000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"500000\",\"signScale\":12},\"SchwabOrderID\":\"1001546948468\",\"OptionsQuote\":{\"PutCallCode\":\"Call\"}},\"LegClientRequestInfo\":{\"SecurityId\":\"DJT   240920C00030000\",\"SecurityIdTypeCd\":\"Symbol\"},\"AccountingRuleCode\":\"Cash\",\"EstimatedNetAmount\":{\"lo\":\"50650000\",\"signScale\":13},\"EstimatedPrincipalAmnt\":{\"lo\":\"50000000\",\"signScale\":13},\"EquityOrderLeg\":{\"EquityOptionsOrderLeg\":{\"OpenClosePositionCode\":\"PC_Open\"}}}],\"OrderCapacityCode\":\"OC_Agency\",\"SettlementType\":\"SettlementType_Regular\",\"Rule80ACode\":73,\"SolicitedCode\":\"Unsolicited\",\"TradeTag\":\"API_TOS:TRADE_ALL\",\"EquityOrder\":{\"TradingSessionCodeOnOrder\":\"REG\"}}}}}}}","seq":1,"key":"Account Activity"}]}]}'
        # r"""{"service":"ACCT_ACTIVITY","timestamp":1726847587056,"command":"SUBS","content":[{"1":"54661285","2":"OrderCreated","3":"{\"SchwabOrderID\":\"1001657905188\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"OrderCreated\",\"OrderCreatedEventEquityOrder\":{\"EventType\":\"OrderCreated\",\"Order\":{\"SchwabOrderID\":\"1001657905188\",\"AccountNumber\":\"54661285\",\"Order\":{\"AccountInfo\":{\"AccountNumber\":\"54661285\",\"AccountBranch\":\"WT\",\"CustomerOrFirmCode\":\"CustomerOrFirmCode_Customer\",\"OrderPlacementCustomerID\":\"353286754\",\"AccountState\":\"MO\",\"AccountTypeCode\":\"Customer\"},\"ClientChannelInfo\":{\"ClientProductCode\":\"M1\",\"EventUserID\":\"O1XX\",\"EventUserType\":\"Client\"},\"LifecycleCreatedTimestamp\":{\"DateTimeString\":\"2024-09-20 11:53:06.929\"},\"LifecycleSchwabOrderID\":\"1001657905188\",\"EntryTimestamp\":{\"DateTimeString\":\"2024-09-20 11:53:06.929\"},\"ExpiryTimeStamp\":{\"DateTimeString\":\"2024-09-20\"},\"AutoConfirm\":true,\"PlanSubmitDate\":{\"DateTimeString\":\"2024-09-20\"},\"SourceOMS\":\"ngOMS\",\"FirmID\":\"CHAS\",\"OrderAccount\":\"TDAAccount\",\"AssetOrderEquityOrderLeg\":{\"OrderInstruction\":{\"HandlingInstructionCode\":\"AutomatedExecutionNoIntervention\",\"ExecutionStrategy\":{\"Type\":\"ES_Limit\",\"LimitExecutionStrategy\":{\"Type\":\"ES_Limit\",\"LimitPrice\":{\"lo\":\"1520000\",\"signScale\":12},\"LimitPriceUnitCode\":\"Units\"}},\"PreferredRoute\":{},\"EquityOrderInstruction\":{}},\"CommissionInfo\":{\"EstimatedOrderQuantity\":{\"lo\":\"2000000\",\"signScale\":12},\"EstimatedPrincipalAmount\":{\"lo\":\"304000000\",\"signScale\":13},\"EstimatedCommissionAmount\":{\"lo\":\"1300000\",\"signScale\":12}},\"AssetType\":\"MajorAssetType_EquityOption\",\"TimeInForce\":\"Day\",\"OrderTypeCode\":\"Limit\",\"OrderLegs\":[{\"LegID\":\"1001657905188\",\"LegParentSchwabOrderID\":\"1001657905188\",\"Quantity\":{\"lo\":\"2000000\",\"signScale\":12},\"QuantityUnitCodeType\":\"SharesOrUnits\",\"LeavesQuantity\":{\"lo\":\"2000000\",\"signScale\":12},\"BuySellCode\":\"Buy\",\"Security\":{\"SchwabSecurityID\":\"102000669\",\"Symbol\":\"SPY   240927P00560000\",\"UnderlyingSymbol\":\"SPY\",\"MajorAssetType\":\"MajorAssetType_EquityOption\",\"PrimaryMarketSymbol\":\"SPY   240927P00560000\",\"ShortDescriptionText\":\"SPDR S\\u0026P 500 09/27/2024 $560 Put\",\"ShortName\":\"SPDR S\\u0026P 500 09/27/2024 $560 Put\",\"CUSIP\":\"0SPY..UR40560000\",\"OptionsSecurityInfo\":{\"PutCallCode\":\"Put\",\"UnderlyingSchwabSecurityID\":\"1281357639\",\"StrikePrice\":{\"lo\":\"560000000\",\"signScale\":12},\"OptionExpiryDate\":{\"DateTimeString\":\"2024-09-27 00:00:00.000\"}}},\"QuoteOnOrderAcceptance\":{\"Ask\":{\"lo\":\"1510000\",\"signScale\":12},\"AskSize\":{\"lo\":\"236\"},\"Bid\":{\"lo\":\"1490000\",\"signScale\":12},\"BidSize\":{\"lo\":\"159\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-09-20 11:53:06.929\"},\"Symbol\":\"SPY   240927P00560000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"1500000\",\"signScale\":12},\"SchwabOrderID\":\"1001657905188\",\"OptionsQuote\":{\"PutCallCode\":\"Put\"}},\"LegClientRequestInfo\":{\"SecurityId\":\"SPY   240927P00560000\",\"SecurityIdTypeCd\":\"Symbol\"},\"AccountingRuleCode\":\"Cash\",\"EstimatedNetAmount\":{\"lo\":\"305300000\",\"signScale\":13},\"EstimatedPrincipalAmnt\":{\"lo\":\"304000000\",\"signScale\":13},\"EquityOrderLeg\":{\"EquityOptionsOrderLeg\":{\"OpenClosePositionCode\":\"PC_Open\"}}}],\"OrderCapacityCode\":\"OC_Agency\",\"SettlementType\":\"SettlementType_Regular\",\"Rule80ACode\":73,\"SolicitedCode\":\"Unsolicited\",\"TradeTag\":\"API_TOS:TRADE_ALL\",\"EquityOrder\":{\"TradingSessionCodeOnOrder\":\"REG\"}}}}}}}","seq":48,"key":"Account Activity"},{"1":"54661285","2":"OrderAccepted","3":"{\"SchwabOrderID\":\"1001657905188\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"OrderAccepted\",\"OrderAcceptedEvent\":{\"EventType\":\"OrderAccepted\",\"CreatedTimeStamp\":{\"DateTimeString\":\"2024-09-20 11:53:06.929\"},\"ExpiryTimeStamp\":{\"DateTimeString\":\"2024-09-20\"},\"Status\":\"Open\",\"TradingSessionCodeOnOrderEntry\":\"REG\",\"QuoteOnOrderEntry\":[{\"Ask\":{\"lo\":\"1510000\",\"signScale\":12},\"AskSize\":{\"lo\":\"236\"},\"Bid\":{\"lo\":\"1490000\",\"signScale\":12},\"BidSize\":{\"lo\":\"159\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-09-20 11:53:06.929\"},\"Symbol\":\"SPY   240927P00560000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"1500000\",\"signScale\":12},\"SchwabOrderID\":\"1001657905188\",\"OptionsQuote\":{\"PutCallCode\":\"Put\"}}]}}}","seq":49,"key":"Account Activity"}]}'""",
        # r"""{"service":"ACCT_ACTIVITY","timestamp":1726847588066,"command":"SUBS","content":[{"1":"54661285","2":"ExecutionRequested","3":"{\"SchwabOrderID\":\"1001657905188\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequested\",\"ExecutionRequestedEventRoutedInfo\":{\"EventType\":\"ExecutionRequested\",\"RouteSequenceNumber\":1,\"RouteInfo\":{\"RouteName\":\"MORGAN_OPT_F1_J2\",\"RouteSequenceNumber\":1,\"RoutedExecutionTimestamp\":{\"DateTimeString\":\"2024-09-20 11:53:06.965\"},\"Quote\":{\"Ask\":{\"lo\":\"1510000\",\"signScale\":12},\"AskSize\":{\"lo\":\"236\"},\"Bid\":{\"lo\":\"1490000\",\"signScale\":12},\"BidSize\":{\"lo\":\"159\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-09-20 11:53:06.929\"},\"Symbol\":\"SPY   240927P00560000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"1500000\",\"signScale\":12},\"SchwabOrderID\":\"1001657905188\",\"OptionsQuote\":{\"PutCallCode\":\"Put\"}},\"RouteRequestedType\":\"New\",\"RoutedQuantity\":{\"lo\":\"2000000\",\"signScale\":12},\"RoutedPrice\":{\"lo\":\"1520000\",\"signScale\":12},\"RouteStatus\":\"RouteCreated\",\"ClientOrderID\":\"1001657905188.1\",\"RoutedTime\":{\"DateTimeString\":\"2024-09-20 11:53:06.965\"},\"RouteTimeInForce\":\"Day\",\"RouteAcknowledgmentTimeStamp\":{}},\"RouteRequestedBy\":\"RR_Broker\",\"LegId\":\"1001657905188\"}}}","seq":50,"key":"Account Activity"},{"1":"54661285","2":"ExecutionRequestCreated","3":"{\"SchwabOrderID\":\"1001657905188\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequestCreated\",\"ExecutionRequestCreatedEvent\":{\"EventType\":\"ExecutionRequestCreated\",\"LegId\":\"1001657905188\",\"RouteName\":\"MORGAN_OPT_F1_J2\",\"RouteRequestType\":\"New\",\"RouteSequenceNumber\":1,\"RouteRequestedBy\":\"RR_Broker\",\"RouteStatus\":\"RouteFixAcknowledged\",\"SenderCompID\":\"SCHWAB\",\"RoutedTime\":{\"DateTimeString\":\"2024-09-20 11:53:06.995\"},\"ClientOrderID\":\"1001657905188.1\"}}}","seq":51,"key":"Account Activity"},{"1":"54661285","2":"ExecutionRequestCompleted","3":"{\"SchwabOrderID\":\"1001657905188\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequestCompleted\",\"ExecutionRequestCompletedEvent\":{\"EventType\":\"ExecutionRequestCompleted\",\"LegId\":\"1001657905188\",\"ResponseType\":\"Accepted\",\"ExecutionTime\":{\"DateTimeString\":\"2024-09-20 11:53:07.053\"},\"RouteSequenceNumber\":1,\"RouteStatus\":\"RouteVenueAccepted\",\"RouteAcknowledgmentTimeStamp\":{\"DateTimeString\":\"2024-09-20 11:53:07.022\"},\"ClientOrderID\":\"1001657905188.1\"}}}","seq":52,"key":"Account Activity"},{"1":"54661285","2":"OrderFillCompleted","3":"{\"SchwabOrderID\":\"1001657905188\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"OrderFillCompleted\",\"OrderFillCompletedEventOrderLegQuantityInfo\":{\"EventType\":\"OrderFillCompleted\",\"LegId\":\"1001657905188\",\"LegStatus\":\"LegClosed\",\"QuantityInfo\":{\"ExecutionID\":\"20240920-EST-ngOMS-13303091620\",\"CumulativeQuantity\":{\"lo\":\"2000000\",\"signScale\":12},\"LeavesQuantity\":{\"signScale\":12},\"AveragePrice\":{\"lo\":\"1500000\",\"signScale\":12}},\"PriceImprovement\":{\"lo\":\"2000000\",\"signScale\":12},\"LegSubStatus\":\"LegSubStatusFilled\",\"ExecutionInfo\":{\"ExecutionSequenceNumber\":1,\"ExecutionId\":\"20240920-EST-ngOMS-13303091620\",\"VenueExecutionID\":\"aTU2Ex-XRn2uN3dXOz8mBwA1\",\"Exchange\":\"CBOE\",\"ExecutionQuantity\":{\"lo\":\"2000000\",\"signScale\":12},\"ExecutionPrice\":{\"lo\":\"1500000\",\"signScale\":12},\"ExecutionTimeStamp\":{\"DateTimeString\":\"2024-09-20 11:53:07.154\"},\"ExecutionTransType\":\"Fill\",\"ExecutionCapacityCode\":\"Agency\",\"RouteName\":\"MORGAN_OPT_F1_J2\",\"RouteSequenceNumber\":1,\"VenuExecutionTimeStamp\":{\"DateTimeString\":\"2024-09-20 11:53:07.124\"},\"ReportingCapacityCode\":\"RC_Agency\",\"ActualChargedCommissionAmount\":{\"lo\":\"1300000\",\"signScale\":12},\"AsOfTimeStamp\":{},\"ActualChargedFeesCommissionAndTax\":{\"StateTaxWithholding\":{\"signScale\":12},\"FederalTaxWithholding\":{\"signScale\":12},\"SECFees\":{\"signScale\":12},\"ORF\":{\"lo\":\"20000\",\"signScale\":12},\"FTT\":{\"signScale\":12},\"TaxWithholding1446\":{\"signScale\":12},\"GoodsAndServicesTax\":{\"signScale\":12},\"IOF\":{\"signScale\":12},\"TAF\":{\"signScale\":12},\"CommissionAmount\":{\"lo\":\"1300000\",\"signScale\":12}},\"ClientOrderID\":\"1001657905188.1\"},\"OrderInfoForTransactionPosting\":{\"LimitPrice\":{\"lo\":\"1520000\",\"signScale\":12},\"OrderTypeCode\":\"Limit\",\"OpenClosePositionCode\":\"PC_Open\",\"BuySellCode\":\"Buy\",\"Quantity\":{\"lo\":\"2000000\",\"signScale\":12},\"StopPrice\":{},\"Symbol\":\"SPY   240927P00560000\",\"SchwabSecurityID\":\"102000669\",\"SolicitedCode\":\"Unsolicited\",\"AccountingRuleCode\":\"Cash\",\"SettlementType\":\"SettlementType_Regular\",\"OrderCreatedUserID\":\"O1XX\",\"OrderCreatedUserType\":\"Venue\",\"ClientProductCode\":\"N1\"}}}}","seq":53,"key":"Account Activity"}]}""",
        # r"""{"service":"ACCT_ACTIVITY","timestamp":1726850946047,"command":"SUBS","content":[{"1":"54661285","2":"OrderCreated","3":"{\"SchwabOrderID\":\"1001659308472\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"OrderCreated\",\"OrderCreatedEventEquityOrder\":{\"EventType\":\"OrderCreated\",\"Order\":{\"SchwabOrderID\":\"1001659308472\",\"AccountNumber\":\"54661285\",\"Order\":{\"AccountInfo\":{\"AccountNumber\":\"54661285\",\"AccountBranch\":\"WT\",\"CustomerOrFirmCode\":\"CustomerOrFirmCode_Customer\",\"OrderPlacementCustomerID\":\"353286754\",\"AccountState\":\"MO\",\"AccountTypeCode\":\"Customer\"},\"ClientChannelInfo\":{\"ClientProductCode\":\"M1\",\"EventUserID\":\"O1XX\",\"EventUserType\":\"Client\"},\"LifecycleCreatedTimestamp\":{\"DateTimeString\":\"2024-09-20 12:49:05.923\"},\"LifecycleSchwabOrderID\":\"1001659308472\",\"EntryTimestamp\":{\"DateTimeString\":\"2024-09-20 12:49:05.923\"},\"ExpiryTimeStamp\":{\"DateTimeString\":\"2024-09-20\"},\"AutoConfirm\":true,\"PlanSubmitDate\":{\"DateTimeString\":\"2024-09-20\"},\"SourceOMS\":\"ngOMS\",\"FirmID\":\"CHAS\",\"OrderAccount\":\"TDAAccount\",\"AssetOrderEquityOrderLeg\":{\"OrderInstruction\":{\"HandlingInstructionCode\":\"AutomatedExecutionNoIntervention\",\"ExecutionStrategy\":{\"Type\":\"ES_Limit\",\"LimitExecutionStrategy\":{\"Type\":\"ES_Limit\",\"LimitPrice\":{\"lo\":\"1700000\",\"signScale\":12},\"LimitPriceUnitCode\":\"Units\"}},\"PreferredRoute\":{},\"EquityOrderInstruction\":{}},\"CommissionInfo\":{\"EstimatedOrderQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"EstimatedPrincipalAmount\":{\"lo\":\"170000000\",\"signScale\":13},\"EstimatedCommissionAmount\":{\"lo\":\"650000\",\"signScale\":12}},\"AssetType\":\"MajorAssetType_EquityOption\",\"TimeInForce\":\"Day\",\"OrderTypeCode\":\"Limit\",\"OrderLegs\":[{\"LegID\":\"1001659308472\",\"LegParentSchwabOrderID\":\"1001659308472\",\"Quantity\":{\"lo\":\"1000000\",\"signScale\":12},\"QuantityUnitCodeType\":\"SharesOrUnits\",\"LeavesQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"BuySellCode\":\"Buy\",\"Security\":{\"SchwabSecurityID\":\"101968678\",\"Symbol\":\"AAPL  240927C00235000\",\"UnderlyingSymbol\":\"AAPL\",\"MajorAssetType\":\"MajorAssetType_EquityOption\",\"PrimaryMarketSymbol\":\"AAPL  240927C00235000\",\"ShortDescriptionText\":\"APPLE INC 09/27/2024 $235 Call\",\"ShortName\":\"APPLE INC 09/27/2024 $235 Call\",\"CUSIP\":\"0AAPL.IR40235000\",\"OptionsSecurityInfo\":{\"PutCallCode\":\"Call\",\"UnderlyingSchwabSecurityID\":\"1973757747\",\"StrikePrice\":{\"lo\":\"235000000\",\"signScale\":12},\"OptionExpiryDate\":{\"DateTimeString\":\"2024-09-27 00:00:00.000\"}}},\"QuoteOnOrderAcceptance\":{\"Ask\":{\"lo\":\"1700000\",\"signScale\":12},\"AskSize\":{\"lo\":\"5\"},\"Bid\":{\"lo\":\"1680000\",\"signScale\":12},\"BidSize\":{\"lo\":\"422\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-09-20 12:49:05.923\"},\"Symbol\":\"AAPL  240927C00235000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"1690000\",\"signScale\":12},\"SchwabOrderID\":\"1001659308472\",\"OptionsQuote\":{\"PutCallCode\":\"Call\"}},\"LegClientRequestInfo\":{\"SecurityId\":\"AAPL  240927C00235000\",\"SecurityIdTypeCd\":\"Symbol\"},\"AccountingRuleCode\":\"Cash\",\"EstimatedNetAmount\":{\"lo\":\"170650000\",\"signScale\":13},\"EstimatedPrincipalAmnt\":{\"lo\":\"170000000\",\"signScale\":13},\"EquityOrderLeg\":{\"EquityOptionsOrderLeg\":{\"OpenClosePositionCode\":\"PC_Open\"}}}],\"OrderCapacityCode\":\"OC_Agency\",\"SettlementType\":\"SettlementType_Regular\",\"Rule80ACode\":73,\"SolicitedCode\":\"Unsolicited\",\"TradeTag\":\"API_TOS:TRADE_ALL\",\"EquityOrder\":{\"TradingSessionCodeOnOrder\":\"REG\"}}}}}}}","seq":109,"key":"Account Activity"},{"1":"54661285","2":"OrderAccepted","3":"{\"SchwabOrderID\":\"1001659308472\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"OrderAccepted\",\"OrderAcceptedEvent\":{\"EventType\":\"OrderAccepted\",\"CreatedTimeStamp\":{\"DateTimeString\":\"2024-09-20 12:49:05.923\"},\"ExpiryTimeStamp\":{\"DateTimeString\":\"2024-09-20\"},\"Status\":\"Open\",\"TradingSessionCodeOnOrderEntry\":\"REG\",\"QuoteOnOrderEntry\":[{\"Ask\":{\"lo\":\"1700000\",\"signScale\":12},\"AskSize\":{\"lo\":\"5\"},\"Bid\":{\"lo\":\"1680000\",\"signScale\":12},\"BidSize\":{\"lo\":\"422\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-09-20 12:49:05.923\"},\"Symbol\":\"AAPL  240927C00235000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"1690000\",\"signScale\":12},\"SchwabOrderID\":\"1001659308472\",\"OptionsQuote\":{\"PutCallCode\":\"Call\"}}]}}}","seq":110,"key":"Account Activity"}]}""",
        # r"""{"service":"ACCT_ACTIVITY","timestamp":1726850947056,"command":"SUBS","content":[{"1":"54661285","2":"ExecutionRequested","3":"{\"SchwabOrderID\":\"1001659308472\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequested\",\"ExecutionRequestedEventRoutedInfo\":{\"EventType\":\"ExecutionRequested\",\"RouteSequenceNumber\":1,\"RouteInfo\":{\"RouteName\":\"DASH_OPT_F1_J1\",\"RouteSequenceNumber\":1,\"RoutedExecutionTimestamp\":{\"DateTimeString\":\"2024-09-20 12:49:05.959\"},\"Quote\":{\"Ask\":{\"lo\":\"1700000\",\"signScale\":12},\"AskSize\":{\"lo\":\"5\"},\"Bid\":{\"lo\":\"1680000\",\"signScale\":12},\"BidSize\":{\"lo\":\"422\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-09-20 12:49:05.923\"},\"Symbol\":\"AAPL  240927C00235000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"1690000\",\"signScale\":12},\"SchwabOrderID\":\"1001659308472\",\"OptionsQuote\":{\"PutCallCode\":\"Call\"}},\"RouteRequestedType\":\"New\",\"RoutedQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"RoutedPrice\":{\"lo\":\"1700000\",\"signScale\":12},\"RouteStatus\":\"RouteCreated\",\"ClientOrderID\":\"1001659308472.1\",\"RoutedTime\":{\"DateTimeString\":\"2024-09-20 12:49:05.959\"},\"RouteTimeInForce\":\"Day\",\"RouteAcknowledgmentTimeStamp\":{}},\"RouteRequestedBy\":\"RR_Broker\",\"LegId\":\"1001659308472\"}}}","seq":111,"key":"Account Activity"},{"1":"54661285","2":"ExecutionRequestCreated","3":"{\"SchwabOrderID\":\"1001659308472\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequestCreated\",\"ExecutionRequestCreatedEvent\":{\"EventType\":\"ExecutionRequestCreated\",\"LegId\":\"1001659308472\",\"RouteName\":\"DASH_OPT_F1_J1\",\"RouteRequestType\":\"New\",\"RouteSequenceNumber\":1,\"RouteRequestedBy\":\"RR_Broker\",\"RouteStatus\":\"RouteFixAcknowledged\",\"SenderCompID\":\"SCHWABTDAMOFP1\",\"RoutedTime\":{\"DateTimeString\":\"2024-09-20 12:49:05.988\"},\"ClientOrderID\":\"1001659308472.1\"}}}","seq":112,"key":"Account Activity"},{"1":"54661285","2":"ExecutionRequestCompleted","3":"{\"SchwabOrderID\":\"1001659308472\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequestCompleted\",\"ExecutionRequestCompletedEvent\":{\"EventType\":\"ExecutionRequestCompleted\",\"LegId\":\"1001659308472\",\"ResponseType\":\"Accepted\",\"ExchangeOrderID\":\"200096977015\",\"ExecutionTime\":{\"DateTimeString\":\"2024-09-20 12:49:06.087\"},\"RouteSequenceNumber\":1,\"RouteStatus\":\"RouteVenueAccepted\",\"RouteAcknowledgmentTimeStamp\":{\"DateTimeString\":\"2024-09-20 12:49:06.056\"},\"ClientOrderID\":\"1001659308472.1\"}}}","seq":113,"key":"Account Activity"},{"1":"54661285","2":"OrderFillCompleted","3":"{\"SchwabOrderID\":\"1001659308472\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"OrderFillCompleted\",\"OrderFillCompletedEventOrderLegQuantityInfo\":{\"EventType\":\"OrderFillCompleted\",\"LegId\":\"1001659308472\",\"LegStatus\":\"LegClosed\",\"QuantityInfo\":{\"ExecutionID\":\"20240920-EST-ngOMS-13304116286\",\"CumulativeQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"LeavesQuantity\":{\"signScale\":12},\"AveragePrice\":{\"lo\":\"1700000\",\"signScale\":12}},\"PriceImprovement\":{\"signScale\":12},\"LegSubStatus\":\"LegSubStatusFilled\",\"ExecutionInfo\":{\"ExecutionSequenceNumber\":1,\"ExecutionId\":\"20240920-EST-ngOMS-13304116286\",\"VenueExecutionID\":\"200551658919\",\"Exchange\":\"CBOE\",\"ExecutionQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"ExecutionPrice\":{\"lo\":\"1700000\",\"signScale\":12},\"ExecutionTimeStamp\":{\"DateTimeString\":\"2024-09-20 12:49:06.201\"},\"ExecutionTransType\":\"Fill\",\"ExecutionCapacityCode\":\"Agency\",\"RouteName\":\"DASH_OPT_F1_J1\",\"RouteSequenceNumber\":1,\"VenuExecutionTimeStamp\":{\"DateTimeString\":\"2024-09-20 12:49:06.168\"},\"ReportingCapacityCode\":\"RC_Agency\",\"ActualChargedCommissionAmount\":{\"lo\":\"650000\",\"signScale\":12},\"AsOfTimeStamp\":{},\"ActualChargedFeesCommissionAndTax\":{\"StateTaxWithholding\":{\"signScale\":12},\"FederalTaxWithholding\":{\"signScale\":12},\"SECFees\":{\"signScale\":12},\"ORF\":{\"lo\":\"10000\",\"signScale\":12},\"FTT\":{\"signScale\":12},\"TaxWithholding1446\":{\"signScale\":12},\"GoodsAndServicesTax\":{\"signScale\":12},\"IOF\":{\"signScale\":12},\"TAF\":{\"signScale\":12},\"CommissionAmount\":{\"lo\":\"650000\",\"signScale\":12}},\"ClientOrderID\":\"1001659308472.1\"},\"OrderInfoForTransactionPosting\":{\"LimitPrice\":{\"lo\":\"1700000\",\"signScale\":12},\"OrderTypeCode\":\"Limit\",\"OpenClosePositionCode\":\"PC_Open\",\"BuySellCode\":\"Buy\",\"Quantity\":{\"lo\":\"1000000\",\"signScale\":12},\"StopPrice\":{},\"Symbol\":\"AAPL  240927C00235000\",\"SchwabSecurityID\":\"101968678\",\"SolicitedCode\":\"Unsolicited\",\"AccountingRuleCode\":\"Cash\",\"SettlementType\":\"SettlementType_Regular\",\"OrderCreatedUserID\":\"O1XX\",\"OrderCreatedUserType\":\"Venue\",\"ClientProductCode\":\"N1\"}}}}","seq":114,"key":"Account Activity"}]}""",
        # r"""{"service":"ACCT_ACTIVITY","timestamp":1727190151694,"command":"SUBS","content":[{"1":"54661285","2":"ChangeAccepted","3":"{\"SchwabOrderID\":\"1001683042944\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ChangeAccepted\",\"ChangeAcceptedEvent\":{\"EventType\":\"ChangeAccepted\",\"CreatedTimeStamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.555\"},\"ExpiryTimeStamp\":{\"DateTimeString\":\"2024-09-24\"},\"TradingSessionCodeOnOrderEntry\":\"REG\",\"QuoteOnOrderEntry\":[{\"Ask\":{\"lo\":\"2740000\",\"signScale\":12},\"AskSize\":{\"lo\":\"15\"},\"Bid\":{\"lo\":\"2720000\",\"signScale\":12},\"BidSize\":{\"lo\":\"12\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.555\"},\"Symbol\":\"TSLA  240927C00260000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"2730000\",\"signScale\":13},\"SchwabOrderID\":\"1001683042944\",\"OptionsQuote\":{\"PutCallCode\":\"Call\"}}],\"Status\":\"Open\",\"LegStatus\":\"LegOpen\",\"LegInfoUpdate\":[{\"LegId\":\"1001683042944\",\"AccountingRuleCode\":\"Cash\",\"IntendedOrderQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"PreviousLegId\":\"1001683042935\"}]}}}","seq":66,"key":"Account Activity"},{"1":"54661285","2":"ExecutionRequested","3":"{\"SchwabOrderID\":\"1001683042935\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequested\",\"ExecutionRequestedEventRoutedInfo\":{\"EventType\":\"ExecutionRequested\",\"RouteSequenceNumber\":2,\"RouteInfo\":{\"RouteName\":\"DASH_OPT_F1_J1\",\"RouteSequenceNumber\":2,\"RoutedExecutionTimestamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.593\"},\"Quote\":{\"Ask\":{\"lo\":\"2780000\",\"signScale\":12},\"AskSize\":{\"lo\":\"67\"},\"Bid\":{\"lo\":\"2760000\",\"signScale\":12},\"BidSize\":{\"lo\":\"5\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-09-24 11:02:23.519\"},\"Symbol\":\"TSLA  240927C00260000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"2770000\",\"signScale\":13},\"SchwabOrderID\":\"1001683042935\",\"OptionsQuote\":{\"PutCallCode\":\"Call\"}},\"RouteRequestedType\":\"Cancel\",\"RoutedQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"RoutedPrice\":{\"lo\":\"2800000\",\"signScale\":12},\"RouteStatus\":\"RouteCreated\",\"ClientOrderID\":\"1001683042935.2\",\"RoutedTime\":{\"DateTimeString\":\"2024-09-24 11:02:30.593\"},\"RouteTimeInForce\":\"Day\",\"RouteAcknowledgmentTimeStamp\":{}},\"RouteRequestedBy\":\"RR_Broker\",\"LegId\":\"1001683042935\"}}}","seq":67,"key":"Account Activity"},{"1":"54661285","2":"ExecutionRequestCompleted","3":"{\"SchwabOrderID\":\"1001683042935\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequestCompleted\",\"ExecutionRequestCompletedEvent\":{\"EventType\":\"ExecutionRequestCompleted\",\"LegId\":\"1001683042935\",\"ResponseType\":\"Accepted\",\"ExecutionTime\":{\"DateTimeString\":\"2024-09-24 11:02:30.719\"},\"RouteSequenceNumber\":1,\"RouteStatus\":\"RouteVenueAccepted\",\"RouteAcknowledgmentTimeStamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.685\"},\"ClientOrderID\":\"1001683042945\"}}}","seq":68,"key":"Account Activity"},{"1":"54661285","2":"ExecutionCreated","3":"{\"SchwabOrderID\":\"1001683042935\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionCreated\",\"ExecutionCreatedEventExecutionInfo\":{\"EventType\":\"ExecutionCreated\",\"LegId\":\"1001683042935\",\"ExecutionInfo\":{\"ExecutionSequenceNumber\":1,\"ExecutionId\":\"20240924-EST-ngOMS-13314546436\",\"ExecutionQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"ExecutionTimeStamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.733\"},\"ExecutionTransType\":\"UROut\",\"ExecutionCapacityCode\":\"Agency\",\"RouteName\":\"DASH_OPT_F1_J1\",\"RouteSequenceNumber\":1,\"VenuExecutionTimeStamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.733\"},\"CancelType\":\"ClientCancel\",\"ReportingCapacityCode\":\"RC_Agency\",\"AsOfTimeStamp\":{},\"ClientOrderID\":\"1001683042935.1\"},\"AsOfTimeStamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.733\"},\"RouteSequenceNumber\":1}}}","seq":69,"key":"Account Activity"},{"1":"54661285","2":"ExecutionRequested","3":"{\"SchwabOrderID\":\"1001683042944\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequested\",\"ExecutionRequestedEventRoutedInfo\":{\"EventType\":\"ExecutionRequested\",\"RouteSequenceNumber\":1,\"RouteInfo\":{\"RouteName\":\"SIG_OPT_F2_J2\",\"RouteSequenceNumber\":1,\"RoutedExecutionTimestamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.735\"},\"Quote\":{\"Ask\":{\"lo\":\"2740000\",\"signScale\":12},\"AskSize\":{\"lo\":\"15\"},\"Bid\":{\"lo\":\"2720000\",\"signScale\":12},\"BidSize\":{\"lo\":\"12\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.555\"},\"Symbol\":\"TSLA  240927C00260000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"2730000\",\"signScale\":13},\"SchwabOrderID\":\"1001683042944\",\"OptionsQuote\":{\"PutCallCode\":\"Call\"}},\"RouteRequestedType\":\"New\",\"RoutedQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"RoutedPrice\":{\"lo\":\"2750000\",\"signScale\":12},\"RouteStatus\":\"RouteCreated\",\"ClientOrderID\":\"1001683042944.1\",\"RoutedTime\":{\"DateTimeString\":\"2024-09-24 11:02:30.735\"},\"RouteTimeInForce\":\"Day\",\"RouteAcknowledgmentTimeStamp\":{}},\"RouteRequestedBy\":\"RR_Broker\",\"LegId\":\"1001683042944\"}}}","seq":70,"key":"Account Activity"},{"1":"54661285","2":"OrderUROutCompleted","3":"{\"SchwabOrderID\":\"1001683042935\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"OrderUROutCompleted\",\"OrderUROutCompletedEvent\":{\"EventType\":\"OrderUROutCompleted\",\"LegId\":\"1001683042935\",\"ExecutionId\":\"20240924-EST-ngOMS-13314546436\",\"LeavesQuantity\":{},\"CancelQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"LegStatus\":\"LegClosed\",\"LegSubStatus\":\"LegSubStatusCancelled\",\"OutCancelType\":\"ClientCancel\",\"VenueExecutionTimeStamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.733\"},\"ExecutionTimeStamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.733\"},\"RouteName\":\"DASH_OPT_F1_J1\"}}}","seq":71,"key":"Account Activity"},{"1":"54661285","2":"ExecutionRequestCreated","3":"{\"SchwabOrderID\":\"1001683042944\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequestCreated\",\"ExecutionRequestCreatedEvent\":{\"EventType\":\"ExecutionRequestCreated\",\"LegId\":\"1001683042944\",\"RouteName\":\"SIG_OPT_F2_J2\",\"RouteRequestType\":\"New\",\"RouteSequenceNumber\":1,\"RouteRequestedBy\":\"RR_Broker\",\"RouteStatus\":\"RouteFixAcknowledged\",\"SenderCompID\":\"CHAS2\",\"RoutedTime\":{\"DateTimeString\":\"2024-09-24 11:02:30.762\"},\"ClientOrderID\":\"1001683042944.1\"}}}","seq":72,"key":"Account Activity"},{"1":"54661285","2":"ExecutionRequestCompleted","3":"{\"SchwabOrderID\":\"1001683042944\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ExecutionRequestCompleted\",\"ExecutionRequestCompletedEvent\":{\"EventType\":\"ExecutionRequestCompleted\",\"LegId\":\"1001683042944\",\"ResponseType\":\"Accepted\",\"ExecutionTime\":{\"DateTimeString\":\"2024-09-24 11:02:30.820\"},\"RouteSequenceNumber\":1,\"RouteStatus\":\"RouteVenueAccepted\",\"RouteAcknowledgmentTimeStamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.788\"},\"ClientOrderID\":\"1001683042944.1\"}}}","seq":73,"key":"Account Activity"}]}""",
        # r"""{"service":"ACCT_ACTIVITY","timestamp":1727190150672,"command":"SUBS","content":[{"1":"54661285","2":"CancelAccepted","3":"{\"SchwabOrderID\":\"1001683042935\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"CancelAccepted\",\"CancelAcceptedEvent\":{\"EventType\":\"CancelAccepted\",\"LifecycleSchwabOrderID\":\"1001683042935\",\"PlanSubmitDate\":{\"DateTimeString\":\"2024-09-24\"},\"ClientProductCode\":\"M1\",\"AutoConfirm\":true,\"CancelTimeStamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.591\"},\"LegCancelRequestInfoList\":[{\"LegID\":\"1001683042935\",\"IntendedOrderQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"ChangedNewOrderID\":\"1001683042944\",\"RequestedAmount\":{\"lo\":\"1000000\",\"signScale\":12},\"LegStatus\":\"LegOpen\",\"LegSubStatus\":\"LegSubStatusCancelled\",\"ChangedNewSchwabOrderId\":\"1001683042944\",\"CancelAcceptedTime\":{\"DateTimeString\":\"2024-09-24 11:02:30.591\"},\"EventUserID\":\"O1XX\"}],\"CancelRequestType\":\"ClientCancel\"}}}","seq":64,"key":"Account Activity"},{"1":"54661285","2":"ChangeCreated","3":"{\"SchwabOrderID\":\"1001683042944\",\"AccountNumber\":\"54661285\",\"BaseEvent\":{\"EventType\":\"ChangeCreated\",\"ChangeCreatedEventEquityOrder\":{\"EventType\":\"ChangeCreated\",\"Order\":{\"SchwabOrderID\":\"1001683042944\",\"AccountNumber\":\"54661285\",\"Order\":{\"AccountInfo\":{\"AccountNumber\":\"54661285\",\"AccountBranch\":\"WT\",\"CustomerOrFirmCode\":\"CustomerOrFirmCode_Customer\",\"OrderPlacementCustomerID\":\"353286754\",\"AccountState\":\"MO\",\"AccountTypeCode\":\"Customer\"},\"ClientChannelInfo\":{\"ClientProductCode\":\"M1\",\"EventUserID\":\"O1XX\",\"EventUserType\":\"Client\"},\"LifecycleCreatedTimestamp\":{\"DateTimeString\":\"2024-09-24 11:02:23.519\"},\"LifecycleSchwabOrderID\":\"1001683042935\",\"EntryTimestamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.555\"},\"ExpiryTimeStamp\":{\"DateTimeString\":\"2024-09-24\"},\"AutoConfirm\":true,\"PlanSubmitDate\":{\"DateTimeString\":\"2024-09-24\"},\"SourceOMS\":\"ngOMS\",\"FirmID\":\"CHAS\",\"OrderAccount\":\"TDAAccount\",\"AssetOrderEquityOrderLeg\":{\"OrderInstruction\":{\"HandlingInstructionCode\":\"AutomatedExecutionNoIntervention\",\"ExecutionStrategy\":{\"Type\":\"ES_Limit\",\"LimitExecutionStrategy\":{\"Type\":\"ES_Limit\",\"LimitPrice\":{\"lo\":\"2750000\",\"signScale\":12},\"LimitPriceUnitCode\":\"Units\"}},\"PreferredRoute\":{},\"EquityOrderInstruction\":{}},\"CommissionInfo\":{\"EstimatedOrderQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"EstimatedPrincipalAmount\":{\"lo\":\"275000000\",\"signScale\":12},\"EstimatedCommissionAmount\":{\"lo\":\"650000\",\"signScale\":12}},\"AssetType\":\"MajorAssetType_EquityOption\",\"TimeInForce\":\"Day\",\"OrderTypeCode\":\"Limit\",\"OrderLegs\":[{\"LegID\":\"1001683042944\",\"LegParentSchwabOrderID\":\"1001683042944\",\"Quantity\":{\"lo\":\"1000000\",\"signScale\":12},\"QuantityUnitCodeType\":\"SharesOrUnits\",\"LeavesQuantity\":{\"lo\":\"1000000\",\"signScale\":12},\"BuySellCode\":\"Sell\",\"Security\":{\"SchwabSecurityID\":\"102003475\",\"Symbol\":\"TSLA  240927C00260000\",\"UnderlyingSymbol\":\"TSLA\",\"MajorAssetType\":\"MajorAssetType_EquityOption\",\"PrimaryMarketSymbol\":\"TSLA  240927C00260000\",\"ShortDescriptionText\":\"TESLA INC 09/27/2024 $260 Call\",\"ShortName\":\"TESLA INC 09/27/2024 $260 Call\",\"CUSIP\":\"0TSLA.IR40260000\",\"OptionsSecurityInfo\":{\"PutCallCode\":\"Call\",\"UnderlyingSchwabSecurityID\":\"1948561409\",\"StrikePrice\":{\"lo\":\"260000000\",\"signScale\":12},\"OptionExpiryDate\":{\"DateTimeString\":\"2024-09-27 00:00:00.000\"}}},\"QuoteOnOrderAcceptance\":{\"Ask\":{\"lo\":\"2740000\",\"signScale\":12},\"AskSize\":{\"lo\":\"15\"},\"Bid\":{\"lo\":\"2720000\",\"signScale\":12},\"BidSize\":{\"lo\":\"12\"},\"QuoteTimestamp\":{\"DateTimeString\":\"2024-09-24 11:02:30.555\"},\"Symbol\":\"TSLA  240927C00260000\",\"QuoteTypeCode\":\"Mark\",\"Mid\":{\"lo\":\"2730000\",\"signScale\":13},\"SchwabOrderID\":\"1001683042944\",\"OptionsQuote\":{\"PutCallCode\":\"Call\"}},\"LegClientRequestInfo\":{\"SecurityId\":\"TSLA  240927C00260000\",\"SecurityIdTypeCd\":\"Symbol\"},\"AccountingRuleCode\":\"Cash\",\"EstimatedNetAmount\":{\"lo\":\"274350000\",\"signScale\":12},\"EstimatedPrincipalAmnt\":{\"lo\":\"275000000\",\"signScale\":12},\"EquityOrderLeg\":{\"EquityOptionsOrderLeg\":{\"OpenClosePositionCode\":\"PC_Close\"}}}],\"OrderCapacityCode\":\"OC_Agency\",\"SettlementType\":\"SettlementType_Regular\",\"Rule80ACode\":73,\"SolicitedCode\":\"Unsolicited\",\"TradeTag\":\"API_TOS:TRADE_ALL\",\"EquityOrder\":{\"TradingSessionCodeOnOrder\":\"REG\"}}}},\"ParentSchwabOrderID\":\"1001683042935\",\"LifecycleSchwabOrderID\":\"1001683042935\"}}}","seq":65,"key":"Account Activity"}]}r"""
    ]
    
    for json_string in testList:
        # Extract the JSON part by removing the timestamp
        
        #find the content
        startingKey = '"3":'
        endingKey = ',"seq":'

        #starting index at 3 where I am looking for the data
        startIndex = json_string.find(startingKey)
        startIndex += len(startingKey)

        #ending index at seq where I am done looking for the data
        endIndex = json_string.find(endingKey)
        endIndex -= len(endingKey)

        for i in range(startIndex, len(json_string)):
            if json_string[i] == '{':
                #start of data
                print(f"{json_string[i:endIndex]}")
                content = json_string[i:endIndex]
                
                #create a function to count up open brackets to add closing ones to the end
                openBrackets = content.count('{')
                closeBrackets = content.count('}')

                missing = openBrackets - closeBrackets
                
                content = content + '}' * missing

                isbalanced = check_balanced_brackets(content)


                data = json.loads(content)
                print(data)
                break
                
                
        

        
        streamer.my_handler(data)
    

def check_balanced_brackets(string):
    stack = []
    
    for char in string:
        if char == '{':
            stack.append(char)  # Push to stack when an open bracket is found
        elif char == '}':
            if not stack:
                return False  # More closing brackets than opening
            stack.pop()  # Pop from stack when a closing bracket is found
    
    # If the stack is empty, all brackets are balanced
    return len(stack) == 0
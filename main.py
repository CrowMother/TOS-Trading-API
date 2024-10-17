import schwabdev #import the package




print("welcome to the Schwab API test Suite")
#links the bot to the client for placing and pulling information
client = schwabdev.Client(<secret key>, <secret key>)  #create a client

#grab the if it it is BTO CTO or other



#start of the main close
def main():
    #send test data
    #test_data.send_test_trade_order()
    
    streamer.set_streamer(client)
    # #streaming of real time account data with 
    target=streamer.start_account_tracking(client)


main()




def set_streamer(client):
    global streamer
    streamer = client.stream
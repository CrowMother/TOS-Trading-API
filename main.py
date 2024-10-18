import schwabdev #import the package



#hit play on this one Josh


print("welcome to the Schwab API test Suite")
#links the bot to the client for placing and pulling information
client = schwabdev.Client("app key", "secret key")  #create a client


#start of the main close
def main():

    streamer.set_streamer(client)
    # #streaming of real time account data with 
    target=streamer.start_account_tracking(client)



def set_streamer(client):
    global streamer
    streamer = client.stream
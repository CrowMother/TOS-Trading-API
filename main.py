import schwabdev #import the package
from Modules import secretkeys
from Modules import universal
from Modules import streamer
import time


print("welcome to the Schwab API test Suite")
#links the bot to the client for placing and pulling information
client = schwabdev.Client(secretkeys.get_app_key(), secretkeys.get_secret())  #create a client

client.update_tokens_auto() #start the auto access token updater
print(client.account_linked().json()) #make api calls 

#start of the main close
def main(client):
    streamer.set_streamer(client)
    #streamer.start_level_one_equity_stream(client)
    streamer.start_account_tracking(client)
    #to do
    #add data streaming to a webserver or another web application to get real time data from client to server
    #
main(client)
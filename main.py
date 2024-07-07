import schwabdev #import the package
from Modules import secretkeys
from Modules import universal

client = schwabdev.Client(secretkeys.get_app_key(), secretkeys.get_secret())  #create a client

client.update_tokens_auto() #start the auto access token updater
print(client.account_linked().json()) #make api calls 


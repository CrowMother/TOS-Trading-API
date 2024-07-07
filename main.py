import schwabdev #import the package
import os
from env import load_dotenv

client = schwabdev.Client('', '')  #create a client

client.update_tokens_auto() #start the auto access token updater

print(client.account_linked().json()) #make api calls

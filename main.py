import schwabdev #import the package
import os
from env import load_dotenv

client = schwabdev.Client('1OfbUtLXOc8AD3yT4445g69TaEBluw3Z', 'wGotKFxzabxR4ZWX')  #create a client

client.update_tokens_auto() #start the auto access token updater

print(client.account_linked().json()) #make api calls
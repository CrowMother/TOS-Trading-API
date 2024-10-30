import schwabdev #import the package
from Modules import secretkeys
from Modules import universal
from datetime import datetime, timedelta
import sqlite3
import json
import time
import threading


order_statuses = [
    "CANCELED", "REPLACED", "FILLED"
]


conn = sqlite3.connect('orders.db')
c = conn.cursor()

# Sample structure for order tracking table
c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    orderId TEXT PRIMARY KEY,
    symbol TEXT,
    orderType TEXT,
    status TEXT,
    enteredTime TEXT,
    filledQuantity REAL,
    is_sent BOOLEAN DEFAULT 0
)
''')


print("welcome to the Schwab API test Suite")
#links the bot to the client for placing and pulling information
client = schwabdev.Client(secretkeys.get_app_key(), secretkeys.get_secret())  #create a client

#grab the if it it is BTO CTO or other

#start of the main close
def main():


    for filter in order_statuses:
        response = fetch_orders_from_last_hour(client, filter)
        #store the data in a file
        print(response)
        universal.write_to_file(response, f"data_{filter}.txt")
        if response:
            filename = f"data_{filter}.json"
            with open(filename, 'w') as file:
                json.dump(response, file, indent=4)
            print(f"Stored JSON data for filter '{filter}' in file '{filename}'")
        else:
            print(f"No data to store for filter '{filter}'")
    


def update_orders(orders):
    new_orders = []
    closed_orders = []
    for order in orders:
        order_id = order['orderId']
        symbol = order['symbol']
        order_type = order['orderType']
        status = order['status']
        entered_time = order['enteredTime']
        filled_quantity = order['filledQuantity']

        # Check if order already exists in the database
        c.execute('SELECT * FROM orders WHERE orderId = ?', (order_id,))
        existing_order = c.fetchone()

        if existing_order:
            # Check for closed orders
            if existing_order[3] != 'CLOSED' and status == 'CLOSED':
                closed_orders.append(order)
                # Perform calculations here if needed
        else:
            # Insert new order
            new_orders.append(order)
            c.execute('''
                INSERT INTO orders (orderId, symbol, orderType, status, enteredTime, filledQuantity)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (order_id, symbol, order_type, status, entered_time, filled_quantity))
    
    # Commit to database
    conn.commit()

    # Send new and closed orders to another server here
    send_orders(new_orders, closed_orders)

def send_orders(new_orders, closed_orders):
    # Replace with actual send logic
    print("Sending new orders:", new_orders)
    print("Sending closed orders:", closed_orders)    



def fetch_orders_from_last_hour(client, filter=None):
    # Get the current date and one week prior
    to_date = datetime.now()
    from_date = to_date - timedelta(hours=1)
    
    
    # Format dates as ISO 8601 strings with milliseconds and timezone
    from_date_str = from_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    to_date_str = to_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    
    
    # Fetch orders within the specified date range for all linked accounts
    response = client.account_orders_all( 
        from_date_str,
        to_date_str,
        None,# Optional: set to limit number of result
        filter    # Optional: filter by status
    )
    if response.status_code == 200:
        # Parse the JSON content
        orders = response.json()
        return orders
    
    return response


main()
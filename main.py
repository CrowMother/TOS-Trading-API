import schwabdev #import the package
from Modules import secretkeys
from Modules import universal
from datetime import datetime, timedelta
import sqlite3
import json
import time
import threading


order_status = "FILLED"


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

    #fetch orders from last hour
    response = fetch_orders_from_last_hour(client, order_status)
    #store the data in a file
    print(response)
    #universal.write_to_file(response, f"data_{order_status}.txt")
    if response:
        filename = f"data_{order_status}.json"
        with open(filename, 'w') as file:
            json.dump(response, file, indent=4)
        print(f"Stored JSON data for filter '{order_status}' in file '{filename}'")
        #update the database
        update_orders(response)
    else:
        print(f"No data to store for filter '{order_status}'")
    
    


def update_orders(orders):
    if not orders:
        return

    new_orders = []
    closed_orders = []
    for order in orders:
        order_id = order['orderId']
        symbol = order['orderLegCollection'][0]['instrument']['symbol'] if 'orderLegCollection' in order else None
        order_type = order['orderType']
        status = order['status']
        entered_time = order['enteredTime']
        filled_quantity = order['filledQuantity']

        # Check if order already exists in the database
        c.execute('SELECT * FROM orders WHERE orderId = ?', (order_id,))
        existing_order = c.fetchone()

        if existing_order:
            # Update the existing order if status changes to closed
            if existing_order[3] != 'CLOSED' and status == 'CLOSED':
                closed_orders.append(order)
                c.execute('''
                    UPDATE orders 
                    SET status = ?, filledQuantity = ?, is_sent = 0
                    WHERE orderId = ?
                ''', (status, filled_quantity, order_id))
        else:
            # Insert new order
            new_orders.append(order)
            c.execute('''
                INSERT INTO orders (orderId, symbol, orderType, status, enteredTime, filledQuantity)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (order_id, symbol, order_type, status, entered_time, filled_quantity))
    
    # Commit changes to database
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
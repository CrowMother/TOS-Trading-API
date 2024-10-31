import schwabdev  # Import the package
from Modules import secretkeys
from Modules import universal
from datetime import datetime, timedelta, timezone
import sqlite3
import json
import time
import threading

order_status = "FILLED"

# Connect to SQLite database
conn = sqlite3.connect('orders.db')
c = conn.cursor()

# Updated structure for order tracking table to include new fields
c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    orderId TEXT PRIMARY KEY,
    underlyingSymbol TEXT,
    orderType TEXT,
    status TEXT,
    enteredTime TEXT,
    filledQuantity REAL,
    description TEXT,
    price REAL,
    putCall TEXT,
    instruction TEXT,
    accountNumber TEXT,
    is_sent BOOLEAN DEFAULT 0
)
''')

print("Welcome to the Schwab API test Suite")

# Link the bot to the client for placing and pulling information
client = schwabdev.Client(secretkeys.get_app_key(), secretkeys.get_secret())  # Create a client

def main():
    # Fetch orders from the last hour
    response = fetch_orders_from_last_hour(client, order_status)
    
    # Store the data in a JSON file
    if response:
        filename = f"data_{order_status}.json"
        with open(filename, 'w') as file:
            json.dump(response, file, indent=4)
        print(f"Stored JSON data for filter '{order_status}' in file '{filename}'")
        # Update the database
        update_orders(response)
    else:
        print(f"No data to store for filter '{order_status}'")

def update_orders(orders):
    if not orders:
        return

    new_orders = []
    closed_orders = []
    for order in orders:
        # Extracting required fields with defaults if fields are missing
        order_id = order['orderId']
        underlying_symbol = order['orderLegCollection'][0]['instrument'].get('underlyingSymbol') if 'orderLegCollection' in order and 'instrument' in order['orderLegCollection'][0] else None
        order_type = order['orderType']
        status = order['status']
        entered_time = order['enteredTime']
        filled_quantity = order['filledQuantity']
        description = order['orderLegCollection'][0]['instrument'].get('description') if 'orderLegCollection' in order and 'instrument' in order['orderLegCollection'][0] else None
        price = order.get('price', None)
        put_call = order['orderLegCollection'][0]['instrument'].get('putcall') if 'orderLegCollection' in order and 'instrument' in order['orderLegCollection'][0] else None
        instruction = order['orderLegCollection'][0].get('instruction', None) if 'orderLegCollection' in order else None
        account_number = order.get('accountNumber', None)

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
    INSERT INTO orders (
        orderId,
        underlyingSymbol,
        orderType,
        status,
        enteredTime,
        filledQuantity,
        description,
        price,
        putCall,
        instruction,
        accountNumber,
        is_sent
    )
    VALUES (
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        0
    )
''', (
    order_id,
    underlying_symbol,
    order_type,
    status,
    entered_time,
    filled_quantity,
    description,
    price,
    put_call,
    instruction,
    account_number
))
    
    # Commit changes to database
    conn.commit()

    # Send new and closed orders to another server here
    send_orders(new_orders, closed_orders)

def send_orders(new_orders, closed_orders):
    # Replace with actual send logic
    print("Sending new orders:", new_orders)
    print("Sending closed orders:", closed_orders)

def fetch_orders_from_last_hour(client, filter=None):
    # Get the current date and one hour prior
    to_date = datetime.now(timezone.utc)
    from_date = to_date - timedelta(hours=1)
    
    # Format dates as ISO 8601 strings with milliseconds and timezone
    from_date_str = from_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    to_date_str = to_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    
    # Fetch orders within the specified date range for all linked accounts
    response = client.account_orders_all( 
        from_date_str,
        to_date_str,
        None,  # Optional: set to limit number of results    
        filter # Optional: Filter by status
    )
    
    if response.status_code == 200:
        # Parse the JSON content
        orders = response.json()
        return orders
    
    return response

# Run the main function
main()

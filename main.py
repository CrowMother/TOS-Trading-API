import schwabdev  # Import the package
from Modules import secretkeys
from Modules import universal
from Modules import webhook
from datetime import datetime, timedelta, timezone

import re
import sqlite3
import json
import time
import threading

order_status = "FILLED"

# Connect to SQLite database
conn = sqlite3.connect('orders.db')
c = conn.cursor()


# Create orders table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS archive (
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
    quantity REAL,
    accountNumber TEXT
)
''')

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
    quantity REAL,
    accountNumber TEXT
)
''')

print("Welcome to the Schwab API test Suite")

# Link the bot to the client for placing and pulling information
client = schwabdev.Client(secretkeys.get_app_key(), secretkeys.get_secret())  # Create a client

def main():
    while True:
        try:
            # Fetch orders from the last hour
            response = fetch_orders_from_last_hour(client, order_status)
            
            # Store the data in a JSON file
            if response:
                #if the response is not empty then update the orders
                update_orders(response)

                # send orders that are in the database
                send_orders()

            #else:
                #print(f"No data to store for filter '{order_status}'")
        except Exception as e:
            print(f"Error(rebooting...): {e}")
            break
        time.sleep(5)


def update_orders(orders):
    if not orders:
        return

    new_orders = []
    closed_orders = []
    for order in orders:
        # Extracting required fields with defaults if fields are missing
        order_id = order['orderId']
        #check if orderID is in the archive table
        c.execute('SELECT 1 FROM archive WHERE orderId = ?', (order_id,))
        if c.fetchone():
            print(f"Order {order_id} already exists in archive. Skipping insert into orders.")
            continue  # Skip to the next order if it exists in archived_orders

        # Extracting required fields
        underlying_symbol = order['orderLegCollection'][0]['instrument'].get('underlyingSymbol') if 'orderLegCollection' in order and 'instrument' in order['orderLegCollection'][0] else None
        order_type = order['orderType']
        status = order['status']
        entered_time = order['enteredTime']
        filled_quantity = order['filledQuantity']
        description = order['orderLegCollection'][0]['instrument'].get('description') if 'orderLegCollection' in order and 'instrument' in order['orderLegCollection'][0] else None
        price = order.get('price', None)
        put_call = order['orderLegCollection'][0]['instrument'].get('putCall') if 'orderLegCollection' in order and 'instrument' in order['orderLegCollection'][0] else None
        instruction = order['orderLegCollection'][0].get('instruction', None) if 'orderLegCollection' in order else None
        account_number = order.get('accountNumber', None)
        quantity = order.get('quantity', None)

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
        quantity,
        accountNumber
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
        ?
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
    quantity,
    account_number
))
    
    # Commit changes to database
    conn.commit()

def send_orders( ):
    # pull order from database
    c.execute('SELECT * FROM orders')
    orders = c.fetchall()
    try:
        for order in orders:
            order_id, underlying_symbol, order_type, status, entered_time, filled_quantity, description, price, put_call, instruction, quantity, account_number = load_data_from_db(order)

            #format message
            if description is None:
                continue
            date, strike = format_description(description)

            #check for closing data (gain loss)
            gain_loss_percentage = gain_loss(description, price, instruction)

            #create generic function to check if closing position
            quantity_string = ""
            quantity_string = check_if_partial_close(instruction, quantity, description)
                        
            #format data into json
            data = format_data(order_id, underlying_symbol, order_type, status, entered_time, filled_quantity, date, strike, price, put_call, instruction, account_number, gain_loss_percentage, quantity_string)

            

            # send webhook
            returnValue = webhook.webhookout(data)

            #move order to sent
            if returnValue == "OK":
                move_order_to_archive(order_id)

    except Exception as e:
        print(f"Error: {e}")


def load_data_from_db(order):
    order_id = order[0]
    underlying_symbol = order[1]
    order_type = order[2]
    status = order[3]
    entered_time = order[4]
    filled_quantity = order[5]
    description = order[6]
    price = order[7]
    put_call = order[8]
    instruction = order[9]
    quantity = order[10]
    account_number = order[11]
    return order_id, underlying_symbol, order_type, status, entered_time, filled_quantity, description, price, put_call, instruction, quantity, account_number

def check_if_partial_close(instruction, quantity, description):
    if instruction == "BUY_TO_CLOSE" or instruction == "SELL_TO_CLOSE":
                print(quantity)
                #if the quantity is greater than the original quantity
                c.execute('''
                    SELECT *
                    FROM archive
                    WHERE description = ?
                    AND instruction IN ('BUY_TO_OPEN', 'SELL_TO_OPEN')
                    ORDER BY enteredTime ASC
                ''', (description,))
                matched = c.fetchone()
                if matched:
                    original_quantity = matched[10]
                    if quantity < original_quantity:
                        return "Partial Close"
                    else:
                        return "Full Close"


def format_data(order_id, underlying_symbol, order_type, status, entered_time, filled_quantity, date, strike, price, put_call, instruction, account_number, gain_loss_percentage, quantity_string):
    data = {
        "order_id": order_id,
        "underlying_symbol": underlying_symbol,
        "order_type": order_type,
        "status": status,
        "entered_time": entered_time,
        "filled_quantity": filled_quantity,
        "date": date,
        "strike": strike,
        "price": price,
        "put_call": put_call,
        "instruction": instruction,
        "account_number": account_number,
        "gain_loss_percentage": gain_loss_percentage,
        "quantity_string": quantity_string
        }
    return data

def gain_loss(description, price, instruction):
    #modify the order to be ascending to get the original price
    c.execute('''
        SELECT *
        FROM archive
        WHERE description = ?
        AND instruction IN ('BUY_TO_OPEN', 'SELL_TO_OPEN')
        ORDER BY enteredTime ASC
        LIMIT 1
    ''', (description,))
    matched = c.fetchone()

    gain_loss_percentage = 0
    if matched and (instruction == 'SELL_TO_CLOSE' or instruction == 'BUY_TO_CLOSE'):
        #calculate if gain or loss
        Original_price = matched[7]
        if Original_price > price:
            gain_loss_percentage = round((Original_price - price) / Original_price * 100, 2)
            gain_loss_percentage = -1 * gain_loss_percentage
        else:
            gain_loss_percentage = round((price - Original_price) / Original_price * 100, 2)
        return gain_loss_percentage
    else:
        return None

#format description
def format_description(description):
    match = re.search(r'(\d{2}/\d{2}/\d{4})\s+\$(\d+)', description)

    if match:
        date = match.group(1)  # Extracted date
        price = match.group(2)  # Extracted price
        return date, price
    else:
        return "", ""

def move_order_to_archive(order_id):
    # Insert the entry into sent
    c.execute('''
        INSERT INTO archive (
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
            quantity,
            accountNumber
        )
        SELECT
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
            quantity,
            accountNumber
        FROM orders
        WHERE orderId = ?
    ''', (order_id,))

    # Delete the entry from the orders table
    c.execute('DELETE FROM orders WHERE orderId = ?', (order_id,))

    # Commit the transaction
    conn.commit()

def fetch_orders_from_last_hour(client, filter=None):
    # Get the current date and one hour prior
    to_date = datetime.now(timezone.utc)
    from_date = to_date - timedelta(hours=240)
    
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

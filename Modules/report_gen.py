"""
This script pulls account data from the Schwab client using the provided client instance and two timestamps.
It retrieves the data, sorts and formats it, and then stores the formatted data in a Google Sheets document.

Functions:
    - fetch_account_data(client): Fetches account data from the Schwab client within the specified time range.
    - create time range(start_timestamp, end_timestamp): Creates a time range from the start and end timestamps.
    - sort_and_format_data(data): Sorts and formats the fetched account data.
    - store_data_in_google_sheets(formatted_data, sheet_id): Stores the formatted data in the specified Google Sheets document.
"""

import re
import logging
import datetime

import gsheet
import data_sort

import universal
import secretkeys
from data_sort import get_all_order_details


SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']



def generate_report(SchwabClient, worksheet):
    """
    Generates a report of the account data from the Schwab client within the specified time range.

    Args:
        client: The Schwab client instance.
        start_timestamp: The start timestamp for the time range.
        end_timestamp: The end timestamp for the time range.

    Returns:
        None
    """
    # fetch the account data from the last week
    data = universal.fetch_orders_from_time_frame(SchwabClient, "FILLED", 168)

    # function call to group the data by opening and closing positions
    formatted_data = group_and_format_data(data)
    # formatted_data = [get_all_order_details(order) for order in data]


    # store the data in Google Sheets
    row = gsheet.get_next_empty_row(worksheet, 2)
    gsheet.copy_headers(worksheet, f"A{row}")
    for data in formatted_data:
        row = gsheet.get_next_empty_row(worksheet, 2)
        row_data = [
            '',
            str(data.get('underlying_symbol', '')),
            str(data.get('expiration_date', '')),
            str(data.get('contract', '')),
            str(data.get('open_price', '')),
            str(data.get('close_price', ''))
        ]
        logging.info(f"Inserting data at row {row}: {row_data}")
        gsheet.insert_data(worksheet, f"A{row}", [row_data])

def group_and_format_data(data):
    """
    Sorts and formats the fetched account data.

    Args:
        data: The fetched account data.

    Returns:
        The sorted and formatted account data.
    """
    grouped_data = group_data(data)
    
    return grouped_data

def format_gsheet_data(data):
    #for each order look for the opening position and the closing position
    #if multiple opens or closes, then pick the highest and lowest respectively
    for order in data:
        logging.info(f"Formatted data: {order}")
        return order

def group_data(data):
    """
    Groups the fetched account data by opening and closing positions.
    """

    #search data for a matching description
    grouped_data_set = []
    # group the data by opening and closing positions
    #print(data)
    for order in data:
        description = data_sort.get_description(order)
        #search for the other side of the trade
        #if the order is a buy, then look for a sell
        if data_sort.get_instruction(order) == "BUY_TO_OPEN" or data_sort.get_instruction(order) == "SELL_TO_OPEN":
            for second_order in data:
                if data_sort.get_instruction(second_order) == "BUY_TO_CLOSE" or data_sort.get_instruction(second_order) == "SELL_TO_CLOSE":
                    if data_sort.get_description(second_order) == description:
                        grouped_data = fill_grouped_data(order, second_order)
                        grouped_data_set.append(grouped_data)
                        print("Matched")
    return grouped_data_set

        #if the order is a sell, then look for a buy
            
        # find data for matching description


def fill_grouped_data(order1, order2):
    """
    Fills the grouped data with the required details.
    """
    data_group = {}
    data_group['underlying_symbol'] = data_sort.get_underlying_symbol(order1)
    data_group['description'] = data_sort.get_description(order1)
    data_group['open_price'] = data_sort.get_price(order1)
    data_group['close_price'] = data_sort.get_price(order2)
    data_group['expiration_date'] = get_expiration_date(data_sort.get_description(order1))
    data_group['contract'] = get_contract(data_sort.get_description(order1))
    
    return data_group
    

def get_expiration_date(description):
    """
    Extracts the expiration date from the description.

    Args:
        description: The description string containing the expiration date.

    Returns:
        The expiration date as a datetime object.
    """
    # Regular expression to match the date in the format MM/DD/YYYY
    date_pattern = re.compile(r'\b(\d{2}/\d{2}/\d{4})\b')
    match = date_pattern.search(description)
    if match:
        date_str = match.group(1)
        logging.info(f"Expiration date found: {date_str}")
        return date_str
    else:
        logging.warning(f"No expiration date found in description: {description}")
        return None
    
def get_contract(description):
    """
    Extracts the contract details from the description.

    Args:
        description: The description string containing the contract details.

    Returns:
        The contract details.
    """
    # Regular expression to match the price and call/put symbols
    contract_pattern = re.compile(r'\$\d+\s(?:Call|Put)')
    match = contract_pattern.search(description)
    if match:
        contract = match.group(0)
        logging.info(f"Contract found: {contract}")
        return contract
    else:
        logging.warning(f"No contract found in description: {description}")
        return None

if __name__ == '__main__':
    SchwabClient = universal.create_client()
    Gclient = gsheet.connect_gsheets_account(secretkeys.get_a_secret("GOOGLE_SHEET_CREDS"))
    worksheet = gsheet.connect_to_sheet(Gclient, "NBT Performance Tracker", "Sheet1")
    generate_report(SchwabClient, worksheet)
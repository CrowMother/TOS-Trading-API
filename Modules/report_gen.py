"""
This script pulls account data from the Schwab client using the provided client instance and two timestamps.
It retrieves the data, sorts and formats it, and then stores the formatted data in a Google Sheets document.

Functions:
    - fetch_account_data(client): Fetches account data from the Schwab client within the specified time range.
    - create time range(start_timestamp, end_timestamp): Creates a time range from the start and end timestamps.
    - sort_and_format_data(data): Sorts and formats the fetched account data.
    - store_data_in_google_sheets(formatted_data, sheet_id): Stores the formatted data in the specified Google Sheets document.
"""

import gsheet
import logging

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

    # sort and format the data
    formatted_data = [get_all_order_details(order) for order in data]
    for order in formatted_data:
        logging.info(f"Formatted data: {order}")
        

    logging.info(f"Formatted data: {formatted_data}")

    # store the data in Google Sheets
    row = gsheet.get_next_empty_row(worksheet, 2)
    gsheet.copy_headers(worksheet, f"A{row}")
    for data in formatted_data:
        row = gsheet.get_next_empty_row(worksheet, 2)
        row_data = [
            '',
            str(data.get('underlying_symbol', '')),
            str(data.get('description', '')),
            str(data.get('price', '')),
            str(data.get('price', ''))
        ]
        logging.info(f"Inserting data at row {row}: {row_data}")
        gsheet.insert_data(worksheet, f"A{row}", [row_data])

    


if __name__ == '__main__':
    SchwabClient = universal.create_client()
    Gclient = gsheet.connect_gsheets_account(secretkeys.get_a_secret("GOOGLE_SHEET_CREDS"))
    worksheet = gsheet.connect_to_sheet(Gclient, "NBT Performance Tracker", "Sheet1")
    generate_report(SchwabClient, worksheet)
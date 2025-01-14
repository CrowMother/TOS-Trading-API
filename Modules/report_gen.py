"""
This script pulls account data from the Schwab client using the provided client instance and two timestamps.
It retrieves the data, sorts and formats it, and then stores the formatted data in a Google Sheets document.

Functions:
    - fetch_account_data(client): Fetches account data from the Schwab client within the specified time range.
    - create time range(start_timestamp, end_timestamp): Creates a time range from the start and end timestamps.
    - sort_and_format_data(data): Sorts and formats the fetched account data.
    - store_data_in_google_sheets(formatted_data, sheet_id): Stores the formatted data in the specified Google Sheets document.
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

import universal
from data_sort import get_all_order_details


SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

def generate_report(client):
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
    data = universal.fetch_orders_from_time_frame(client, "FILLED", 168)

    # sort and format the data
    formatted_data = [get_all_order_details(order) for order in data]
    print(formatted_data)

    


if __name__ == '__main__':
    client = universal.create_client()
    generate_report(client)
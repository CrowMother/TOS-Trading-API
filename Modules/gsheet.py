import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the scope for accessing Google Sheets and Drive
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']


def gsheetTest(worksheet):
    try:
        # Fetch the header row
        logging.info("Fetching header row from Google Sheet")
        headers = worksheet.row_values(1)
        logging.info(f"Headers: {headers}")

        # Fetch data into a Pandas DataFrame
        logging.info("Fetching data from Google Sheet")
        data = worksheet.get_all_records(expected_headers=headers)
        df = pd.DataFrame(data)
        logging.info(f"Data fetched: {df}")

        # Write new data to Google Sheet
        logging.info("Updating Google Sheet with new data")
        new_data = [
            ['Week', 'Ticker'],
            ['1/16/25', 'QQQ'],
            ['', "AAPL"],
        ]
        logging.info("Attempting to update Google Sheet")
        worksheet.update('A1', new_data)
        logging.info("Google Sheet updated successfully")

    except gspread.exceptions.APIError as e:
        logging.error(f"API error occurred: {e.response.text}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def insert_data(worksheet, location, data):
    try:
        logging.info("Attempting to update Google Sheet")
        worksheet.update(location, data)
        logging.info("Google Sheet updated successfully")
    except gspread.exceptions.APIError as e:
        logging.error(f"API error occurred: {e.response.text}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def get_next_empty_row(worksheet, column):
    try:
        # Fetch all values in the specified column
        values = worksheet.col_values(column)
        logging.info(f"Values in column {column}: {values}")

        # Find the index of the first empty cell in the column
        empty_index = len(values) + 1
        logging.info(f"Next empty row in column {column}: {empty_index}")
        return empty_index
    except Exception as e:
        logging.error(f"An error occurred while getting the next empty row: {e}")
        return None

def get_all_records(worksheet):
    try:
        # Fetch the header row
        logging.info("Fetching header row from Google Sheet")
        headers = worksheet.row_values(1)
        logging.info(f"Headers: {headers}")

        # Fetch data into a Pandas DataFrame
        logging.info("Fetching data from Google Sheet")
        data = worksheet.get_all_records(expected_headers=headers)
        df = pd.DataFrame(data)
        logging.info(f"Data fetched:\n{df}")
        return df
    except gspread.exceptions.APIError as e:
        logging.error(f"API error occurred: {e.response.text}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def test_file(file_path):
    if os.path.isfile(file_path):
        print("File exists")
    else:
        print("File does not exist")

def connect_gsheets_account(file_path):
    try:
        # Authenticate using the service account key file
        logging.info("Authenticating with Google Sheets API")
        credentials = Credentials.from_service_account_file(
            file_path, scopes=SCOPES)
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def copy_headers(worksheet, location):
    # Use the inbuilt gsheet function to set the value at a given row and column to the headers
    # Example A17 [=A1, =B1, ...]
    try:
        worksheet.update(
        location,
        [
            ['=A1', '=B1', '=C1', '=D1', '=E1', '=F1', '=G1', '=H1', '=I1', '=J1']
        ],
        value_input_option='USER_ENTERED'
    )
    except gspread.exceptions.APIError as e:
        logging.error(f"API error occurred: {e.response.text}")


def connect_to_sheet(client, spreadsheet_name, worksheet_name):
    try:
        # Open the Google Sheet
        logging.info("Opening Google Sheet")
        spreadsheet = client.open(spreadsheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        return worksheet
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    # Modify the file path to be dynamic based on the environment or configuration
    file_path = r'd:\coding stuff\TOS-Trading-API\weekly-reports-bot.json'
    test_file(file_path)
    client = connect_gsheets_account(file_path)
    worksheet = connect_to_sheet(client, "NBT Performance Tracker", "Sheet1")
    copy_headers(worksheet, 'A18')
    #test insert data
    insert_data(worksheet, 'A5', [['Week', 'Ticker', 'Exp.', 'Contract', 'Entry', 'Max Exit / Stop Price', 'Max Exit / Stop Price Percentage','Win / Loss', 'Notes'], ['1/17/25', 'QQQ1'], ['1/17/25', 'AAPL', '1/19/2025', '1.00C', '1.00', '2.00']])
    #test get_next_empty_row
    get_next_empty_row(worksheet, 2)

    

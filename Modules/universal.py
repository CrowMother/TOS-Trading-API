import datetime
import schwabdev
import secretkeys

from datetime import datetime, timezone, timedelta

#red error codes
def error_code(text):
    print_combined("[ERROR]:", text, "31")

#green Okay
def okay_code(text):
    print_combined("[OKAY]:", text, "32")

#yellow warnings
def warning_code(text):
    print_combined("[WARNING]:", text, "33")

#prints frist part colored and second normal
def print_combined(colored_text, non_colored_text, color_code):
    reset_code = "\033[0m"
    colored_text = f"\033[{color_code}m{colored_text}\033[0m"
    print(colored_text + non_colored_text)

#prints in one color for the whole message
def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033]")

def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')



#reading configuration file for setting variables

def split_string_at_char(inputString, splitChar, SectionNum):
    try:
        splitSections = str(inputString).split(splitChar)
        if len(splitSections) > SectionNum:
            return splitSections[SectionNum]
        else:
            return ""
    except ValueError as e:
        error_code(f"Value unable to be split and or returned:{str(inputString)}. Error : {str(e)}")


def create_client():
    client = schwabdev.Client(secretkeys.get_app_key(), secretkeys.get_secret())  # Create a client
    return client

#write to file
def write_to_file(data, fileName="data.txt"):
    with open(fileName, 'w') as f:
        f.write(str(data))


def fetch_orders_from_time_frame(client, filter=None, hours_ago=1):
    # Get the current date and one hour prior
    to_date = datetime.now(timezone.utc)
    from_date = to_date - timedelta(hours=hours_ago)
    
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
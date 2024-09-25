import datetime

def write_to_log(log_message):
    log_file='logfile.txt'
    """
    Write a string message to a log file with a timestamp.

    Args:
        log_message (str): The message to write to the log file.
        log_file (str): The path to the log file (default is 'logfile.txt').
    """
    with open(log_file, 'a') as file:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f'{log_message}\n')
        print(f"Data logged:\n{log_message}")


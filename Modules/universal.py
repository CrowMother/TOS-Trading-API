import datetime

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

def time_stamp():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
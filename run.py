# Import packages
import gspread
from google.oauth2.service_account import Credentials

# APIs to access in order for the program to run
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Your-PT-Friend')

clients_init_conditions = SHEET.worksheet('clients_initial_conditions')
clients_progress = SHEET.worksheet('clients_progress')


def start_program():
    """
    Welcomes the PT and asks what action needs to be taken:
    -Adding a new client
    -Checking an existing client's progress
    -Deleting a client from the records
    """
    print("Welcome! How can I help you today?\n")
    print("Choose an option between the following:")
    print("1. Add a new client")
    print("2. Check a client's progress")
    print("3. Say goodbye to a client")

    option = (input("Insert a number from the above options (1, 2 or 3):\n"))
    
    if task_validation(option):
        choice = int(option)

        if choice == 1:
            add_new_client()
        elif choice == 2:
            check_progress()
        else:
            delete_client()

    
def task_validation(choice):
    """
    Inside the try, convert the chosen option into an integer.
    Raises a value error if the string can't be converted into an integer
    or if the choice is not 1, 2 or 3.
    """
    try:
        task = int(choice)
        if (task != 1) and (task != 2) and (task != 3):
            raise ValueError(
                f"{task} is not a valid option!"
                )
    except ValueError as e:
        print(
            f"Invalid data: {e}. Please choose an option between 1, 2 or 3."
            )
        return False

    return True


def add_new_client():
    print("Going to the new client page")


def check_progress():
    print("Going to the check progress page")


def delete_client():
    print("Going to delete client page")


start_program()
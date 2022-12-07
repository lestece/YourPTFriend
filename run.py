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


def is_empty_string(data):
    """
    Checks that the inputted data is not an empty string.
    """
    try:
        if data == "":
            raise ValueError("You need to provide the requested information!")
    except ValueError as e:
        print(f"Invalid data: {e}")
        return True
    return False


def add_new_client():
    """
    Takes the client data as input
    """
    print("You're adding a new client! Insert the following information.\n")
    # Input name
    while True: 
        name = input("Full name:")
        # Checks that the inputted name is not blank space
        if is_empty_string(name):
            print("Please insert client's name.")
            continue
        # Checks if the name is already in the records
        elif clients_init_conditions.find(name):
            print("There's already another client registered with the same name.")
            print("Please provide an extra identification for this client")
            print("so that he/she can be discerned.")
            continue
        else:
            while True:
                gender = input("Gender(F or M):")
                # Checks that the inputted gender is not blank space
                if is_empty_string(gender):
                    print("Please insert client's gender.")
                    continue
                # Makes sure the gender is either F or M
                elif (gender.upper() != 'F') and (gender.upper() != 'M'):
                    print("Please answer with either 'F' or 'M'")
                    continue
                else:
                    while True:
                        age = input("Age:")
                        # Checks that the inputted age is not blank space
                        if is_empty_string(age):
                            print("Please insert client's age.")
                            continue
                        # Checks that the insterted age is a number
                        elif not age.isnumeric():
                            print("Inserted age needs to be a number.")
                            continue
                        # Makes sure the age is a realistic value
                        elif (int(age) < 14) or (int(age) > 100):
                            print("Please insert a valid age.")
                            continue
                        else:
                            while True:
                                height = input("Height(cm):")
                                # Checks that the inputted height is not blank space
                                if is_empty_string(height):
                                    print("Please insert client's height.")
                                    continue
                                # Checks that the insterted height is a number
                                elif not height.isnumeric():
                                    print("Inserted height needs to be a number.")
                                    continue
                                # Makes sure the height is in cm and not feet
                                # Also checks that the inserted height is realistic
                                # Takes into account the heights of shortest and tallest people in the world
                                elif (int(height) < 63) or (int(height) > 272):
                                    print("Please insert a valid height in cm.")
                                    print("Example: 167")
                                    continue
                                else:
                                    while True:
                                        weight = input("Weight(kg):")
                                        # Checks that the inputted weight is not blank space
                                        if is_empty_string(weight):
                                            print("Please insert client's weight.")
                                            continue
                                        # Checks that the inserted weight is a number
                                        elif not weight.isnumeric():
                                            print("Inserted weight needs to be a number.")
                                            continue
                                        # Makes sure the weight insterted is realistic
                                        # Takes into account the weights of heaviest and lightest people in the world
                                        elif (int(weight) < 24) or (int(weight) > 635):
                                            print("Please insert a valid weight in kg.")
                                            print("Example: 87")
                                            continue
                                        else:
                                            while True:
                                                print("For the following requested information, choose one of the following:")
                                                print("Sedentary: SED")
                                                print("Lightly active: LA")
                                                print("Moderately active: MA")
                                                print("Very active: VA")
                                                print("Extremely active: EA")
                                                activity = input("Activity level:")
                                                body_fat = input("Body fat (Do not type %, example: 12):")
                                                print("Now, what's the client's main goal?")
                                                print("A. Weight maintenance")
                                                print("B. Weight loss / cutting")
                                                print("C. Weight gain / bulking")
                                                goal = input("Goal (A, B or C):")


def check_progress():
    print("Going to the check progress page")


def delete_client():
    print("Going to delete client page")


start_program()
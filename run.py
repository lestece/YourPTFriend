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

clients_init_conditions = SHEET.worksheet('clients initial conditions')
clients_progress = SHEET.worksheet('clients progress')


class Client:
    """
    Client class
    """
    def __init__(self, name, gender, age, height, weight, activity, 
                 body_fat, goal):
        self.name = name
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight
        self.activity = activity
        self.body_fat = body_fat
        self.goal = goal

    def client_description(self):
        return (
            f"{self.name} is a {self.age} years old {self.gender} client,"
            f"{self.height} tall and that weights {self.weight}."
            f"Taking into account that the client's activity level is {self.activity},"
            f"body fat is {self.body_fat} %, tdee is ... and the goal is to {self.goal},"
            f"the estimated daily calorie intake is..."
        )


def start_program():
    """
    Welcomes the PT and asks what action needs to be taken:
    -Adding a new client
    -Checking an existing client's progress
    -Deleting a client from the records
    """
    print("Welcome! How can I help you today?\n"
          "Choose an option between the following:\n"
          "1. Add a new client\n"
          "2. Check a client's progress\n"
          "3. Say goodbye to a client\n")

    option = (input("Insert a number from the above options (1, 2 or 3):\n"))
    
    if task_validation(option):
        choice = int(option)

        if choice == 1:
            take_client_data()
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


def translate_activity_factor(activity_level):
    """
    Assigns the corresponding activity factor to the 
    activity level inserted by the user
    """
    activity_factor = ""

    if activity_level == "SED":
        activity_factor = 1.2
    elif activity_level == "LA":
        activity_factor = 1.375
    elif activity_level == "MA":
        activity_factor = 1.55
    elif activity_level == "VA":
        activity_factor = 1.725
    else:
        activity_factor = 1.9
    
    return activity_factor


def update_new_client_worksheet(data):
    """
    Receives a list containing data to insert 
    in the relevant worksheet
    """
    client_dict = data.__dict__
    client_list = list(client_dict.values())
    print("Updating clients records...")
    clients_init_conditions.append_row(client_list)
    print("New client correctly insterted in your clients records!")


def take_client_data():
    """
    Takes the client data as input.
    After input validation, the data is inserted in a new_client list.
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
            break
           
    # Input gender
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
            break
    # Input age
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
            break

    # Input height
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
            break

    # Input weight
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
            break

    # Input activity level
    while True:
        print("Sedentary: SED")
        print("Lightly active: LA")
        print("Moderately active: MA")
        print("Very active: VA")
        print("Extremely active: EA")
        activity = input("Activity level:")
        # Checks that the inputted activity level is not blank space
        if is_empty_string(activity):
            print("Please insert client's activity level.")
            continue
        # Checks that the inserted activity level is valid
        elif (
            (activity.upper() != 'SED') and
            (activity.upper() != 'LA') and
            (activity.upper() != 'MA') and
            (activity.upper() != 'VA') and
            (activity.upper() != 'EA')
             ):
            print("Please choose a valid activity level from the options provided.")
            continue
        else:
            activity_factor = translate_activity_factor(activity.upper())
            break

    # Input body fat percentage
    while True:
        body_fat = input("Body fat (Do not type %, example: 12): %")
        # Checks that the inputted body fat % is not an empty string
        if is_empty_string(body_fat):
            print("Please insert client's body fat %.")
            continue
        # Makes sure the insterted body fat percentage is a number
        elif not body_fat.isnumeric():
            print("Body fat percentage needs to be a numeric value.\n Example: 22")
            continue
        # Checks that the inserted body fat percentage is realistic
        elif (int(body_fat) < 5) or (int(body_fat) > 40):
            print("Please insert a correct body fat percentage.")
            continue
        else:
            break

    # Input client's goal
    print("Now, what's the client's main goal?")
    while True:
        print("A. Weight maintenance")
        print("B. Weight loss / cutting")
        print("C. Weight gain / bulking")
        goal_letter = input("Goal (A, B or C):")
        goal_capitalize = goal_letter.upper()
        # Checks that the inputted goal is not an empty string
        if is_empty_string(goal_capitalize):
            print("Please insert client's goal")
            continue
        # Checks that the inserted goal is one of the available options
        elif (goal_capitalize != 'A') and (goal_capitalize != 'B') and (goal_capitalize != 'C'):
            print("Please choose one of the available options.")
            continue
        else:
            goal = ""
            if goal_capitalize == 'A':
                goal = 'maintain weight'
            elif goal_capitalize == 'B':
                goal = 'lose weight'
            else:
                goal = 'gain weight'
            break
    
    new_client = Client(name, gender, age, height, weight, activity_factor, body_fat, goal) 
    check_new_client_data(new_client)


def check_new_client_data(client_data):
    """
    Checks that the inserted client data is correct and
    there's no errors.
    """
    print(
        f"The details of the new client are as follows:"
        f"{client_data.client_description()}"
    ) 

    while True:
        correct = input("Is client data correct? (y/n):")
        if correct.lower() == 'y':
            update_new_client_worksheet(client_data)
        elif correct.lower() == 'n':
            print("Please reinstert the new client data!")
            take_client_data()
        else:
            print("Please answer with yes or no.")
            continue


def check_progress():
    print("Going to the check progress page")


def delete_client():
    print("Going to delete client page")


start_program()
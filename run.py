# # Import packages
import gspread
from google.oauth2.service_account import Credentials

import tdee_formulas

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
                 body_fat, goal, tdee):
        self.name = name
        self.gender = gender
        self.age = age
        self.height = height
        self.weight = weight
        self.activity = activity
        self.body_fat = body_fat
        self.goal = goal
        self.tdee = tdee

    def client_description(self):
        return (
            f"{self.name} is a {self.age} years old {self.gender} client, "
            f"{self.height} tall and that weights {self.weight}. "
            f"Taking into account that the client's activity level is "
            f"{self.activity}, body fat is {self.body_fat} %, tdee is "
            f"{self.tdee} and the goal is to {self.goal}."
        )


def task(option):
    """
    Based on the user inputted choice, 
    it calls the relevant function connected
    to the task.
    """
    if task_validation(option):
        choice = int(option)

        if choice == 1:
            take_client_data()
        elif choice == 2:
            check_progress()
        elif choice == 3:
            delete_client()
        else:
            exit()
    else:
        next_task()


def task_validation(choice):
    """
    Inside the try, convert the chosen option into an integer.
    Raises a value error if the string can't be converted into an integer
    or if the choice is not 1, 2 or 3.
    """
    try:
        task = int(choice)
        if (task != 1) and (task != 2) and (task != 3) and (task != 4):
            raise ValueError(
                f"{task} is not a valid option!"
                )
    except ValueError as e:
        print(
            f"Invalid data: {e}. Please choose an option between"
            f"the options above: "
            )
        return False

    return True


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
    task(option)


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


def weight_validation(weight):
    """
    Validates the inputted weight
    """
    # Checks that the inputted weight is not blank space
    if is_empty_string(weight):
        print("Please insert client's weight.")
        return False
    # Checks that the inserted weight is a number
    elif not weight.isnumeric():
        print("Inserted weight needs to be a number.")
        return False
    # Makes sure the weight insterted is realistic
    # Takes into account the weights of heaviest and
    # lightest people in the world
    elif (int(weight) < 24) or (int(weight) > 635):
        print("Please insert a valid weight in kg.")
        print("Example: 87")
        return False
    else:
        return True


def body_fat_validation(body_fat):
    """
    Validates the inputted body fat
    """
    # Checks that the inputted body fat % is not an empty string
    if is_empty_string(body_fat):
        print("Please insert client's body fat %.")
        return False
    # Makes sure the insterted body fat percentage is a number
    elif not body_fat.isnumeric():
        print("Body fat percentage needs to be a numeric value.\n"
                         "Example: 22")
        return False
    # Checks that the inserted body fat percentage is realistic
    elif (int(body_fat) < 5) or (int(body_fat) > 40):
        print("Please insert a correct body fat percentage.")
        return False
    else:
        return True


def update_clients_progress(name, weight, body_fat):
    """
    Updates the clients progress worksheet with
    the latest weight and body fat percentages
    of a specified client.
    """
    print("Updating client progress records")
    values = [name, weight, body_fat]
    clients_progress.append_row(values)
    print("Client data successfully added to the progress records!")


def update_new_client_worksheet(data):
    """
    Receives a list containing data to insert
    in the relevant worksheet
    """
    client_dict = data.__dict__
    client_list = list(client_dict.values())
    print("Updating clients records...")
    clients_init_conditions.append_row(client_list)
    print("New client correctly insterted in your clients records!"
          "Some of your client data will also be added to the"
          "client progress records so that you can keep track of the"
          "changes in weight and body fat"
          )


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
            print("There's already another client registered with"
                  " the same name.\n Please provide an extra identification"
                  "for this client so that he/she can be discerned from the"
                  "one already existing"
                  )
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
        # Takes into account the heights of shortest and
        # tallest people in the world
        elif (int(height) < 63) or (int(height) > 272):
            print("Please insert a valid height in cm.")
            print("Example: 167")
            continue
        else:
            break

    # Input weight
    while True:
        weight = input("Weight(kg):")
        if weight_validation(weight):
            break
        else:
            continue

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
            print("Please choose a valid activity level"
                  "from the options provided."
                  )
            continue
        else:
            break

    # Input body fat percentage
    while True:
        body_fat = input("Body fat (Do not type %, example: 12): %")
        if body_fat_validation(body_fat):
            break
        else:
            continue

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
        elif (
              (goal_capitalize != 'A') and
              (goal_capitalize != 'B') and
              (goal_capitalize != 'C')
        ):
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

    tdee = tdee_formulas.calculate_tdee(gender, int(weight), int(height),
                                        activity.upper())
    new_client = Client(name.capitalize(), gender, age, height, weight, activity,
                        body_fat, goal, tdee)
    check_new_client_data(new_client)


def calculate_weekly_kcal_burnt():
    """
    Calculates an average of how many calories per week
    the client will burn from workouts
    """
    availability = int(input("How many days per week can your client train?"
                             "Please insert a number between 1 - 5:"
                             )
                       )
    # Client's availability input validation
    while True:
        # Checks that the insterted value is not an empty string
        if is_empty_string(availability):
            print("Please type an answer.")
            continue
        elif (availability < 1) or (availability > 5):
            print("Please insert a valid number of times per week.")
            continue
        else:
            # Calculates an avg of how many kcal per week
            # are burnt from workouts
            kcal_per_workout = 300
            weekly_kcal_burnt = kcal_per_workout * availability
            break

    return weekly_kcal_burnt


def calculate_daily_calorie_intake(goal, tdee):
    """
    Calculates how many calories per day should be consumed.
    It takes into account the amount of calories burnt per week
    during workouts, the client's goal and the tdee.
    """
    weekly_kcal_burnt = calculate_weekly_kcal_burnt()
    spreaded_weekly_kcal = weekly_kcal_burnt / 7

    if goal == 'maintain weight':
        daily_kcal_intake = tdee + spreaded_weekly_kcal
    elif goal == 'lose weight':
        daily_kcal_intake = tdee + spreaded_weekly_kcal - 500
    else:
        daily_kcal_intake = tdee + spreaded_weekly_kcal + 500

    return round(daily_kcal_intake)


def next_task():
    """
    Asks the user what to do next
    """
    print("What do you want to do now?\n"
          "1. Add a new client\n"
          "2. Check a client's progress\n"
          "3. Say goodbye to a client\n"
          "4. Exit the program\n"
          ) 
    option = int(input("Choose between the options above."))
    task(option)


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
            update_clients_progress(client_data.name, client_data.weight,
                                    client_data.body_fat)
            daily_calorie_intake = calculate_daily_calorie_intake(
                                   client_data.goal,
                                   client_data.tdee)
            print(
                f"{client_data.name} recommended daily calorie intake, "
                f"based on the {client_data.goal} goal and "
                f"on the number of workouts per week, "
                f"is around {daily_calorie_intake} kcal.")
            next_task()

        elif correct.lower() == 'n':
            print("Please reinstert the new client data!")
            take_client_data()
        else:
            print("Please answer with yes or no.")
            continue


def check_client_exists(name):
    """
    Check that the inputted client's name exists
    in the clients progress worksheet.
    """
    clients_record = clients_progress.col_values(1)
    clients_lower = [client.lower() for client in clients_record]
    # Gets the row number of the latest entry for the specified name
    # thanks to a list iteration in reversed.
    # Instructions found on StackOverflow:
    # https://stackoverflow.com/questions/529424/traverse-a-list-in-reverse-order-in-python
    for i, e in reversed(list(enumerate(clients_lower))):
        if e == name:
            index = i + 1
            return index
    else:
        print(f"{name} cannot be found in the records."
              f"Please enter a correct name to check the progress"
              f" of an existing client")
        check_progress()


def get_latest_data(row):
    """
    Gets the latest inserted data for that client
    """
    latest_entry = clients_progress.row_values(row)
    latest_weight = latest_entry[1]
    latest_body_fat = latest_entry[2]
    return latest_weight, latest_body_fat


def get_new_data():
    """
    Get's client's new weight
    and body fat through user input
    and stores the values
    in a list
    """
    new_data = []
    while True:
        new_weight = input("Please provide client's new weight:")
        if weight_validation(new_weight):
            new_data.append(new_weight)
            break
        else:
            continue
    while True:
        new_body_fat = input("Please provide client's new body fat:")
        if body_fat_validation(new_body_fat):
            new_data.append(new_body_fat)
            break
        else:
            continue

    return new_data


def get_goal(client_name):
    """
    Gets client's goal from the
    clients initial conditions worksheet
    """
    # clients = clients_init_conditions.col_values(1)
    # clients_lower = clients.lower()
    # print(clients)
    client_find = clients_init_conditions.find(client_name.capitalize())
    client_row = clients_init_conditions.row_values(client_find.row)
    for data in client_row:
        if 'weight' in data:
            return data


def check_progress():
    """
    Checks the client's progress by comparing 
    the latest inserted weight and body fat percentage
    with the ones that are being inserted and,
    based on what the original goal was,
    gives a response
    """
    client_name = (input("Insert the client name: ").lower())
    client_row = check_client_exists(client_name)
    print(f"Client exists in records!\n"
          f"Getting the latest weight and body fat in the records...")
    old_data = get_latest_data(client_row)
    new_data = get_new_data()
    goal = get_goal(client_name)
    # Compare old data and new data at the same time
    comparation = []
    for old, new in zip(old_data, new_data):
        difference = int(old) - int(new)
        comparation.append(difference)
    print(comparation)
    

def delete_client():
    print("Going to delete client page")


start_program()

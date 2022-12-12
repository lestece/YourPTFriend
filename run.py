# Import packages
import os
from time import sleep
# https://medium.com/analytics-vidhya/how-to-print-emojis-using-python-2e4f93443f7e
from emoji import emojize
import sys
import click
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
            f"{self.height}cm tall and that weights {self.weight}kg. "
            f"Taking into account that the client's activity level is "
            f"{self.activity}, body fat is {self.body_fat} %, tdee is "
            f"{self.tdee}kcal and the goal is to {self.goal}.\n\n"
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
            os.system('cls' if os.name == 'nt' else 'clear')
            take_client_data()
        elif choice == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            check_progress()
        elif choice == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
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
        if not choice.isnumeric():
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"'{choice}' is not an option.\n"
                  f"Please answer with a number from the available choices."
                  f"\n\n")
            return False
        else:
            task = int(choice)
            if (task != 1) and (task != 2) and (task != 3) and (task != 4):
                raise ValueError(
                    f"{task} is not an option!"
                    )
    except ValueError as e:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(
            f"{e}\nPlease choose a valid one.\n\n"
            )
        return False

    return True


def typing_effect(words):
    """
    It creates a sort of typing effect when displaying
    the string passed as parameter.
    This has been implemented thanks to Stack Overflow at the link:
    https://stackoverflow.com/questions/20302331/typing-effect-in-python
    """
    for char in words:
        sleep(0.02)
        sys.stdout.write(char)
        sys.stdout.flush()


def start_program():
    """
    Welcomes the PT and asks what action needs to be taken:
    -Adding a new client
    -Checking an existing client's progress
    -Deleting a client from the records
    """
    print("""\
    
    ██╗   ██╗ ██████╗ ██╗   ██╗██████╗       
    ╚██╗ ██╔╝██╔═══██╗██║   ██║██╔══██╗      
     ╚████╔╝ ██║   ██║██║   ██║██████╔╝      
      ╚██╔╝  ██║   ██║██║   ██║██╔══██╗      
       ██║   ╚██████╔╝╚██████╔╝██║  ██║      
       ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝      
                                             
            ██████╗ ████████╗                
            ██╔══██╗╚══██╔══╝                
            ██████╔╝   ██║                   
            ██╔═══╝    ██║                   
            ██║        ██║                   
            ╚═╝        ╚═╝                   
                                             
███████╗██████╗ ██╗███████╗███╗   ██╗██████╗ 
██╔════╝██╔══██╗██║██╔════╝████╗  ██║██╔══██╗
█████╗  ██████╔╝██║█████╗  ██╔██╗ ██║██║  ██║
██╔══╝  ██╔══██╗██║██╔══╝  ██║╚██╗██║██║  ██║
██║     ██║  ██║██║███████╗██║ ╚████║██████╔╝
╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝ 
                                             

    """)
    sleep(1.5)
    os.system('cls' if os.name == 'nt' else 'clear')
    words = (f"Welcome coach!\n\n\n"
             f"My job is to support you in your PT occupation\n" 
             f"by taking charge of the boring tasks so that\n"
             f"you can entirely focus on creating those sweaty workouts"
             f"{emojize(':droplet:')}\n\n"
             f"What do you want me to do for you today?\n\n"
             f"1. Add a new client to your client's records "
             f"{emojize(':plus:')}\n"
             f"2. Check a client's progress {emojize(':chart_increasing:')}\n"
             f"3. Say goodbye to a client {emojize(':minus:')}\n\n")
    typing_effect(words)
    option = (input("Choose an option from the above (1, 2 or 3):\n"))
    task(option)


def is_empty_string(data):
    """
    Checks that the inputted data is not an empty string.
    """
    try:
        if data == "":
            raise ValueError("You need to provide the requested information!")
    except ValueError as e:
        print(f"You didn't answer. {e}")
        return True
    return False


def weight_validation(weight):
    """
    Validates the inputted weight
    """
    # Checks that the inputted weight is not blank space
    if is_empty_string(weight):
        print("\nPlease insert client's weight.")
        return False
    # Checks that the inserted weight is a number
    elif not weight.isnumeric():
        print("\nInserted weight needs to be a number.")
        return False
    # Makes sure the weight insterted is realistic
    # Takes into account the weights of heaviest and
    # lightest people in the world
    elif (int(weight) < 24) or (int(weight) > 635):
        print("\nPlease insert a valid weight in kg."
              "Example: 87")
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
    values = [name.capitalize(), weight, body_fat]
    clients_progress.append_row(values)


def update_new_client_worksheet(data):
    """
    Receives a list containing data to insert
    in the relevant worksheet
    """
    client_dict = data.__dict__
    client_list = list(client_dict.values())
    words = ("Updating clients records...\n\n")
    typing_effect(words)
    clients_init_conditions.append_row(client_list)
    sleep(1)
    print("New client correctly insterted in your clients records!\n\n")
    sleep(2)


def take_client_data():
    """
    Takes the client data as input.
    After input validation, the data is inserted in a new_client list.
    """
    print("You're adding a new client!\n\n"
          "Please insert the following requested information.\n\n")
    sleep(1)
    # Input name
    while True:
        name = input("Full name: ")
        # Checks that the inputted name is not blank space
        if is_empty_string(name):
            print("You need to insert the client's name.\n")
            continue
        # Checks that the inserted name is not a number
        elif name.isnumeric():
            print("\nClient's name cannot be a number.\n"
                  "\nPlease insert a valid one.\n")
        
        # Checks if the name is already in the records
        elif clients_init_conditions.find(name.capitalize()):
            words = ("\nThere's already another client registered with "
                     "the same name.\nPlease provide extra identification "
                     "for this client so that he/she can be discerned "
                     "from the one already existing with the same name.\n\n"
                     )
            typing_effect(words)
            continue
        else:
            break

    # Input gender
    while True:
        sleep(0.3)
        gender = input("\nGender(F or M): ")
        # Checks that the inputted gender is not blank space
        if is_empty_string(gender):
            print("\nPlease insert client's gender.")
            continue
        # Makes sure the gender is either F or M
        elif (gender.upper() != 'F') and (gender.upper() != 'M'):
            print("\nPlease answer with either 'F' or 'M'.")
            continue
        else:
            break
    # Input age
    while True:
        sleep(0.3)
        age = input("\nAge: ")
        # Checks that the inputted age is not blank space
        if is_empty_string(age):
            print("Please insert client's age.")
            continue
        # Checks that the insterted age is a number
        elif not age.isnumeric():
            print("\nAge needs to be a number.")
            continue
        # Makes sure the age is a realistic value
        elif (int(age) < 14) or (int(age) > 100):
            print("\nPlease insert a valid age.\n"
                  "Clients cannot be younger than 14\n"
                  "or older than 100.\n")
            continue
        else:
            break

    # Input height
    while True:
        sleep(0.3)
        height = input("\nHeight(cm): ")
        # Checks that the inputted height is not blank space
        if is_empty_string(height):
            print("\nPlease insert client's height.")
            continue
        # Checks that the insterted height is a number
        elif not height.isnumeric():
            print("\nInserted height needs to be a number.")
            continue
        # Makes sure the height is in cm and not feet
        # Also checks that the inserted height is realistic
        # Takes into account the heights of shortest and
        # tallest people in the world
        elif (int(height) < 63) or (int(height) > 272):
            print("\nPlease insert a valid height in cm.\n"
                  "Example: 167")
            continue
        else:
            break

    # Input weight
    while True:
        sleep(0.3)
        weight = input("\nWeight(kg): ")
        if weight_validation(weight):
            break
        else:
            continue

    # Input activity level
    while True:
        sleep(0.2)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Please choose one of the following activity levels.\n")
        click.echo("- Sedentary: " + click.style("SED\n"
                   , fg="magenta", underline=True) + 
                   "- Lightly active: " + click.style("LA\n"
                   , fg="magenta", underline=True) +
                   "- Moderately active: " + click.style("MA\n"
                   , fg="magenta", underline=True) +
                   "- Very active: " + click.style("VA\n"
                   , fg="magenta", underline=True) +
                   "- Extremely active: " + click.style("EA\n"
                   , fg="magenta", underline=True))

        activity = input("Activity level: ")
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
            print("Please choose a valid activity level "
                  "from the options provided.\n \n"
                  )
            continue
        else:
            break

    # Input body fat percentage
    while True:
        body_fat = input("Body fat: % ")
        if body_fat_validation(body_fat):
            break
        else:
            continue

    # Input client's goal
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Now, what's {name.capitalize()}'s main goal?\n\n")
    while True:
        print("A. Weight maintenance")
        print("B. Weight loss / cutting")
        print("C. Weight gain / bulking\n\n")
        goal_letter = input("Goal (A, B or C): ")
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
    new_client = Client(name.capitalize(), gender, age, height, weight, 
                        activity, body_fat, goal, tdee)
    check_new_client_data(new_client)


def calculate_weekly_kcal_burnt():
    """
    Calculates an average of how many calories per week
    the client will burn from workouts
    """
    sleep(0.3)
    os.system('cls' if os.name == 'nt' else 'clear')
    words = ("How many days per week can the client train?\n\n")
    typing_effect(words)
    availability = int(input("Please insert a number between 1 - 5: "))
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
    print(f"What do you want to do?\n\n"
          f"1. Add a new client {emojize(':plus:')}\n"
          f"2. Check a client's progress {emojize(':chart_increasing:')}\n"
          f"3. Say goodbye to a client {emojize(':minus:')}\n"
          f"4. Exit the program {emojize(':cross_mark:')}\n"
          ) 
    option = input("Choose between the options above.")
    task(option)


def check_new_client_data(client_data):
    """
    Checks with the user if all of the inserted client data
    is correct and there's no errors.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(
        f"The details of the new client are as follows: \n \n")
    words = (f"{client_data.client_description()}")
    typing_effect(words)

    while True:
        correct = input("Does all of the data look correct? (y/n): ")
        os.system('cls' if os.name == 'nt' else 'clear')
        if correct.lower() == 'y':
            update_new_client_worksheet(client_data)
            update_clients_progress(client_data.name, client_data.weight,
                                    client_data.body_fat)
            daily_calorie_intake = calculate_daily_calorie_intake(
                                   client_data.goal,
                                   client_data.tdee)
            sleep(0.1)
            os.system('cls' if os.name == 'nt' else 'clear')                       
            words = (
                    f"{client_data.name}'s recommended daily calorie intake, "
                    f"based on the {client_data.goal} goal and "
                    f"on the number of workouts per week, "
                    f"is around {daily_calorie_intake} kcal.\n\n")
            typing_effect(words)
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
    latest_entry.pop(0)
    keys = ["weight", "body_fat"]
    old_data = dict(zip(keys, latest_entry))
    
    return old_data


def get_new_data():
    """
    Get's client's new weight
    and body fat through user input
    and stores the values
    in a list
    """
    new_data_list = []
    while True:
        new_weight = input("Please provide client's new weight:")
        if weight_validation(new_weight):
            new_data_list.append(new_weight)
            break
        else:
            continue
    while True:
        new_body_fat = input("Please provide client's new body fat:")
        if body_fat_validation(new_body_fat):
            new_data_list.append(new_body_fat)
            break
        else:
            continue
    keys = ["weight", "body_fat"]
    new_data = dict(zip(keys, new_data_list))
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


def check_body_fat_improvement(client_name, old_body_fat, new_body_fat):
    """
    Establishes an improvement or not
    of the client's health by comparing
    the body fat data
    """
    if old_body_fat > new_body_fat:
        print(f"We can notice a body fat reduction of "
              f"{old_body_fat - new_body_fat} so the"
              f" {client_name} overall health has improved.")
    elif old_body_fat < new_body_fat:
        print(f"{client_name} body fat has increased since last time."
              f" with a {new_body_fat - old_body_fat} % more body fat, "
              f"some changes need to occur.")
    else:
        print(f"{client_name}'s body fat hasn't changed, "
              f"so maybe we should consider tweacking up a bit the program")


def check_progress():
    """
    Checks the client's progress by comparing 
    the latest inserted weight and body fat percentage
    with the ones that are currently being inserted and,
    based on what the original goal was,
    gives a positive or negative response.
    """
    client_name = (input("Insert the client name: ").lower())
    client_row = check_client_exists(client_name)
    print(f"Client exists in records!\n"
          f"Getting the latest weight and body fat in the records...")
    old_data = get_latest_data(client_row)
    old_weight = int(old_data['weight'])
    old_body_fat = int(old_data['body_fat'])
    new_data = get_new_data()
    new_weight = int(new_data['weight'])
    new_body_fat = int(new_data['body_fat'])
    goal = get_goal(client_name)
    
    if 'lose' in goal:
        if old_weight > new_weight:
            print(f"Well done! \n"
                  f"{client_name} original goal was to {goal}c"
                  f"and based on the new data insterted we can "
                  f"establish a {old_weight - new_weight} kg weight loss.")
        elif old_weight < new_weight:
            print(f"Something needs to be changed.\n"
                  f"{client_name} wants to {goal} but based on the "
                  f"new insterted weight there's been a weight gain "
                  f"of {new_weight - old_weight} kg.")
        else:
            print(f"We need to work harder!\n"
                  f"{client_name}'s weight doesn't seems to want to change!")
    elif 'gain' in goal:
        if old_weight > new_weight:
            print(f"Something needs to be changed. "
                  f"{client_name} wants to {goal} but based on the "
                  f"new insterted weight there's been a weight loss "
                  f"of {old_weight - new_weight} kg.")
        elif old_weight < new_weight:
            print(f"Well done! \n"
                  f"{client_name} original goal was to {goal} "
                  f"and based on the new data insterted we can "
                  f"establish a {new_weight - old_weight} kg weight gain.")
        else:
            print(f"We need to work harder!"
                  f"{client_name}'s weight doesn't seems to want to change!")
    else:
        if old_weight > new_weight:
            print(f"Something needs to be changed.\n"
                  f"{client_name} wants to {goal} but based on the "
                  f"new insterted weight there's been a weight loss "
                  f"of {old_weight - new_weight} kg.")
        elif old_weight < new_weight:
            print(f"Something needs to be changed.\n"
                  f"{client_name} wants to {goal} but based on the "
                  f"new insterted weight there's been a weight gain "
                  f"of {new_weight - old_weight} kg.")
        else:
            print(f"Well done!\n"
                  f"{client_name} original goal was to {goal} "
                  f"and at today it has stayed the same!")

    check_body_fat_improvement(client_name, old_body_fat, new_body_fat)
    update_clients_progress(client_name, new_weight, new_body_fat)
    next_task()


def delete_client():
    """
    Deletes a specified client from the records.
    Client is removed both from the initial conditions worksheet
    and the progress worksheet.
    """
    client_to_delete = input("Please insert the name of the client "
                             "we are saying goodbye to: \n")
    # Check that the client exists in the records
    client_find = clients_init_conditions.find(client_to_delete.capitalize())
    if client_find:
        # If client exists, remove from initial conditions worksheet
        print("Removing client from records...")
        client_row = client_find.row
        clients_init_conditions.delete_rows(client_row)
    else:
        print(f"There's no client under name of {client_to_delete}.")
        delete_client()  
    # Loop that deletes every row containing that client name
    # in the client progress worksheet
    while True:
        client_progress_find = clients_progress.find(client_to_delete
                                                     .capitalize())
        if client_progress_find:
            client_progress_row = client_progress_find.row
            clients_progress.delete_rows(client_progress_row)
            continue
        else:
            print("Client successfully removed! "
                  "Now you have an extra availability.")
            next_task()


start_program()

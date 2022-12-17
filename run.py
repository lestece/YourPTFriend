# Import packages
import os
from time import sleep
# https://medium.com/analytics-vidhya/how-to-print-emojis-using-python-2e4f93443f7e
from emoji import emojize
import sys
# https://mauricebrg.com/article/2020/08/cli_text_styling_progress_bars_and_prompts_with_click.html
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
                click.style(self.name, fg="blue", bold=True) +
                " is a " +
                click.style(self.age, fg="blue", bold=True) +
                " years old " +
                click.style(self.gender, fg="blue", bold=True) +
                " client, \n" +
                click.style(self.height, fg="blue", bold=True) +
                " tall and that weights " +
                click.style(self.weight, fg="blue", bold=True) +
                " kg.\nThe client's activity level is " +
                click.style(self.activity, fg="blue", bold=True) +
                ",\nbody fat is " +
                click.style(self.body_fat, fg="blue", bold=True) +
                " %, TDEE is " +
                click.style(self.tdee, fg="blue", bold=True) +
                " kcal\nand the goal is to " +
                click.style(self.goal, fg="blue", bold=True) + ".\n\n")


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
            os.system('cls' if os.name == 'nt' else 'clear')
            words = (f"\n\nThank you for relying on my service!\n\n"
                     f"See you next time "
                     f"{emojize(':smiling_face_with_smiling_eyes:')}\n\n\n\n")
            typing_effect(words)
            sleep(0.5)
            print("""\

                        ██████╗ ██╗   ██╗███████╗██╗
                        ██╔══██╗╚██╗ ██╔╝██╔════╝██║
                        ██████╔╝ ╚████╔╝ █████╗  ██║
                        ██╔══██╗  ╚██╔╝  ██╔══╝  ╚═╝
                        ██████╔╝   ██║   ███████╗██╗
                        ╚═════╝    ╚═╝   ╚══════╝╚═╝
                  """)
            sleep(10)
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
        sleep(0.04)
        sys.stdout.write(char)
        sys.stdout.flush()


def progress_bar() -> None:
    """
    Shows a progress bar
    """

    with click.progressbar(label="",
                           length=100,
                           show_eta=False) as progress_bar:
        for i in range(20):
            progress_bar.update(i)
            sleep(0.05)


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
    sleep(3.5)
    os.system('cls' if os.name == 'nt' else 'clear')
    words = (f"\n\nWelcome Coach!\n\n\n"
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
    sleep(0.2)
    try:
        if data == "":
            raise ValueError("You need to provide "
                             "the requested information!\n")
    except ValueError as e:
        print(f"\nYou didn't answer. {e}")
        return True
    return False


def weight_validation(weight):
    """
    Validates the inputted weight
    """
    # Checks that the inputted weight is not blank space
    if is_empty_string(weight):
        print("\nPlease insert client's weight.\n")
        return False
    # Checks that the inserted weight is a number
    elif not weight.isnumeric():
        print("\nInserted weight needs to be a number.\n")
        return False
    # Makes sure the weight insterted is realistic
    # Takes into account the weights of heaviest and
    # lightest people in the world
    elif (int(weight) < 24) or (int(weight) > 635):
        print("\nPlease insert a valid weight in kg.\n"
              "Example: 87\n\n")
        return False
    else:
        return True


def body_fat_validation(body_fat):
    """
    Validates the inputted body fat
    """
    # Checks that the inputted body fat % is not an empty string
    if is_empty_string(body_fat):
        print("\nPlease insert client's body fat %.")
        return False
    # Makes sure the insterted body fat percentage is a number
    elif not body_fat.isnumeric():
        print("\nBody fat percentage needs to be a numeric value.\n"
              "Example: 22")
        return False
    # Checks that the inserted body fat percentage is realistic
    elif (int(body_fat) < 5) or (int(body_fat) > 40):
        print("\nPlease insert a correct body fat percentage.")
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
    progress_bar()
    clients_init_conditions.append_row(client_list)
    print("\n\nNew client correctly insterted in your clients records!\n\n")
    sleep(2)


def take_client_data():
    """
    Takes the client data as input.
    After input validation, the data is inserted in a new_client list.
    """
    print("You're adding a new client!\n\n")
    sleep(1)
    print("Please insert the following requested information.\n\n")
    sleep(1)
    # Input name
    while True:
        name = input("Full name: \n")
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
                     " the same name.\nPlease provide extra identification "
                     "for this client so that \nhe/she can be discerned "
                     "from the one already existing with the same name.\n\n"
                     )
            typing_effect(words)
            continue
        else:
            break

    # Input gender
    while True:
        sleep(0.3)
        gender_letter = input("\nGender(F or M): \n")
        # Checks that the inputted gender is not blank space
        if is_empty_string(gender_letter):
            print("\nPlease insert client's gender.")
            continue
        # Makes sure the gender is either F or M
        elif (gender_letter.upper() != 'F') and (gender_letter.upper() != 'M'):
            print("\nPlease answer with either 'F' or 'M'.")
            continue
        else:
            if gender_letter.upper() == 'F':
                gender = "female"
            else:
                gender = "male"
            break
    # Input age
    while True:
        sleep(0.3)
        age = input("\nAge: \n")
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
        height = input("\nHeight(cm): \n")
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
        weight = input("\nWeight(kg): \n")
        if weight_validation(weight):
            break
        else:
            continue

    # Input activity level
    sleep(0.2)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Please choose one of the following activity levels.\n")
    while True:
        click.echo("- Sedentary: " +
                   click.style("SED\n", fg="magenta", bold=True) +
                   "- Lightly active: " +
                   click.style("LA\n", fg="magenta", bold=True) +
                   "- Moderately active: " +
                   click.style("MA\n", fg="magenta", bold=True) +
                   "- Very active: " +
                   click.style("VA\n", fg="magenta", bold=True) +
                   "- Extremely active: " +
                   click.style("EA\n", fg="magenta", bold=True))

        activity = input("Activity level: \n")
        # Checks that the inputted activity level is not blank space
        if is_empty_string(activity):
            sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
            words = ("Please insert client's activity level.\n\n")
            typing_effect(words)
            sleep(0.3)
            continue
        # Checks that the inserted activity level is valid
        elif (
            (activity.upper() != 'SED') and
            (activity.upper() != 'LA') and
            (activity.upper() != 'MA') and
            (activity.upper() != 'VA') and
            (activity.upper() != 'EA')
             ):
            words = (f"\n'{activity}' is not an option!\n"
                     f"\n'Please insert client's activity level.\n\n")
            typing_effect(words)
            sleep(1)
            continue
        else:
            if activity.upper() == 'SED':
                activity_level = 'sedentary'
            elif activity.upper() == 'LA':
                activity_level = 'lightly active'
            elif activity.upper() == 'MA':
                activity_level = 'moderately active'
            elif activity.upper() == 'VA':
                activity_level = 'very active'
            elif activity.upper() == 'EA':
                activity_level = 'extremely active'
            break

    # Input body fat percentage
    while True:
        body_fat = input("\nBody fat:\n% ")
        if body_fat_validation(body_fat):
            break
        else:
            continue

    # Input client's goal
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Now, what's {name.capitalize()}'s main goal?\n\n")
    while True:
        click.echo(click.style("A.", fg="green", bold=True) +
                   " Weight maintenance\n" +
                   click.style("B.", fg="green", bold=True) +
                   " Weight loss / cutting\n" +
                   click.style("C.", fg="green", bold=True) +
                   " Weight gain / bulking\n")
        goal_letter = input("Client's goal (A, B or C): ")
        goal_capitalize = goal_letter.upper()
        # Checks that the inputted goal is not an empty string
        if is_empty_string(goal_capitalize):
            print("\nPlease insert client's goal!")
            continue
        # Checks that the inserted goal is one of the available options
        elif (
              (goal_capitalize != 'A') and
              (goal_capitalize != 'B') and
              (goal_capitalize != 'C')
        ):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nPlease choose one of the available options.")
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
                        activity_level, body_fat, goal, tdee)
    check_new_client_data(new_client)


def calculate_weekly_kcal_burnt():
    """
    Calculates an average of how many calories per week
    the client will burn from workouts
    """
    sleep(0.2)
    os.system('cls' if os.name == 'nt' else 'clear')
    words = ("How many days per week can the client train?\n\n")
    typing_effect(words)
    availability = int(input("Please insert a number between 1 - 5: \n"))
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


def user_done():
    """
    Waits for the user to press ENTER key
    when done with the outputted information
    """
    enter = input("Press ENTER when you are ready\n"
                  "to close this information.")
    while True:
        if enter == "":
            os.system('cls' if os.name == 'nt' else 'clear')
            words = ("What do you want to do next?\n\n")
            typing_effect(words)
            next_task()
        else:
            enter = input("\nPlease press ENTER.")
            continue


def next_task():
    """
    Asks the user what to do next
    """
    print(
          f"1. Add a new client {emojize(':plus:')}\n"
          f"2. Check a client's progress {emojize(':chart_increasing:')}\n"
          f"3. Say goodbye to a client {emojize(':minus:')}\n"
          f"4. Exit the program {emojize(':cross_mark:')}\n"
          )
    option = input("Choose between the options above.\n")
    task(option)


def check_new_client_data(client_data):
    """
    Checks with the user if all of the inserted client data
    is correct and there's no errors.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("The details of the new client are as follows: \n \n")
    words = (f"{client_data.client_description()}")
    typing_effect(words)

    while True:
        correct = input("Does all of the data look correct? (y/n): ")
        sleep(0.5)
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
            print("Processing..\n\n")
            progress_bar()
            sleep(1.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            words = (
                    f"\n\n{client_data.name}'s recommended daily calorie "
                    f"intake,\nbased on the {client_data.goal} goal and\n"
                    f"on the number of workouts per week,\n"
                    f"is around {daily_calorie_intake} kcal.\n\n")
            typing_effect(words)
            sleep(2)
            user_done()

        elif correct.lower() == 'n':
            print("Please reinstert the new client data!")
            take_client_data()
        else:
            print("Please answer with 'y' or 'n'.")
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
        print(f"\n'{name}' cannot be found in the records.\n"
              f"Please enter a correct name to check the progress\n"
              f" of an existing client.\n")
        return False


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
    sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')
    new_data_list = []
    while True:
        new_weight = input("\n\nProvide client's new weight: \n")
        if weight_validation(new_weight):
            new_data_list.append(new_weight)
            break
        else:
            continue
    while True:
        new_body_fat = input("\n\nProvide client's new body fat: \n")
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
    sleep(2)
    if old_body_fat > new_body_fat:
        words = (f"And we can notice a body fat reduction of\n"
                 f"{old_body_fat - new_body_fat} so "
                 f"{client_name}'s overall health "
                 f"has improved. {emojize(':party_popper:')}\n\n\n\n\n")
    elif old_body_fat < new_body_fat:
        words = (f"And {client_name}'s body fat has increased since last time "
                 f"{emojize(':face_screaming_in_fear:')}\n"
                 f"With a {new_body_fat - old_body_fat} % more body fat, "
                 f"some changes need to occur.\n\n\n\n\n")
    else:
        words = (f"And {client_name}'s body fat has stayed the same, "
                 f"so maybe we should consider tweaking up a bit the program "
                 f"{emojize(':face_with_monocle:')}\n\n\n\n\n")
    typing_effect(words)


def check_progress():
    """
    Checks the client's progress by comparing
    the latest inserted weight and body fat percentage
    with the ones that are currently being inserted and,
    based on what the original goal was,
    gives a positive or negative response.
    """
    words = (f"\nYou're checking a client's progress!\n\n"
             f"Please provide the information requested below "
             f"{emojize(':down_arrow:')}\n\n")
    typing_effect(words)
    while True:
        client_name = (input("Insert the client's name: ").lower())
        if is_empty_string(client_name):
            continue
        else:
            client_row = check_client_exists(client_name)
            if not client_row:
                continue
            else:
                print(f"\nGreat! {client_name.capitalize()} is "
                      f"in your records.")
                sleep(0.5)
                words = ("\nGetting the latest weight and "
                         "body fat registered...\n\n")
                typing_effect(words)
                progress_bar()
                old_data = get_latest_data(client_row)
                old_weight = int(old_data['weight'])
                old_body_fat = int(old_data['body_fat'])
                new_data = get_new_data()
                new_weight = int(new_data['weight'])
                new_body_fat = int(new_data['body_fat'])
                goal = get_goal(client_name)

                words = "\n\nBear with me while I do some math...\n"
                typing_effect(words)
                progress_bar()
                sleep(2.5)
                os.system('cls' if os.name == 'nt' else 'clear')
                client_capitalized = client_name.capitalize()
                if 'lose' in goal:
                    if old_weight > new_weight:
                        words = (f"\n\nWell done! \n"
                                 f"{client_capitalized} original goal was to\n"
                                 f"{goal} and based on the new data insterted "
                                 f"we\n can establish a "
                                 f"{old_weight - new_weight} kg\nweight loss "
                                 f"{emojize(':flexed_biceps:')}\n\n\n")
                    elif old_weight < new_weight:
                        words = (f"\n\nSomething needs to be changed.\n"
                                 f"{client_capitalized} wants to {goal} but "
                                 f"based\non the new insterted weight "
                                 f"there's been a\nweight gain of "
                                 f"{new_weight - old_weight} kg"
                                 f" {emojize(':frowning_face:')}\n\n\n")
                    else:
                        words = (f"\n\nWe need to work harder!\n"
                                 f"{client_capitalized}'s weight doesn't seem"
                                 f"\nto want to change! "
                                 f"{emojize(':confused_face:')}\n\n\n")
                    break
                elif 'gain' in goal:
                    if old_weight > new_weight:
                        words = (f"\n\nSomething needs to be changed. "
                                 f"{client_capitalized} wants to {goal} but "
                                 f"based on the new insterted weight "
                                 f"there's been a weightloss of "
                                 f"{old_weight - new_weight} kg."
                                 f" {emojize(':frowning_face:')}\n\n\n")
                    elif old_weight < new_weight:
                        words = (f"\n\nWell done! \n"
                                 f"{client_capitalized} original goal was to "
                                 f"{goal} and based on the new data insterted "
                                 f"we can establish a "
                                 f"{new_weight - old_weight} kg weight gain "
                                 f"{emojize(':flexed_biceps:')}\n\n\n")
                    else:
                        words = (f"\n\nWe need to work harder!"
                                 f"{client_capitalized}'s weight doesn't seem "
                                 f"towant to change! "
                                 f"{emojize(':confused_face:')}\n\n\n")
                    break
                else:
                    if old_weight > new_weight:
                        words = (f"\n\nSomething needs to be changed.\n"
                                 f"{client_capitalized} wants to {goal} but "
                                 f"based on the new insterted weight "
                                 f"there's been a weight loss of "
                                 f"{old_weight - new_weight} kg."
                                 f" {emojize(':frowning_face:')}\n\n\n")
                    elif old_weight < new_weight:
                        words = (f"\n\nSomething needs to be changed.\n"
                                 f"{client_capitalized} wants to {goal} but "
                                 f"based on the new insterted weight "
                                 f"there's been a weight gain of "
                                 f"{new_weight - old_weight} kg."
                                 f" {emojize(':frowning_face:')}\n\n\n")
                    else:
                        words = (f"\n\nWell done!\n"
                                 f"{client_capitalized} original goal was to "
                                 f"{goal} and at today it has stayed the same!"
                                 f"{emojize(':flexed_biceps:')}\n\n\n")
                    break
    typing_effect(words)
    check_body_fat_improvement(client_capitalized, old_body_fat, new_body_fat)
    update_clients_progress(client_name, new_weight, new_body_fat)
    sleep(2)
    user_done()
    next_task()


def delete_client():
    """
    Deletes a specified client from the records.
    Client is removed both from the initial conditions worksheet
    and the progress worksheet.
    """
    client_to_delete = input("\n\nPlease insert the name of the client "
                             "we are saying goodbye to: \n")
    # Check that the client exists in the records
    client_find = clients_init_conditions.find(client_to_delete.capitalize())
    if client_find:
        # If client exists, remove from initial conditions worksheet
        words = ("\n\nRemoving client from records...\n\n\n")
        typing_effect(words)
        progress_bar()
        client_row = client_find.row
        clients_init_conditions.delete_rows(client_row)
    else:
        print(f"\n\nThere's no client under name of {client_to_delete}.\n\n")
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
            print(f"\n\n{client_to_delete.capitalize()} "
                  f"has been successfully removed!\n")
            sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n\nWhat do you want to do next?\n\n")
            next_task()


start_program()

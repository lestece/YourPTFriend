# YourPTfriend Testing

## TABLE OF CONTENTS

1) [Manual Testing](#1-manual-testing)
    - [Task choice](#task-choice)
    - [Add new client](#add-new-client)
    - [Check client's progress](#check-clients-progress)
    - [Delete client](#delete-client-from-records)
    - [Exit program](#exit-the-program)
    - [User control 'Enter'](#user-control-enter)
2) [Code Validation](#2-code-validation)
3) [Bugs and fixes](#3-bugs-and-fixes)

[⬅ Back to the README.md file](README.md)
- - - 
## 1) MANUAL TESTING

### TASK CHOICE

#### - __Input validation__
The task choice input has been validated to only accept one of the available tasks option. Empty strings, special characters, letters, numbers different from 1-4 are not accepted and the user gets a tailored prompt to insert the correct value. 
![Task choice validation](images/testing-images/task-choice-validation.gif)

#### - __Task 1 option tested__
If option 1(_add a new client_) is chosen, the program correctly calls the _take_client_data()_ function to collect the new client data.
![Task one tested](images/testing-images/task-one-option-tested.gif)

#### - __Task 2 option tested__
Option 2(_check a client's progress_) selection correctly triggers the _check_progress()_ function.
![Task two tested](images/testing-images/task-two-option-tested.gif)

#### - __Task 3 option tested__
The _delete_client()_ function to delete a client from the records is correctly called if option 3 is inputted in the task choice input.
![Task three tested](images/testing-images/task-three-option-tested.gif)

#### - __Task 4 option tested__
When option 4 is chosen, the program correctly closes by giving the user goobye.
![Task four tested](images/testing-images/task-four-option-tested.gif)

[Back to top ↑](TESTING.md/#yourptfriend-testing)
- - -
### ADD NEW CLIENT

#### - __Inputs validation__


##### __Name__
The name inputs only accepts values that are not: empty strings, numbers, special characters, names that are shorter than 3 letters or already existing names.
![Name input validation](images/testing-images/add-client-name-validation.gif)

##### __Gender__
The input that asks for the client's gender validates that no empty strings or characters other than 'f' or 'm' are inserted.
![Gender input validation](images/testing-images/add-client-gender-validation.gif)

##### __Age__
Only numbers between 14 and 100 are accepted into the client's age input. Also, empty strings are not allowed.
![Age input validation](images/testing-images/add-client-age-validation.gif)

##### __Height__
The height input validation makes sure that empty strings are rejected and only numbers between 63 and 272 are accepted. The height of the shortest and the tallest person ever existed have been taken into account as parameters.
![Height input validation](images/testing-images/add-client-height-validation.gif)

##### __Weight__
The weight input only accepts numbers between 24 and 635 (lightest and heaviest person ever recorded). No empty strings are allowed.
The validation comes from the _weight_validation function_ that is also called _when validating the client's new weight when checking the progress_.
![Weight input validation](images/testing-images/add-client-weight-validation.gif)

##### __Activity level__
Nothing but the specific options available is accepted into the input that takes the client's activity level.
![Activity level input validation](images/testing-images/add-client-aclev-validation.gif)

##### __Body fat__
Only numbers between 5 and 40 (realistic/possible parameters) are accepted in the body fat input.
_The same validation, coming from the body_fat_validation() function, is used when asking the user for the client's new body fat to check the progress (Task option 2: Check client's progress)._
![Body fat input validation](images/testing-images/add-client-bodyfat-validation.gif)

##### __Goal__
The goal input is validated so that no empty strings, numbers, special characters or letters different from 'a', 'b' or 'c' are accepted.
![Goal input validation](images/testing-images/add-client-goal-validation.gif)

##### __Confirm new client data__
When asking the user for confirmation related to the newly inserted data, the input validates that the user answers with either 'y' or 'n'.
![Confirm client data input validation](images/testing-images/new-client-data-confirm-valid.gif)

##### __Client's availability__
The input that asks for the client's availability after updating the worksheets with the new client data, correctly validates that the user is not inserting empty strings, symbols, letters, numbers out of the range 1-5.
![Client's availability input validation](images/testing-images/clients-availability-validation.gif)
- - -
#### - __Client's data confirmation__

##### __Confirmed(y): Worksheets update__
When the user answers positively to confirm the new client's data, the _update_new_client_worksheet()_ and _update_clients_progress()_ functions are correctly triggered and the _clients initial conditions_ and _clients progress_ worksheets in the _Your-PT-Friend_ Google Sheets file are successfully updated with the new client data.
![New client worksheets update](images/testing-images/new-client-worksheets-update.gif)

##### __Not confirmed(n): Restart take_client_data__
If the user answers with 'no' ('n') to the input asking for confirmation for the new user data, the _take_client_data()_ function is correctly called and the user is asked again for all of the data.
![Go back to inserting new client data](images/testing-images/client-data-not-confirmed.gif)
- - - 
#### - __Formulas__
All of the functions containing the formulas to calculate TDEE and reach the daily calorie intake have been manually tested using as an example 3 different fictional clients, each with a varied set of data, goal and weekly availability for workouts.
![Clients examples](images/testing-images/clients-example-testing.png)


##### __TDEE_FORMULAS FILE__
If manually calculating the TDEE  using the formulas contained in _tdee_formulas.py_ file, the TDEE results obtained on the _clients initial conditions_ worksheet (screenshot above) prove to be accurate. 

1) __Rick__

LBM = 0.407 * 120 + 0.267 * 187 - 19.2 = 79.569

BMR = 79.569 * 21.6 + 370 = 2088.6904

TEF = 2088.6904 * 0.1 = 208.86904

TEA = (2088.6904 * 1.2) - 2088.6904 = 417.73808

__TDEE__ = 2088.6904 + 208.86904 + 417.73808 = _2715.29_(__2715__)


2) __Sarah__

LBM = 0.252 * 52 + 0.473 * 158 - 48.3 = 39.538  

BMR = 39.538 * 21.6 + 370 = 1224.0208  

TEF = 1224.0208 * 0.1 = 122.40208  

TEA = (1224.0208 * 1.725) - 1224.0208 = 887.41508  

__TDEE__ = 1224.0208 + 122.40208 + 887.41508 = _2233.83_(__2234__)


3) __Jenna__

LBM = 0.252 * 54 + 0.473 * 168 - 48.3 = 44.772

BMR = 44.772 * 21.6 + 370 = 1337.0752

TEF = 1337.0752 * 0.1 = 133.70752

TEA = (1337.0752 * 1.375) - 1337.0752 = 501.4032

__TDEE__ = 1337.0752 + 133.70752 + 501.4032 = _1972.18_(__1972__)

- - - 

##### __Daily calorie intake formulas__
To test the daily calorie intake function and related ones, I set a different availability parameter for each client in the examples.

1) __Rick__
![Rick's daily calorie intake](images/testing-images/rick-testing-example.png)

Rick's availability to workouts was set to 2 days per week.

Weekly kcal burnt from workouts = 300 * 2 days x week = 600 kcal

Daily kcal burnt from workout = 600kcal / 7 = 85.71

__Daily calorie intake__ = 2715 + 85.71 - 500 = 2300.71 (__2301__)


2) __Sarah__
![Sarah's daily calorie intake](images/testing-images/sarah-testing-example.png)

Sarah's availability to workouts was set to 4 days per week.

Weekly kcal burnt from workouts = 300 * 4 days x week = 1200 kcal

Daily kcal burnt from workout = 1200kcal / 7 = 171.42

__Daily calorie intake__ = 2234 + 171.42 = 2405.42 (__2405__)


2) __Jenna__
![Jenna's daily calorie intake](images/testing-images/jenna-testing-example.png)

Jenna's availability to workouts was set to 3 days per week.

Weekly kcal burnt from workouts = 300 * 3 days x week = 900 kcal

Daily kcal burnt from workout = 900kcal / 7 = 128.57

__Daily calorie intake__ = 1972 + 128.57 + 500 = 2600.57 (__2601__)

[Back to top ↑](TESTING.md/#yourptfriend-testing)
- - -

### CHECK CLIENT'S PROGRESS

#### - __Existing client's name__
When checking a client's progress, the input that asks for the client's name correctly validates that the name exists in the worksheets.
![Check client's actually exists](images/testing-images/check-client-progress-name.gif)

#### - __New body weight and fat validation__
I tested that also the new body weight and body fat inputs validation is working. 
![New body weight and fat validation](images/testing-images/client-new-weight-and-body-fat-testing.gif)

#### - Progress results

For testing the accuracy of the client's progress result, I used the same fictional clients used above for the daily calorie intake functions.

![Client progress examples testing](images/testing-images/progress-results-testing.png)

1) Rick

Rick's new weight and body fat have been inputted so that the progress results would return a __negative/fail response__:
Considering his initial goal was to lose weight and latest registered weight and body fat were respectively 120kg and 35%, the new data provided have been 122kg and 36%. 

![Client progress fail testing](images/testing-images/client-progress-fail-testing.png)

2) Sarah

Sarah's new new data was to test a __successful response__:
Being the initial goal to maintain weight, I used the same latest recorded data: 52kg and 16%. 

![Client progress success testing](images/testing-images/client-progress-success-testing.png)

3) Jenna

Jenna has been used to test a __neutral/no change occured response__:
To gain weight was the initial goal, so I used the same latest recorded data of 54kg and 12%. 

![Client progress neutral testing](images/testing-images/client-progress-neutral-testing.png)

[Back to top ↑](TESTING.md/#yourptfriend-testing)

- - - 
### DELETE CLIENT FROM RECORDS
![Delete client testing](images/testing-images/delete-client-testing.gif)
The third task choice option (for deleting a client from the records) has been thoroughly tested. The user needs to insert the name of a client that exists in the records and, upon correct insertion of a valid one, the client is successfully removed from the worksheets.

- - - 
### EXIT THE PROGRAM
![Exit the program testing](images/testing-images/exit-program-testing.gif)
When the user selects the fourth option to exit, the program successfully displays the goodbye.
- - -

### USER CONTROL 'ENTER'
!['Enter' user control](images/testing-images/enter-validation-and-next-task.gif)

The 'Enter' input to give some control to the user after the outputs required from each task have been displayed, is correctly validated to only accept the return key(empty string) and successfully calls the _next_task()_ function.

- - - 
## 2) CODE VALIDATION
All the .py files have been passed through the [CI Python Linter Validator](https://pep8ci.herokuapp.com/#) and __no errors__ were returned.

![Python validation main](images/testing-images/ci-python-linter-main.png)

![Python validation tdee formulas](images/testing-images/ci-python-linter-tdee-formulas.png)

[Back to top ↑](TESTING.md/#yourptfriend-testing)
- - -
## 3) BUGS AND FIXES

### - CLIENT AVAILABILITY INPUT BUG
![Availability bug](images/testing-images/workouts-per-week-bug.gif)
While testing all of the inputs when adding a new client to the records and their validations, a bug was found in the client's availability to workouts per week: a __value error__ was triggered when trying to input a letter to check the validation, because of the statement to convert the string into an integer.
Fixed by adding an extra validation to that input to check if the inserted value was not a number and, in that case, prompt the user to a correct value insertion.

### - ACTIVITY LEVEL BUG 
While testing the activity level validations, I noticed that the message to the user to notify the invalidity of the inputted empty string was showing up for only milliseconds (and it was barely interceptable). The issue was coming from the _'clear screen' method set too soon at the start of the While loop_.
Fixed by removing the clearing screen from the while loop and adding it instead, together with some added time, at the beginning of the if statement validating the empty string.
![Activity level bug](images/testing-images/activity-level-bug-1.png)

### - CLIENT'S GOAL INPUT BUG 
Also when testing the validations for the client's goal input, the same error regarding the invalid inputted value message disappearing too soon was noticed:
![Client's goal input bug](images/testing-images/client-goal-input-bug.gif)

Fixed by adding more time to the message showing.

### - CLIENT DATA CONFIRMATION VALIDATION BUG
When checking the validity of the inputted value regarding the confirmation of the new client's data, I noticed that the input request was repeating itself after the screen had been cleaned and the user had no chance to check the client description containing the inserted data anymore:
![Client data confirmation validation bug](images/testing-images/new-client-conf-validation-bug.png)

The issue has been resolved by recalling the client description from the client class before continuing the loop:
![Client data confirmation validation fix](images/testing-images/client-data-confirmation-bug-fix.png)

### - TDEE FORMULA BUG
In the process of testing the reliability of the formulas to calculate the client's TDEE, I found that the TDEE reported in the clients init conditions worksheet weren't right. 
The problem only seemed to happen with female clients, because the male client's result was right:
![TDEE bug](images/testing-images/tdee-bug.png)

Trying to understand where the issue was coming from, I calculated the female clients' TDEE using the male formula for calculating the LBM: this time the result obtained was the same as the one reported in the worksheet.

It was then clear that the problem was coming from the calculate_lbm() function and, particularly, from the "gender" argument passed into the function. Going back to the run.py file and checking the value of the gender variable, I discovered that it didn't match with the value contained in the if statement condition that was checking if the client was female ('f'):
![Gender bug](images/testing-images/gender-bug.png)

Easily fixed by changing the if statement condition with the correct value of the passed argument:
![Gender bug fix](images/testing-images/gender-bug-fix.gif)


[Back to top ↑](TESTING.md/#yourptfriend-testing)
import os
import gspread  # API for google sheets
import sys
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('srs_training_tracker')

skills = SHEET.worksheet('skills')

data = skills.get_all_values()


# print(data)  # shows get data from worksheet is functioning
def clear_screen():
    os.system('clear')


def welcome():
    """
    Welcome title and introduction text
    """
    print('\n+-+-+-+')
    print('|S|R|S|')
    print('+-+-+-+-+-+-+-+-+')
    print('|T|r|a|i|n|i|n|g|')
    print('+-+-+-+-+-+-+-+-+')
    print('|A|p|p|')
    print('+-+-+-+\n')

    print('This app records and reports staff training for all SRS skills\n')
    print('1. You can add a new staff member along with any approved SRS')
    print('skills they have\n')
    print('2. You can update existing staff records when staff achieve')
    print('new skills\n')
    print('3. You can search by:\n')
    print('*SRS skill')
    print('    - who is approved for a particular skill\n')
    print('*Staff member')
    print('    - what skills a particular staff member has\n')
    print('*Full info')
    print('    - All staff and all skills in one table\n')


def welcome_menu():
    """
    Gives 3 options to user: enter new staff member;
        update staff member; search.  Sends user to
        selected menu page after successful input.
        Manages input errors.
    """
    print('MENU OPTIONS\n')
    print('1: Enter a new staff member & add skills')
    print('2: Update skills for an existing staff member')
    print('3: Search records by skill, staff or all\n')

    while True:
        try:
            answer = int(input('Enter 1, 2 or 3 to proceed (or 0 to exit):\n'))
        except ValueError:
            # if entering a letter or other non-number key return to input
            print('please choose a valid option from the menu\n')
            continue
        if answer > 3:
            #  if entering a number not 1-3 or 9, set to return to input
            print('please choose a valid option from the menu\n')
            continue
        break
    if answer == 1:
        print('you answered one')
        clear_screen()
    elif answer == 2:
        print('you answered two')
    elif answer == 3:
        print('you answered three')
    elif answer == 0:
        sys.exit("You are exiting the system")
    #  each option will send user to appropriate new menu/page (add function)


def reg_new_staff():
    """
    Captures new staff name/position details
    & adds to staff worksheet
    """
    print('You have opted to enter a new staff member')
    print('Please enter details with no spaces, numbers or symbols\n')
    fname = input('Enter first name of staff member:\n').lower()
    lname = input('Enter last name of staff member:\n').lower()
    position = input('Enter staff position - Junior, Senior or CS:\n')
    print(f'You entered: {fname} {lname}, {position}')


welcome()
welcome_menu()
reg_new_staff()

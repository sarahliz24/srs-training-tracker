"""
importing python modules
"""
import os
import sys
import gspread  # API for google sheets
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
staff = SHEET.worksheet('staff')
training_log = SHEET.worksheet('training_log')

# data = skills.get_all_values()
# print(data)  # shows get data from worksheet is functioning


def clear_screen():
    """
    Clears screen
    """
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
        reg_new_staff()
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

    while True:
        try:
            fname = input('Enter first name of staff member:\n').upper()
            lname = input('Enter last name of staff member:\n').upper()
            position = input('Enter staff position - \
                            Junior, Senior or CS:\n').upper()
            print(f'You entered: {fname} {lname}; position: {position}')
        except ValueError():
            # if entering a letter or other non-number key return to input
            print('please try again as your entry is invalid\n')
            continue
        else:
            if not fname.isalpha():
                print('please try again as your first name entry is invalid\n')
                continue
            if not lname.isalpha():
                print('please try again as your last name entry is invalid\n')
                continue
            if not position.isalpha():
                print('please try again as your position entry is invalid\n')
                continue
            if position != 'JUNIOR':
                if position != 'SENIOR':
                    if position != 'CS':
                        print('please try again, your position \
                        entry is invalid\n')
                        continue
            answer2 = input('is this information correct (Y or N)?\n').upper()
            if answer2 != 'Y':
                print('Try input again')
            if answer2 == 'Y':
                # False
                clear_screen()
                print('Sending information to worksheet')
                # send info to worksheet
                staff_id = len(staff.get_all_values())
                # gets length of rows in staff spreadsheet
                staff_entry = [staff_id, fname, lname, position]
                staff.append_row(staff_entry)
                print(staff_entry)
                break
        finally:
            print('Staff member entry successful')
            print('Now to update staff skills\n')
            skill_menu()


def skill_menu():
    """
    Gives user list of skills that can be added to staff profile
    Allows user to add skills to staff profile
    """
    skills_list = skills.get_all_values()
    # returns a list of lists from skills worksheet
    skills_dict = {i[0]: i[1] for i in skills_list}
    # converts list to dictionary using dictionary comprehension

    print('SRS SKILLS LIST\n')
    for key in skills_dict:
        print(key, skills_dict[key])
        # loops over dict, prints each key & value on a single line

    print('\n')
    print('Instructions\n')
    print('To add a skill - enter the skill number')

    skill_to_input = str(input('Enter skill number:\n'))
    # takes input from user, converts to string for dictionary use

    for key, value in skills_dict.items():
        if skill_to_input == key:
            print(f'You selected {key}: {value}')
            answer3 = input('is this information correct (Y or N)?\n').upper()
            if answer3 != 'Y':
                print('Try input again')
                clear_screen()
                skill_menu()
            if answer3 == 'Y':
                print('Sending information to worksheet')
                skill_entry = ['', skill_to_input, '']
                training_log.append_row(skill_entry)
                # send info to training log worksheet
                break


welcome()
welcome_menu()

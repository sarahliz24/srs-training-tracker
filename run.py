"""
importing python modules
"""
import os
import sys
import datetime
import gspread  # API for google sheets
from google.oauth2.service_account import Credentials
from tabulate import tabulate

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
    print('1. You can add a new staff member along with any SRS')
    print('   skills they have\n')
    print('2. You can update existing staff records when staff achieve')
    print('   new skills\n')
    print('3. You can search by:')
    print('   *SRS skill')
    print('       - who is approved for a particular skill')
    print('   *Staff member')
    print('       - what skills a particular staff member has')
    print('   *Full info')
    print('       - All staff and all skills in one table\n')


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
        find_staff()
    elif answer == 3:
        print('you answered three')
        search_menu()
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
                clear_screen()
                print('Sending information to worksheet')
                # send info to worksheet
                staff_id = len(staff.get_all_values())
                # gets length of rows in staff spreadsheet
                global staff_entry
                staff_entry = [staff_id, fname, lname, position]
                staff.append_row(staff_entry)
                print(staff_entry)
                print('Staff member entry successful')
                print('Now to update staff skills\n')
                skill_menu(staff_entry)
                return staff_entry


def skill_menu(staff_entry):
    """
    Gives user list of skills that can be added to staff profile
    Allows user to add skills to staff profile
    """
    skills_list = skills.get_all_values()
    # returns a list of lists from skills worksheet
    global skills_dict
    skills_dict = {i[0]: i[1] for i in skills_list}
    # converts list to dictionary using dictionary comprehension

    print('SRS SKILLS LIST\n')
    for key in skills_dict:
        print(key, skills_dict[key])
        # loops over dict, prints each key & value on a single line

    print('\n')
    print('Instructions\n')
    print('To add a skill - enter the skill number')

    user_skill_input(staff_entry)


def entry_date():
    """
    captures date of skill entry
    """
    # now = date.today()


def user_skill_input(staff_entry):
    """
    takes user input, checks validity, stores input in
    training log worksheet
    """
    # skills_list = skills.get_all_values()
    # skills_dict = {i[0]: i[1] for i in skills_list}

    global skill_to_input
    skill_to_input = str(input('Enter skill number:\n'))
    # takes input from user, converts to string for dictionary use
    if int(skill_to_input) <= len(skills.get_all_values()):
        for key, value in skills_dict.items():
            if skill_to_input == key:
                print(f'You selected {key}: {value}')
                answer3 = input('is this correct (Y or N)?\n').upper()
                if answer3 != 'Y':
                    print('\nTry input again')
                    clear_screen()
                    skill_menu(staff_entry)
                if answer3 == 'Y':
                    print('Sending information to worksheet')
                    # send info to skills worksheet
                    date = str(datetime.date.today())
                    skill_entry = [staff_entry[0], skill_to_input, date]
                    training_log.append_row(skill_entry)
                    more_skill_input(staff_entry)
                    break
    else:
        print('\nTry input again - you did not enter a valid number\n')
        skill_menu(staff_entry)

    return skill_to_input


def more_skill_input(staff_entry):
    """
    Give user option to enter further skills
    """
    answer4 = input('Do you want to enter another skill (Y or N)?\n').upper()

    if answer4 != 'Y':
        print('\n Returning to main menu')
        clear_screen()
        welcome_menu()
    if answer4 == 'Y':
        print('Make another selection\n')
        skill_menu(staff_entry)


def find_staff():
    """
    Take user input for staff member to search for
    and return as a list
    """
    print("UPDATE STAFF MEMBER'S SKILLS\n")
    fname_existing = input("Enter first name of staff member:\n")
    # get user to input staff name
    print(f"you entered {fname_existing}. Is this correct?")
    # error handling goes here
    lname_existing = input("Enter last name of staff member:\n")
    print(f"you entered {lname_existing}. Is this correct?")
    # error handling goes here
    global requested_name
    requested_name = [fname_existing.upper(), lname_existing.upper()]
    get_staff_id()
    print('')
    return requested_name


def get_staff_id():
    """
    get staff id
    """
    name_check = staff.get_all_values()
    print('')

    name_check_dict = {i[0]: i[1:3] for i in name_check}
    # converts list to dictionary & assigns staff id as the key
    print('')

    for key, value in name_check_dict.items():
        for i in value:
            if requested_name == value:
                staff_id_found = key
                # print(f'Enter skill for {value[0]} {value[1]}')
                display_staff_skills(staff_id_found)
                # skill_menu(staff_id_found)
                return str(staff_id_found)


def display_staff_skills(staff_id_found):
    """
    displays list of skills assigned to staff member
    """
    t_log = training_log.get_all_values()

    skills_list = skills.get_all_values()
    skills_dict = {i[0]: i[1] for i in skills_list}

    print(
        f"Here is a list of {requested_name[0]} {requested_name[1]}'s")
    print('current skills\n')

    i = 1
    # current_skills = []
    while i < len(t_log):
        if t_log[i][0] == staff_id_found:
            x = t_log[i][1]
            for key, value in skills_dict.items():
                if x in key:
                    print(f'{key} : {value}')
                    # current_skills.append(key)
        i += 1
    # return current_skills

    display_staff_menu()


def display_staff_menu():
    """
    loads menu choices after user views staff skills
    """
    print('\nDo you want to:\n')
    print('1: Search for another staff member')
    print("2: Update this staff member's skills")
    print('0: Return to main menu\n')

    try:
        answer5 = int(input('Enter 1 or 2 to proceed (or 0 to exit):\n'))
    except ValueError:
        # if entering a letter or other non-number key return to input
        print('please choose a valid option from the menu\n')
    else:
        if answer5 > 2:
            #  if entering a number not 1-3 or 9, set to return to input
            print('please choose a valid option from the menu\n')
    if answer5 == 1:
        print('you answered one')
        find_staff()
    elif answer5 == 2:
        skill_menu(staff_entry)
    elif answer5 == 0:
        sys.exit("You are exiting the system")


def check_skill_dupl(skill_to_input, staff_id_found):
    """
    check for skill duplication
    # if skill to input already in display staff skills list,
    return warning to user
    """
    t_log = training_log.get_all_values()

    # skills_list = skills.get_all_values()
    # skills_dict = {i[0]: i[1] for i in skills_list}
    i = 1
    while i < len(t_log):
        if (t_log[i][0] == staff_id_found) & (t_log[i][1] == skill_to_input):
            print("we need to change this")
        i += 1


def search_menu():
    """
    displays menu with options for user to search by
    staff member, skill or all
    """
    print('SEARCH MENU OPTIONS\n')
    print('1: Staff search - displays all skills for a staff member')
    print('2: Skill search - displays all staff members who have a skill')
    print('3: Search all - displays all staff and skills')
    print('0: Return to main menu\n')

    while True:
        try:
            answer = int(input('Enter 1, 2 or 3 to proceed (or 0 to exit):\n'))
        except ValueError:
            # if entering a letter or other non-number key return to input
            print('please choose a valid number option from the menu\n')
        else:
            if answer > 3:
                # if entering a number not 0-3, set to return to input
                print('please choose 0 - 3 from the menu\n')
            if answer == 1:
                print('you answered one')
                find_staff()
                break
            elif answer == 2:
                print('you answered two')
            elif answer == 3:
                print('you answered three')
            elif answer == 0:
                sys.exit("You are exiting the system")
            #  each option will send user to appropriate new menu/page


welcome()
welcome_menu()

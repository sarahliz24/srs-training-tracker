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
    print('1. You can add a new staff member')
    print('2. You can update staff records when staff achieve new skills')
    print('3. You can search by:')
    print('   *SRS skill')
    print('       - who is approved for a particular skill')
    print('   *Staff member')
    print('       - what skills a particular staff member has')
    print('   *Full info')
    print('       - All staff and all skills in one table\n')


def main():
    """
    Gives 3 options to user: enter new staff member;
        update staff member; search.  Sends user to
        selected menu page after successful input.
        Manages input errors.
    """
    print('MENU OPTIONS\n')
    print('1: Enter a new staff member')
    print('2: Update skills for a staff member')
    print('3: Search records by skill, staff or all\n')

    while True:
        try:
            answer = int(input('Enter 1, 2 or 3 to proceed (or 0 to exit):\n'))
        except ValueError:
            # if entering a letter or other non-number key return to input
            print('please choose a number (only) from the menu\n')
            continue
        if answer > 3:
            #  if entering a number not 1-3 or 9, set to return to input
            print('please choose number 0, 1, 2, or 3 from the menu\n')
            continue
        break
    if answer == 1:
        print('you answered one')
        clear_screen()
        reg_new_staff()
    elif answer == 2:
        print('you answered two')
        find_staff()
        get_staff_id()
        display_staff_skills()
        skill_menu()
        user_skill_input()
    elif answer == 3:
        print('you answered three')
        search_menu()
    elif answer == 0:
        sys.exit("You are exiting the system")


def storing_new_staff(fname, lname, position):
    """
    if user confirms entry is correct, assigns staff id,
    sends staff info to workshet
    """
    clear_screen()
    print('Sending information to worksheet')
    # send info to worksheet
    staff_id = len(staff.get_all_values())
    # gets length of rows in staff spreadsheet
    # global staff_entry
    staff_entry = [staff_id, fname, lname, position]
    staff.append_row(staff_entry)
    # print(staff_entry)
    print('Staff member entry successful')
    print('Returning to main menu\n')
    main()


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
            position = input(
                'Enter staff position - Junior, Senior or CS:\n').upper()
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
                storing_new_staff(fname, lname, position)


def skills_dict():
    """
    docsting goes here
    """
    skills_list = skills.get_all_values()
    # returns a list of lists from skills worksheet
    # global skills_dict
    skills_dict1 = {i[0]: i[1] for i in skills_list}
    # converts list to dictionary using dictionary comprehension

    return skills_dict1


def skill_menu():
    """
    Gives user list of skills that can be added to staff profile
    """
    skills1 = skills_dict()

    print('SRS SKILLS LIST\n')
    for key in skills1:
        print(key, skills1[key])
        # loops over dict, prints each key & value on a single line

    print('\n')
    print('Instructions\n')
    print('To add a skill - enter the skill number')


def entry_date():
    """
    captures date of skill entry
    """
    # now = date.today()


def user_skill_input():
    """
    takes user input, checks validity, stores input in
    training log worksheet
    """
    # skills_list = skills.get_all_values()
    # skills_dict = {i[0]: i[1] for i in skills_list}
    staff_id1 = get_staff_id()
    # global skill_to_input
    skill_to_input = str(input('Enter skill number:\n'))
    skills1 = skills_dict()
    # takes input from user, converts to string for dictionary use
    if int(skill_to_input) <= len(skills.get_all_values()):
        for key, value in skills1.items():
            if skill_to_input == key:
                print(f'You selected {key}: {value}')
                answer3 = input('is this correct (Y or N)?\n').upper()
                if answer3 != 'Y':
                    print('\nTry input again')
                    clear_screen()
                    skill_menu()
                if answer3 == 'Y':
                    print('Sending information to worksheet')
                    # send info to skills worksheet
                    date = str(datetime.date.today())
                    skill_entry = [staff_id1, skill_to_input, date]
                    training_log.append_row(skill_entry)
                    more_skill_input()
                    break
    else:
        print('\nTry input again - you did not enter a valid number\n')
        skill_menu()

    # return skill_to_input


def more_skill_input():
    """
    Give user option to enter further skills
    """
    answer4 = input('Do you want to enter another skill (Y or N)?\n').upper()

    if answer4 != 'Y':
        print('\n Returning to main menu')
        clear_screen()
        main()
    if answer4 == 'Y':
        print('Make another selection\n')
        skill_menu()
        user_skill_input()


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
                return staff_id_found


def display_staff_skills():
    """
    displays list of skills assigned to staff member
    """
    t_log = training_log.get_all_values()

    # skills_list = skills.get_all_values()
    # skills_dict = {i[0]: i[1] for i in skills_list}
    skills1 = skills_dict()
    staff_id_found1 = get_staff_id()

    print(
        f"Here is a list of {requested_name[0]} {requested_name[1]}'s")
    print('current skills\n')
    # add error checking if staff have no skills yet

    i = 1
    # current_skills = []
    while i < len(t_log):
        if t_log[i][0] == staff_id_found1:
            xxx = t_log[i][1]
            for key, value in skills1.items():
                if xxx in key:
                    print(f'{key} : {value}')
                    # current_skills.append(key)
        i += 1


def display_staff_menu():
    """
    loads menu choices after user views staff skills
    """
    print('\nDo you want to:\n')
    print('1: Search for another staff member')
    print('0: Return to main menu\n')

    try:
        answer5 = int(input('Enter 1 to proceed (or 0 to exit):\n'))
    except ValueError:
        # if entering a letter or other non-number key return to input
        print('please choose a valid option from the menu\n')
    else:
        if answer5 != 0 or 1:
            #  if entering a number not 0 or 1, set to return to input
            print('please choose a valid option from the menu\n')
    if answer5 == 1:
        print('you answered one')
        find_staff()
        get_staff_id()
        display_staff_skills()
        display_staff_menu()
    else:
        main()


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
    clear_screen()

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
                find_staff()
                get_staff_id()
                display_staff_skills()
                display_staff_menu()
            elif answer == 2:
                print('you answered skill search')
                # get_skill_id()
                # staff_w_skill_id()
                skill_search_result()
            elif answer == 3:
                print('you answered three')
                # search_all()
            elif answer == 0:
                sys.exit("You are exiting the system")
            #  each option will send user to appropriate new menu/page


def get_skill_id():
    """
    gets skill id from user input
    """
    skills1 = skills_dict()
    # print(f"This is from get_skill_id {skills1}")

    for key in skills1:
        print(key, skills1[key])
        # loops over dict, prints each key & value on a single line

    print('\nWhich skill do you want to query?')
    skill_id_key = input("Enter number 1 - 9:\n")
    # print(type(skill_id_key)) = string
    # print(f"skill key is {skill_id_key}")
    # staff_w_skill_id(skill_id_key)
    print(f"Staff with skill number {skill_id_key} are:\n")
    return skill_id_key


def staff_w_skill_id():
    """
    Takes skill id
    Searches training log for staff with that skill id
    Returns list with the relevant staff ids
    """
    skill_id_key = get_skill_id()

    t_log = training_log.get_all_values()

    staff_with_skill = []
    i = 0
    while i < len(t_log):
        if t_log[i][1] == skill_id_key:
            staff_with_skill.extend(t_log[i][0])
            print(f"staff ids with this skill: {staff_with_skill}")
            # returns a list with the staff ids
        i += 1
    return staff_with_skill


def skill_search_result():
    """
    Takes in staff_with_skill, skill_id_key & prints list
    of staff names assigned that skill
    """
    name_check = staff.get_all_values()
    name_check_dict = {i[0]: i[1:4] for i in name_check}

    staff_with_skill1 = staff_w_skill_id()

    i = 0
    while i < len(staff_with_skill1):
        for key, value in name_check_dict.items():
            abc = staff_with_skill1[i]
            if abc in key:
                print(f'{value[0]} {value[1]}, position {value[2]}')
        i += 1


if __name__ == '__main__':
    welcome()
    main()

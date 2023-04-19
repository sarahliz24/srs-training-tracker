"""
importing python modules
"""
import os
import sys
import datetime
from time import sleep
import gspread  # API for google sheets
from google.oauth2.service_account import Credentials
from colorama import init, Fore, Style
init(autoreset=True)

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


def clear_screen():
    """
    Clears screen
    """
    os.system('clear')


def welcome():
    """
    Welcome title and introduction text
    """
    print(Fore.BLUE + Style.BRIGHT + '           +-+-+-+')
    print(Fore.BLUE + Style.BRIGHT + '           |S|R|S|')
    print(Fore.BLUE + Style.BRIGHT + '       +-+-+-+-+-+-+-+-+')
    print(Fore.BLUE + Style.BRIGHT + '      |T|r|a|i|n|i|n|g|')
    print(Fore.BLUE + Style.BRIGHT + '       +-+-+-+-+-+-+-+-+')
    print(Fore.BLUE + Style.BRIGHT + '            |A|p|p|')
    print(Fore.BLUE + Style.BRIGHT + '           +-+-+-+\n')

    print('This app records & reports staff training for all SRS skills\n')
    print('1. You can add a new staff member')
    print('2. You can update staff records when staff achieve skills')
    print('3. You can search by:')
    print('   *SRS skill')
    print('       - who is approved for a particular skill')
    print('   *Staff member')
    print('       - what skills a particular staff member has')


def main():
    """
    Gives 3 options to user: enter new staff member;
    update staff member; search.  Sends user to
    selected menu page after successful input.
    Manages input errors.
    """
    print(Fore.BLUE + Style.BRIGHT + '\nMENU OPTIONS')
    print('1: Enter a new staff member')
    print('2: Update skills for a staff member')
    print('3: Search records by skill or staff\n')

    while True:
        try:
            answer = int(input(Fore.GREEN
                         + 'Enter 1, 2 or 3 to proceed (or 0 to exit):\n'))
        except ValueError:
            # if entering a letter or other non-number key return to input
            print(Fore.RED + 'please choose a number (only) from the menu\n')
            continue
        if answer > 3:
            #  if entering a number not 1-3 or 9, set to return to input
            print(
                Fore.RED + 'Please choose number 0 - 3 from the menu\n')
            continue
        break
    if answer == 1:
        clear_screen()
        reg_new_staff()
    elif answer == 2:
        find_staff()
        get_staff_id()
        display_staff_skills()
        skill_menu()
        user_skill_input()
    elif answer == 3:
        clear_screen()
        search_menu()
    elif answer == 0:
        print(Fore.YELLOW + "You are exiting the system")
        clear_screen()
        sys.exit()


def check_for_duplication(fname, lname, position):
    """
    Checks for duplicate fname/lname combination
    in staff worksheet.  If found sends user back
    to name entry. If no duplication moves to storing
    new staff function
    """
    name_check = staff.get_all_values()
    i = 0
    while i < len(name_check):
        if fname == name_check[i][1] and lname == name_check[i][2]:
            print(Fore.RED + '\n***Duplicate staff entry, try again***\n')
            reg_new_staff()
            break
        i += 1
    storing_new_staff(fname, lname, position)


def storing_new_staff(fname, lname, position):
    """
    stores new staff in worksheet
    """
    clear_screen()
    print('Sending information to worksheet')
    sleep(1)
    staff_id = len(staff.get_all_values())
    staff_entry = [staff_id, fname, lname, position]
    staff.append_row(staff_entry)
    print('Staff member entry successful')
    print('Returning to main menu\n')
    main()


def reg_new_staff():
    """
    Captures new staff name/position details
    & adds to staff worksheet
    """
    print(Fore.BLUE + Style.BRIGHT
          + 'You have opted to enter a new staff member')
    print('Please enter details with no spaces, numbers or symbols\n')

    while True:
        try:
            fname = input(
                'Enter first name of staff member:\n').upper()
            lname = input('Enter last name of staff member:\n').upper()
            position = input(
                'Enter staff position - Junior, Senior or CS:\n').upper()
            print(Fore.GREEN +
                  f'\n You entered: {fname} {lname}; position: {position}')
        except ValueError():
            print(Fore.RED + 'Please try again as your entry is invalid\n')
            continue
        else:
            reg_staff_validation(fname, lname, position)


def reg_staff_validation(fname, lname, position):
    """
    Validates new staff registration entry
    """
    try:
        if not fname.isalpha():
            print(Fore.RED + 'Try again, first name entry is invalid\n')
            reg_new_staff()
        elif not lname.isalpha():
            print(Fore.RED + 'Try again, last name entry is invalid\n')
            reg_new_staff()
        elif not position.isalpha():
            print(Fore.RED + 'Try again, position entry is invalid\n')
            reg_new_staff()
        elif position != 'JUNIOR' and position != 'SENIOR' and \
                position != 'CS':
            print(Fore.RED + 'Try again, position entry is invalid\n')
            reg_new_staff()
    except ValueError:
        print(Fore.RED + 'Try again, entry is invalid\n')
        reg_new_staff()
    else:
        answer2 = input(Fore.GREEN
                        + 'Is this information correct (Y or N)?\n').upper()
        if answer2 != 'Y':
            print(Fore.RED + '\nTry input again')
            reg_new_staff()
        elif answer2 == 'Y':
            check_for_duplication(fname, lname, position)


def skills_dict():
    """
    Creates skills dictionary from skills list for re-use
    """
    skills_list = skills.get_all_values()
    # returns a list of lists from skills worksheet
    skills_dict1 = {i[0]: i[1] for i in skills_list}
    # converts list to dictionary using dictionary comprehension

    return skills_dict1


def skill_menu():
    """
    Gives user list of skills that can be added to staff profile
    """
    skills1 = skills_dict()

    print(Fore.BLUE + Style.BRIGHT + '\nSRS SKILLS LIST\n')
    for key in skills1:
        print(key, skills1[key])
        # loops over dict, prints each key & value on a single line

    print('\n')
    print(Fore.BLUE + Style.BRIGHT + 'Instructions')
    print('To add a skill - enter the skill number\n')


def user_skill_input():
    """
    takes user input, checks validity, stores input in
    training log worksheet
    """
    staff_id1 = get_staff_id()
    skills1 = skills_dict()

    try:
        skill_to_input = (input(Fore.BLUE + Style.BRIGHT
                          + '\nEnter skill number:\n'))

        # skill_to_input_int = int(skill_to_input)
        # convert skill_to_input into integer for use with comparison below

        if int(skill_to_input) <= len(skills.get_all_values()):
            for key, value in skills1.items():
                if skill_to_input == key:
                    print(Fore.GREEN + f'You selected {key}: {value}')
                    answer3 = input(Fore.GREEN +
                                    'is this correct (Y or N)?\n').upper()
                    if answer3 != 'Y':
                        print(Fore.RED + '\nTry input again')
                        clear_screen()
                        display_staff_skills()
                        user_skill_input()
                    if answer3 == 'Y':
                        date = str(datetime.date.today())
                        skill_entry = [staff_id1, skill_to_input, date]
                        vaildation_user_skill_input(skill_entry)
                        training_log.append_row(skill_entry)
                        print('Sending information to worksheet')
                        sleep(1)
                        more_skill_input()
        else:
            print(Fore.RED +
                  '\nTry again - you did not enter a valid number\n')
            user_skill_input()

    except ValueError:
        print(Fore.RED + "You must enter a number only")
        user_skill_input()


def vaildation_user_skill_input(skill_entry):
    """
    Checks if skill entry is a duplicate, sends user
    to more_skill_input if duplicate found
    """
    t_log = training_log.get_all_values()

    i = 0
    while i < len(t_log):
        if t_log[i][0] == skill_entry[0]:
            if t_log[i][1] == skill_entry[1]:
                print(Fore.RED + '\nDuplicate entry, try again')
                more_skill_input()
                break
        i += 1


def more_skill_input():
    """
    Give user option to enter further skills
    """
    answer4 = input(Fore.BLUE + Style.BRIGHT
                    + 'Do you want to enter another skill (Y or N)?\n').upper()

    if answer4 != 'Y':
        print('\n Returning to main menu')
        clear_screen()
        main()
    if answer4 == 'Y':
        print(Fore.BLUE + Style.BRIGHT + 'Make another selection\n')
        skill_menu()
        user_skill_input()


def find_staff():
    """
    Take user input for fname & lname for existing
    staff in worksheet, return as a list
    """
    while True:
        try:
            print(Fore.BLUE + Style.BRIGHT + "\nFIND STAFF MEMBER:\n")
            print('Please enter details with no spaces, numbers or symbols\n')
            fname_existing = input(
                "Enter first name of staff member:\n").upper()
            lname_existing = input(
                "Enter last name of staff member:\n").upper()
        except Exception:
            continue
        else:
            if not fname_existing.isalpha():
                print(Fore.RED + 'Your first name entry is invalid')
                find_staff_breaker()
            if not lname_existing.isalpha():
                print(Fore.RED + 'Your last name entry is invalid')
                find_staff_breaker()
                continue
            break

    global requested_name
    requested_name = [fname_existing, lname_existing]
    get_staff_id()
    return requested_name


def find_staff_breaker():
    """
    If name inputs in find_staff are invalid, gives
    user option to try again or return to main menu
    """
    answer6 = int(input(Fore.GREEN
                  + 'Enter 1 to try again, 0 to go to main menu:\n'))
    if answer6 == 0:
        main()
    elif answer6 == 1:
        find_staff()
    else:
        print(Fore.RED + 'Please choose number 0 or 1 from the menu')
        find_staff_breaker()


def get_staff_id():
    """
   Validates staff id exists (based on requested_name),
   returns user to find_staff if not
    """
    name_check = staff.get_all_values()
    name_check_dict = {i[0]: i[1:3] for i in name_check}
    # converts list to dictionary & assigns staff id as the key
    name_check_values = name_check_dict.values()

    if requested_name in name_check_values:
        for key, value in name_check_dict.items():
            for i in value:
                if requested_name == value:
                    staff_id_found = key
                    return staff_id_found
    else:
        print(Fore.RED + "\nStaff member does not exist, try again\n")
        get_id_breaker()


def get_id_breaker():
    """
    If name inputs in get_staff_id not found, gives
    user option to try again or return to main or
    search menu
    """
    answer7 = int(input(Fore.GREEN
                  + 'Enter 0: main menu, 1: search menu, 2: try again:'))
    if answer7 == 0:
        main()
    elif answer7 == 1:
        search_menu()
    elif answer7 == 2:
        find_staff()
    else:
        print(Fore.RED + 'Please choose number 0 -2 from the menu')
        get_id_breaker()


def display_staff_skills():
    """
    displays list of skills assigned to staff member
    """
    t_log = training_log.get_all_values()

    skills1 = skills_dict()
    staff_id_found1 = get_staff_id()

    clear_screen()

    print(Fore.BLUE +
          f"\nHere is a list of {requested_name[0]} {requested_name[1]}'s")
    print(Fore.GREEN + 'current skills\n')

    key_dict = {}
    i = 1
    while i < len(t_log):
        if t_log[i][0] == staff_id_found1:
            xxx = t_log[i][1]
            for key, value in skills1.items():
                if xxx in key:
                    print(f'{key} : {value}')
                    key_dict[f'{key}'] = 'Add'
        i += 1
    if not key_dict:
        print(Fore.RED + "No skills are assigned to this staff member\n")


def display_staff_menu():
    """
    loads menu choices after user views staff skills
    """
    print(Fore.BLUE + Style.BRIGHT + '\nDo you want to:\n')
    print('1: Search for another staff member')
    print('2: Add skills for this staff member')
    print('0: Return to main menu\n')

    try:
        answer5 = int(input('Enter 1 or 2 to proceed (or 0 for main menu):\n'))
        if answer5 == 1:
            find_staff()
            get_staff_id()
            display_staff_skills()
            display_staff_menu()
        if answer5 == 2:
            skill_menu()
            user_skill_input()
        if answer5 == 0:
            main()
    except ValueError:
        # if entering a letter or other non-number key return to input
        print(Fore.RED + 'please choose a valid option from the menu\n')
    else:
        if answer5 != 0 or 1 or 2:
            #  if entering a number not 0 or 1, set to return to input
            print(Fore.RED + 'please choose a valid option from the menu\n')


def search_menu():
    """
    displays menu with options for user to search by
    staff member, skill or all
    """
    # clear_screen()

    while True:
        try:
            print(Fore.BLUE + Style.BRIGHT + 'SEARCH MENU OPTIONS\n')
            print('1: Staff search - displays all skills for a staff member')
            print('2: Skill search - displays all staff members with skill')
            print('0: Return to main menu\n')
            answer = int(input(Fore.GREEN + 'Enter 0, 1 or 2 to proceed:\n'))
        except ValueError:
            # if entering a letter or other non-number key return to input
            print(Fore.RED +
                  'Please choose a valid number option from the menu\n')
        else:
            if answer > 2:
                # if entering a number not 0-2, set to return to input
                print(Fore.RED + '\nPlease choose 0 - 2 from the menu\n')
            if answer == 1:
                find_staff()
                get_staff_id()
                display_staff_skills()
                display_staff_menu()
            elif answer == 2:
                print('\nSKILL SEARCH\n')
                skill_search_result()
            elif answer == 0:
                main()


def get_skill_id():
    """
    Gets skill id from user input
    """
    skills1 = skills_dict()

    for key in skills1:
        print(key, skills1[key])
        # loops over dict, prints each key & value on a single line

    print(Fore.GREEN + '\nWhich skill do you want to query?')

    while True:
        try:
            skill_id_key = int(input(Fore.GREEN + "Enter number 1 - 9:\n"))
        except ValueError:
            print('Please enter a number only\n')
            continue
        else:
            if skill_id_key < 0 or skill_id_key > 9:
                print('Please enter number 1 - 9\n')
                continue
        break

    print(f"\nStaff with skill number {skill_id_key} are:\n")

    return str(skill_id_key)


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
            # returns a list with the staff ids
        i += 1

    if not staff_with_skill:
        print(Fore.RED
              + "There are no staff registered with this skill\n")
        # sleep(3)
        search_menu()
    else:
        return staff_with_skill


def skill_search_result():
    """
    Takes in staff_with_skill, skill_id_key & prints list
    of staff names assigned that skill
    """
    name_check = staff.get_all_values()
    name_check_dict = {i[0]: i[1:4] for i in name_check}
    print(name_check_dict)

    staff_with_skill1 = staff_w_skill_id()
    print(staff_with_skill1)

    # try:
    # if staff_with_skill1 in name_check_dict.items():
    i = 0
    while i < len(staff_with_skill1):
        for key, value in name_check_dict.items():
            abc = staff_with_skill1[i]
            if abc in key:
                print(f'{value[0]} {value[1]}, position: {value[2]}')
        i += 1
    print('')
    # except TypeError:
    # skill_search_result()
    # else:
    # print(Fore.RED + "No staff are assigned this skill\n")


if __name__ == '__main__':
    welcome()
    main()

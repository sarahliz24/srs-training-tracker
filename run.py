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

data = skills.get_all_values()

# print(data)  # shows get data from worksheet is functioning


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


welcome()

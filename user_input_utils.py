import requests

my_art = """ .oooooo..o                      o8o                            oooooooooo.                        oooo        
d8P'    `Y8                      `"'                            `888'   `Y8b                       `888        
Y88bo.      oo.ooooo.  oooo d8b oooo  ooo. .oo.    .oooooooo     888     888  .oooo.   ooo. .oo.    888  oooo  
 `"Y8888o.   888' `88b `888""8P `888  `888P"Y88b  888' `88b      888oooo888' `P  )88b  `888P"Y88b   888 .8P'   
     `"Y88b  888   888  888      888   888   888  888   888      888    `88b  .oP"888   888   888   888888.    
oo     .d8P  888   888  888      888   888   888  `88bod8P'      888    .88P d8(  888   888   888   888 `88b.  
8""88888P'   888bod8P' d888b    o888o o888o o888o `8oooooo.     o888bood8P'  `Y888""8o o888o o888o o888o o888o 
             888                                  d"     YD                                                    
            o888o                                 "Y88888P'         """


def bad_word_list():
    """ Scrapes a list of bad words from 'https://www.cs.cmu.edu/~biglou/resources/bad-words.txt'"""
    url = 'https://www.cs.cmu.edu/~biglou/resources/bad-words.txt'
    r = requests.get(url)
    bad_words = [w for w in r.text.split()]
    return bad_words


def collect_accounts_info():
    """ Collects user information needed to open a new bank account."""
    account_type = input('Please enter the account type \n Checking or Savings? \n').lower()
    first_name = input('Please enter your first name. \n')
    last_name = input('Please enter your last name. \n')
    address = input('Please enter your address. Format: Street, Apt, City, State \n')
    age = input('Please enter your age. \n')

    return [account_type, first_name, last_name, address, age]


def validate_accounts_info(new_user_info):
    """ Validates user information needed to open a new bank account."""
    if new_user_info[0].lower() not in ['checking', 'savings']:
        return 'Invalid Account type found, please try again!'
    if any(x.lower() in bad_word_list() for x in [new_user_info[1], new_user_info[2]]):
        return 'Inappropriate vocabulary found in name, please try again!'
    if len(new_user_info[3]) < 8:
        return 'Please input full address, please try again!'

    try:
        new_user_info[4] = int(new_user_info[4])
    except ValueError:
        return 'Please input a numerical value for age.'

    if new_user_info[4] < 18:
        return 'Sorry minors cannot obtain bank accounts.'

    return 'passed'


def collect_services_info():
    """ Collects user information needed for a loan or credit card."""
    print('Thanks for applying, the following information is needed in order to continue with your application.')
    credit_score = input('Please enter your current credit score. \n')
    income = input('Please enter your yearly income. \n')
    first_name = input('Please enter your first name. \n')
    last_name = input('Please enter your last name. \n')
    address = input('Please enter your address. Format: Street, Apt, City, State \n')
    age = input('Please enter your age. \n')

    return [credit_score, income, first_name, last_name, address, age]


def validate_services_info(new_user_info):
    """ Validates user information needed to apply for a loan or credit card."""
    try:
        new_user_info[0] = int(new_user_info[0])
    except ValueError:
        return 'Please input a numerical value for credit score. Please reapply.'
    if new_user_info[0] < 300 or new_user_info[0] > 850:
        return 'Invalid Credit Score, score must fall between 300 and 850! Please reapply.'

    try:
        new_user_info[1] = float(new_user_info[1])
    except ValueError:
        return 'Please input a numerical value for income. Please reapply.'
    if new_user_info[1] < 0:
        return 'Please input a positive numerical value for income. Please reapply.'

    if any(x.lower() in bad_word_list() for x in [new_user_info[2], new_user_info[3]]):
        return 'Inappropriate vocabulary found in name, please try again!'

    if len(new_user_info[4]) < 8:
        return 'Please input full address, please try again!'

    try:
        new_user_info[5] = int(new_user_info[5])
    except ValueError:
        return 'Please input a numerical value for age.'
    if new_user_info[5] < 18:
        return 'Sorry minors cannot obtain our services.'

    return 'passed'

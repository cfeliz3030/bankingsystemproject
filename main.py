from bank import BankAccount, Services
from customers import Customer
from user_input_utils import my_art, validate_accounts_info, validate_services_info, \
    collect_services_info, collect_accounts_info

print(my_art)

print('\nHi, Welcome to Spring Bank!\n')

active_session = True
logged_in = False
user = None

while active_session:
    is_existing_customer = input('Are you an existing customer? Yes or No.\n').lower()

    if is_existing_customer == 'yes':
        user_id, user_pin = input(
            "Thank you, please enter your account id and account pin separated by a ','\n").split(',')
        user = Customer(user_id=user_id, account_pin=user_pin)
        if user.correct_credentials():
            print('Thanks, you have logged in successfully! \n')
            logged_in = True
            active_session = False
        else:
            active_session = False
    elif is_existing_customer == 'no':
        new_customer_choice = input('Would you like to open a new bank account? \nPress 1 \nFor more '
                                    'services...\nPress 2 \n')
        if new_customer_choice == '1':
            new_account_info = collect_accounts_info()
            if validate_accounts_info(new_account_info) == 'passed':
                user = BankAccount(new_account_info[0], new_account_info[1], new_account_info[2], new_account_info[3],
                                   new_account_info[4])
                user.insert_customer()
                user.insert_account()
                print(user.account_credentials(), "\nYou'll need to log back in as an "
                                                  "existing user.")
            else:
                print(validate_accounts_info(new_account_info))
                active_session = False
        elif new_customer_choice == '2':
            print('Here at Spring Bank, we also offer personal loans and credit cards...')
            services = input('For personal loans, \nPress 1 \nFor credit cards \nPress 2 \nElse session will end. \n')
            if services == '1':
                services_info = collect_services_info()
                if validate_services_info(services_info) == 'passed':
                    user = Services(services_info[0], services_info[1], services_info[2], services_info[3],
                                    services_info[4], services_info[5])
                    total_loan = input('What is the loan amount? \n')
                    try:
                        user.loan_amount = float(total_loan)
                    except ValueError:
                        print('Please provide a valid numerical input for loan amount!')

                    term_length = input('How long will you need to repay the loan (years) ? \n')
                    try:
                        user.term = int(term_length)
                    except ValueError:
                        print('Please provide a valid numerical input for loan term!')

                    if user.get_loan():
                        user.insert_customer()
                        user.insert_loan()
                        active_session = False
                    else:
                        active_session = False
                else:
                    print(validate_services_info(services_info))

            elif services == '2':
                services_info = collect_services_info()
                if validate_services_info(services_info) == 'passed':
                    user = Services(services_info[0], services_info[1], services_info[2], services_info[3],
                                    services_info[4], services_info[5])
                    if user.get_credit_card():
                        user.insert_customer()
                        user.insert_credit_card()
                        active_session = False
                    else:
                        active_session = False
                else:
                    print(validate_services_info(services_info))

            else:
                active_session = False
    else:
        print('Unknown input provided, goodbye!')
        active_session = False

while logged_in:

    existing_customer_choice = input('What would you like to do next? \n 1 - Check Balance \n 2 - Withdraw \n 3 - '
                                     'Deposit \n 4 - End '
                                     'Session \n').lower()

    if existing_customer_choice == '1':
        print(f'Account Balance: ${user.current_acc_value()}')
    elif existing_customer_choice == '2':
        withdraw_amount = input('How much would you like to withdraw? \n')
        try:
            user.amount = float(withdraw_amount)
            print(user.withdraw_query())
        except ValueError:
            print('Please provide a valid numerical input!')
    elif existing_customer_choice == '3':
        deposit_amount = input('How much would you like to deposit? \n')
        try:
            user.amount = float(deposit_amount)
            print(user.deposit_query())
        except ValueError:
            print('Please provide a valid numerical input!')
    elif existing_customer_choice == '4':
        end = input('Would you like to end this session? \n Yes or No \n').lower()
        if end == 'yes':
            print('Thank you, have a great day!')
            logged_in = False

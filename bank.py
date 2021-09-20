from customers import Customer, logger
import uuid
from datetime import date
from db_utils import MyDB
import random


class BankAccount(Customer):
    """
    A class that creates a new bank account for a customer, and provides account log-in credentials
    This class uses values(first_name,last_name,address,age) from Customer class in order to create a new bank account.
    """
    def __init__(self, account_type, first_name, last_name, address, age):
        """
        Constructs necessary attributes for creating a new bank account.
        :param account_type: str
        :param first_name: str
        :param last_name: str
        :param address: str
        :param age: int
        :param balance: float
        :param account_pin: int
        """
        super().__init__(first_name, last_name, address, age, user_id=str(uuid.uuid4().fields[-1])[:5])
        self.account_type = account_type
        self.balance = 0
        self.account_pin = random.randint(1000, 9999)

    def account_credentials(self):
        """ Provides customer with bank account log-in credentials."""
        return f"""The following lines will be your log-in credentials, do not share with anyone... \nid number:{self.user_id}\npin number:{self.account_pin} """

    def insert_account(self):
        """ Inserts newly created bank account into 'accounts' table."""
        logger.info('Opening a new bank account for customer.')
        sql = """
        insert into accounts(id,balance,account_type,account_pin)
        values(%s,%s,%s,%s)"""
        recs = (self.user_id, self.balance, self.account_type, self.account_pin)

        db = MyDB()
        db.insert_query(sql, recs)
        logger.info('Account for customer was successfully created.')

        return 'Account added to database.'


class Services(Customer):
    """
    A class that provides a new customer with other bank services. A customer can apply for either a loan or credit
    card.
    """

    def __init__(self, credit_score, income, first_name, last_name, address, age, loan_amount=None, term=None):
        """
        Constructs all the necessary attributes needed in order to apply for a loan or credit card.
        :param credit_score: int
        :param income: int
        :param first_name: str
        :param last_name: str
        :param address: str
        :param age: int
        :param loan_amount: float
        :param term: int
        """
        super().__init__(first_name, last_name, address, age, user_id=str(uuid.uuid4().fields[-1])[:5])
        self.credit_score = credit_score
        self.income = income
        self.loan_amount = loan_amount
        self.term = term

    def calculate_interest_rate_loan(self):
        """ This function uses a customers credit score in order to calculate their interest rate for a loan"""
        if type(self.credit_score) != str and 300 <= self.credit_score <= 850:
            if self.credit_score < 500:
                interest_rate = False
            elif self.credit_score < 550:
                interest_rate = 0.12
            elif self.credit_score < 750:
                interest_rate = 0.08
            else:
                interest_rate = 0.05
        else:
            print('Invalid Credit Score, score must fall between 300 and 850!')
            return False
        return interest_rate

    # https://www.bankrate.com/loans/personal-loans/how-to-calculate-loan-interest/

    def calculate_interest_rate_cc(self):
        """ This function uses a customers credit score in order to calculate their interest rate for a credit card."""
        if type(self.credit_score) != str and 300 <= self.credit_score <= 850:
            if self.credit_score < 500:
                interest_rate = False
            elif self.credit_score < 550:
                interest_rate = 0.25
            elif self.credit_score < 750:
                interest_rate = 0.20
            else:
                interest_rate = 0.15
        else:
            print('Invalid Credit Score, score must fall between 300 and 850!')
            return False
        return interest_rate

    def calculate_credit_limit(self):
        """ This function uses a customers income in order to calculate their credit line for a credit card"""
        if type(self.income) != str and self.income > 0:
            if 500 <= self.income <= 20000:
                credit_limit = 500
            elif self.income < 45000:
                credit_limit = 5000
            else:
                credit_limit = 10000
        else:
            print('Invalid income format please provide a positive numerical input!')
            return False
        return credit_limit

    def get_loan(self):
        """ Approves or denies customer a loan using credit score"""
        logger.info('Preparing to provide a loan service to customer.')
        if not self.calculate_interest_rate_loan():
            print('Sorry based on your credit score your request for a loan has been denied.')
            logger.info('Customer failed loan requirements.')
            return False
        elif any(type(i) == str or i < 0 for i in [self.loan_amount, self.term]):
            return 'Please provide a positive numerical value for loan amount and term.'
        else:
            print('Generating loan, please wait...')
            interest_amount = self.loan_amount * self.calculate_interest_rate_loan() * self.term
            total_loan = interest_amount + self.loan_amount
            print(f'Based on your credit score of {self.credit_score} you will pay ${interest_amount} '
                  f'in interest for the loan.')
            print(f'Congratulations your loan of ${self.loan_amount} over {self.term} years with an '
                  f'interest rate of {self.calculate_interest_rate_loan()} has been approved!')
            print('Your loan will be transferred within a couple of days.')
            logger.info('Customer passed loan requirements.')
            return True

    def insert_loan(self):
        """ Insert customer loan information into 'loans' table."""
        sql = """
        insert into loans(id,loan_amount,term,origin_date,interest_rate)
        values(%s,%s,%s,%s,%s)"""
        recs = (self.user_id, self.loan_amount, self.term, self.loan_date(), self.calculate_interest_rate_loan())

        db = MyDB()
        db.insert_query(sql, recs)

        return 'Loan added to database.'

    def get_credit_card(self):
        """ Approves or denies customer for a credit card using income and credit score."""
        logger.info('Preparing to provide credit card service to customer.')
        if not self.calculate_interest_rate_cc() or not self.calculate_credit_limit():
            print('Sorry based on your credit score or income your request for a credit card has been denied.')
            logger.info('Customer failed credit card requirements.')
            return False
        else:
            print('Generating credit card, please wait...')
            print(f'Based on your credit score and income, you have been approved for a '
                  f'credit card with a starting limit of ${self.calculate_credit_limit()}. Your new credit card will '
                  f'be delivered within 5 business days.')
            logger.info('Customer passed credit card requirements.')
            return True

    def insert_credit_card(self):
        """ Insert customer credit card information into 'credit_cards' table."""
        sql = """
        insert into credit_cards(id,credit_line,origin_date,interest_rate)
        values(%s,%s,%s,%s)"""
        recs = (self.user_id, self.calculate_credit_limit(), self.loan_date(), self.calculate_interest_rate_cc())

        db = MyDB()
        db.insert_query(sql, recs)

        return 'Credit Card added to database.'

    @staticmethod
    def loan_date():
        return str(date.today())



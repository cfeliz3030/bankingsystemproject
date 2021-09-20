import logging
import uuid
from datetime import date, datetime
from db_utils import MyDB

# create logger object to record customer interactions
logger = logging.getLogger(__name__)
file = logging.FileHandler('customers.log', mode='a')
logger.setLevel(logging.INFO)
special_format = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file.setFormatter(special_format)
logger.addHandler(file)


class Customer:
    """
    A class to represent a new or returning customer. If you are creating a new customer the only attributes needed
    are the customers first name, last name, address and age. Otherwise if you are a returning customer the only
    attributes needed are user_id and account_pin. After logging-in, a customer can interact with their bank account.
    """
    def __init__(self, first_name=None, last_name=None, address=None, age=None, user_id=None, account_pin=None,
                 amount=None):
        """
        Constructs necessary attributes for new and existing customer.

        :param first_name: str
        :param last_name: str
        :param address: str
        :param age: int
        :param user_id: int, If user_id is not passed new user_id is generated
        :param account_pin: int
        :param amount: float
        """

        self.first = first_name
        self.last = last_name
        self.address = address
        self.age = age
        self.user_id = user_id if user_id else str(uuid.uuid4().fields[-1])[:5]
        self.account_pin = account_pin
        self.amount = amount

    @property
    def full_name(self):
        """ Returns customer fullname"""
        return self.first + ' ' + self.last

    @staticmethod
    def account_date():
        """generates account open date"""
        return str(date.today())

    @staticmethod
    def transaction_id():
        """generates transaction unique identifier"""
        uuid.uuid4()
        return str(uuid.uuid4().fields[-1])[:8]

    @staticmethod
    def trans_date():
        """generates transaction timestamp"""
        return datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    def insert_customer(self):
        """ Insert customer information into customers table"""
        logger.info('Creating new customer.')
        sql = """
        insert into customers(id,name,address,age,member_since)
        values(%s,%s,%s,%s,%s)"""
        recs = (self.user_id, self.full_name, self.address, self.age, self.account_date())

        db = MyDB()
        db.insert_query(sql, recs)
        logger.info('Customer added to database.')
        return 'Customer added to database.'

    def correct_credentials(self):
        """ Validate users account log-in credentials using 'accounts' table """
        logger.info('Checking User credentials')
        sql = ''' select * from accounts
                    where id = %s and account_pin = %s'''
        values = (self.user_id, self.account_pin)

        db = MyDB()
        creds = db.fetch_one_query(sql, values)
        if creds:
            logger.info('User credentials passed.')
            return True
        else:
            logger.error(f'Incorrect account id or pin, please try again!, Account ID Entered: {self.user_id}')
            print(f'Incorrect account id or pin, please try again!, Account ID Entered: {self.user_id}')
            return False

    def current_acc_value(self):
        """ Queries 'accounts' table and returns user account balance"""
        sql = ''' select balance from accounts
            where id = %s and account_pin = %s'''
        values = (self.user_id, self.account_pin)

        db = MyDB()
        balance = db.fetch_one_query(sql, values)

        if balance:
            return balance[0]

        return 'Account balance not found.'

    def withdraw_query(self):
        """ Allows a customer to withdraw money from their account. If withdrawal is valid, the
        account balance is updated and a transaction log is generated."""
        logger.info(f'User is going to withdraw money.')

        if type(self.amount) == str or self.amount <= 0:
            return 'Please enter a numerical positive value!'

        elif self.current_acc_value() < self.amount:
            logger.info(f'Withdrawal Failed:insufficient funds')
            return 'Sorry insufficient funds!'

        else:
            f'Withdrawing ${self.amount} from bank account.'

            sql = ''' update accounts set balance = %s
                where id = %s and account_pin = %s'''
            values = (self.current_acc_value() - self.amount, self.user_id, self.account_pin)

            log_trans = ''' insert into transactions(account_id,transaction_id,transaction_type,transaction_date,amount)
                values(%s,%s,%s,%s,%s)'''
            recs = (self.user_id, self.transaction_id(), 'Withdraw', self.trans_date(), self.amount)

            db = MyDB()
            db.insert_query(sql, values, close_conn=False)
            db.insert_query(log_trans, recs)
            logger.info(f'User withdrawal successful.')
            return f'Account balance updated!\nNew Balance: ${self.current_acc_value()}'

    def deposit_query(self):
        """ Allows a customer to deposit money from their account. If deposit is valid, the
                account balance is updated and a transaction log is generated."""
        logger.info(f'User is going to deposit money.')

        if type(self.amount) == str or self.amount <= 0:
            logger.info(f'Deposit Failed: invalid value {self.amount}')
            return 'Please enter a numerical positive value!'

        else:
            f'Depositing ${self.amount} into bank account.'

            sql = ''' update accounts set balance = %s
            where id = %s and account_pin = %s'''
            values = (self.current_acc_value() + self.amount, self.user_id, self.account_pin)

            log_trans = ''' insert into transactions(account_id,transaction_id,transaction_type,transaction_date,amount)
                values(%s,%s,%s,%s,%s)'''
            recs = (self.user_id, self.transaction_id(), 'Deposit', self.trans_date(), self.amount)

            db = MyDB()
            db.insert_query(sql, values, close_conn=False)
            db.insert_query(log_trans, recs)
            logger.info(f'User deposit successful.')
            return f'Account balance updated!\nNew Balance: ${self.current_acc_value()}'

    def close_account(self):
        """Allows a customer to close their account"""
        logger.info(f'Preparing to delete Account ID: {self.user_id}.')
        sql = '''DELETE FROM accounts WHERE id='%s'
        '''
        values = (self.user_id,)

        db = MyDB()
        db.delete_query(sql, values)

        logger.info(f'Account ID: {self.user_id} has been deleted by user.')
        return 'Account deleted!'



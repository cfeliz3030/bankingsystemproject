import logging
import psycopg2

# create logger to log all interactions with database
logger = logging.getLogger(__name__)
file = logging.FileHandler('db.log', mode='a')
logger.setLevel(logging.INFO)
special_format = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file.setFormatter(special_format)
logger.addHandler(file)

# please input database credentials below
host = 'host'
port = 'port'
user = 'user'
password = 'password'
database = 'database'


class MyDB:
    """ This class creates a connection to a database, and contains functionality for CRUD operations"""
    def __init__(self):
        self.db_connection = psycopg2.connect(host=host, user=user, password=password, database=database, port=port)
        self.db_cur = self.db_connection.cursor()

    def insert_query(self, query, values, close_conn=True):
        """ Inserts records into a database"""
        logger.info(f'Inserting Records:{values} into {database}')
        if close_conn:
            try:
                self.db_cur.execute(query, values)
                self.db_connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                self.db_cur.close()
        else:
            try:
                self.db_cur.execute(query, values)
                self.db_connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        return logger.info(f'Insert Records successful.')

    def delete_query(self, query, values):
        """ Removes records from a database"""
        logger.info(f'Deleting Records:{values} from {database}')
        try:
            self.db_cur.execute(query, values)
            self.db_connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.db_cur.close()
        return logger.info(f'Records Deleted:{values}')

    def fetch_all_query(self, query, values=None):
        """ Returns all records from a table"""
        table_data = self.db_cur.execute(query, values)
        table_data = self.db_cur.fetchall()
        return table_data

    def fetch_one_query(self, query, values=None):
        """ Returns a single record from a table"""
        table_data = self.db_cur.execute(query, values)
        table_data = self.db_cur.fetchone()
        return table_data

    def create_table(self, query, close_conn=True):
        """ Creates a new table"""
        logger.info(f'Inserting new table into {database}')
        if close_conn:
            try:
                self.db_cur.execute(query)
                self.db_connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                self.db_cur.close()
        else:
            try:
                self.db_cur.execute(query)
                self.db_connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        return logger.info(f'New table added into {database}')


# create database connection instance
db = MyDB()

# The code found below is used to generate multiple tables needed in database.

# create Customers
sql = """ create table customers(
id int not null primary key,
name varchar(40),
address varchar(40),
age int,
member_since date
)
 """
db.create_table(sql,close_conn=False)


# create Accounts
sql = """ create table accounts(
id int not null primary key,
balance float,
account_type varchar(40),
account_pin int
)
 """
db.create_table(sql, close_conn=False)

# create Loans
sql = """ create table loans(
id int not null primary key,
loan_amount float,
term int,
origin_date date,
interest_rate float
)
 """
db.create_table(sql, close_conn=False)

# create Credit cards
sql = """ create table credit_cards(
id int not null primary key,
credit_line float,
origin_date date,
interest_rate float
)
 """
db.create_table(sql, close_conn=False)

# create Transactions
sql = """ create table transactions(
transaction_id int not null primary key,
account_id int,
amount float,
transaction_type varchar(40),
transaction_date date
)
 """
db.create_table(sql)




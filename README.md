# Banking System Project


## Built With
Python 3.6

## Prerequisites
* Create AWS account
https://aws.amazon.com/
* psycopg2
```pip install psycopg2```
* requests
```pip install requests```

## Installation
* Setup AWS RDS(Postgres) database
https://www.youtube.com/watch?v=RerDL93sBdY&t=833s
* Clone the repo
``` git clone https://github.com/cfeliz3030/bankingsystemproject.git ```
* Gather database credentials from AWS and enter into 'db_utils.py'
```
# please input database credentials below 
host = 'host' 
port = 'port'
user = 'user'
password = 'password'
database = 'database' 
```

## Requirements
* Python 3.6+
* AWS Account
* AWS RDS Database

## Usage
* After entering database credentials, run 'db_utils.py'. This script will generate the tables needed for storing data.
``` python3 db_utils.py ```
* Run 'user_input_utils.py' to create utility functions needed for 'main.py'.
``` python3 user_input_utils.py```
* Run 'customers.py' and 'bank.py' to create Customer, Account, and Services classes.
``` python3 customers.py ```
``` python3 bank.py ```
* Lastly, we can run 'main.py' to start the banking system.
``` python3 main.py```

The first output should look like this...
![Screen Shot 2021-09-19 at 8 49 25 PM](https://user-images.githubusercontent.com/60493376/133962525-bd1b26c6-73aa-4665-a362-cce7c108d09e.png)

Further examples below:

If the user would like to open a new account.

![Screen Shot 2021-09-19 at 8 55 07 PM](https://user-images.githubusercontent.com/60493376/133962664-8aeffb13-77f5-4dc1-a4d4-2fe6128eabd5.png)

If the user would like to apply for a loan.

![Screen Shot 2021-09-19 at 8 53 34 PM](https://user-images.githubusercontent.com/60493376/133962727-ec71d3a1-2cc1-4d3e-a5a0-fba5a09a70cb.png)

Please note, two separate log files will also be generated along 'main.py'. A 'customers.log' tracking all of the customers interactions, and a 'db.log' which tracks any database interactions.

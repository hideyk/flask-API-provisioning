import psycopg2 as pg
import psycopg2.extras as pg_extras
from psycopg2 import OperationalError
import yaml
import os

# DB configurations
db_config_file = "db.yml"
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, db_config_file)) as f:
    db_config = yaml.load(f, Loader=yaml.FullLoader)


def create_connection():
    connection = None
    try:
        connection = pg.connect(
            database=db_config['DATABASE'],
            user=db_config['USER'],
            password=db_config['PASS'],
            host=db_config['HOST'],
        )
        connection.set_session(autocommit=True)
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


# Check if there is existing record with username in users table
def check_user_exists(username):
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT firstName from users WHERE username=%s", [username])
        if cur.fetchall():
            return True
        else:
            return False


# Check if there is existing record with phonenumber in users table
def check_number_exists(phonenumber):
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT firstName from users WHERE phonenumber=%s", [phonenumber])
        if cur.fetchall():
            return True
        else:
            return False


# Create a new user
def create_new_user(username, firstname, lastname, phonenumber):
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO users (username, firstname, lastname, phonenumber)
                        VALUES (%s, %s, %s, %s)""", (username, firstname, lastname, phonenumber))
    return {
        "username": username,
        "firstname": firstname,
        "lastname": lastname,
        "phonenumber": phonenumber
    }


# Show details for a particular user
def show_user(username):
    conn = create_connection()
    with conn.cursor(cursor_factory = pg_extras.DictCursor) as cur:
        cur.execute("SELECT username, firstname, lastname, balance, phonenumber FROM users WHERE username=%s", [username])
        user_details = cur.fetchone()
    return {
        "username": user_details[0],
        "firstname": user_details[1],
        "lastname": user_details[2],
        "balance": user_details[3],
        "phonenumber": user_details[4]
    }


# Show all users in users table
def show_all_users():
    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute("""SELECT username, firstname, lastname, balance, phonenumber FROM users""")
        users = cur.fetchall()
    result = []
    for user in users:
        user_details = {
            "username": user[0],
            "firstname": user[1],
            "lastname": user[2],
            "balance": user[3],
            "phonenumber": user[4]
        }
        result.append(user_details)
    return result


# Show balance for a particular user
def show_balance(username):
    if not check_user_exists(username):
        return (403, f"User {username} does not exist.")

    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT balance FROM users WHERE username=%s", [username])
        balance = cur.fetchone()
    return balance[0]


# Update balance for a particular user
def update_balance(username, amount):
    if not check_user_exists(username):
        return (403, f"User {username} does not exist.")

    conn = create_connection()
    with conn.cursor() as cur:
        cur.execute("UPDATE users SET balance=%s WHERE username=%s;", (amount, username))
    return amount


# print(show_all_users())
# print(show_balance('hidey'))
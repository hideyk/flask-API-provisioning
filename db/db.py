import psycopg2 as pg
from psycopg2 import OperationalError
import yaml

# DB configurations
config_file = "./db.yml"
with open(config_file) as f:
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
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def check_user_exists(username):
    conn = create_connection()
    conn.set_session(autocommit=True)
    with conn.cursor() as cur:
        cur.execute("SELECT firstName from users WHERE username=%s", [username])
        if cur.fetchall():
            return True
        else:
            return False

def check_number_exists(phonenumber):
    conn = create_connection()
    conn.set_session(autocommit=True)
    with conn.cursor() as cur:
        cur.execute("SELECT firstName from users WHERE phonenumber=%s", [phonenumber])
        if cur.fetchall():
            return True
        else:
            return False

def create_new_user(username, firstname, lastname, phonenumber):
    if check_user_exists(username):
        return (403, f"User {username} already exists.")
    
    if check_number_exists(phonenumber):
        return (403, f"Phone number {phonenumber} already registered.")
    
    conn = create_connection()
    conn.set_session(autocommit=True)
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO users (username, firstname, lastname, phonenumber)
                        VALUES (%s, %s, %s, %s)""", (username, firstname, lastname, phonenumber))
    return (200, f"{username} user inserted.")

result = create_new_user('hidasdey', 'hideyuki', 'kanazawa', 98184007)
print(result)
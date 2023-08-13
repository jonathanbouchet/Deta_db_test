import streamlit as st
from typing import Any
import datetime
from deta import Deta

DETA_KEY = st.secrets['DETA_KEY']
DETA_DB_table_name = st.secrets['DETA_DB_table_name']

# initialize DETA
deta = Deta(DETA_KEY)
db = deta.Base(DETA_DB_table_name)


def update_config():
    """
    update config by reading database in order to all updates users
    :return: tmp_config
    """
    # auth cookies parameters
    cookie_expiry_days = 0
    cookie_key = "my_random_key"
    cookie_name = "random_cookie_name"
    pre_authorized: list[Any] = []

    credentials_from_db = retrieve_db_credentials(db)
    print(f"config from DB:{credentials_from_db}")

    # overwrite config for updating later on
    tmp_config = {
        'cookie': {'expiry_days': 0, 'key': 'my_random_key', 'name': 'random_cookie_name'},
        'credentials': credentials_from_db,
        'preauthorized': {'email': pre_authorized}
    }
    print(f"overwritten config:{tmp_config}")
    return tmp_config

def fetch_db(db) -> list:
    """
    fetch Deta database collection
    :param db:
    :return:
    """
    users = db.fetch()
    print(f"fetched DB users:{users}")
    return users.items


def retrieve_db_credentials(db) -> dict:
    """
    make credentials dictionary from Deta database in the format needed for streamlit-authentication
    :return:
    """
    users = fetch_db(db)
    emails = []
    usernames = []
    names = []
    passwords = []
    created_at = []
    for user in users:
        created_at.append(user['created_at'])
        emails.append(user['email'])
        usernames.append(user['key'])
        passwords.append(user['password'])
        names.append(user['name'])
    credentials = {"usernames": {}}
    for username, name, password in zip(usernames, names, passwords):
        user_dict = {"name": name, "password": password}
        credentials["usernames"].update({username: user_dict})
    print(f"all users credentials:{credentials}")
    return credentials


def get_user_key(db):
    """
    Fetch User Emails
    :return List of user emails:
    """
    users = db.fetch()
    emails = []
    for user in users.items:
        emails.append(user['key'])
    return emails


def insert_user(key, email, password, name, db) -> bool:
    """
    Inserts Users into the DB
    :param key:
    :param email:
    :param password:
    :param name:
    :return User Upon successful Creation:
    """
    date_created = str(datetime.datetime.now())
    try:
        db.put({'key': key, 'email': email, 'password': password, 'name': name, 'created_at': date_created})
        return True
    except Exception as e:
        print(e)
        return False


def add_user(usernames: dict) -> None:
    """
    :param config:
    :return:
    """
    print(f"in update_config")
    current_keys = get_user_key(db)
    print(f"current users in DB:{current_keys}")
    updated_usernames = usernames['usernames']
    updated_keys = list(updated_usernames.keys())
    print(f"updated users in UI:{updated_keys}")

    # find updated key
    new_key = [x for x in updated_keys if x not in current_keys][0]
    print(f"new key:{new_key}")
    # get its credentials:
    new_credential = usernames['usernames'][new_key]
    created_at = datetime.datetime.now()
    print(f"new user:{new_credential}, created at:{created_at}, key:{new_key}")
    added_user = insert_user(new_key,
                             new_credential['email'],
                             new_credential['password'],
                             new_credential['name'],
                             db)
    if added_user:
        print(f"{new_key} successfully added to DB")
    else:
        print(f"{new_key} not added to DB")
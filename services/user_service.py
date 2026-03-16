from db.mongo_client import get_db
from config.settings import USERS_COLLECTION

def get_next_user_id():
    client, db = get_db()
    try:
        last = db[USERS_COLLECTION].find_one(sort=[("user_id", -1)])
        return (last["user_id"] + 1) if last and "user_id" in last else 1001
    finally:
        client.close()

def email_exists(email):
    client, db = get_db()
    try:
        return db[USERS_COLLECTION].find_one({"email": email}) is not None
    finally:
        client.close()

def insert_user(user_doc):
    client, db = get_db()
    try:
        db[USERS_COLLECTION].insert_one(user_doc)
    finally:
        client.close()

def get_user_by_id(user_id):
    client, db = get_db()
    try:
        return db[USERS_COLLECTION].find_one({"user_id": user_id}, {"_id": 0})
    finally:
        client.close()
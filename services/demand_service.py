from db.mongo_client import get_db
from config.settings import DEMAND_COLLECTION

def insert_demand(record):
    client, db = get_db()
    try:
        db[DEMAND_COLLECTION].insert_one(record)
    finally:
        client.close()

def fetch_all_demand():
    client, db = get_db()
    try:
        return list(db[DEMAND_COLLECTION].find({}, {"_id": 0}))
    finally:
        client.close()

def fetch_last_n_records(user_id, n=7):
    client, db = get_db()
    try:
        return list(
            db[DEMAND_COLLECTION]
            .find({"user_id": user_id}, {"_id": 0})
            .sort("Date", -1)
            .limit(n)
        )
    finally:
        client.close()

def fetch_prev_day_demand(user_id):
    records = fetch_last_n_records(user_id, n=1)
    return records[0]["Total_Batter_Required_kg"] if records else 0.0
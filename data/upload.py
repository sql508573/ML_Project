import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from config import DEMAND_COLLECTION

def check_data_in_db():
    """Query and display data from MongoDB (no CSV file used)"""
    print("\n===== Check MongoDB Data =====\n")
    
    client, db = get_db()
    try:
        count = db[DEMAND_COLLECTION].count_documents({})
        print(f"📊 Total records in '{DEMAND_COLLECTION}' collection: {count}")
        if count > 0:
            print("✅ Data is ready for training and inference.")
        else:
            print("⚠️  No data found. Please populate MongoDB first.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    check_data_in_db()
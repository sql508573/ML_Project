"""Debug script - Inspect database data"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from config import DEMAND_COLLECTION
import pandas as pd


def debug_data():
    """Debug and inspect database data"""
    print("\n===== Database Debug Info =====\n")
    
    client, db = get_db()
    
    try:
        # Get collection stats
        collection = db[DEMAND_COLLECTION]
        count = collection.count_documents({})
        print(f"📊 Total demand records: {count}")
        
        if count > 0:
            # Sample records
            sample = list(collection.find().limit(5))
            df_sample = pd.DataFrame(sample)
            print(f"\n📋 Sample records (first 5):")
            print(df_sample.to_string())
            
            # Date range
            dates = collection.distinct("Date")
            if dates:
                print(f"\n📅 Date range: {min(dates)} to {max(dates)}")
            
            # Users represented
            users = collection.distinct("user_id")
            print(f"👥 Unique users: {len(set(users))}")
        else:
            print("⚠️  No demand records found.")
    
    finally:
        client.close()


if __name__ == "__main__":
    debug_data()

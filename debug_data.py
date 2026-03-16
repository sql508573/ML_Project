import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.mongo_client import get_db
from config.settings import DEMAND_COLLECTION
import pandas as pd

client, db = get_db()
try:
    records = list(db[DEMAND_COLLECTION].find().limit(3))
    print(f"Total records in MongoDB: {db[DEMAND_COLLECTION].count_documents({})}")
    print(f"\nFirst 3 records:\n")
    
    for i, record in enumerate(records):
        print(f"Record {i+1}:")
        print(f"  Keys: {list(record.keys())}")
        if '_id' in record:
            del record['_id']
        print(f"  Data: {record}\n")
    
    # Try preprocessing
    print("\n" + "="*50)
    print("Testing preprocessing...")
    from ml.preprocess import preprocess
    
    all_records = list(db[DEMAND_COLLECTION].find({}, {"_id": 0}))
    df = pd.DataFrame(all_records)
    print(f"\nBefore preprocessing: {len(df)} records")
    print(f"Columns: {list(df.columns)}\n")
    
    df_processed = preprocess(df)
    print(f"After preprocessing: {len(df_processed)} records")
    if len(df_processed) > 0:
        print(f"Columns: {list(df_processed.columns)}")
        print(f"\nFirst row:\n{df_processed.iloc[0]}")
    
finally:
    client.close()

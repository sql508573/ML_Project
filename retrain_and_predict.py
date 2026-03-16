import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from services.demand_service import fetch_all_demand
from ml.preprocess import preprocess
from ml.train import train

def retrain_and_predict():
    print("\nFetching all demand data from MongoDB and retraining global model...\n")
    
    all_data = fetch_all_demand()
    if not all_data:
        print("No data available in MongoDB.")
        return

    df = preprocess(pd.DataFrame(all_data))
    print(f"Training on {len(df)} records from all users...\n")
    result = train(df)
    if result == (None, None):
        return
    print("✓ Global model retrained and saved.")

if __name__ == "__main__":
    retrain_and_predict()
'''

---

**Execution order remains the same:**
```
python data/upload.py
python register_user.py
python retrain_and_predict.py   ← initial train

python inference.py             ← anytime
python data/log_daily.py        ← end of day
python retrain_and_predict.py   ← end of day after logging

'''
"""Retrain and Predict script - Retrain models with latest data"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from services import fetch_all_demand
from ml import preprocess, train


def run_retrain_and_predict():
    """Retrain models with all available data"""
    print("\n===== Retrain Models =====\n")
    
    print("📊 Fetching all demand data from MongoDB...")
    all_data = fetch_all_demand()
    
    if not all_data:
        print("❌ No demand data found in database.")
        return
    
    print(f"✓ Loaded {len(all_data)} records")
    
    df = pd.DataFrame(all_data)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.drop(columns=["_id"], errors="ignore")
    
    print(f"\n🔧 Preprocessing data...")
    df_processed = preprocess(df)
    
    if df_processed is None or len(df_processed) == 0:
        print("❌ Preprocessing failed or no data available.")
        return
    
    print(f"✓ Preprocessed {len(df_processed)} records")
    
    print(f"\n🤖 Training models...")
    train(df_processed)
    
    print(f"\n✅ Models trained and saved successfully!")


if __name__ == "__main__":
    run_retrain_and_predict()

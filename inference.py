import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.user_service import get_user_by_id
from services.demand_service import fetch_last_n_records, fetch_all_demand
from ml.train import load_models
from ml.predict import build_features, predict

def run_inference():
    user_id_input = input("Enter User ID: ").strip()
    if not user_id_input.isdigit():
        print("User ID must be a number.")
        return

    user_id = int(user_id_input)
    user = get_user_by_id(user_id)
    if not user:
        print(f"No user found with User ID: {user_id}")
        return

    records = fetch_last_n_records(user_id, n=14)
    if len(records) < 7:
        print("Need at least 7 historical records for this user to run personalized inference.")
        return

    all_data = fetch_all_demand()
    global_avg = 0.0
    if all_data:
        global_avg = sum(x.get("Total_Batter_Required_kg", 0) for x in all_data) / len(all_data)

    features = build_features(user, records, global_avg_demand=global_avg)
    if features is None:
        return

    rf_model, xgb_model = load_models()
    predict(rf_model, xgb_model, features, user["name"])

if __name__ == "__main__":
    run_inference()
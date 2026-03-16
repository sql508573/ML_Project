import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.user_service import get_user_by_id
from services.demand_service import fetch_last_n_records
from ml.train import load_models
from ml.predict import build_features, predict

def run_inference():
    user_id_input = input("Enter User ID: ").strip()
    if not user_id_input.isdigit():
        print("User ID must be a number.")
        return

    user_id = int(user_id_input)
    user    = get_user_by_id(user_id)
    if not user:
        print(f"No user found with User ID: {user_id}")
        return

    records  = fetch_last_n_records(user_id, n=7)
    features = build_features(user, records)
    if features is None:
        return

    rf_model, xgb_model = load_models()
    predict(rf_model, xgb_model, features, user["name"])

if __name__ == "__main__":
    run_inference()
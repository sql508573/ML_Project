import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from config.settings import FEATURE_COLS, TARGET_COL, MODELS_DIR
from ml.evaluate import evaluate

def train(df):
    # Need minimum data for train/test split
    if len(df) < 5:
        print(f"Error: Not enough data to train. Have {len(df)} records, need at least 5.")
        print("Please ensure the 731 historical records are in MongoDB.")
        return None, None
    
    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    rf_model = RandomForestRegressor(n_estimators=200, random_state=42)
    rf_model.fit(X_train, y_train)
    evaluate("Random Forest", y_test, rf_model.predict(X_test))

    xgb_model = XGBRegressor(n_estimators=200, learning_rate=0.05, random_state=42, verbosity=0)
    xgb_model.fit(X_train, y_train)
    evaluate("XGBoost", y_test, xgb_model.predict(X_test))

    os.makedirs(MODELS_DIR, exist_ok=True)
    with open(os.path.join(MODELS_DIR, "rf_model.pkl"), "wb") as f:
        pickle.dump(rf_model, f)
    with open(os.path.join(MODELS_DIR, "xgb_model.pkl"), "wb") as f:
        pickle.dump(xgb_model, f)

    print(f"\nModels saved to '{MODELS_DIR}/'.")
    return rf_model, xgb_model

def load_models():
    with open(os.path.join(MODELS_DIR, "rf_model.pkl"), "rb") as f:
        rf_model = pickle.load(f)
    with open(os.path.join(MODELS_DIR, "xgb_model.pkl"), "rb") as f:
        xgb_model = pickle.load(f)
    return rf_model, xgb_model
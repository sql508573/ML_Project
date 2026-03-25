import pandas as pd
from datetime import datetime

def build_features(user, records, global_avg_demand=0.0, weight_own=0.7):
    today = datetime.today()
    next_dow = today.weekday()
    default_temp = 30.0

    if len(records) < 7:
        print("Error: Need at least 7 days of user historical data for reliable prediction.")
        return None

    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    last = df.iloc[-1]
    lag_1 = last["Total_Batter_Required_kg"]
    lag_2 = df.iloc[-2]["Total_Batter_Required_kg"] if len(df) >= 2 else lag_1
    lag_3 = df.iloc[-3]["Total_Batter_Required_kg"] if len(df) >= 3 else lag_1
    rolling_mean = df["Total_Batter_Required_kg"].iloc[-7:].mean()
    rolling_std = df["Total_Batter_Required_kg"].iloc[-7:].std()

    blended_prev = (weight_own * lag_1 + (1 - weight_own) * float(global_avg_demand)) if global_avg_demand else lag_1

    return pd.DataFrame([{ 
        "Day_of_Week"       : next_dow,
        "Month"             : today.month,
        "Is_Weekend"        : 1 if next_dow in [5, 6] else 0,
        "Avg_Temp_C"        : default_temp,
        "Rainy_Day"         : 0,
        "Public_Holiday"    : 0,
        "Promotion_Flag"    : 0,
        "Prev_Day_Demand_kg": blended_prev,
        "Lag_1"             : lag_1,
        "Lag_2"             : lag_2,
        "Lag_3"             : lag_3,
        "Rolling_Mean_7"    : rolling_mean,
        "Rolling_Std_7"     : rolling_std if not pd.isna(rolling_std) else 0,
    }])


def predict(rf_model, xgb_model, features, user_name, verbose=True):
    """
    Make prediction using ensemble of Random Forest and XGBoost
    
    Args:
        rf_model: Trained Random Forest model
        xgb_model: Trained XGBoost model
        features: Feature dataframe
        user_name: Name of user (for display)
        verbose: Whether to print predictions (default True)
        
    Returns:
        dict: {rf_pred, xgb_pred, avg_pred}
    """
    rf_pred = rf_model.predict(features)[0]
    xgb_pred = xgb_model.predict(features)[0]
    avg_pred = (rf_pred + xgb_pred) / 2

    if verbose:
        print(f"\n========== Next Day Prediction for {user_name} ==========")
        print(f"Random Forest  : {rf_pred:.2f} kg")
        print(f"XGBoost        : {xgb_pred:.2f} kg")
        print(f"Average        : {avg_pred:.2f} kg")
    
    return {
        "rf_pred": rf_pred,
        "xgb_pred": xgb_pred,
        "avg_pred": avg_pred
    }

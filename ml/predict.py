import pandas as pd
from datetime import datetime

def build_features(user, records):
    today    = datetime.today()
    next_dow = today.weekday()
    
    # Use default shop sales as baseline if no history
    default_sales = user["shop_defaults"]["typical_restaurant_sales_kg"]

    if len(records) == 0:
        # No historical data - use shop defaults
        print(f"No historical data found. Using shop defaults ({default_sales:.2f} kg).")
        return pd.DataFrame([{
            "Day_of_Week"       : next_dow,
            "Month"             : today.month,
            "Is_Weekend"        : 1 if next_dow in [5, 6] else 0,
            "Avg_Temp_C"        : user["shop_defaults"]["avg_temp_c"],
            "Rainy_Day"         : 0,
            "Public_Holiday"    : 0,
            "Promotion_Flag"    : 0,
            "Prev_Day_Demand_kg": default_sales,
            "Lag_1"             : default_sales,
            "Lag_2"             : default_sales,
            "Lag_3"             : default_sales,
            "Rolling_Mean_7"    : default_sales,
            "Rolling_Std_7"     : 0,
        }])

    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    last_row = df.iloc[-1]
    
    # Fill missing lags with last available value or default
    lag_1 = last_row["Total_Batter_Required_kg"]
    lag_2 = df.iloc[-2]["Total_Batter_Required_kg"] if len(df) >= 2 else lag_1
    lag_3 = df.iloc[-3]["Total_Batter_Required_kg"] if len(df) >= 3 else lag_1
    rolling_mean = df["Total_Batter_Required_kg"].iloc[-7:].mean()
    rolling_std = df["Total_Batter_Required_kg"].iloc[-7:].std()

    return pd.DataFrame([{
        "Day_of_Week"       : next_dow,
        "Month"             : today.month,
        "Is_Weekend"        : 1 if next_dow in [5, 6] else 0,
        "Avg_Temp_C"        : user["shop_defaults"]["avg_temp_c"],
        "Rainy_Day"         : 0,
        "Public_Holiday"    : 0,
        "Promotion_Flag"    : 0,
        "Prev_Day_Demand_kg": lag_1,
        "Lag_1"             : lag_1,
        "Lag_2"             : lag_2,
        "Lag_3"             : lag_3,
        "Rolling_Mean_7"    : rolling_mean,
        "Rolling_Std_7"     : rolling_std if not pd.isna(rolling_std) else 0,
    }])

def predict(rf_model, xgb_model, features, user_name):
    rf_pred  = rf_model.predict(features)[0]
    xgb_pred = xgb_model.predict(features)[0]

    print(f"\n========== Next Day Prediction for {user_name} ==========")
    print(f"Random Forest  : {rf_pred:.2f} kg")
    print(f"XGBoost        : {xgb_pred:.2f} kg")
    print(f"Average        : {(rf_pred + xgb_pred) / 2:.2f} kg")
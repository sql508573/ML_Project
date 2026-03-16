import pandas as pd
import numpy as np

def preprocess(df):
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Assign default user_id (0) to records without user_id (historical CSV data)
    df["user_id"] = df["user_id"].fillna(0)
    
    df = df.sort_values(["user_id", "Date"]).reset_index(drop=True)

    # Group by user_id to create lag features within each user's data
    df["Lag_1"] = df.groupby("user_id")["Total_Batter_Required_kg"].shift(1)
    df["Lag_2"] = df.groupby("user_id")["Total_Batter_Required_kg"].shift(2)
    df["Lag_3"] = df.groupby("user_id")["Total_Batter_Required_kg"].shift(3)
    df["Rolling_Mean_7"] = df.groupby("user_id")["Total_Batter_Required_kg"].shift(1).rolling(window=7).mean()
    df["Rolling_Std_7"]  = df.groupby("user_id")["Total_Batter_Required_kg"].shift(1).rolling(window=7).std()

    return df.dropna().reset_index(drop=True)
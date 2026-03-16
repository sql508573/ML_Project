import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI      = os.getenv("MONGO_URI")
DB_NAME        = "BatterShopDB"
USERS_COLLECTION  = "Users"
DEMAND_COLLECTION = "DailyDemand"
MODELS_DIR     = "models"

FEATURE_COLS = [
    "Day_of_Week", "Month", "Is_Weekend", "Avg_Temp_C",
    "Rainy_Day", "Public_Holiday", "Promotion_Flag",
    "Prev_Day_Demand_kg", "Lag_1", "Lag_2", "Lag_3",
    "Rolling_Mean_7", "Rolling_Std_7",
]

TARGET_COL = "Total_Batter_Required_kg"
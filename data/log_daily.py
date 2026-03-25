import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from schemas.demand_schema import build_demand_doc
from services.demand_service import insert_demand, fetch_prev_day_demand
from services.user_service import get_user_by_id

def log_daily():
    print("\n===== Log Daily Sales Data =====\n")

    user_id_input = input("Enter User ID: ").strip()
    if not user_id_input.isdigit():
        print("User ID must be a number.")
        return
    user_id = int(user_id_input)

    user = get_user_by_id(user_id)
    if not user:
        print(f"No user found with User ID: {user_id}")
        return

    date_input = input("Date (YYYY-MM-DD) [press Enter for today]: ").strip()
    date_obj = datetime.today() if not date_input else datetime.strptime(date_input, "%Y-%m-%d")

    try:
        restaurant_sales = float(input("Restaurant Sales today (kg): ").strip())
        retail_sales     = float(input("Retail Sales today (kg): ").strip())
        rainy            = int(input("Rainy day? (1=Yes, 0=No): ").strip())
        holiday          = int(input("Public holiday? (1=Yes, 0=No): ").strip())
        promo            = int(input("Promotion? (1=Yes, 0=No): ").strip())
        temp_input       = input("Average Temperature today (°C) [default 30]: ").strip()
        temp             = float(temp_input) if temp_input else 30.0
    except ValueError:
        print("Invalid input.")
        return

    prev_demand = fetch_prev_day_demand(user_id)
    record = build_demand_doc(user_id, date_obj, temp, rainy, holiday, promo,
                              restaurant_sales, retail_sales, prev_demand)
    insert_demand(record)

    print(f"\nLogged {restaurant_sales + retail_sales:.2f} kg for {user['name']} on {date_obj.strftime('%Y-%m-%d')}.")

if __name__ == "__main__":
    log_daily()
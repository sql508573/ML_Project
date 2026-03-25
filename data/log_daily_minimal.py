import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from schemas import build_demand_doc
from services import insert_demand, fetch_prev_day_demand, get_user_by_id


def run_log_daily_minimal():
    print("\n===== Log Daily Sales (Minimal Input) =====\n")

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
    try:
        date_obj = datetime.strptime(date_input, "%Y-%m-%d") if date_input else datetime.today()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    try:
        amount_sold = float(input("Total batter sold today (kg): ").strip())
        rainy = int(input("Rainy day? (1=Yes, 0=No) [default 0]: ").strip() or 0)
        holiday = int(input("Public holiday? (1=Yes, 0=No) [default 0]: ").strip() or 0)
        promo = int(input("Promotion today? (1=Yes, 0=No) [default 0]: ").strip() or 0)
    except ValueError:
        print("Invalid numeric input.")
        return

    constants = user.get("shop_constants", {})
    share = float(constants.get("restaurant_sales_share", 0.6))
    restaurant_sales = amount_sold * share
    retail_sales = amount_sold - restaurant_sales
    temp = float(30.0)  # default temperature

    prev_demand = fetch_prev_day_demand(user_id)
    record = build_demand_doc(user_id, date_obj, temp, rainy, holiday, promo,
                              restaurant_sales, retail_sales, prev_demand)
    insert_demand(record)

    print(f"\nLogged {amount_sold:.2f} kg for user_id={user_id} on {date_obj.strftime('%Y-%m-%d')}")


if __name__ == "__main__":
    run_log_daily_minimal()

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import re
from schemas.user_schema import build_user_doc
from services.user_service import get_next_user_id, email_exists, insert_user

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_phone(phone):
    return re.match(r"^\d{10}$", phone)

def register_user():
    print("\n===== Register New Batter Shop User =====\n")

    name  = input("Full Name: ").strip()
    email = input("Email ID: ").strip()
    phone = input("Phone Number (10 digits): ").strip()
    age   = input("Age: ").strip()
    location = input("Batter Shop Location: ").strip()

    if not name or not location:
        print("Name and location cannot be empty.")
        return
    if not validate_email(email):
        print("Invalid email.")
        return
    if not validate_phone(phone):
        print("Invalid phone number.")
        return
    if not age.isdigit():
        print("Age must be a number.")
        return
    if email_exists(email):
        print("Email already registered.")
        return

    try:
        base_daily_demand_kg = float(input("Baseline daily batter demand estimate (kg): ").strip())
        restaurant_sales_share = float(input("Fraction to restaurants (0-1, e.g. 0.65): ").strip())
    except ValueError:
        print("Invalid numeric input.")
        return
    if not 0 <= restaurant_sales_share <= 1:
        print("Restaurant share must be between 0 and 1.")
        return

    user_id  = get_next_user_id()
    user_doc = build_user_doc(user_id, name, email, phone, age, location, base_daily_demand_kg, restaurant_sales_share)
    insert_user(user_doc)
    print(f"\nRegistered successfully. Your User ID is: {user_id}")

if __name__ == "__main__":
    register_user()
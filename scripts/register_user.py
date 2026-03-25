"""User registration script - CLI entry point"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas import build_user_doc
from services import get_next_user_id, email_exists, insert_user
from utils import validate_email, validate_phone, validate_numeric, validate_user_input


def register_user():
    """Interactive user registration"""
    print("\n===== Register New Batter Shop User =====\n")

    name  = input("Full Name: ").strip()
    email = input("Email ID: ").strip()
    phone = input("Phone Number (10 digits): ").strip()
    age   = input("Age: ").strip()
    location = input("Batter Shop Location: ").strip()

    if not name or not location:
        print("❌ Name and location cannot be empty.")
        return
    
    if not validate_email(email):
        print("❌ Invalid email format.")
        return
    
    if not validate_phone(phone):
        print("❌ Invalid phone number. Must be 10 digits.")
        return
    
    is_valid, _ = validate_numeric(age, allow_float=False)
    if not is_valid:
        print("❌ Age must be a number.")
        return
    
    if email_exists(email):
        print("❌ Email already registered.")
        return

    try:
        base_daily_demand_kg_str = input("Baseline daily batter demand estimate (kg): ").strip()
        is_valid, base_daily_demand_kg = validate_numeric(base_daily_demand_kg_str, allow_float=True)
        if not is_valid:
            raise ValueError("Invalid numeric input for demand")
        
        restaurant_sales_share_str = input("Fraction to restaurants (0-1, e.g. 0.65): ").strip()
        is_valid, restaurant_sales_share = validate_numeric(restaurant_sales_share_str, allow_float=True)
        if not is_valid:
            raise ValueError("Invalid numeric input for share")
    
    except (ValueError, TypeError) as e:
        print(f"❌ Invalid input: {str(e)}")
        return
    
    if not (0 <= restaurant_sales_share <= 1):
        print("❌ Restaurant share must be between 0 and 1.")
        return

    user_id  = get_next_user_id()
    user_doc = build_user_doc(
        user_id, name, email, phone, age, location,
        base_daily_demand_kg, restaurant_sales_share
    )
    insert_user(user_doc)

    print(f"\n✅ User registered successfully!")
    print(f"   User ID: {user_id}")
    print(f"   Name: {name}")
    print(f"   Location: {location}")


if __name__ == "__main__":
    register_user()

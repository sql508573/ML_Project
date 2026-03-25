def build_user_doc(user_id, name, email, phone, age, location, base_daily_demand_kg, restaurant_sales_share):
    return {
        "user_id": user_id,
        "name": name,
        "email": email,
        "phone": phone,
        "age": int(age),
        "location": location,
        "shop_constants": {
            "base_daily_demand_kg": float(base_daily_demand_kg),
            "restaurant_sales_share": float(restaurant_sales_share),
        }
    }

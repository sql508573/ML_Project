def build_user_doc(user_id, name, email, phone, age, location, avg_temp, restaurant_sales):
    return {
        "user_id"  : user_id,
        "name"     : name,
        "email"    : email,
        "phone"    : phone,
        "age"      : int(age),
        "location" : location,
        "shop_defaults": {
            "avg_temp_c"                  : float(avg_temp),
            "typical_restaurant_sales_kg" : float(restaurant_sales),
        }
    }
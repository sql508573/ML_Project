def build_demand_doc(user_id, date_obj, temp, rainy, holiday, promo,
                     restaurant_sales, retail_sales, prev_demand):
    total = restaurant_sales + retail_sales
    return {
        "user_id"                  : user_id,
        "Date"                     : date_obj.strftime("%Y-%m-%d"),
        "Day_of_Week"              : date_obj.weekday(),
        "Month"                    : date_obj.month,
        "Is_Weekend"               : 1 if date_obj.weekday() in [5, 6] else 0,
        "Avg_Temp_C"               : float(temp),
        "Rainy_Day"                : int(rainy),
        "Public_Holiday"           : int(holiday),
        "Promotion_Flag"           : int(promo),
        "Restaurant_Sales_kg"      : float(restaurant_sales),
        "Retail_Sales_kg"          : float(retail_sales),
        "Total_Batter_Required_kg" : float(total),
        "Pct_Sold_to_Restaurant"   : round(restaurant_sales / total, 4) if total > 0 else 0,
        "Prev_Day_Demand_kg"       : float(prev_demand),
    }
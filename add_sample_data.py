#!/usr/bin/env python3
"""
Add sample data to MongoDB for testing and development
Run this to populate the database with 30 days of sample data
"""
import sys
import os
from datetime import datetime, timedelta

def add_sample_data():
    """Add 30 days of sample demand data to MongoDB"""
    
    print("\n" + "="*60)
    print("📊 Add Sample Data to MongoDB")
    print("="*60 + "\n")
    
    try:
        from pymongo import MongoClient
        from dotenv import load_dotenv
        
        # Load environment
        load_dotenv()
        uri = os.getenv("MONGO_URI")
        
        if not uri:
            print("❌ MONGO_URI not found in .env")
            return False
        
        print("  → Connecting to MongoDB...", end=" ", flush=True)
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ Connected")
        
        db = client["BatterShopDB"]
        
        # Create sample data (30 days)
        print("  → Creating sample data (30 days)...", end=" ", flush=True)
        
        sample_data = []
        base_date = datetime.now() - timedelta(days=30)
        
        for i in range(30):
            current_date = base_date + timedelta(days=i)
            
            # Realistic variations
            base_demand = 50  # kg
            variation = 10 * (i % 10) - 45  # Creates variation
            demand = base_demand + variation + (5 if i % 7 == 0 else 0)  # Higher on certain days
            
            restaurant_share = 0.65
            restaurant_sales = demand * restaurant_share
            retail_sales = demand * (1 - restaurant_share)
            
            record = {
                "user_id": 1001,
                "Date": current_date,
                "Avg_Temp_C": 28 + (5 * (i % 8) - 20),  # Temp varies 8-33°C
                "Rainy_Day": 1 if i % 5 == 0 else 0,  # Rainy every 5 days
                "Public_Holiday": 1 if i % 15 == 0 else 0,  # Holiday every 15 days
                "Promotion_Flag": 1 if i % 7 == 0 else 0,  # Promo every 7 days
                "restaurant_sales_kg": round(restaurant_sales, 2),
                "retail_sales_kg": round(retail_sales, 2),
                "Total_Batter_Required_kg": round(demand, 2),
            }
            sample_data.append(record)
        
        print("✅ Sample data created")
        
        # Check existing data
        print("  → Checking existing records...", end=" ", flush=True)
        collection = db["DailyDemand"]
        existing = collection.count_documents({"user_id": 1001})
        print(f"✅ Found {existing} existing records")
        
        # Delete old sample data
        if existing > 0:
            print("  → Removing old sample data...", end=" ", flush=True)
            collection.delete_many({"user_id": 1001})
            print("✅ Cleaned")
        
        # Insert new data
        print("  → Inserting 30 days of sample data...", end=" ", flush=True)
        result = collection.insert_many(sample_data)
        print(f"✅ Inserted {len(result.inserted_ids)} records")
        
        # Create user if doesn't exist
        print("  → Creating sample user...", end=" ", flush=True)
        users_collection = db["Users"]
        
        existing_user = users_collection.find_one({"user_id": 1001})
        
        if not existing_user:
            sample_user = {
                "user_id": 1001,
                "name": "Raj's Batter Shop",
                "email": "raj@battershop.com",
                "phone": "9876543210",
                "age": 35,
                "location": "Mumbai",
                "shop_constants": {
                    "base_daily_demand_kg": 50,
                    "restaurant_sales_share": 0.65,
                }
            }
            users_collection.insert_one(sample_user)
            print("✅ User created")
        else:
            print("✅ User already exists")
        
        # Verify
        print("  → Verifying data...", end=" ", flush=True)
        count = collection.count_documents({"user_id": 1001})
        user_count = users_collection.count_documents({})
        print(f"✅ {count} demand records, {user_count} users")
        
        print("\n✅ Sample data added successfully!\n")
        print("Next steps:")
        print("  1. Register your own user: python3 main.py register")
        print("  2. Train models: python3 main.py retrain")
        print("  3. Get prediction: python3 main.py predict")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def add_production_data():
    """Add production data from CSV or database"""
    print("\n" + "="*60)
    print("📊 Add Production Data")
    print("="*60 + "\n")
    
    print("To add production data:")
    print("1. Prepare your data in CSV format with columns:")
    print("   - user_id, Date, Avg_Temp_C, Rainy_Day, Public_Holiday")
    print("   - Promotion_Flag, restaurant_sales_kg, retail_sales_kg")
    print("\n2. Use dataset_creator.py if you have a batter_shop_data.csv")
    print("\n3. Or import directly using pymongo:")
    print("   - Create a Python script with pymongo.MongoClient")
    print("   - Insert your records")
    
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Add data to MongoDB")
    parser.add_argument(
        "--production",
        action="store_true",
        help="Show how to add production data"
    )
    
    args = parser.parse_args()
    
    if args.production:
        success = add_production_data()
    else:
        success = add_sample_data()
    
    sys.exit(0 if success else 1)

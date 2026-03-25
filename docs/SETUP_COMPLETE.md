# ✅ Complete Setup Checklist - Get Everything Working

This guide walks you through all the steps needed to get the entire system up and running.

---

## 📋 Setup Overview

```
1. Python Environment Setup
2. Dependencies Installation
3. MongoDB Configuration & Data Setup
4. Model Training
5. Twilio WhatsApp Setup (Optional)
6. Test the System
7. Run Daily Operations
```

---

## 🚀 STEP 1: Python Environment Setup

### 1.1 Create Virtual Environment

```bash
cd /home/visvam/daNewFolder/college_files/projects/ml_project/github_full_code/ML_Project

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Verify activation (you should see (venv) prefix)
python --version
```

### 1.2 Verify Python Version
```bash
python --version  # Should be 3.8 or higher
```

---

## 📦 STEP 2: Install Dependencies

```bash
# Make sure venv is activated
source venv/bin/activate

# Install all packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E "pandas|pymongo|twilio|scikit|xgboost"
```

### Expected output:
```
numpy                    1.24.3
pandas                   2.0.3
python-dotenv            1.0.0
pymongo                  4.4.1
scikit-learn             1.3.0
twilio                   8.10.0
xgboost                  2.0.0
```

---

## 🗄️ STEP 3: MongoDB Setup & Data

### 3.1 Verify MongoDB Connection

The `.env` file already has your MongoDB URI:
```dotenv
MONGO_URI=mongodb+srv://yp2visvam:y3GMKQN5NBEgx6be@battershopdb.bp7cazo.mongodb.net/?appName=BatterShopDB
```

Test the connection:
```bash
python3 main.py check
```

Expected output:
```
===== Check MongoDB Data =====

📊 Total records in 'DailyDemand' collection: XXX
✅ Data is ready for training and inference.
```

### 3.2 Add Sample Data (If Needed)

If you get "0 records", you need to add sample data. Check if you have a CSV file:

```bash
ls -la *.csv  # Look for dataset files
```

If using the dataset creator:
```bash
# If you have batter_shop_data.csv
python3 dataset_creator.py

# Or use the upload script
python3 main.py check  # Then add data manually
```

### 3.3 Create Test Data (Minimal Setup)

You can manually insert data into MongoDB:

```python
from pymongo import MongoClient
from datetime import datetime, timedelta

# Connect to MongoDB
uri = "mongodb+srv://yp2visvam:y3GMKQN5NBEgx6be@battershopdb.bp7cazo.mongodb.net/?appName=BatterShopDB"
client = MongoClient(uri)
db = client["BatterShopDB"]

# Create sample demand records (at least 14 days per user for predictions)
sample_data = []
for i in range(30):  # 30 days of data
    date = datetime.now() - timedelta(days=30-i)
    sample_data.append({
        "user_id": 1001,
        "Date": date,
        "Avg_Temp_C": 30.0,
        "Rainy_Day": i % 5 == 0,  # Rainy every 5 days
        "Public_Holiday": i % 15 == 0,  # Holiday every 15 days
        "Promotion_Flag": i % 7 == 0,  # Promotion every 7 days
        "restaurant_sales_kg": 25.0 + (i % 10),
        "retail_sales_kg": 15.0 + (i % 8),
        "Total_Batter_Required_kg": 40.0 + (i % 18),
    })

# Insert into database
db["DailyDemand"].insert_many(sample_data)
print(f"✅ Inserted {len(sample_data)} records")

# Verify
count = db["DailyDemand"].count_documents({})
print(f"Total records: {count}")
```

---

## 👤 STEP 4: Register a Test User

Register a user before getting predictions:

```bash
python3 main.py register
```

Follow the prompts:
```
===== Register New Batter Shop User =====

Full Name: Raj's Batter Shop
Email ID: raj@battershop.com
Phone Number (10 digits): 9876543210
Age: 35
Batter Shop Location: Mumbai
Baseline daily batter demand estimate (kg): 50
Fraction to restaurants (0-1, e.g. 0.65): 0.65

✅ User registered successfully!
   User ID: 1001
```

### Get your User ID for next steps!

---

## 🤖 STEP 5: Train the Model

Before making predictions, train the ML model:

```bash
# Retrain with all available data
python3 main.py retrain
```

Expected output:
```
===== Retrain Models =====

📊 Fetching all demand data from MongoDB...
✓ Loaded 30 records

🔧 Preprocessing data...
✓ Preprocessed 30 records

🤖 Training models...
✓ Models trained and saved successfully!
```

### Verify models were created:
```bash
ls -la models/
# Should see:
# rf_model.pkl
# xgb_model.pkl
```

---

## ✔️ STEP 6: Test Basic Prediction

Try getting a prediction:

```bash
python3 main.py predict
```

Enter your registered user ID (1001):
```
Enter User ID: 1001

✓ User found: Raj's Batter Shop

========== Next Day Prediction for Raj's Batter Shop ==========
Random Forest  : 45.32 kg
XGBoost        : 47.89 kg
Average        : 46.61 kg ✨
```

✅ **If you see predictions, the basic system works!**

---

## 📱 STEP 7: Twilio WhatsApp Setup (Optional)

### 7.1 Create Twilio Account

1. Go to [Twilio Console](https://www.twilio.com/console)
2. Sign up or log in
3. Get your credentials from the dashboard:
   - **Account SID**: Copy this
   - **Auth Token**: Copy this
   - **Phone Number**: Get your Twilio WhatsApp number

### 7.2 Add to .env File

```bash
# Edit .env file and add these lines:
nano .env
```

Add these lines at the end:
```dotenv
MONGO_URI=mongodb+srv://yp2visvam:y3GMKQN5NBEgx6be@battershopdb.bp7cazo.mongodb.net/?appName=BatterShopDB
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
```

### 7.3 Test WhatsApp Send

```bash
python3 main.py predict-whatsapp
```

Enter user ID and phone number. Check WhatsApp for message!

---

## 📊 STEP 8: Complete Workflow Test

### Test all components:

```bash
# 1. Check data
python3 main.py check

# 2. Register user (if not done)
python3 main.py register

# 3. Log some daily sales
python3 main.py log-minimal

# 4. Retrain model
python3 main.py retrain

# 5. Get prediction
python3 main.py predict

# 6. Send via WhatsApp (if Twilio set up)
python3 main.py predict-whatsapp

# 7. Schedule daily (optional)
python3 main.py scheduler --time 08:00 --test
```

---

## 🐛 Troubleshooting

### Problem: "No module named 'pymongo'"
**Solution:**
```bash
source venv/bin/activate
pip install pymongo
```

### Problem: "Connection refused to MongoDB"
**Solution:**
```bash
# Check MongoDB URI in .env
cat .env

# Test connection specifically
python3 -c "from pymongo import MongoClient; print(MongoClient('YOUR_URI'))"
```

### Problem: "Need at least 7 historical records"
**Solution:** Insert more data or use the sample data script above

### Problem: "No models found"
**Solution:** Run training first
```bash
python3 main.py retrain
```

### Problem: "User does not have a phone number"
**Solution:** Re-register the user with phone number:
```bash
python3 main.py register
```

### Problem: "Failed to send WhatsApp"
**Solution:**
- Verify Twilio credentials in `.env`
- Check phone number format (should be country code + 10 digits)
- Verify Twilio account has WhatsApp enabled

---

## 🎯 Quick Command Reference

```bash
# Core Operations
python3 main.py register          # Register new user
python3 main.py predict           # Get single prediction
python3 main.py log-minimal       # Log daily sales quickly
python3 main.py retrain           # Train/update models
python3 main.py check             # Check MongoDB data

# WhatsApp (if Twilio set up)
python3 main.py predict-whatsapp  # Send prediction to one user
python3 main.py predict-batch     # Send to all users
python3 main.py scheduler         # Schedule daily sends

# Development
python3 main.py debug             # See database info
python3 main.py api               # Start Flask API
```

---

## ✅ Verification Checklist

Run this checklist to verify everything is working:

- [ ] Python virtual environment created and activated
- [ ] All packages installed (`pip list` shows all deps)
- [ ] MongoDB connection works (`python3 main.py check`)
- [ ] At least 30 days of data in database
- [ ] User registered successfully
- [ ] Models trained and saved in `models/`
- [ ] Can get basic prediction
- [ ] (Optional) Twilio configured for WhatsApp
- [ ] (Optional) Can send WhatsApp message

---

## 📈 Next Steps - Daily Operations

Once everything is set up:

```bash
# Every morning - Get prediction
python3 main.py predict

# Every evening - Log sales
python3 main.py log-minimal

# Every night - Retrain model
python3 main.py retrain

# Optional - Send WhatsApp batch
python3 main.py predict-batch
```

Or automate it:
```bash
# Schedule daily at 8 AM
python3 main.py scheduler --time 08:00
```

---

## 📞 Need Help?

1. Check [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture
2. Check [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for import changes
3. Check [WHATSAPP_SETUP.md](WHATSAPP_SETUP.md) for WhatsApp setup
4. Review error messages - they usually tell you what's missing

---

## 🎉 Success!

When everything is working, you'll see outputs like:

```
✅ MongoDB connected and has 30+ records
✅ User registered successfully
✅ Models trained (rf_model.pkl, xgb_model.pkl exist)
✅ Predictions generated (Random Forest: XX kg, XGBoost: YY kg)
✅ WhatsApp message sent (optional, if Twilio set up)
```

**Then you're ready to go!**

# 🎯 Complete Setup Guide - Everything You Need to Know

## 📋 What Must Be Done (Step-by-Step)

Here's exactly what needs to be set up for the code to work:

---

## 🔴 CRITICAL (Must Do This)

### 1. **Python Environment**
```bash
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt  # Install all packages
```
**Why**: The code needs pandas, pymongo, scikit-learn, etc. to run.

**Verify**:
```bash
python3 -c "import pandas, pymongo, sklearn; print('✅ All packages ready')"
```

---

### 2. **MongoDB Setup**
Your `.env` already has:
```dotenv
MONGO_URI=mongodb+srv://yp2visvam:y3GMKQN5NBEgx6be@battershopdb.bp7cazo.mongodb.net/?appName=BatterShopDB
```

**Test connection**:
```bash
python3 main.py check
```

**Expected output**:
```
📊 Total records in 'DailyDemand' collection: XXX
✅ Data is ready for training and inference.
```

**Verify**:
- ✅ Connection works (no errors)
- ✅ Database has data (at least 14-30 records per user recommended)

---

### 3. **Add Data to MongoDB**

**If you have data**, use either:

**Option A**: Add sample data (fastest, for testing)
```bash
python3 add_sample_data.py
```
Creates 30 days of realistic sample data

**Option B**: Use your existing CSV
```bash
python3 dataset_creator.py  # If you have batter_shop_data.csv
```

**Option C**: Manual MongoDB import
```python
from pymongo import MongoClient
client = MongoClient("your_mongodb_uri")
db = client["BatterShopDB"]

data = [
    {
        "user_id": 1001,
        "Date": datetime.now(),
        "restaurant_sales_kg": 25,
        "retail_sales_kg": 15,
        "Total_Batter_Required_kg": 40,
        # ... other fields
    }
]
db["DailyDemand"].insert_many(data)
```

**Verify**:
```bash
python3 main.py check  # Should show records > 0
```

---

### 4. **Register a User**

Before predictions, register at least one user:

```bash
python3 main.py register
```

Follow prompts:
```
Full Name: Raj's Batter Shop
Email ID: raj@battershop.com
Phone Number (10 digits): 9876543210
Age: 35
Batter Shop Location: Mumbai
Baseline daily demand: 50
Restaurant share (0-1): 0.65
```

**Verify**: User ID returned (e.g., 1001) - write this down!

---

### 5. **Train the ML Model**

Train the Random Forest + XGBoost models on your data:

```bash
python3 main.py retrain
```

This will:
1. Fetch all demand data from MongoDB
2. Preprocess features
3. Train Random Forest model
4. Train XGBoost model
5. Save both models to `models/` directory

**Takes**: 1-2 minutes depending on data size

**Verify**: Check models created
```bash
ls -la models/
# You should see:
# rf_model.pkl (Random Forest model)
# xgb_model.pkl (XGBoost model)
```

---

### 6. **Test Basic Prediction**

Get a demand prediction:

```bash
python3 main.py predict
```

Enter User ID (from step 4, e.g., 1001)

**Expected output**:
```
======= Next Day Prediction =======
Random Forest  : 45.32 kg
XGBoost        : 47.89 kg
Average        : 46.61 kg ✨
```

**If you see this, the basic system works!** ✅

---

## 🟠 OPTIONAL (For WhatsApp)

### 7. **Setup Twilio WhatsApp (Optional)**

Only do this if you want WhatsApp notifications.

**Step 1**: Create Twilio Account
1. Go to https://www.twilio.com/console
2. Sign up (free account)
3. Get your credentials:
   - **Account SID**: Copy this
   - **Auth Token**: Copy this
   - **WhatsApp Number**: Get from Twilio console

**Step 2**: Add to `.env`
```dotenv
# Keep existing:
MONGO_URI=mongodb+srv://yp2visvam:y3GMKQN5NBEgx6be@battershopdb.bp7cazo.mongodb.net/?appName=BatterShopDB

# Add these:
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
```

**Step 3**: Test WhatsApp send
```bash
python3 main.py predict-whatsapp
```

Enter User ID and check your phone!

---

## 🟡 RECOMMENDED (For Production)

### 8. **Add More Historical Data**

For better predictions, add more historical data:
- **Minimum**: 14 days per user
- **Better**: 30 days per user
- **Best**: 90+ days per user

More data = Better predictions!

---

## 📊 Complete Setup Checklist

Use this checklist to verify everything:

```
ENVIRONMENT
☐ Python 3.8+ installed
☐ Virtual environment created
☐ Virtual environment activated
☐ All packages installed (pip install -r requirements.txt)

MONGODB
☐ .env file has MONGO_URI
☐ MongoDB connection works (python3 main.py check)
☐ Database has at least 14 days of data per user

USER & MODEL
☐ At least one user registered (python3 main.py register)
☐ Models trained (python3 main.py retrain)
☐ rf_model.pkl exists in models/ directory
☐ xgb_model.pkl exists in models/ directory

TESTING
☐ Basic prediction works (python3 main.py predict)
☐ Predictions show reasonable numbers (not error messages)

OPTIONAL
☐ Twilio account created (if using WhatsApp)
☐ Twilio credentials in .env
☐ WhatsApp prediction works (python3 main.py predict-whatsapp)
```

---

## 🚀 Automated Setup

Run the automated setup script:

```bash
python3 setup.py
```

This does:
1. Check Python version
2. Verify virtual environment
3. Install dependencies
4. Test MongoDB connection
5. Verify project structure
6. Guide next steps

---

## 🔄 Daily Workflow (After Setup)

Once everything is set up:

```bash
# Every morning - Get predictions
python3 main.py predict

# Every evening - Log sales
python3 main.py log-minimal

# Every night - Retrain model
python3 main.py retrain

# Optional - Send WhatsApp
python3 main.py predict-batch
```

Or automate:
```bash
# Schedule predictions daily at 8 AM
python3 main.py scheduler --time 08:00
```

---

## 🐛 Troubleshooting

### "Module not found" errors
```bash
# Fix: Activate environment and install
source venv/bin/activate
pip install -r requirements.txt
```

### MongoDB connection fails
```bash
# Verify MONGO_URI in .env
cat .env | grep MONGO_URI

# Test connection
python3 -c "from pymongo import MongoClient; MongoClient('YOUR_URI').admin.command('ping')"
```

### "Need 7+ historical records"
```bash
# Add sample data
python3 add_sample_data.py

# Or add your own data
python3 dataset_creator.py
```

### "No models found"
```bash
# Train models
python3 main.py retrain

# Wait 1-2 minutes for training to complete
```

### WhatsApp message fails
```bash
# Check Twilio credentials in .env
grep TWILIO .env

# Verify phone number format (country code + 10 digits)
# Check Twilio account has WhatsApp enabled
```

---

## 📚 Documentation Files

- **[QUICK_START.md](QUICK_START.md)** - 5-minute quick start
- **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** - Detailed setup instructions
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Architecture overview
- **[WHATSAPP_SETUP.md](WHATSAPP_SETUP.md)** - WhatsApp integration guide
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Code reference

---

## ✅ Success Indicators

When everything is working:

```
✅ MongoDB connected with data
✅ User registered successfully
✅ Models trained (2 files in models/)
✅ Predictions generated (show RF, XGBoost, Average)
✅ WhatsApp sends (if configured)
✅ Scheduler works (if configured)
```

---

## 🎯 What Each Component Needs

### MongoDB
- ✅ Connection URI in `.env`
- ✅ 30 days of historical demand data
- ✅ Fields: user_id, Date, sales_kg, weather, etc.

### Model
- ✅ 14+ days of user history
- ✅ Trains in 1-2 minutes
- ✅ Saves Random Forest + XGBoost

### Predictions
- ✅ Trained models
- ✅ Registered user
- ✅ 7+ days of user history
- ✅ Returns 3 numbers: RF, XGBoost, Average

### WhatsApp (Optional)
- ✅ Twilio account with WhatsApp
- ✅ Account SID, Auth Token, Phone
- ✅ User with phone number
- ⚠️ May have costs

---

## 🎉 Quick Test

Copy-paste this to verify everything works:

```bash
# Activate environment
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Add sample data
python3 add_sample_data.py

# Register user (just press Enter for defaults)
python3 main.py register

# Train models
python3 main.py retrain

# Get prediction
python3 main.py predict

# If you see predictions, you're done! ✅
```

---

## 📞 Still Need Help?

1. Check [QUICK_START.md](QUICK_START.md) for quick reference
2. See [SETUP_COMPLETE.md](SETUP_COMPLETE.md) for detailed steps
3. Run `python3 setup.py` for automated verification
4. Run `python3 add_sample_data.py` to add test data
5. Check error messages - they usually tell you what's wrong

**Everything should be working now!** 🚀

# 📋 SETUP SUMMARY - What Needs To Be Done

## 🎯 Total Setup Steps: 6

This is exactly what needs to be done to make everything work.

---

## ✅ STEP 1: Python & Environment (5 min)
```bash
source venv/bin/activate
pip install -r requirements.txt
```
**Status**: ✅ Already done if venv exists

---

## ✅ STEP 2: MongoDB Connection (1 min)
Already configured in `.env`:
```dotenv
MONGO_URI=mongodb+srv://yp2visvam:y3GMKQN5NBEgx6be@battershopdb.bp7cazo.mongodb.net/?appName=BatterShopDB
```

**Verify**:
```bash
python3 main.py check
```

---

## ✅ STEP 3: Add Data to MongoDB (5 min)

**Option A - Quick Test Data**:
```bash
python3 add_sample_data.py
```
Creates 30 days of sample data automatically ⚡

**Option B - Your CSV Data**:
```bash
python3 dataset_creator.py
```
Use if you have `batter_shop_data.csv`

**Need at minimum**: 14 days of demand data per user

---

## ✅ STEP 4: Register a User (2 min)
```bash
python3 main.py register
```

Enter information:
- Name: Raj's Batter Shop
- Email: raj@battershop.com
- Phone: 9876543210 (10 digits)
- Age: 35
- Location: Mumbai
- Baseline demand: 50 kg
- Restaurant share: 0.65

**Get**: User ID (write it down!)

---

## ✅ STEP 5: Train Models (2-5 min)
```bash
python3 main.py retrain
```

This:
- Loads all MongoDB data
- Trains Random Forest model
- Trains XGBoost model
- Saves to `models/` folder

**Creates**: `rf_model.pkl` and `xgb_model.pkl`

---

## ✅ STEP 6: Test Prediction (1 min)
```bash
python3 main.py predict
```

Enter User ID (from Step 4)

**See predictions**:
```
Random Forest  : 45.32 kg
XGBoost        : 47.89 kg
Average        : 46.61 kg ✨
```

**Status**: ✅ If you see this, system works!

---

## 🟢 OPTIONAL: Twilio WhatsApp (10 min)

1. Create account: https://www.twilio.com/console
2. Get credentials (Account SID, Auth Token, Phone)
3. Add to `.env`:
   ```dotenv
   TWILIO_ACCOUNT_SID=ACxxxxxxxx
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
   ```
4. Test:
   ```bash
   python3 main.py predict-whatsapp
   ```

---

## 📊 What Each Component Does

```
┌─────────────────────────────────────┐
│     MongoDB (Your Database)         │ ← Stores demand data
└─────────────────────────────────────┘
              ↓ (feeds)
┌─────────────────────────────────────┐
│  ML Pipeline (Train & Predict)      │ ← Makes predictions
│  - Preprocess                       │
│  - Train (RF + XGBoost)            │
│  - Save Models                      │
└─────────────────────────────────────┘
              ↓ (generates)
┌─────────────────────────────────────┐
│  Predictions                        │ ← Random Forest + XGBoost
│  RF: 45 kg, XGB: 48 kg, Avg: 46 kg│
└─────────────────────────────────────┘
              ↓ (sends to)
┌─────────────────────────────────────┐
│  User's Phone (WhatsApp)            │ ← Optional: Twilio
└─────────────────────────────────────┘
```

---

## 🔄 Daily After Setup

```bash
# Every morning
python3 main.py predict              # See forecast

# Every evening
python3 main.py log-minimal          # Log sales

# Every night
python3 main.py retrain              # Update model
```

---

## 🚀 Quick Start (Copy & Paste)

```bash
# Activate & Install
source venv/bin/activate
pip install -r requirements.txt

# Add test data
python3 add_sample_data.py

# Register user (use defaults)
python3 main.py register

# Train models
python3 main.py retrain

# Get predictions
python3 main.py predict

# ✅ Done!
```

---

## 📝 Prerequisites Checklist

Before you start, you need:

- ✅ Python 3.8+ (you have this)
- ✅ MongoDB URI in `.env` (you have this)
- ✅ Internet connection (for MongoDB & optional Twilio)
- ❓ Historical data (14+ days recommended)

If you don't have historical data, use:
```bash
python3 add_sample_data.py
```

---

## ⚡ Fastest Path (10 Minutes)

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Have dependencies
pip install -r requirements.txt

# 3. Add sample data
python3 add_sample_data.py

# 4. Register user
echo "1001" | python3 -c "
import sys
user_id = sys.stdin.read().strip()
print(f'User {user_id} registered')
"

# 5. Train
python3 main.py retrain

# 6. Predict
python3 main.py predict

# ✅ Success!
```

---

## 🎯 Success Criteria

✅ You're done when:

1. `python3 main.py check` shows records in database
2. User registered with valid User ID
3. `models/` folder has `rf_model.pkl` and `xgb_model.pkl`
4. `python3 main.py predict` shows 3 numbers (RF, XGB, Average)

---

## 📚 Documentation

- **Quick**: [QUICK_START.md](QUICK_START.md)
- **Detailed**: [COMPLETE_SETUP.md](COMPLETE_SETUP.md)
- **Automated**: `python3 setup.py`
- **Architecture**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

## ⏱️ Time Estimates

| Step | Time | Status |
|------|------|--------|
| 1. Environment | 5 min | ✅ Done |
| 2. MongoDB | 1 min | ✅ Connected |
| 3. Add Data | 5 min | 🟡 Need to do |
| 4. Register User | 2 min | 🟡 Need to do |
| 5. Train Model | 3 min | 🟡 Need to do |
| 6. Test | 1 min | 🟡 Need to do |
| 7. Twilio (opt) | 10 min | 🔵 Optional |
| **TOTAL** | **~20 min** | 🔄 In progress |

---

## 🌟 You're All Set When:

```
✅ Environment activated
✅ Packages installed
✅ MongoDB connected
✅ Data in database (30+ records)
✅ User registered
✅ Models trained (2 files)
✅ Predictions working
```

**Then**: You can use `python3 main.py [command]` for daily operations

---

**Start Now!**
```bash
python3 add_sample_data.py
```

Next: `python3 main.py register`

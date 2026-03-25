# 🎯 QUICK START - Everything You Need

## ⚡ TL;DR (5 Minutes)

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Install dependencies (if first time)
pip install -r requirements.txt

# 3. Check MongoDB connection
python3 main.py check

# 4. Register a user
python3 main.py register

# 5. Train the model
python3 main.py retrain

# 6. Get a prediction
python3 main.py predict

# Done! ✅
```

---

## 📋 Complete Checklist (What Needs to Be Done)

### ✅ Step 1: Environment Setup
- [ ] Python 3.8+ installed
- [ ] Virtual environment created: `python3 -m venv venv`
- [ ] Virtual environment activated: `source venv/bin/activate`

### ✅ Step 2: Install Packages
- [ ] Run: `pip install -r requirements.txt`
- [ ] Verify: `pip list` shows all packages

### ✅ Step 3: MongoDB
- [ ] MongoDB URI in `.env`: `MONGO_URI=mongodb+srv://...`
- [ ] Connection works: `python3 main.py check`
- [ ] At least 14 days of data per user
  - Option A: Already have CSV data → run dataset_creator
  - Option B: Manually insert sample data using MongoDB script

### ✅ Step 4: User Registration
- [ ] Register at least one user: `python3 main.py register`
- [ ] User has valid email and phone
- [ ] Note the User ID (e.g., 1001)

### ✅ Step 5: Model Training
- [ ] Run: `python3 main.py retrain`
- [ ] Verify models created: `ls models/` shows `rf_model.pkl` and `xgb_model.pkl`

### ✅ Step 6: Test Prediction
- [ ] Run: `python3 main.py predict`
- [ ] Enter User ID from registration
- [ ] Should see predictions: Random Forest, XGBoost, Average

### ❓ Optional: WhatsApp Setup
- [ ] Create Twilio account (free): https://www.twilio.com/console
- [ ] Get Account SID and Auth Token
- [ ] Get WhatsApp phone number from Twilio
- [ ] Add to `.env`:
  ```dotenv
  TWILIO_ACCOUNT_SID=ACxxxxxxxx
  TWILIO_AUTH_TOKEN=your_token
  TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
  ```
- [ ] Test: `python3 main.py predict-whatsapp`

---

## 🔄 Daily Workflow

```bash
# Every morning at 8 AM - Get predictions
python3 main.py predict              # Single user
python3 main.py predict-batch        # All users

# Every evening - Log sales
python3 main.py log-minimal          # Quick entry
python3 main.py log                  # Detailed entry

# Every night - Retrain model
python3 main.py retrain

# Optional - Automate daily at 8 AM
python3 main.py scheduler --time 08:00
```

---

## 🎯 All Available Commands

| Command | Purpose |
|---------|---------|
| `python3 main.py register` | Register new user |
| `python3 main.py predict` | Get prediction (single) |
| `python3 main.py predict-whatsapp` | Send prediction via WhatsApp |
| `python3 main.py predict-batch` | Send to all users |
| `python3 main.py log` | Log sales (detailed) |
| `python3 main.py log-minimal` | Log sales (quick) |
| `python3 main.py check` | Check MongoDB |
| `python3 main.py retrain` | Train models |
| `python3 main.py api` | Start API server |
| `python3 main.py scheduler` | Schedule daily predictions |
| `python3 main.py debug` | Debug info |

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "No module named..." | `source venv/bin/activate && pip install -r requirements.txt` |
| "Connection refused" | Check MongoDB URI in `.env` |
| "Need 7+ records" | Insert more data into MongoDB |
| "No models found" | Run `python3 main.py retrain` |
| "User not found" | Register with `python3 main.py register` |

---

## 📁 File Structure

```
ML_Project/
├── main.py                    ← Main CLI
├── .env                       ← Configuration (MongoDB, Twilio)
├── requirements.txt           ← Python packages
├── setup.py                   ← Automated setup
│
├── scripts/                   ← All CLI commands
├── config/                    ← Settings
├── database/                  ← MongoDB connection
├── services/                  ← Business logic
├── ml/                        ← ML pipeline (train, predict)
├── models/                    ← Saved models (auto-created)
│
└── docs/
    ├── SETUP_COMPLETE.md      ← Detailed setup guide
    ├── PROJECT_STRUCTURE.md   ← Architecture
    ├── MIGRATION_GUIDE.md     ← Import reference
    ├── WHATSAPP_SETUP.md      ← Twilio guide
    └── README.md              ← Main readme
```

---

## 🚀 Automated Setup

```bash
# Run automated setup script
python3 setup.py

# This does:
# 1. Check Python version
# 2. Create virtual environment
# 3. Install dependencies
# 4. Test MongoDB connection
# 5. Verify project structure
```

---

## 📊 What Each Component Needs

### MongoDB
- ✅ Connection URI in `.env`
- ✅ At least 14 days of data per user
- ✅ Fields: user_id, Date, restaurant_sales_kg, retail_sales_kg, weather, holidays, etc.

### Model Training
- ✅ 14+ days of data per user
- ✅ Trains Random Forest + XGBoost
- ✅ Saves to `models/`
- ✅ Takes 1-2 minutes

### Predictions
- ✅ Trained models in `models/`
- ✅ Registered user
- ✅ 7+ days of user history
- ✅ Returns RF prediction, XGBoost prediction, average

### WhatsApp (Optional)
- ✅ Twilio account with WhatsApp enabled
- ✅ Account SID, Auth Token, Phone number in `.env`
- ✅ User with phone number registered
- ⚠️ Requires internet connection
- ⚠️ May have costs (check Twilio pricing)

---

## ✅ Success Indicators

```
✅ MongoDB has data                    (python3 main.py check)
✅ User is registered                  (python3 main.py register)
✅ Models are trained                  (models/ has 2 PKL files)
✅ Predictions work                    (python3 main.py predict)
✅ WhatsApp sends (optional)           (python3 main.py predict-whatsapp)
```

---

## 🎯 System Architecture

```
MongoDB Database
    ↓ (stores)
User Data & Historical Demand
    ↓ (feeds)
ML Pipeline (Preprocess → Train → Predict)
    ↓ (generates)
Predictions (RF + XGBoost averaged)
    ↓ (sends via)
WhatsApp API (Twilio)
    ↓
User's Phone
```

---

## 📞 Help Resources

1. **Detailed Setup**: See `SETUP_COMPLETE.md`
2. **Architecture**: See `PROJECT_STRUCTURE.md`
3. **Code Reference**: See `MIGRATION_GUIDE.md`
4. **WhatsApp Setup**: See `WHATSAPP_SETUP.md`
5. **Run This**: `python3 setup.py` for automated setup

---

## ⚡ Get Started Now!

```bash
# Copy-paste this:
source venv/bin/activate
pip install -r requirements.txt
python3 main.py check
python3 main.py register
python3 main.py retrain
python3 main.py predict
```

**That's it! You should see predictions! 🎉**

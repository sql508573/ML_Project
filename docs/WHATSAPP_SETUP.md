# 📱 WhatsApp Integration Setup Guide

This guide explains how to set up and use the Twilio WhatsApp integration to send demand predictions to users.

## 🚀 Quick Setup

### Step 1: Install Twilio Package

```bash
pip install twilio
# Or if updating existing installation:
pip install -r requirements.txt
```

### Step 2: Get Twilio Credentials

1. Go to [Twilio Console](https://www.twilio.com/console)
2. Sign up or log in
3. From the dashboard, copy your:
   - **Account SID**
   - **Auth Token**
4. Go to **Messaging → WhatsApp** section
5. Set up your WhatsApp sandbox or create a WhatsApp Business number
6. Copy your **WhatsApp Phone Number** (format: `whatsapp:+1234567890`)

### Step 3: Configure Environment Variables

Add these to your `.env` file:

```env
# Existing settings
MONGO_URI=mongodb://localhost:27017

# Twilio WhatsApp settings
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155552671
```

⚠️ **Important:** Keep your `.env` file secret! Never commit it to Git.

---

## 📖 Usage

### Option 1: Send Prediction to Single User

```bash
python inference_whatsapp.py
```

Then enter the User ID when prompted. The script will:
1. Fetch user data and historical records
2. Generate demand prediction
3. Send it via WhatsApp with formatted message

**Example Output:**
```
Enter User ID: 1001
✓ User found: Raj's Batter Shop
📱 Phone: 9876543210
...
📨 Sending prediction via WhatsApp...
✅ WhatsApp sent successfully to 9876543210
   Message ID: SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Option 2: Send Predictions to All Users (Batch Mode)

```bash
python inference_whatsapp.py --batch
```

This will:
1. Fetch all registered users
2. Generate predictions for each user with sufficient data
3. Send all predictions via WhatsApp
4. Show summary of successful/failed messages

**Example Output:**
```
📋 Found 3 users. Generating predictions...

Processing user 1001: Raj's Batter Shop... ✓
Processing user 1002: Priya's Batter Shop... ✓
Processing user 1003: Demo Shop... ⚠️  (no phone, skipped)

📨 Sending 2 predictions via WhatsApp...

✅ Successfully sent 2/2 messages
   ✅ WhatsApp sent successfully to 9876543210
   ✅ WhatsApp sent successfully to 8765432109
```

---

## 📤 WhatsApp Message Format

Users receive messages like this:

```
🍽️ Batter Demand Prediction - Next Day

Hi Raj! 👋

📊 Your Demand Forecast:
• Random Forest: 45.32 kg
• XGBoost: 47.89 kg
• Recommended: 46.61 kg ✨

Prepare accordingly for tomorrow! 📦
--
ML Batter Prediction System
```

---

## 🔧 Python API Usage

You can also integrate WhatsApp directly in your code:

```python
from services.whatsapp_service import WhatsAppService
from services.user_service import get_user_by_id
from ml.train import load_models
from ml.predict import build_features, predict
from services.demand_service import fetch_last_n_records, fetch_all_demand

# Get user and make prediction
user_id = 1001
user = get_user_by_id(user_id)
records = fetch_last_n_records(user_id, n=14)
all_data = fetch_all_demand()
global_avg = sum(x.get("Total_Batter_Required_kg", 0) for x in all_data) / len(all_data)

features = build_features(user, records, global_avg_demand=global_avg)
rf_model, xgb_model = load_models()
prediction = predict(rf_model, xgb_model, features, user["name"], verbose=False)

# Send via WhatsApp
ws = WhatsAppService()
result = ws.send_prediction(
    user_phone=user["phone"],
    user_name=user["name"],
    rf_pred=prediction["rf_pred"],
    xgb_pred=prediction["xgb_pred"]
)

if result["success"]:
    print(f"Message sent! ID: {result['sid']}")
else:
    print(f"Error: {result['message']}")
```

---

## 🐛 Troubleshooting

### Error: "Missing Twilio credentials"
- ✓ Check `.env` file exists in project root
- ✓ Verify all three variables are set: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_NUMBER`
- ✓ No typos in `.env`

### Error: "User does not have a phone number"
- ✓ Re-register the user with `python register_user.py`
- ✓ Ensure you provide a valid 10-digit phone number during registration

### Error: "Failed to send WhatsApp: 21211"
- This means the recipient phone number is invalid
- ✓ Verify phone number format (must be 10 digits)
- ✓ Check if the number has WhatsApp installed

### Error: "Need at least 7 historical records"
- ✓ User needs 7+ days of logged demand data
- ✓ Log daily sales using `python data/log_daily.py`

### Twilio Sandbox Mode Limitations
- In sandbox mode, all users must opt-in by sending "join" message to sandbox number
- In production, use WhatsApp Business API

---

## 📅 Automated Daily Workflow

Create a cron job to send predictions daily at 8 AM:

```bash
# Edit crontab
crontab -e

# Add this line:
0 8 * * * cd /path/to/ML_Project && source venv/bin/activate && python inference_whatsapp.py --batch >> /tmp/whatsapp_predictions.log 2>&1
```

---

## 🔒 Security Notes

1. **Never commit `.env`** - It contains API keys
2. **Keep credentials secret** - Don't share Twilio account SID or auth token
3. **Phone numbers** - Store securely in MongoDB, don't log them
4. **API costs** - Twilio charges per WhatsApp message (check pricing)

---

## 📞 Support

- Twilio Docs: https://www.twilio.com/docs/whatsapp
- WhatsApp Business API: https://www.whatsapp.com/business/api
- Twilio Python SDK: https://www.twilio.com/docs/libraries/python

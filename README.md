# Batter Shop Demand Prediction ML Pipeline

A machine learning system that predicts daily batter demand for multiple batter shops using historical sales data, weather, and event information.

## Prerequisites

- Python 3.8+
- MongoDB (running locally or remote)
- Git

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ML_Project.git
cd ML_Project
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:
```bash
pip install pandas scikit-learn xgboost pymongo python-dotenv
```

### 5. Configure MongoDB

**Option A: Local MongoDB**
```bash
# Make sure MongoDB is running
mongod
```

**Option B: MongoDB Atlas (Cloud)**
1. Create account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster and get connection string

### 6. Setup Environment Variables

Create `.env` file in project root:
```
MONGO_URI=mongodb://localhost:27017
```

Or for MongoDB Atlas:
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

---

## Workflow

### Initial Setup (One-time)

```bash
# 1. Verify MongoDB has data
python data/upload.py
# Output: Shows total records in MongoDB

# 2. Register a batter shop user
python register_user.py
# Interactive prompts - enter shop details
# Returns: User ID (e.g., 1001)

# 3. Train initial global model
python retrain_and_predict.py
# Trains on all data and saves models
```

### Daily Operations

All commands are now available through a unified CLI interface:

```bash
# Register new user
python main.py register

# Get prediction for a user  
python main.py predict

# Send prediction via WhatsApp (single)
python main.py predict-whatsapp

# Send predictions to all users (batch)
python main.py predict-batch

# Schedule automatic daily predictions
python main.py scheduler --time 08:00

# Log daily sales
python main.py log              # Detailed entry
python main.py log-minimal      # Quick entry

# Check MongoDB data
python main.py check

# Retrain models
python main.py retrain

# Start API server
python main.py api

# Debug info
python main.py debug
```

**Or run scripts individually:**
```bash
python scripts/register_user.py
python scripts/inference.py
python scripts/inference_whatsapp.py --batch
python scripts/retrain_and_predict.py
```

---

## 📁 Project Structure

The codebase follows a **modular, layered architecture**. See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed walkthrough.

Quick overview:

```bash
config/        - Settings & configuration
database/      - MongoDB connection layer
schemas/       - Data structure builders  
services/      - Business logic layer
ml/            - Machine learning pipeline
data/          - Data utilities (logging, verification)
utils/         - Validators, logging, helpers
api/           - Flask REST API
scripts/       - CLI entry points
```

---

## 🎯 Workflow

### Initial Setup (One-time)

After installation, setup your system:

```bash
# 1. Verify MongoDB has data
python main.py check

# 2. Register a batter shop user
python main.py register
# Interactive prompts - enter shop details
# Returns: User ID (e.g., 1001)

# 3. Train initial global model
python main.py retrain
# Trains on all data and saves models
```

### Daily Operations

```bash
# 1. Morning: Get prediction for a user
python main.py predict
# Enter user_id → Get demand prediction

# Or send to all users via WhatsApp
python main.py predict-batch

# 2. End of day: Log today's sales
python main.py log              # Full details
python main.py log-minimal      # Quick summary

# 3. End of day: Retrain with updated data
python main.py retrain
```

### 📱 WhatsApp Notifications

Send demand predictions via WhatsApp to users:

```bash
# Single user prediction via WhatsApp
python main.py predict-whatsapp
# Enter user_id → Prediction sent to their phone

# Batch: Send predictions to all users
python main.py predict-batch

# Schedule automatic daily predictions
python main.py scheduler --time 08:00
```

**Setup:** See [WHATSAPP_SETUP.md](WHATSAPP_SETUP.md) for Twilio configuration

---

## Project Structure

```
ML_Project/
├── .env                          # Environment variables (MONGO_URI)
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
├── requirements.txt              # Python dependencies
│
├── config/                       # Configuration
│   ├── __init__.py
│   └── settings.py              # Database & feature columns config
│
├── db/                           # Database layer
│   └── mongo_client.py          # MongoDB connection
│
├── schemas/                      # Data structure builders
│   ├── user_schema.py           # User document structure
│   └── demand_schema.py         # Demand document structure
│
├── services/                     # Business logic & queries
│   ├── user_service.py          # User CRUD operations
│   └── demand_service.py        # Demand CRUD operations
│
├── ml/                           # Machine learning pipeline
│   ├── preprocess.py            # Feature engineering
│   ├── train.py                 # Model training (RF + XGBoost)
│   ├── predict.py               # Feature building & predictions
│   └── evaluate.py              # Model metrics (MAE, RMSE, R²)
│
├── data/                         # Data utilities
│   ├── upload.py                # Check MongoDB data
│   └── log_daily.py             # Daily sales logging
│
├── models/                       # Saved trained models (auto-created)
│   ├── rf_model.pkl            # Random Forest model
│   └── xgb_model.pkl           # XGBoost model
│
├── inference.py                  # Make predictions (entry point)
├── register_user.py              # Register new users (entry point)
├── retrain_and_predict.py        # Retrain models (entry point)
│
├── venv/                         # Virtual environment (not in git)
└── __pycache__/                  # Python cache (not in git)
```

---

## Entry Points

| Script | Purpose | When to Use |
|--------|---------|-----------|
| `inference.py` | Get demand prediction | Morning - anytime |
| `register_user.py` | Register new batter shop | Once per shop |
| `retrain_and_predict.py` | Retrain global model | After initial setup, nightly |
| `data/upload.py` | Check MongoDB data | Verify data exists |
| `data/log_daily.py` | Log daily sales data | End of each day |
| `inference_whatsapp.py` | Send prediction via WhatsApp | Morning - send to single/all users |
| `schedule_whatsapp_predictions.py` | Schedule automatic WhatsApp sends | Run once, sends daily at set time |

---

## Features Used (13 total)

**Temporal:**
- Day_of_Week, Month, Is_Weekend

**Environmental:**
- Avg_Temp_C, Rainy_Day, Public_Holiday

**Business:**
- Promotion_Flag, Prev_Day_Demand_kg

**Lag & Rolling Statistics:**
- Lag_1, Lag_2, Lag_3
- Rolling_Mean_7, Rolling_Std_7

**Target Variable:**
- Total_Batter_Required_kg (restaurant + retail sales)

---

## Models

- **Random Forest**: 200 decision trees
- **XGBoost**: 200 boosted trees, learning_rate=0.05
- **Prediction**: Average of both models

---

## Database

**Name:** BatterShopDB

**Collections:**
- **Users**: user_id, name, email, phone, age, location, shop_constants
- **DailyDemand**: user_id, Date, features, sales data (1463+ records)

---

## Troubleshooting

**MongoDB connection error:**
```
Ensure MongoDB is running. Start with: mongod
```

**"Not enough data to train" error:**
```
Need at least 5 preprocessed records. 
Ensure historical data is uploaded to MongoDB.
```

**Module import error:**
```
Verify you're in the virtual environment:
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Mac/Linux
```

**Models not found:**
```
Train the model first:
python retrain_and_predict.py
```

---

## Example Workflow

```bash
# Day 1 - Setup
python register_user.py        # Register user 1001
python retrain_and_predict.py  # Train models

# Day 2+ - Daily Use
python inference.py            # Morning: predict demand
python data/log_daily.py       # Evening: log sales
python retrain_and_predict.py  # Evening: retrain model

# Repeat daily...
```

---

## Notes

- All data flows through **MongoDB** (no CSV files used at runtime)
- Models are **global** - trained on all user data
- Each user's predictions use their own last 7 days + global model
- Lag features are created **per user** (no leakage between users)

---

## Support

For issues or questions, check:
1. MongoDB is running and `.env` is configured
2. All Python dependencies installed: `pip list`
3. Historical data exists: `python data/upload.py`

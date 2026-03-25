# 📁 Project Structure - ML Batter Shop Demand Prediction System

## Overview

The codebase is organized in a modular, layered architecture for maintainability and scalability:

```
ML_Project/
│
├── 📄 main.py                      # CLI entry point - router for all commands
├── 📄 __main__.py                  # Python -m entry point
├── 📄 .env                         # Environment variables (MongoDB URI, Twilio creds)
├── 📄 requirements.txt             # Python dependencies
├── 📄 README.md                    # Main documentation
├── 📄 WHATSAPP_SETUP.md           # WhatsApp integration guide
│
├── 📁 config/                      # ⚙️ Configuration & Settings
│   ├── __init__.py                # Exports settings
│   └── settings.py                # Core configuration (MongoDB, feature columns)
│
├── 📁 database/                    # 🗄️ Database Layer
│   ├── __init__.py                # Exports database utilities
│   └── mongo_client.py            # MongoDB connection management
│
├── 📁 schemas/                     # 📋 Data Schemas
│   ├── __init__.py                # Exports schema builders
│   ├── user_schema.py             # User data structure
│   └── demand_schema.py           # Demand record structure
│
├── 📁 services/                    # 🔧 Business Logic Layer
│   ├── __init__.py                # Exports all services
│   ├── user_service.py            # User CRUD operations
│   ├── demand_service.py          # Demand CRUD operations
│   └── whatsapp_service.py        # Twilio WhatsApp integration
│
├── 📁 ml/                          # 🤖 Machine Learning Pipeline
│   ├── __init__.py                # Exports ML functions
│   ├── preprocess.py              # Feature engineering & preprocessing
│   ├── train.py                   # Model training (Random Forest + XGBoost)
│   ├── predict.py                 # Feature building & predictions
│   └── evaluate.py                # Model evaluation metrics
│
├── 📁 data/                        # 📊 Data Utilities
│   ├── __init__.py                # Exports data functions
│   ├── upload.py                  # Check MongoDB data
│   ├── log_daily.py               # Log daily sales (detailed)
│   └── log_daily_minimal.py       # Log daily sales (minimal input)
│
├── 📁 utils/                       # 🛠️ Utility Functions
│   ├── __init__.py                # Exports utilities
│   ├── logger.py                  # Logging setup & configuration
│   └── validators.py              # Input validation functions
│
├── 📁 api/                         # 🌐 API Layer
│   ├── __init__.py                # Exports API app factory
│   └── interface.py               # Flask REST API endpoints
│
├── 📁 scripts/                     # 🚀 CLI Entry Points (Scripts)
│   ├── __init__.py                # Package marker
│   ├── register_user.py           # Register new user
│   ├── inference.py               # Get single prediction
│   ├── inference_whatsapp.py      # Send via WhatsApp (single/batch)
│   ├── retrain_and_predict.py     # Retrain models
│   ├── schedule_whatsapp.py       # Schedule daily predictions
│   └── debug.py                   # Debug database
│
├── 📁 models/                      # 💾 Saved Models (auto-generated)
│   ├── rf_model.pkl               # Random Forest model
│   └── xgb_model.pkl              # XGBoost model
│
└── 📁 __pycache__/                 # Python cache (auto-generated)
```

---

## 🏗️ Architecture Layers

### 1. **Database Layer** (`database/`)
- Handles all MongoDB connections
- Centralized connection management
- **Clean separation**: Business logic doesn't create connections

```python
from database import get_db  # Always use this
```

### 2. **Schema Layer** (`schemas/`)
- Defines data structures for users and demand records
- Document builders for MongoDB documents
- Ensures data consistency

```python
from schemas import build_user_doc, build_demand_doc
```

### 3. **Services Layer** (`services/`)
- **User Service**: User CRUD operations, user lookups
- **Demand Service**: Demand data operations
- **WhatsApp Service**: External API integration (Twilio)
- **Business logic encapsulation**: All data operations here

```python
from services import get_user_by_id, insert_demand, WhatsAppService
```

### 4. **ML Pipeline** (`ml/`)
- **Preprocess**: Feature engineering, data cleaning
- **Train**: Model training, model persistence
- **Predict**: Feature building, inference
- **Evaluate**: Performance metrics

```python
from ml import preprocess, train, build_features, predict
```

### 5. **Utilities** (`utils/`)
- **Logger**: Centralized logging
- **Validators**: Input validation helpers
- **DRY principle**: Reusable functions

```python
from utils import validate_email, validate_phone, get_logger
```

### 6. **Data Utilities** (`data/`)
- **Upload**: Check MongoDB data
- **Log Daily**: Log sales with full details
- **Log Minimal**: Quick sales logging

```python
from data import check_data_in_db, run_log_daily
```

### 7. **API Layer** (`api/`)
- Flask REST endpoints
- External system integration
- JSON request/response handling

```python
from api import create_app
app = create_app()
```

### 8. **CLI Scripts** (`scripts/`)
- Entry points for user-facing operations
- Each script is independent
- All can be called via `main.py`

```python
from scripts import register_user, run_inference
```

### 9. **Configuration** (`config/`)
- Centralized settings
- Environment variables
- ML model parameters

```python
from config import MONGO_URI, FEATURE_COLS, TARGET_COL
```

---

## 🎯 Import Patterns

### ✅ **DO: Use Package Imports**
```python
# Good - Shorter, cleaner
from config import MONGO_URI, FEATURE_COLS
from services import get_user_by_id, insert_demand, WhatsAppService
from ml import train, predict, build_features
from utils import validate_email, get_logger
from database import get_db
```

### ❌ **DON'T: Import from Submodules**
```python
# Avoid - Longer, exposes internals
from config.settings import MONGO_URI
from services.user_service import get_user_by_id
from ml.train import train
```

---

## 🚀 Using the CLI

All commands go through `main.py`:

```bash
# New user registration
python main.py register

# Get prediction
python main.py predict

# WhatsApp prediction (single user)
python main.py predict-whatsapp

# WhatsApp batch (all users)
python main.py predict-batch

# Schedule daily predictions
python main.py scheduler --time 08:00

# Log daily sales
python main.py log                # Detailed
python main.py log-minimal        # Quick entry

# Check data
python main.py check

# Retrain models
python main.py retrain

# Start API server
python main.py api

# Debug info
python main.py debug
```

Or run individually:
```bash
python scripts/register_user.py
python scripts/inference.py
```

---

## 📦 Module Responsibilities

| Module | Responsibility | Dependencies |
|--------|---|---|
| `config/` | Settings, constants | None |
| `database/` | DB connections | `config/` |
| `schemas/` | Data structures | `config/` |
| `services/` | Business logic | `database/`, `schemas/`, `config/` |
| `ml/` | ML operations | `config/` |
| `data/` | Data utilities | `services/`, `schemas/`, `database/` |
| `utils/` | Helper functions | None |
| `api/` | REST endpoints | `services/`, `ml/` |
| `scripts/` | CLI entry points | `services/`, `ml/`, `data/` |

---

## 🔄 Data Flow Example

**User registers → Gets prediction → Receives WhatsApp message:**

```
scripts/register_user.py
    ↓
schemas/build_user_doc
    ↓
services/insert_user
    ↓ (uses)
database/get_db
    ↓
MongoDB
```

**Prediction workflow:**

```
scripts/inference_whatsapp.py
    ↓
services/get_user_by_id, fetch_last_n_records
    ↓ (uses)
database/get_db
    ↓
ml/build_features, predict
    ↓
services/WhatsAppService/send_prediction
    ↓
Twilio API
```

---

## 📝 Adding New Features

### Adding a new service:
1. Create `services/new_service.py`
2. Add function to `services/__init__.py`
3. Import: `from services import new_service_func`

### Adding a new utility:
1. Create `utils/helper.py`
2. Add to `utils/__init__.py`
3. Import: `from utils import helper_func`

### Adding a new API endpoint:
1. Define route in `api/interface.py`
2. Use existing services
3. Return JSON response

---

## 🗂️ Best Practices

1. **Always import from packages, not submodules**
   - `from services import get_user_by_id` ✅
   - `from services.user_service import...` ❌

2. **Keep layers separate**
   - Don't import from scripts in other scripts
   - Services don't import scripts
   - ML doesn't know about database

3. **Use centralized imports**
   - Everything goes through `config/`
   - All data ops through `services/`
   - All ML through `ml/`

4. **Configuration is immutable**
   - Never modify settings at runtime
   - Use environment variables for secrets

5. **Services are stateless**
   - Pure functions where possible
   - No global state
   - Easy to test

---

## 🧪 Testing Structure

For future tests:

```
tests/
├── test_services.py          # Service unit tests
├── test_ml.py                # ML pipeline tests
├── test_api.py               # API endpoint tests
└── test_validators.py        # Validator tests
```

---

## 📚 Key Files Reference

| Need to... | Use this module | Function/Class |
|------------|---|---|
| Connect to DB | `database/` | `get_db()` |
| Create user doc | `schemas/` | `build_user_doc()` |
| Store/fetch user | `services/` | `insert_user()`, `get_user_by_id()` |
| Get predictions | `ml/` | `build_features()`, `predict()` |
| Send WhatsApp | `services/` | `WhatsAppService` |
| Validate input | `utils/` | `validate_email()`, etc |
| Setup logging | `utils/` | `setup_logging()` |
| Create API | `api/` | `create_app()` |
| Run CLI | `main.py` | `main()` or use scripts/ |

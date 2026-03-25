# 🔄 Migration Guide - Old to New Structure

After the codebase refactoring, some imports and file locations have changed. This guide helps you update your code.

---

## 📍 File Location Changes

### Entry Point Scripts

| **What** | **Old Command** | **New Command** |
|----------|---|---|
| Register user | `python register_user.py` | `python main.py register` or `python scripts/register_user.py` |
| Get prediction | `python inference.py` | `python main.py predict` or `python scripts/inference.py` |
| WhatsApp send | `python inference_whatsapp.py` | `python main.py predict-whatsapp` or `python scripts/inference_whatsapp.py` |
| WhatsApp batch | `python inference_whatsapp.py --batch` | `python main.py predict-batch` or `python scripts/inference_whatsapp.py --batch` |
| Scheduler | `python schedule_whatsapp_predictions.py` | `python main.py scheduler` or `python scripts/schedule_whatsapp.py` |
| Retrain models | `python retrain_and_predict.py` | `python main.py retrain` or `python scripts/retrain_and_predict.py` |
| Debug data | `python debug_data.py` | `python main.py debug` or `python scripts/debug.py` |
| Log sales | `python data/log_daily.py` | `python main.py log` or `python data/log_daily.py` |
| API server | `python api_interface.py` | `python main.py api` or custom code using `api.create_app()` |

---

## 🔧 Import Changes

### Configuration

```python
# ❌ OLD
from config.settings import MONGO_URI, DB_NAME, FEATURE_COLS, TARGET_COL

# ✅ NEW
from config import MONGO_URI, DB_NAME, FEATURE_COLS, TARGET_COL
```

### Database

```python
# ❌ OLD
from db.mongo_client import get_db

# ✅ NEW
from database import get_db
```

### Schemas

```python
# ❌ OLD
from schemas.user_schema import build_user_doc
from schemas.demand_schema import build_demand_doc

# ✅ NEW
from schemas import build_user_doc, build_demand_doc
```

### Services

```python
# ❌ OLD
from services.user_service import get_user_by_id, get_all_users, insert_user, email_exists
from services.demand_service import fetch_last_n_records, fetch_all_demand, insert_demand
from services.whatsapp_service import WhatsAppService

# ✅ NEW
from services import (
    get_user_by_id,
    get_all_users,
    insert_user,
    email_exists,
    fetch_last_n_records,
    fetch_all_demand,
    insert_demand,
    WhatsAppService,
)
```

### ML Pipeline

```python
# ❌ OLD
from ml.preprocess import preprocess
from ml.train import train, load_models
from ml.predict import build_features, predict
from ml.evaluate import evaluate

# ✅ NEW
from ml import preprocess, train, load_models, build_features, predict, evaluate
```

### Data Utilities

```python
# ❌ OLD
from data.upload import check_mongodb_data
from data.log_daily import log_daily
from data.log_daily_minimal import log_daily_minimal

# ✅ NEW
from data import check_data_in_db, run_log_daily, run_log_daily_minimal
```

### Utilities (NEW)

```python
# ✅ NEW - These didn't exist before
from utils import validate_email, validate_phone, validate_numeric, get_logger

# Setup logging
logger = get_logger(__name__)
logger.info("My message")

# Validate inputs
if validate_email(user_email):
    print("Valid email")
```

### API

```python
# ❌ OLD
import api_interface
api_interface.app.run()

# ✅ NEW
from api import create_app
app = create_app()
app.run()
```

---

## 📝 Common Patterns - Before & After

### Custom Script Using Old Structure

```python
# ❌ OLD - Old imports and pattern
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.user_service import get_user_by_id
from services.demand_service import fetch_last_n_records, fetch_all_demand
from ml.train import load_models
from ml.predict import build_features, predict
from db.mongo_client import get_db
from config.settings import FEATURE_COLS

def my_custom_function():
    user = get_user_by_id(1001)
    records = fetch_last_n_records(1001, n=14)
    all_data = fetch_all_demand()
    # ... rest of code
```

### Same Script with New Structure

```python
# ✅ NEW - Cleaner imports and pattern
from services import get_user_by_id, fetch_last_n_records, fetch_all_demand
from ml import load_models, build_features, predict
from database import get_db
from config import FEATURE_COLS

def my_custom_function():
    user = get_user_by_id(1001)
    records = fetch_last_n_records(1001, n=14)
    all_data = fetch_all_demand()
    # ... rest of code (exactly the same!)
```

---

## 🎯 Migration Checklist

- [ ] Update all `from config.settings import` → `from config import`
- [ ] Update all `from db.mongo_client import` → `from database import`
- [ ] Update all `from services.X_service import` → `from services import`
- [ ] Update all `from ml.X import` → `from ml import`
- [ ] Update all `from schemas.X_schema import` → `from schemas import`
- [ ] Update all `from data.X import` → `from data import`
- [ ] Change script calls from direct execution to `python main.py <command>`
- [ ] Remove old root-level scripts if using `main.py`
- [ ] Review any custom API code to use `from api import create_app`

---

## 🔍 Finding What Moved

### Function is in services?
```python
from services import the_function_name
```

### Function is in ml?
```python
from ml import the_function_name
```

### Configuration constant?
```python
from config import THE_CONSTANT
```

### Validation or logging utility?
```python
from utils import validator_or_logger_function
```

### Need database connection?
```python
from database import get_db
```

---

## ❓ Troubleshooting

### Error: `ModuleNotFoundError: No module named 'services.user_service'`
**Solution:** Use the new import style
```python
# ❌ This is old
from services.user_service import get_user_by_id

# ✅ Use this instead
from services import get_user_by_id
```

### Error: `ModuleNotFoundError: No module named 'db'`
**Solution:** The `db/` module was renamed to `database/`
```python
# ❌ Old
from db.mongo_client import get_db

# ✅ New
from database import get_db
```

### Error: `ImportError: cannot import name 'app' from 'api_interface'`
**Solution:** The API structure changed. Use the factory function
```python
# ❌ Old
from api_interface import app

# ✅ New
from api import create_app
app = create_app()
```

### Scripts aren't found
**Solution:** They moved to `scripts/` directory
```bash
# ❌ Old
python register_user.py

# ✅ New - Use main.py
python main.py register

# ✅ Or call scripts directly
python scripts/register_user.py
```

---

## 📚 Learn More

- See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed architecture
- See [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) for what changed
- Check individual `__init__.py` files to see what's exported from each module

---

## 💡 Pro Tips

1. **Use the CLI** - Most operations go through `main.py` now
2. **Check `__init__.py`** - See what's exported from each package
3. **Follow import patterns** - All imports should be from packages, not submodules
4. **See examples** - Check `scripts/` for working examples of imports

---

## ✅ Verification

After migrating, verify your code works:

```bash
# Run a simple test
python main.py check       # Should show DB record count

# Register a test user
python main.py register    # Should complete registration

# Get a prediction
python main.py predict     # Should work if data exists
```

If you get import errors, refer back to the import changes table above.

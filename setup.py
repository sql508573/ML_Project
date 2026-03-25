#!/usr/bin/env python3
"""
Automated setup script for ML Batter Shop system
Handles environment setup, dependencies, and initial configuration
"""
import sys
import os
import subprocess
from datetime import datetime, timedelta

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"🚀 {text}")
    print(f"{'='*60}\n")

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"  → {description}...", end=" ", flush=True)
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print_success("Done")
            return True
        else:
            print_error(f"Failed: {result.stderr[:100]}")
            return False
    except subprocess.TimeoutExpired:
        print_error("Timeout")
        return False
    except Exception as e:
        print_error(str(e)[:100])
        return False

def setup_python_env():
    """Setup Python virtual environment"""
    print_header("STEP 1: Python Environment")
    
    # Check Python version
    print("  → Checking Python version...", end=" ", flush=True)
    result = subprocess.run("python3 --version", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        version = result.stdout.strip()
        print(f"✅ {version}")
    else:
        print_error("Python 3 not found")
        return False
    
    # Create venv if doesn't exist
    if not os.path.exists("venv"):
        if run_command("python3 -m venv venv", "Creating virtual environment"):
            print_success("Virtual environment created")
        else:
            return False
    else:
        print_success("Virtual environment already exists")
    
    return True

def install_dependencies():
    """Install required packages"""
    print_header("STEP 2: Install Dependencies")
    
    # Upgrade pip
    if run_command("pip install --upgrade pip", "Upgrading pip"):
        pass
    
    # Install requirements
    if run_command("pip install -r requirements.txt", "Installing packages from requirements.txt"):
        print_success("All packages installed")
        return True
    else:
        print_error("Failed to install packages")
        return False

def check_mongodb():
    """Check MongoDB connection"""
    print_header("STEP 3: MongoDB Setup")
    
    print("  → Testing MongoDB connection...", end=" ", flush=True)
    try:
        from pymongo import MongoClient
        from dotenv import load_dotenv
        
        load_dotenv()
        uri = os.getenv("MONGO_URI")
        
        if not uri:
            print_error("MONGO_URI not found in .env")
            return False
        
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        
        db = client["BatterShopDB"]
        collection = db["DailyDemand"]
        count = collection.count_documents({})
        
        print(f"✅ Connected")
        print(f"  → Records in database: {count}")
        
        if count < 14:
            print_info(f"Need at least 14 records for predictions (have {count})")
            print_info("Use: python3 -c \"from pymongo import MongoClient; ...\" to add sample data")
            return None  # Warn but don't fail
        
        return True
    except Exception as e:
        print_error(str(e)[:100])
        return False

def add_env_variables():
    """Add Twilio env variables (optional)"""
    print_header("STEP 4: Environment Variables")
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print_error(".env file not found")
        return False
    
    print_success(".env file found")
    
    # Read .env
    with open(".env", "r") as f:
        env_content = f.read()
    
    # Check what's configured
    has_mongo = "MONGO_URI" in env_content
    has_twilio = "TWILIO_ACCOUNT_SID" in env_content
    
    print(f"  ✅ MongoDB URI: {'Configured' if has_mongo else 'Missing'}")
    print(f"  ⚙️  Twilio: {'Configured' if has_twilio else 'Not configured'}")
    
    if not has_twilio:
        print_info("WhatsApp features need Twilio setup (optional)")
        print_info("See WHATSAPP_SETUP.md for instructions")
    
    return True

def train_models():
    """Ask to train models"""
    print_header("STEP 5: Model Training")
    
    if os.path.exists("models/rf_model.pkl"):
        print_success("Models already trained")
        return True
    else:
        print_info("Models not found. Run: python3 main.py retrain")
        return None  # Warn but don't fail

def verify_system():
    """Verify system is working"""
    print_header("STEP 6: System Verification")
    
    print("  → Checking project structure...", end=" ", flush=True)
    required_dirs = ["config", "database", "services", "ml", "data", "scripts", "utils", "api"]
    
    all_exist = all(os.path.isdir(d) for d in required_dirs)
    
    if all_exist:
        print_success("All directories found")
    else:
        missing = [d for d in required_dirs if not os.path.isdir(d)]
        print_error(f"Missing: {', '.join(missing)}")
        return False
    
    return True

def print_next_steps():
    """Print next steps"""
    print_header("NEXT STEPS")
    
    print("""
1. ADD DATA TO MONGODB
   → Need at least 14-30 days of historical data per user
   → Use dataset_creator.py or insert sample data
   
2. REGISTER A USER
   python3 main.py register
   
3. TRAIN MODELS
   python3 main.py retrain
   
4. GET PREDICTIONS
   python3 main.py predict
   
5. (OPTIONAL) SETUP TWILIO
   - Get Twilio account: https://www.twilio.com/console
   - Add credentials to .env
   - python3 main.py predict-whatsapp
   
6. SCHEDULE DAILY PREDICTIONS
   python3 main.py scheduler --time 08:00

📚 Read SETUP_COMPLETE.md for detailed instructions
""")

def main():
    """Run setup"""
    print("\n" + "="*60)
    print("🎯 ML BATTER SHOP - AUTOMATED SETUP")
    print("="*60)
    
    # Step 1: Python env
    if not setup_python_env():
        print_error("Python environment setup failed")
        return False
    
    # Step 2: Dependencies
    if not install_dependencies():
        print_error("Dependencies installation failed")
        return False
    
    # Step 3: MongoDB
    result = check_mongodb()
    if result is False:
        print_error("MongoDB connection failed")
        return False
    elif result is None:
        print_info("MongoDB connected but has limited data")
    
    # Step 4: Environment
    if not add_env_variables():
        print_error("Environment setup failed")
        return False
    
    # Step 5: Models
    result = train_models()
    if result is None:
        print_info("Models need to be trained after adding data")
    
    # Step 6: Verify
    if not verify_system():
        print_error("System verification failed")
        return False
    
    # Success!
    print_header("✅ SETUP COMPLETE!")
    
    print("""
Your system is ready! Next steps:

1. Add historical data to MongoDB (at least 30 days per user)
2. Register a user: python3 main.py register
3. Train models: python3 main.py retrain
4. Get predictions: python3 main.py predict

📚 For detailed instructions, see SETUP_COMPLETE.md
""")
    
    print_next_steps()
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

#!/usr/bin/env python
"""
Main CLI entry point for the ML Batter Shop Demand Prediction System

Usage:
    python main.py register          - Register a new user
    python main.py predict           - Get prediction for a user
    python main.py predict-whatsapp  - Send prediction via WhatsApp
    python main.py predict-batch     - Send predictions to all users (batch)
    python main.py scheduler         - Schedule daily WhatsApp predictions
    python main.py log               - Log daily sales data
    python main.py log-minimal       - Log daily sales (minimal input)
    python main.py check             - Check MongoDB data
    python main.py retrain           - Retrain models with latest data
    python main.py api               - Start Flask API server
    python main.py debug             - Debug database information
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Main CLI dispatcher"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()

    try:
        if command == "register":
            from scripts.register_user import register_user
            register_user()

        elif command == "predict":
            from scripts.inference import run_inference
            run_inference()

        elif command == "predict-whatsapp":
            from scripts.inference_whatsapp import run_inference_whatsapp
            run_inference_whatsapp()

        elif command == "predict-batch":
            from scripts.inference_whatsapp import run_inference_whatsapp_batch
            run_inference_whatsapp_batch()

        elif command == "scheduler":
            from scripts.schedule_whatsapp import main as scheduler_main
            scheduler_main()

        elif command == "log":
            from data import run_log_daily
            run_log_daily()

        elif command == "log-minimal":
            from data import run_log_daily_minimal
            run_log_daily_minimal()

        elif command == "check":
            from data import check_data_in_db
            check_data_in_db()

        elif command == "retrain":
            from scripts.retrain_and_predict import run_retrain_and_predict
            run_retrain_and_predict()

        elif command == "api":
            from api.interface import create_app
            app = create_app()
            print("\n🚀 Starting API server on http://127.0.0.1:5000")
            print("📖 API Endpoints:")
            print("   POST /predict - Get demand prediction")
            print("   POST /log     - Log daily sales data")
            print("\n(Press Ctrl+C to stop)\n")
            app.run(debug=True, host="0.0.0.0", port=5000)

        elif command == "debug":
            from scripts.debug import debug_data
            debug_data()

        else:
            print(f"❌ Unknown command: {command}\n")
            print(__doc__)
            sys.exit(1)

    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("\n💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n🛑 Operation cancelled by user.")
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

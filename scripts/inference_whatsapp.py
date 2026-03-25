"""WhatsApp Inference Script - Send demand predictions via Twilio WhatsApp API"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import (
    get_user_by_id, 
    fetch_last_n_records, 
    fetch_all_demand,
    WhatsAppService,
)
from ml import load_models, build_features, predict


def run_inference_whatsapp():
    """Get prediction for user and send via WhatsApp"""
    print("\n===== WhatsApp Prediction - Single User =====\n")
    
    user_id_input = input("Enter User ID: ").strip()
    if not user_id_input.isdigit():
        print("❌ User ID must be a number.")
        return

    user_id = int(user_id_input)
    user = get_user_by_id(user_id)
    if not user:
        print(f"❌ No user found with User ID: {user_id}")
        return

    print(f"✓ User found: {user['name']}")
    
    # Check if phone number exists
    if "phone" not in user or not user["phone"]:
        print("❌ User does not have a phone number. Please register with a valid phone number.")
        return
    
    print(f"📱 Phone: {user['phone']}")
    
    # Fetch prediction
    records = fetch_last_n_records(user_id, n=14)
    if len(records) < 7:
        print("❌ Need at least 7 historical records for this user to run prediction.")
        return

    all_data = fetch_all_demand()
    global_avg = 0.0
    if all_data:
        global_avg = sum(x.get("Total_Batter_Required_kg", 0) for x in all_data) / len(all_data)

    features = build_features(user, records, global_avg_demand=global_avg)
    if features is None:
        return

    rf_model, xgb_model = load_models()
    prediction = predict(rf_model, xgb_model, features, user["name"], verbose=True)
    
    # Send via WhatsApp
    print("\n📨 Sending prediction via WhatsApp...")
    try:
        ws = WhatsAppService()
        result = ws.send_prediction(
            user_phone=user["phone"],
            user_name=user["name"],
            rf_pred=prediction["rf_pred"],
            xgb_pred=prediction["xgb_pred"]
        )
        
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"   Message ID: {result['sid']}")
        else:
            print(f"❌ {result['message']}")
    
    except ValueError as e:
        print(f"❌ Configuration Error: {str(e)}")
        print("\n📋 Setup Instructions:")
        print("   1. Get Twilio credentials from https://www.twilio.com/console")
        print("   2. Add to your .env file:")
        print("      TWILIO_ACCOUNT_SID=your_account_sid")
        print("      TWILIO_AUTH_TOKEN=your_auth_token")
        print("      TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890")
        print("   3. Re-run this script")
    
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")


def run_inference_whatsapp_batch():
    """Send predictions to all registered users"""
    print("\n===== WhatsApp Predictions - Batch Mode =====\n")
    
    from services import get_all_users
    
    users = get_all_users()
    if not users:
        print("❌ No users found in database.")
        return
    
    print(f"📋 Found {len(users)} users. Generating predictions...\n")
    
    predictions_list = []
    
    for user in users:
        user_id = user.get("user_id")
        print(f"Processing user {user_id}: {user.get('name')}...", end=" ")
        
        # Skip if no phone
        if "phone" not in user or not user["phone"]:
            print("⚠️  (no phone, skipped)")
            continue
        
        try:
            records = fetch_last_n_records(user_id, n=14)
            if len(records) < 7:
                print("⚠️  (insufficient data, skipped)")
                continue
            
            all_data = fetch_all_demand()
            global_avg = 0.0
            if all_data:
                global_avg = sum(x.get("Total_Batter_Required_kg", 0) for x in all_data) / len(all_data)
            
            features = build_features(user, records, global_avg_demand=global_avg)
            if features is None:
                print("❌ (feature building failed)")
                continue
            
            rf_model, xgb_model = load_models()
            prediction = predict(rf_model, xgb_model, features, user["name"], verbose=False)
            
            predictions_list.append({
                "user_phone": user["phone"],
                "user_name": user["name"],
                "rf_pred": prediction["rf_pred"],
                "xgb_pred": prediction["xgb_pred"]
            })
            print("✓")
        
        except Exception as e:
            print(f"❌ (error: {str(e)})")
            continue
    
    if not predictions_list:
        print("\n❌ No valid predictions to send.")
        return
    
    # Send all predictions
    print(f"\n📨 Sending {len(predictions_list)} predictions via WhatsApp...\n")
    try:
        ws = WhatsAppService()
        results = ws.send_bulk_predictions(predictions_list)
        
        success_count = sum(1 for r in results if r["success"])
        print(f"\n✅ Successfully sent {success_count}/{len(results)} messages")
        
        for result in results:
            status = "✅" if result["success"] else "❌"
            print(f"   {status} {result['message']}")
    
    except ValueError as e:
        print(f"❌ Configuration Error: {str(e)}")
        print("\n📋 Setup Instructions:")
        print("   1. Get Twilio credentials from https://www.twilio.com/console")
        print("   2. Add to your .env file:")
        print("      TWILIO_ACCOUNT_SID=your_account_sid")
        print("      TWILIO_AUTH_TOKEN=your_auth_token")
        print("      TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890")
        print("   3. Re-run this script")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Send demand predictions via WhatsApp")
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Send predictions to all users"
    )
    
    args = parser.parse_args()
    
    if args.batch:
        run_inference_whatsapp_batch()
    else:
        run_inference_whatsapp()

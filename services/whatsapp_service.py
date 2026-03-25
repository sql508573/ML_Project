"""
Twilio WhatsApp Integration for sending demand predictions to users
"""
import os
from dotenv import load_dotenv

# Try to import twilio, provide helpful error if not installed
try:
    from twilio.rest import Client
except ImportError:
    raise ImportError(
        "Twilio is not installed. Install it with: pip install twilio"
    )

load_dotenv()

class WhatsAppService:
    def __init__(self):
        """Initialize Twilio WhatsApp client"""
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone = os.getenv("TWILIO_WHATSAPP_NUMBER")  # e.g., "whatsapp:+14155552671"
        
        if not all([self.account_sid, self.auth_token, self.twilio_phone]):
            raise ValueError(
                "Missing Twilio credentials. Set TWILIO_ACCOUNT_SID, "
                "TWILIO_AUTH_TOKEN, and TWILIO_WHATSAPP_NUMBER in .env"
            )
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_prediction(self, user_phone, user_name, rf_pred, xgb_pred):
        """
        Send demand prediction via WhatsApp
        
        Args:
            user_phone (str): User's phone number (10 digits, e.g., "9876543210")
            user_name (str): User's name
            rf_pred (float): Random Forest prediction
            xgb_pred (float): XGBoost prediction
            
        Returns:
            dict: {success: bool, message: str, sid: str or None}
        """
        try:
            # Format phone number for WhatsApp
            whatsapp_phone = f"whatsapp:+91{user_phone}"  # India country code
            
            # Build prediction message
            avg_pred = (rf_pred + xgb_pred) / 2
            message_body = (
                f"🍽️ *Batter Demand Prediction - Next Day*\n\n"
                f"Hi {user_name}! 👋\n\n"
                f"📊 *Your Demand Forecast:*\n"
                f"• Random Forest: {rf_pred:.2f} kg\n"
                f"• XGBoost: {xgb_pred:.2f} kg\n"
                f"• *Recommended: {avg_pred:.2f} kg* ✨\n\n"
                f"Prepare accordingly for tomorrow! 📦\n"
                f"--\nML Batter Prediction System"
            )
            
            # Send via Twilio
            message = self.client.messages.create(
                from_=self.twilio_phone,
                body=message_body,
                to=whatsapp_phone
            )
            
            return {
                "success": True,
                "message": f"WhatsApp sent successfully to {user_phone}",
                "sid": message.sid
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to send WhatsApp: {str(e)}",
                "sid": None
            }
    
    def send_bulk_predictions(self, predictions_list):
        """
        Send predictions to multiple users
        
        Args:
            predictions_list (list): List of dicts with keys:
                - user_phone, user_name, rf_pred, xgb_pred
                
        Returns:
            list: List of result dicts
        """
        results = []
        for pred in predictions_list:
            result = self.send_prediction(
                pred["user_phone"],
                pred["user_name"],
                pred["rf_pred"],
                pred["xgb_pred"]
            )
            results.append(result)
        return results

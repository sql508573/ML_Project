"""Schedule script - Automated daily WhatsApp predictions"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from scripts.inference_whatsapp import run_inference_whatsapp_batch


class PredictionScheduler:
    """Schedule WhatsApp predictions to be sent at specific times"""
    
    def __init__(self, time_str="08:00"):
        """
        Initialize scheduler
        
        Args:
            time_str (str): Time in HH:MM format (24-hour) to send predictions daily
        """
        try:
            import schedule
            self.schedule = schedule
        except ImportError:
            raise ImportError(
                "The 'schedule' package is required. Install with: pip install schedule"
            )
        
        self.time_str = time_str
    
    def send_predictions_job(self):
        """Job function to send predictions"""
        print(f"\n{'='*60}")
        print(f"⏰ Running scheduled WhatsApp prediction job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        try:
            run_inference_whatsapp_batch()
        except Exception as e:
            print(f"\n❌ Error in scheduled job: {str(e)}")
        
        print(f"\n✅ Job completed at {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}\n")
    
    def start(self):
        """Start the scheduler"""
        import time
        
        self.schedule.every().day.at(self.time_str).do(self.send_predictions_job)
        
        print(f"📅 Scheduler started!")
        print(f"⏰ Predictions will be sent daily at {self.time_str}")
        print(f"ℹ️  Press Ctrl+C to stop the scheduler\n")
        
        while True:
            try:
                self.schedule.run_pending()
                time.sleep(60)  # Check every minute if a job needs to run
            except KeyboardInterrupt:
                print("\n\n🛑 Scheduler stopped by user.")
                break
            except Exception as e:
                print(f"\n❌ Scheduler error: {str(e)}")
                print("⏰ Scheduler will continue...\n")
                time.sleep(60)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Schedule daily WhatsApp predictions"
    )
    parser.add_argument(
        "--time",
        type=str,
        default="08:00",
        help="Time to send predictions (HH:MM format, 24-hour). Default: 08:00"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Send one batch immediately for testing (doesn't schedule)"
    )
    
    args = parser.parse_args()
    
    # Validate time format
    try:
        time_parts = args.time.split(":")
        if len(time_parts) != 2:
            raise ValueError("Invalid time format")
        hour, minute = int(time_parts[0]), int(time_parts[1])
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Hour must be 0-23, minute must be 0-59")
    except (ValueError, IndexError) as e:
        print(f"❌ Invalid time format: {str(e)}")
        print("Please use HH:MM format (e.g., 08:00 for 8 AM)")
        sys.exit(1)
    
    if args.test:
        print("🧪 Running test batch WhatsApp send...\n")
        run_inference_whatsapp_batch()
    else:
        try:
            scheduler = PredictionScheduler(time_str=args.time)
            scheduler.start()
        except ImportError as e:
            print(f"❌ {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()

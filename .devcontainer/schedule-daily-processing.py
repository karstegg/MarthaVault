#!/usr/bin/env python3
"""
Automated daily report processing scheduler for Codespaces
Runs continuously and processes reports at specified times
"""

import schedule
import time
import subprocess
import logging
import json
from datetime import datetime, timedelta
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/daily-processing.log'),
        logging.StreamHandler()
    ]
)

class DailyReportScheduler:
    def __init__(self):
        self.script_path = "/workspaces/MarthaVault/.devcontainer/extract-whatsapp-reports.py"
        
    def process_yesterday(self):
        """Process reports for yesterday (most common use case)"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Check if yesterday's reports already exist
        if self.reports_exist_for_date(yesterday):
            logging.info(f"✅ Reports for {yesterday} already exist, skipping")
            return
            
        logging.info(f"🎯 Processing yesterday's reports: {yesterday}")
        self.process_date(yesterday)
    
    def process_recent_missing(self):
        """Process any missing reports from recent days using smart detection"""
        
        logging.info("🤖 Running smart detection for missing reports...")
        
        try:
            # Run smart detection
            result = subprocess.run([
                "python3", "/workspaces/MarthaVault/.devcontainer/auto-detect-missing-reports.py", "--json"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and result.stdout.strip():
                missing_dates = json.loads(result.stdout.strip())
                
                if missing_dates:
                    logging.info(f"🔍 Found {len(missing_dates)} missing dates: {missing_dates}")
                    
                    # Process up to 3 most recent missing dates
                    for date_str in missing_dates[:3]:
                        logging.info(f"🎯 Processing missing date: {date_str}")
                        self.process_date(date_str)
                        time.sleep(30)  # Wait between processing
                else:
                    logging.info("✅ No missing dates found")
            else:
                logging.warning("⚠️ Smart detection failed or returned no data")
                
        except Exception as e:
            logging.error(f"❌ Smart detection error: {e}")
    
    def reports_exist_for_date(self, date_str):
        """Check if reports already exist for a given date"""
        
        # Convert date to path format
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        year_month = date_obj.strftime("%Y-%m")
        day = date_obj.strftime("%d")
        
        report_dir = f"/workspaces/MarthaVault/daily_production/data/{year_month}/{day}"
        
        if not os.path.exists(report_dir):
            return False
            
        # Check for JSON files (more reliable indicator)
        json_files = [f for f in os.listdir(report_dir) if f.endswith('.json')]
        
        return len(json_files) > 0
    
    def process_date(self, target_date):
        """Process reports for a specific date"""
        
        logging.info(f"🎯 Starting automated processing for {target_date}")
        
        try:
            # Run the extraction script
            result = subprocess.run([
                "python3", self.script_path, target_date
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logging.info(f"✅ Successfully processed {target_date}")
                logging.info(f"Output: {result.stdout}")
            else:
                logging.error(f"❌ Failed to process {target_date}")
                logging.error(f"Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            logging.error(f"⏰ Timeout processing {target_date}")
        except Exception as e:
            logging.error(f"💥 Exception processing {target_date}: {e}")
    
    def process_specific_date(self, date_str):
        """Wrapper for processing a specific date from command line"""
        self.process_date(date_str)

def main():
    scheduler = DailyReportScheduler()
    
    # Schedule daily processing at 8:00 AM (when morning reports typically arrive)
    schedule.every().day.at("08:00").do(scheduler.process_yesterday)
    
    # Schedule afternoon check at 2:00 PM for any missed reports using smart detection
    schedule.every().day.at("14:00").do(scheduler.process_recent_missing)
    
    logging.info("🕐 Daily report scheduler started")
    logging.info("📅 Scheduled times:")
    logging.info("  - 08:00: Process previous day reports")
    logging.info("  - 14:00: Smart detection for missed reports")
    
    # If specific date provided as argument, process it immediately
    if len(os.sys.argv) > 1:
        target_date = os.sys.argv[1]
        logging.info(f"🎯 Processing specific date: {target_date}")
        scheduler.process_date(target_date)
        return
    
    # Main scheduler loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        logging.info("🛑 Scheduler stopped by user")
    except Exception as e:
        logging.error(f"💥 Scheduler error: {e}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Smart date detection for missing WhatsApp reports
Analyzes existing reports and identifies gaps for processing
"""

import os
import sys
import glob
import json
from datetime import datetime, timedelta, date
from pathlib import Path
import subprocess

class MissingReportDetector:
    def __init__(self):
        self.repo_root = "/workspaces/MarthaVault"
        self.data_dir = f"{self.repo_root}/daily_production/data"
        self.group_chat_id = "27834418149-1537194373@g.us"
        
    def get_existing_report_dates(self):
        """Get all dates that have existing reports"""
        existing_dates = set()
        
        # Scan for existing JSON files (more reliable than markdown)
        pattern = f"{self.data_dir}/*/*/*.json"
        json_files = glob.glob(pattern)
        
        for json_file in json_files:
            # Extract date from filename like: 2025-07-01_gloria.json
            filename = os.path.basename(json_file)
            if filename.startswith("20"):  # Year starts with 20
                date_part = filename.split('_')[0]
                try:
                    parsed_date = datetime.strptime(date_part, "%Y-%m-%d").date()
                    existing_dates.add(parsed_date)
                except ValueError:
                    continue
        
        return sorted(existing_dates)
    
    def find_missing_dates(self, start_date=None, end_date=None):
        """Find missing dates in a range"""
        
        if not start_date:
            start_date = date(2025, 7, 1)  # Default start
        if not end_date:
            end_date = date.today() - timedelta(days=1)  # Yesterday
            
        print(f"🔍 Scanning for missing reports from {start_date} to {end_date}")
        
        existing_dates = self.get_existing_report_dates()
        print(f"📊 Found {len(existing_dates)} existing report dates")
        
        missing_dates = []
        current_date = start_date
        
        while current_date <= end_date:
            # Process ALL days (including weekends)
            # Mining operations vary by site - some run 7 days/week, others don't
            # We process whatever WhatsApp reports were actually sent
            if current_date not in existing_dates:
                missing_dates.append(current_date)
            current_date += timedelta(days=1)
        
        return missing_dates
    
    def analyze_recent_gaps(self, days_back=30):
        """Find recent gaps in reporting"""
        end_date = date.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=days_back)
        
        return self.find_missing_dates(start_date, end_date)
    
    def get_processing_priority(self, missing_dates):
        """Prioritize dates for processing"""
        
        if not missing_dates:
            return []
            
        today = date.today()
        prioritized = []
        
        for missing_date in missing_dates:
            days_ago = (today - missing_date).days
            
            # Priority scoring
            if days_ago <= 3:
                priority = "🔴 HIGH"    # Very recent
            elif days_ago <= 7:
                priority = "🟡 MEDIUM"  # Last week
            elif days_ago <= 30:
                priority = "🟢 LOW"     # Last month
            else:
                priority = "⚪ ARCHIVE" # Older
            
            prioritized.append({
                "date": missing_date,
                "days_ago": days_ago,
                "priority": priority
            })
        
        # Sort by days ago (most recent first)
        prioritized.sort(key=lambda x: x["days_ago"])
        return prioritized
    
    def check_whatsapp_data_availability(self, target_date):
        """Check if WhatsApp MCP has data for the target date"""
        
        days_ago = (date.today() - target_date).days
        
        # Quick heuristic check first
        if days_ago > 90:
            return False, "WhatsApp data likely expired (>90 days)"
        
        # Try to actually check with WhatsApp MCP if available
        try:
            # Format date for MCP query
            start_time = f"{target_date}T00:00:00"
            end_time = f"{target_date}T23:59:59"
            
            # This would be the actual MCP call when the server is available
            # For now, we'll use a heuristic based on typical WhatsApp retention
            
            if days_ago > 60:
                return True, "Data may be available (check required - older data)"
            elif days_ago > 30:
                return True, "Data should be available (moderate age)"
            else:
                return True, "Data should be available (recent)"
                
        except Exception as e:
            # Fallback to heuristic if MCP check fails
            if days_ago <= 30:
                return True, f"Data likely available (MCP check failed: {str(e)[:50]})"
            else:
                return False, f"Data uncertain (MCP check failed: {str(e)[:50]})"
    
    def generate_processing_plan(self, max_dates=10):
        """Generate a smart processing plan"""
        
        print("🎯 Generating smart processing plan...")
        print("=" * 50)
        
        # Find missing dates
        missing_dates = self.analyze_recent_gaps(days_back=90)
        
        if not missing_dates:
            print("✅ No missing dates found in recent period")
            return []
        
        # Prioritize dates
        prioritized = self.get_processing_priority(missing_dates)
        
        # Limit to reasonable batch size
        plan = prioritized[:max_dates]
        
        print(f"📋 Processing Plan ({len(plan)} dates):")
        print("   Includes all days - mining operations vary by site/weekend schedule")
        print()
        
        for item in plan:
            target_date = item["date"]
            priority = item["priority"]
            days_ago = item["days_ago"]
            day_name = target_date.strftime("%A")
            
            # Check data availability
            available, reason = self.check_whatsapp_data_availability(target_date)
            status = "✅" if available else "❌"
            
            print(f"  {priority} | {target_date} ({day_name}) | {days_ago} days ago | {status} {reason}")
        
        print()
        print("💡 The system will process whatever reports were actually sent")
        print("   (Some sites operate 7 days/week, others may skip weekends)")
        return [item["date"] for item in plan if self.check_whatsapp_data_availability(item["date"])[0]]

def main():
    detector = MissingReportDetector()
    
    if len(sys.argv) == 1:
        # Auto-detect mode
        print("🤖 Auto-detection mode")
        processing_dates = detector.generate_processing_plan()
        
        if processing_dates:
            print(f"🚀 Ready to process {len(processing_dates)} dates:")
            for date_obj in processing_dates:
                print(f"  - {date_obj}")
            
            print()
            print("💡 To process these dates:")
            print("   python /workspaces/MarthaVault/.devcontainer/extract-whatsapp-reports.py <date>")
            print("   or")
            print("   /workspaces/MarthaVault/.devcontainer/process-missing-reports.sh")
            
        else:
            print("✅ No dates require processing")
            
    elif sys.argv[1] == "--json":
        # JSON output mode for automation
        processing_dates = detector.generate_processing_plan()
        dates_str = [d.strftime("%Y-%m-%d") for d in processing_dates]
        print(json.dumps(dates_str))
        
    else:
        # Specific date range mode
        try:
            start_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
            end_date = datetime.strptime(sys.argv[2], "%Y-%m-%d").date() if len(sys.argv) > 2 else None
            missing = detector.find_missing_dates(start_date, end_date)
            
            for missing_date in missing:
                print(missing_date.strftime("%Y-%m-%d"))
                
        except ValueError:
            print("Usage: python auto-detect-missing-reports.py [start-date] [end-date]")
            print("       python auto-detect-missing-reports.py --json")
            sys.exit(1)

if __name__ == "__main__":
    main()
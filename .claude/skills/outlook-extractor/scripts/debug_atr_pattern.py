#!/usr/bin/env python3
"""
Debug script to investigate ATR (Operational Excellence) recurring meetings.
Checks the actual pattern properties and dates returned by GetNextOccurrence.
"""

import win32com.client
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Connect to Outlook
outlook = win32com.client.Dispatch("Outlook.Application")
ns = outlook.GetNamespace("MAPI")
calendar_folder = ns.GetDefaultFolder(9)  # 9 = olFolderCalendar

def format_dt(dt):
    """Format datetime for display."""
    if dt is None:
        return "None"
    # Remove timezone info if present
    if hasattr(dt, 'tzinfo') and dt.tzinfo:
        dt = dt.replace(tzinfo=None)
    return dt.strftime("%Y-%m-%d %H:%M:%S (%A)")

print("=" * 80)
print("DEBUGGING ATR RECURRING PATTERNS")
print("=" * 80)

# Search for ATR meetings
found_atr = False
for item in calendar_folder.Items:
    if "Operational Excellence" in item.Subject and "ATR" in item.Subject:
        print(f"\n{'=' * 80}")
        print(f"MEETING: {item.Subject}")
        print(f"{'=' * 80}")
        print(f"Start: {format_dt(item.Start)}")
        print(f"End: {format_dt(item.End)}")
        print(f"IsRecurring: {item.IsRecurring}")

        if item.IsRecurring:
            pattern = item.GetRecurrencePattern()
            print(f"\nRecurrence Pattern Details:")
            print(f"  RecurrenceType: {pattern.RecurrenceType}")
            print(f"    (0=Daily, 1=Weekly, 2=Monthly, 3=MonthNth, 5=Yearly, 6=YearNth)")
            print(f"  Interval: {pattern.Interval}")
            try:
                print(f"  DayOfWeekMask: {pattern.DayOfWeekMask}")
            except:
                pass
            try:
                print(f"  DayOfMonth: {pattern.DayOfMonth}")
            except:
                pass
            try:
                print(f"  Instance: {pattern.Instance}")
            except:
                pass
            try:
                print(f"  MonthOfYear: {pattern.MonthOfYear}")
            except:
                pass
            try:
                print(f"  Occurrences: {pattern.Occurrences}")
            except:
                pass
            try:
                print(f"  PatternStartDate: {format_dt(pattern.PatternStartDate)}")
            except:
                pass
            try:
                print(f"  PatternEndDate: {format_dt(pattern.PatternEndDate)}")
            except:
                pass
            try:
                print(f"  NoEndDate: {pattern.NoEndDate}")
            except:
                pass

            # Try to get next occurrences starting from today
            test_date = datetime(2025, 11, 10)
            print(f"\nTesting GetNextOccurrence() from {test_date.strftime('%Y-%m-%d')}:")

            try:
                for i in range(5):
                    next_occ = pattern.GetNextOccurrence(test_date)
                    if next_occ is None:
                        print(f"  Occurrence {i+1}: None (no more occurrences)")
                        break
                    # Remove timezone info if present
                    if next_occ.tzinfo:
                        next_occ = next_occ.replace(tzinfo=None)
                    print(f"  Occurrence {i+1}: {format_dt(next_occ)}")
                    test_date = next_occ + timedelta(days=1)
            except Exception as e:
                print(f"  ERROR calling GetNextOccurrence: {e}")

            # Manual calculation for MonthNth
            if pattern.RecurrenceType == 3:
                print(f"\nManual calculation for MonthNth pattern:")
                # Try to calculate next occurrence using relativedelta
                test_date = datetime(2025, 11, 10)
                for i in range(3):
                    calc_date = test_date + relativedelta(months=pattern.Interval)
                    print(f"  Manual step {i+1}: {test_date.strftime('%Y-%m-%d')} + {pattern.Interval} months = {calc_date.strftime('%Y-%m-%d (%A)')}")
                    test_date = calc_date

        found_atr = True

if not found_atr:
    print("\nNo ATR (Operational Excellence ATR) meetings found in calendar.")
    print("\nSearching for any recurring meetings...")
    count = 0
    for item in calendar_folder.Items:
        if item.IsRecurring and count < 5:
            print(f"\n  - {item.Subject}")
            print(f"    Start: {format_dt(item.Start)}")
            pattern = item.RecurrencePattern
            print(f"    RecurrenceType: {pattern.RecurrenceType}")
            count += 1

print("\n" + "=" * 80)
print("END DEBUG")
print("=" * 80)

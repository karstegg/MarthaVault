#!/usr/bin/env python3
"""
Convert extracted calendar JSON to Obsidian calendar event files.
Creates YYYY-MM-DD - Event Title.md files with proper YAML frontmatter.
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Path to the extracted calendar JSON
json_file = "outlook_calendar.json"
obsidian_schedule_dir = r"C:\Users\10064957\My Drive\GDVault\MarthaVault\Schedule"

# Load the JSON data
with open(json_file, 'r') as f:
    events = json.load(f)

# Create the Schedule directory if it doesn't exist
os.makedirs(obsidian_schedule_dir, exist_ok=True)

print(f"Converting {len(events)} events to Obsidian calendar format...")
print(f"Output directory: {obsidian_schedule_dir}\n")

created_files = []
for event in events:
    subject = event['Subject']
    start_str = event['Start']
    end_str = event['End']
    location = event['Location']
    organizer = event['Organizer']

    # Parse the datetime strings
    start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
    end_dt = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")

    # Check if it's an all-day event (no specific time distinction)
    is_all_day = False

    # Generate the filename
    date_str = start_dt.strftime("%Y-%m-%d")
    # Sanitize the subject for filename
    safe_subject = "".join(c for c in subject if c.isalnum() or c in " -_").strip()
    filename = f"{date_str} - {safe_subject}.md"
    filepath = os.path.join(obsidian_schedule_dir, filename)

    # Generate the YAML frontmatter
    yaml_content = f"""---
title: {subject}
allDay: {"true" if is_all_day else "false"}
date: {date_str}
startTime: "{start_dt.strftime('%H:%M')}"
endTime: "{end_dt.strftime('%H:%M')}"
completed: null
permalink: schedule/{date_str.replace('-', '')}-{safe_subject.lower().replace(' ', '-')}
---

# {subject}

**Time:** {start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')} SAST
**Location:** {location if location else 'Not specified'}
**Organizer:** {organizer if organizer else 'Not specified'}
"""

    # Write the file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        created_files.append((filepath, subject, start_dt))
        print(f"[OK] Created: {filename}")
    except Exception as e:
        print(f"[ERROR] Error creating {filename}: {e}")

# Summary
print(f"\n{'=' * 80}")
print(f"Created {len(created_files)} calendar event files")

# Group by date
from collections import defaultdict
by_date = defaultdict(list)
for filepath, subject, dt in created_files:
    date_key = dt.strftime("%Y-%m-%d (%A)")
    by_date[date_key].append((subject, dt.strftime("%H:%M")))

print(f"\nEvents by date:")
for date_key in sorted(by_date.keys()):
    print(f"\n  {date_key}")
    for subject, time in sorted(by_date[date_key], key=lambda x: x[1]):
        print(f"    - {time}: {subject}")

print(f"\n{'=' * 80}")

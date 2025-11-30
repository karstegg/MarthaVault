#!/usr/bin/env python3
"""
Outlook COM API Integration Script

This is the executable script for the outlook-extractor skill.
It provides command-line access to Microsoft Outlook functionality including:
- Email extraction with date filtering
- Calendar event extraction
- Contact extraction
- Email sending with attachments
- Email deletion with filters
- Meeting creation and deletion

USAGE:
    python outlook_extractor.py emails --days 7 --limit 50
    python outlook_extractor.py calendar --days 30
    python outlook_extractor.py send-email --to "user@company.com" --subject "Title" --body "Message"
    python outlook_extractor.py delete-email --subject "spam" --limit 5
    python outlook_extractor.py create-meeting --subject "Meeting" --start "2025-10-25 10:00"
    python outlook_extractor.py contacts --limit 100
    python outlook_extractor.py all

REQUIREMENTS:
    - Windows operating system
    - Microsoft Outlook installed and running
    - Python 3.7+
    - pywin32 package: pip install pywin32 --upgrade
"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta

# Fix encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul')
    sys.stdout.reconfigure(encoding='utf-8')

try:
    import win32com.client
except ImportError:
    print("ERROR: pywin32 not installed. Run: pip install pywin32 --upgrade", file=sys.stderr)
    sys.exit(1)


class OutlookExtractor:
    """Main class for Outlook COM API interactions"""

    def __init__(self):
        """Initialize Outlook connection"""
        try:
            # Try GetActiveObject first (existing instance), fallback to Dispatch (new instance)
            try:
                self.outlook = win32com.client.GetActiveObject("Outlook.Application")
            except:
                self.outlook = win32com.client.Dispatch("Outlook.Application")

            self.namespace = self.outlook.GetNamespace("MAPI")
            print("✓ Connected to Outlook")
        except Exception as e:
            print(f"✗ Error connecting to Outlook: {e}", file=sys.stderr)
            sys.exit(1)

    def _format_datetime_sast(self, dt):
        """
        Format datetime as SAST local time string (no timezone indicator).
        All Outlook times are already in SAST - strip any +00:00 suffix.

        Args:
            dt: datetime object

        Returns:
            String in format "YYYY-MM-DD HH:MM:SS"
        """
        if dt is None:
            return ""

        # Normalize timezone (remove tzinfo if present)
        if hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)

        # Format as SAST local time (no timezone indicator)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def _get_recurring_dates(self, recurrence_pattern, start_date, end_date):
        """
        Get all occurrences of a recurring event within a date range

        Args:
            recurrence_pattern: Outlook RecurrencePattern object
            start_date: Start datetime
            end_date: End datetime

        Returns:
            List of datetime objects for each occurrence
        """
        occurrences = []
        try:
            # Use GetNextOccurrence method - this is more reliable
            current = start_date
            max_iterations = 366  # Prevent infinite loops
            iterations = 0

            while iterations < max_iterations:
                iterations += 1
                try:
                    next_occ = recurrence_pattern.GetNextOccurrence(current)
                    if next_occ is None or next_occ > end_date:
                        break

                    # Normalize timezone
                    if next_occ.tzinfo is not None:
                        next_occ = next_occ.replace(tzinfo=None)

                    if next_occ <= end_date:
                        occurrences.append(next_occ)
                        current = next_occ + timedelta(hours=1)  # Move past this occurrence
                    else:
                        break

                except Exception as e:
                    break

        except Exception as e:
            pass  # Silently fail for debugging

        return occurrences

    def list_all_folders(self):
        """
        List all available folders (default + subfolders)

        Returns:
            Dictionary with folder names and paths
        """
        folders_dict = {}

        try:
            # Get default folders
            inbox = self.namespace.GetDefaultFolder(6)  # Inbox
            sent = self.namespace.GetDefaultFolder(5)   # Sent Items

            folders_dict['Inbox'] = 'Inbox (main)'
            folders_dict['Sent Items'] = 'Sent Items (main)'

            # Get all subfolders under Inbox
            try:
                inbox_subfolders = inbox.Folders
                for folder_idx in range(inbox_subfolders.Count):
                    subfolder = inbox_subfolders.Item(folder_idx + 1)
                    subfolder_path = f"Inbox\\{subfolder.Name}"
                    folders_dict[subfolder_path] = f"└─ {subfolder.Name}"

                    # Get sub-subfolders (2 levels deep)
                    try:
                        sub_subfolders = subfolder.Folders
                        for sub_idx in range(sub_subfolders.Count):
                            sub_subfolder = sub_subfolders.Item(sub_idx + 1)
                            sub_path = f"Inbox\\{subfolder.Name}\\{sub_subfolder.Name}"
                            folders_dict[sub_path] = f"  └─ {sub_subfolder.Name}"
                    except:
                        pass
            except:
                pass

            return folders_dict
        except Exception as e:
            print(f"✗ Error listing folders: {e}", file=sys.stderr)
            return {}

    def get_emails_from_subfolder(self, folder_path, limit=20, days_back=30):
        """
        Extract emails from a specific subfolder path

        Args:
            folder_path: Full folder path (e.g., "Inbox\\Production\\N2")
            limit: Maximum number of emails to return
            days_back: Number of days to look back

        Returns:
            List of email dictionaries
        """
        try:
            # Navigate to the folder
            parts = folder_path.split('\\')

            if parts[0] == 'Inbox':
                current_folder = self.namespace.GetDefaultFolder(6)  # Start at Inbox
            elif parts[0] == 'Sent Items':
                current_folder = self.namespace.GetDefaultFolder(5)
            else:
                print(f"✗ Unknown folder root: {parts[0]}", file=sys.stderr)
                return []

            # Navigate through subfolders
            for part in parts[1:]:
                found = False
                for folder_idx in range(current_folder.Folders.Count):
                    subfolder = current_folder.Folders.Item(folder_idx + 1)
                    if subfolder.Name == part:
                        current_folder = subfolder
                        found = True
                        break
                if not found:
                    print(f"✗ Subfolder not found: {part} in {current_folder.Name}", file=sys.stderr)
                    return []

            items = current_folder.Items
            sort_field = "[ReceivedTime]"
            items.Sort(sort_field, False)

            cutoff_date = datetime.now() - timedelta(days=days_back)
            emails = []

            print(f"\nExtracting {limit} emails from {folder_path} (last {days_back} days)...")

            for item in items:
                if len(emails) >= limit:
                    break

                try:
                    email_time = item.ReceivedTime

                    # Normalize timezone for comparison
                    if email_time.tzinfo is not None:
                        email_time = email_time.replace(tzinfo=None)
                    if cutoff_date.tzinfo is not None:
                        cutoff_date = cutoff_date.replace(tzinfo=None)

                    if email_time < cutoff_date:
                        continue

                    email_data = {
                        'From': item.SenderName,
                        'Subject': item.Subject,
                        'ReceivedTime': str(email_time),
                        'Unread': item.Unread,
                        'Attachments': item.Attachments.Count
                    }
                    email_data = {k: v for k, v in email_data.items() if v is not None}
                    emails.append(email_data)

                except Exception as e:
                    print(f"  Warning: Could not process item: {e}", file=sys.stderr)
                    continue

            return emails

        except Exception as e:
            print(f"✗ Error extracting emails from subfolder: {e}", file=sys.stderr)
            return []

    def search_folders_by_name(self, search_term, limit=20, days_back=30):
        """
        Search all folders matching a name pattern and extract emails from all matches

        Args:
            search_term: Partial folder name to search for (case-insensitive)
            limit: Maximum number of emails to return
            days_back: Number of days to look back

        Returns:
            List of email dictionaries from all matching folders
        """
        all_emails = []
        search_term_lower = search_term.lower()
        matched_folders = []

        try:
            # Check Inbox subfolders
            inbox = self.namespace.GetDefaultFolder(6)
            print(f"\nSearching for folders matching '{search_term}'...")

            # First level
            for folder_idx in range(inbox.Folders.Count):
                subfolder = inbox.Folders.Item(folder_idx + 1)
                if search_term_lower in subfolder.Name.lower():
                    matched_folders.append(f"Inbox\\{subfolder.Name}")
                    print(f"✓ Found: Inbox\\{subfolder.Name}")

                # Second level
                try:
                    for sub_idx in range(subfolder.Folders.Count):
                        sub_subfolder = subfolder.Folders.Item(sub_idx + 1)
                        if search_term_lower in sub_subfolder.Name.lower():
                            matched_folders.append(f"Inbox\\{subfolder.Name}\\{sub_subfolder.Name}")
                            print(f"✓ Found: Inbox\\{subfolder.Name}\\{sub_subfolder.Name}")
                except:
                    pass

            # Extract emails from all matched folders
            if matched_folders:
                print(f"\nExtracting emails from {len(matched_folders)} matching folder(s)...")
                for folder_path in matched_folders:
                    folder_emails = self.get_emails_from_subfolder(folder_path, limit=limit, days_back=days_back)
                    all_emails.extend(folder_emails)
            else:
                print(f"✗ No folders matching '{search_term}' found")

            # Limit total results
            all_emails = all_emails[:limit]
            return all_emails

        except Exception as e:
            print(f"✗ Error searching folders: {e}", file=sys.stderr)
            return []

    def get_emails(self, limit=20, days_back=30, folder='Inbox'):
        """
        Extract emails from specified folder

        Args:
            limit: Maximum number of emails to return
            days_back: Number of days to look back
            folder: Folder to search ('Inbox' or 'Sent Items')

        Returns:
            List of email dictionaries
        """
        try:
            # Map folder name to Outlook folder constant
            folder_map = {
                'Inbox': 6,        # olFolderInbox
                'Sent Items': 5    # olFolderSentMail
            }

            folder_id = folder_map.get(folder, 6)  # Default to Inbox
            target_folder = self.namespace.GetDefaultFolder(folder_id)
            items = target_folder.Items

            # Use appropriate sort field based on folder
            sort_field = "[SentOn]" if folder == "Sent Items" else "[ReceivedTime]"
            items.Sort(sort_field, False)

            cutoff_date = datetime.now() - timedelta(days=days_back)
            emails = []

            print(f"\nExtracting {limit} emails from {folder} (last {days_back} days)...")

            for item in items:
                if len(emails) >= limit:
                    break

                try:
                    # Use SentOn for Sent Items, ReceivedTime for Inbox
                    if folder == "Sent Items":
                        email_time = item.SentOn
                        time_field_name = "SentOn"
                    else:
                        email_time = item.ReceivedTime
                        time_field_name = "ReceivedTime"

                    # Normalize timezone for comparison
                    if email_time.tzinfo is not None:
                        email_time = email_time.replace(tzinfo=None)
                    if cutoff_date.tzinfo is not None:
                        cutoff_date = cutoff_date.replace(tzinfo=None)

                    # Skip older emails - continue to check others
                    if email_time < cutoff_date:
                        continue

                    email_data = {
                        'From': item.SenderName if folder != "Sent Items" else "Me (Gregory Karsten)",
                        'To': item.To if folder == "Sent Items" else None,
                        'Subject': item.Subject,
                        time_field_name: str(email_time),
                        'Unread': item.Unread if folder != "Sent Items" else None,
                        'Attachments': item.Attachments.Count
                    }
                    # Remove None values for cleaner output
                    email_data = {k: v for k, v in email_data.items() if v is not None}
                    emails.append(email_data)

                except Exception as e:
                    print(f"  Warning: Could not process item: {e}", file=sys.stderr)
                    continue

            return emails

        except Exception as e:
            print(f"✗ Error extracting emails: {e}", file=sys.stderr)
            return []

    def get_calendar_events(self, days_ahead=7, limit=20, from_week_start=False):
        """
        Extract upcoming calendar events from ALL calendars (default + shared/delegated)

        Args:
            days_ahead: Number of days ahead to check
            limit: Maximum number of events to return
            from_week_start: If True, include events from Monday of current week (default: False)

        Returns:
            List of event dictionaries
        """
        try:
            now = datetime.now()
            cutoff_date = now + timedelta(days=days_ahead)

            # If from_week_start is True, set start time to Monday 00:00:00 of current week
            if from_week_start:
                # Calculate Monday of current week (0 = Monday, 6 = Sunday)
                days_since_monday = now.weekday()  # 0=Monday, 1=Tuesday, etc.
                week_start = now - timedelta(days=days_since_monday)
                week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
                start_date = week_start
                print(f"\nExtracting calendar events from Monday {week_start.strftime('%Y-%m-%d')} to {cutoff_date.strftime('%Y-%m-%d')} (limit: {limit})...")
            else:
                start_date = now
                print(f"\nExtracting calendar events for next {days_ahead} days (limit: {limit})...")

            events = []
            calendars_checked = 0

            calendars_to_check = []

            # Get calendar from all stores (handles multiple accounts and shared calendars)
            # EXCLUDE Archives and student accounts
            try:
                stores = self.namespace.Stores
                for store_idx in range(stores.Count):
                    store = stores.Item(store_idx + 1)

                    # Skip Archives and student accounts
                    if 'Archives' in store.DisplayName or 'student' in store.DisplayName.lower():
                        continue

                    try:
                        root_folder = store.GetRootFolder()
                        folders = root_folder.Folders
                        for folder_idx in range(folders.Count):
                            folder = folders.Item(folder_idx + 1)
                            # Look for calendar folders (DefaultItemType = 1 for appointments)
                            if hasattr(folder, 'DefaultItemType') and folder.DefaultItemType == 1:
                                if folder.Name == 'Calendar':  # Skip subfolders, only main Calendar
                                    calendars_to_check.append(folder)
                                    calendars_checked += 1
                    except:
                        pass
            except:
                pass  # Fallback: try default calendar
                try:
                    default_calendar = self.namespace.GetDefaultFolder(9)  # 9 = Calendar
                    calendars_to_check.append(default_calendar)
                    calendars_checked += 1
                except:
                    pass

            # Also check Inbox for pending meeting invitations/responses
            try:
                inbox = self.namespace.GetDefaultFolder(6)  # 6 = Inbox
                # Pending meeting requests show up as email items with IPM.Schedule.Meeting.Request
                inbox_items = inbox.Items
                for item in inbox_items:
                    if len(events) >= limit:
                        break
                    try:
                        # Check if it's a meeting request
                        if hasattr(item, 'Start') and hasattr(item, 'End'):
                            start_time = item.Start
                            if start_time.tzinfo is not None:
                                start_time = start_time.replace(tzinfo=None)

                            if start_time >= now.replace(tzinfo=None) and start_time <= cutoff_date.replace(tzinfo=None):
                                event_data = {
                                    'Subject': item.Subject,
                                    'Start': self._format_datetime_sast(item.Start),
                                    'End': self._format_datetime_sast(item.End),
                                    'Location': getattr(item, 'Location', ''),
                                    'Organizer': getattr(item, 'Organizer', 'Unknown') if hasattr(item, 'Organizer') else 'Unknown'
                                }
                                # Check if not already in events
                                if not any(e['Subject'] == event_data['Subject'] and e['Start'] == event_data['Start'] for e in events):
                                    events.append(event_data)
                    except:
                        pass
            except:
                pass  # No inbox or error accessing it

            print(f"  Checking {calendars_checked} calendar(s)...")

            # Process all calendars
            for calendar in calendars_to_check:
                if len(events) >= limit:
                    break

                try:
                    items = calendar.Items
                    items.Sort("[Start]")

                    for item in items:
                        if len(events) >= limit:
                            break

                        try:
                            # Check if this is a recurring event
                            is_recurring = item.IsRecurring if hasattr(item, 'IsRecurring') else False

                            if is_recurring:
                                # For recurring events, expand occurrences within the date range
                                try:
                                    pattern = item.GetRecurrencePattern()
                                    pattern_start = pattern.PatternStartDate
                                    pattern_end = pattern.PatternEndDate

                                    # First, check for exceptions (rescheduled occurrences)
                                    # Also track deleted exceptions to skip them in regular occurrence calculation
                                    deleted_dates = set()
                                    try:
                                        exceptions = pattern.Exceptions
                                        for exc_idx in range(exceptions.Count):
                                            exc = exceptions.Item(exc_idx + 1)
                                            try:
                                                # Track deleted/declined occurrences
                                                if exc.Deleted:
                                                    deleted_dates.add(exc.OriginalDate.date())
                                                    continue  # Skip deleted exceptions

                                                if hasattr(exc, 'AppointmentItem'):
                                                    appt = exc.AppointmentItem
                                                    exc_start = appt.Start
                                                    exc_end = appt.End

                                                    # Normalize timezone
                                                    if exc_start.tzinfo is not None:
                                                        exc_start = exc_start.replace(tzinfo=None)
                                                    if exc_end.tzinfo is not None:
                                                        exc_end = exc_end.replace(tzinfo=None)

                                                    # Check if this exception is in our date range
                                                    if exc_end >= start_date.replace(tzinfo=None) and exc_start <= cutoff_date.replace(tzinfo=None):
                                                        event_data = {
                                                            'Subject': appt.Subject,
                                                            'Start': self._format_datetime_sast(exc_start),
                                                            'End': self._format_datetime_sast(exc_end),
                                                            'Location': appt.Location,
                                                            'Organizer': appt.Organizer if hasattr(appt, 'Organizer') else item.Organizer
                                                        }
                                                        if not any(e['Subject'] == event_data['Subject'] and e['Start'] == event_data['Start'] for e in events):
                                                            events.append(event_data)
                                            except:
                                                pass
                                    except:
                                        pass  # No exceptions

                                    # Calculate which occurrences fall in our date range
                                    # Get the first occurrence
                                    occurrence_date = pattern_start
                                    occurrence_count = 0
                                    max_occurrences = pattern.Occurrences if pattern.Occurrences else 100

                                    def _get_next_month_nth(current_date, instance, day_of_week_mask):
                                        """
                                        Calculate the next occurrence of a MonthNth pattern.

                                        Args:
                                            current_date: Starting date
                                            instance: Which occurrence (1=1st, 2=2nd, 3=3rd, etc.)
                                            day_of_week_mask: Bitmask for day of week (1=Sun, 2=Mon, 4=Tue, 8=Wed, 16=Thu, 32=Fri, 64=Sat)

                                        Returns:
                                            datetime of the next occurrence
                                        """
                                        from dateutil.relativedelta import relativedelta

                                        # Map bitmask to day of week (0=Monday, 6=Sunday)
                                        day_map = {1: 6, 2: 0, 4: 1, 8: 2, 16: 3, 32: 4, 64: 5}
                                        target_dow = day_map.get(day_of_week_mask, 2)  # Default to Wednesday

                                        # Start with first day of next month
                                        next_month = current_date + relativedelta(months=1)
                                        first_of_month = next_month.replace(day=1)

                                        # Find the first occurrence of the target day of week in this month
                                        days_until_target = (target_dow - first_of_month.weekday()) % 7
                                        first_occurrence = first_of_month + timedelta(days=days_until_target)

                                        # Calculate the nth occurrence
                                        nth_occurrence = first_occurrence + timedelta(weeks=instance - 1)

                                        return nth_occurrence

                                    while occurrence_count < max_occurrences:
                                        if len(events) >= limit:
                                            break

                                        # Skip this occurrence if it was deleted/declined
                                        occurrence_date_only = occurrence_date.date() if isinstance(occurrence_date, datetime) else occurrence_date
                                        if occurrence_date_only in deleted_dates:
                                            # Move to next occurrence without processing
                                            if pattern.RecurrenceType == 3:  # MonthNth
                                                try:
                                                    occurrence_date = _get_next_month_nth(occurrence_date, pattern.Instance, pattern.DayOfWeekMask)
                                                except:
                                                    occurrence_date = occurrence_date + timedelta(days=30)
                                            elif pattern.RecurrenceType == 0:  # olRecursDaily
                                                occurrence_date = occurrence_date + timedelta(days=pattern.Interval)
                                            elif pattern.RecurrenceType == 1:  # olRecursWeekly
                                                occurrence_date = occurrence_date + timedelta(weeks=pattern.Interval)
                                            else:
                                                occurrence_date = occurrence_date + timedelta(days=30)
                                            occurrence_count += 1
                                            continue

                                        # Calculate the datetime for this occurrence
                                        occurrence_start = datetime.combine(occurrence_date, item.Start.time())
                                        occurrence_end = datetime.combine(occurrence_date, item.End.time())

                                        # Check if this occurrence is in our date range
                                        if occurrence_end >= start_date.replace(tzinfo=None) and occurrence_start <= cutoff_date.replace(tzinfo=None):
                                            event_data = {
                                                'Subject': item.Subject,
                                                'Start': self._format_datetime_sast(occurrence_start),
                                                'End': self._format_datetime_sast(occurrence_end),
                                                'Location': item.Location,
                                                'Organizer': item.Organizer
                                            }

                                            # Avoid duplicates
                                            if not any(e['Subject'] == event_data['Subject'] and e['Start'] == event_data['Start'] for e in events):
                                                events.append(event_data)

                                        # Move to next occurrence
                                        if pattern.RecurrenceType == 3:  # MonthNth
                                            try:
                                                occurrence_date = _get_next_month_nth(occurrence_date, pattern.Instance, pattern.DayOfWeekMask)
                                            except:
                                                # Fall back if calculation fails
                                                occurrence_date = occurrence_date + timedelta(days=30)
                                        elif pattern.RecurrenceType == 0:  # olRecursDaily
                                            occurrence_date = occurrence_date + timedelta(days=pattern.Interval)
                                        elif pattern.RecurrenceType == 1:  # olRecursWeekly
                                            occurrence_date = occurrence_date + timedelta(weeks=pattern.Interval)
                                        elif pattern.RecurrenceType == 2:  # olRecursMonthly
                                            try:
                                                from dateutil.relativedelta import relativedelta
                                                occurrence_date = occurrence_date + relativedelta(months=pattern.Interval)
                                            except:
                                                occurrence_date = occurrence_date + timedelta(days=30 * pattern.Interval)
                                        elif pattern.RecurrenceType == 5:  # olRecursYearly
                                            try:
                                                from dateutil.relativedelta import relativedelta
                                                occurrence_date = occurrence_date + relativedelta(years=pattern.Interval)
                                            except:
                                                occurrence_date = occurrence_date + timedelta(days=365 * pattern.Interval)
                                        else:
                                            break

                                        occurrence_count += 1

                                        # Safety check to prevent infinite loops
                                        if occurrence_count > 1000:
                                            break

                                except Exception as e:
                                    # If recurring expansion fails, fall back to single event
                                    start_time = item.Start
                                    end_time = item.End

                                    if start_time.tzinfo is not None:
                                        start_time = start_time.replace(tzinfo=None)
                                    if end_time.tzinfo is not None:
                                        end_time = end_time.replace(tzinfo=None)

                                    if end_time >= start_date.replace(tzinfo=None) and start_time <= cutoff_date.replace(tzinfo=None):
                                        event_data = {
                                            'Subject': item.Subject,
                                            'Start': self._format_datetime_sast(item.Start),
                                            'End': self._format_datetime_sast(item.End),
                                            'Location': item.Location,
                                            'Organizer': item.Organizer
                                        }
                                        if not any(e['Subject'] == event_data['Subject'] and e['Start'] == event_data['Start'] for e in events):
                                            events.append(event_data)
                            else:
                                # Non-recurring event - process normally
                                start_time = item.Start
                                end_time = item.End

                                # Normalize timezone
                                if start_time.tzinfo is not None:
                                    start_time = start_time.replace(tzinfo=None)
                                if end_time.tzinfo is not None:
                                    end_time = end_time.replace(tzinfo=None)

                                # Include events within the date range
                                if end_time < start_date.replace(tzinfo=None):
                                    continue

                                # Only within range
                                if start_time > cutoff_date.replace(tzinfo=None):
                                    continue

                                event_data = {
                                    'Subject': item.Subject,
                                    'Start': self._format_datetime_sast(item.Start),
                                    'End': self._format_datetime_sast(item.End),
                                    'Location': item.Location,
                                    'Organizer': item.Organizer
                                }

                                # Avoid duplicates
                                if not any(e['Subject'] == event_data['Subject'] and e['Start'] == event_data['Start'] for e in events):
                                    events.append(event_data)

                        except Exception as e:
                            print(f"  Warning: Could not process event: {e}", file=sys.stderr)
                            continue

                except Exception as e:
                    print(f"  Warning: Could not process calendar: {e}", file=sys.stderr)
                    continue

            return events

        except Exception as e:
            print(f"✗ Error extracting calendar: {e}", file=sys.stderr)
            return []

    def get_contacts(self, limit=100):
        """
        Extract contacts

        Args:
            limit: Maximum number of contacts to return

        Returns:
            List of contact dictionaries
        """
        try:
            contacts_folder = self.namespace.GetDefaultFolder(10)  # 10 = Contacts
            items = contacts_folder.Items

            contacts = []
            print(f"\nExtracting contacts (limit: {limit})...")

            for item in items:
                if len(contacts) >= limit:
                    break

                try:
                    contact_data = {
                        'Name': item.FullName,
                        'Email': item.Email1Address,
                        'Phone': item.PrimaryTelephoneNumber,
                        'Company': item.CompanyName
                    }
                    contacts.append(contact_data)
                except Exception as e:
                    print(f"  Warning: Could not process contact: {e}", file=sys.stderr)
                    continue

            return contacts

        except Exception as e:
            print(f"✗ Error extracting contacts: {e}", file=sys.stderr)
            return []

    def search_contact(self, search_name):
        """
        Search for a contact by name and return email address
        Searches both personal contacts and Global Address List (GAL)

        Args:
            search_name: Name to search for (first name, last name, or full name)

        Returns:
            Email address if found, None otherwise
        """
        try:
            search_lower = search_name.lower()
            matches = []

            # Search personal contacts first
            try:
                contacts_folder = self.namespace.GetDefaultFolder(10)  # 10 = Contacts
                items = contacts_folder.Items

                for item in items:
                    try:
                        full_name = item.FullName if item.FullName else ""
                        email = item.Email1Address if item.Email1Address else ""

                        if search_lower in full_name.lower() and email:
                            matches.append({
                                'name': full_name,
                                'email': email,
                                'source': 'Personal Contacts'
                            })
                    except:
                        continue
            except:
                pass

            # Search Global Address List (GAL)
            try:
                gal = self.namespace.GetGlobalAddressList()
                entries = gal.AddressEntries

                for entry in entries:
                    try:
                        name = entry.Name if entry.Name else ""
                        if search_lower in name.lower():
                            # Get email address
                            try:
                                email = entry.GetExchangeUser().PrimarySmtpAddress
                            except:
                                try:
                                    email = entry.Address
                                except:
                                    email = None

                            if email and "@" in email:
                                matches.append({
                                    'name': name,
                                    'email': email,
                                    'source': 'Global Address List'
                                })
                    except:
                        continue
            except:
                pass

            if len(matches) == 0:
                print(f"✗ No contacts found matching '{search_name}'")
                return None
            elif len(matches) == 1:
                print(f"✓ Found: {matches[0]['name']} <{matches[0]['email']}> [{matches[0]['source']}]")
                return matches[0]['email']
            else:
                print(f"✓ Found {len(matches)} matches for '{search_name}':")
                for i, match in enumerate(matches[:10], 1):  # Show first 10
                    print(f"  {i}. {match['name']} <{match['email']}> [{match['source']}]")
                print(f"\n→ Using first match: {matches[0]['email']}")
                return matches[0]['email']

        except Exception as e:
            print(f"✗ Error searching contacts: {e}", file=sys.stderr)
            return None

    def send_email(self, to_recipients, subject, body, cc_recipients=None,
                   bcc_recipients=None, attachment=None, priority='normal', draft=False):
        """
        Send an email or show draft for review

        Args:
            to_recipients: Email recipient(s) - comma-separated string or list
            subject: Email subject
            body: Email message body
            cc_recipients: CC recipients (optional)
            bcc_recipients: BCC recipients (optional)
            attachment: File path to attach (optional)
            priority: Email priority - 'low', 'normal', 'high'
            draft: If True, show email without sending (default: False)
        """
        try:
            # Create mail item
            mail = self.outlook.CreateItem(0)  # 0 = MailItem

            # Note: Importance property cannot be set via COM API on some Outlook configurations
            # Skipping priority setting due to COM restrictions

            # Parse recipients
            if isinstance(to_recipients, str):
                to_list = [r.strip() for r in to_recipients.split(',')]
            else:
                to_list = to_recipients

            # Set recipients
            for to_email in to_list:
                mail.Recipients.Add(to_email)

            # Add CC recipients
            if cc_recipients:
                if isinstance(cc_recipients, str):
                    cc_list = [r.strip() for r in cc_recipients.split(',')]
                else:
                    cc_list = cc_recipients

                for cc_email in cc_list:
                    recipient = mail.Recipients.Add(cc_email)
                    recipient.Type = 2  # 2 = CC

            # Add BCC recipients
            if bcc_recipients:
                if isinstance(bcc_recipients, str):
                    bcc_list = [r.strip() for r in bcc_recipients.split(',')]
                else:
                    bcc_list = bcc_recipients

                for bcc_email in bcc_list:
                    recipient = mail.Recipients.Add(bcc_email)
                    recipient.Type = 3  # 3 = BCC

            # Set subject and body with signature
            mail.Subject = subject

            # Convert plain text body to HTML with formatted signature
            body_html = body.replace('\n', '<br>')
            signature_html = """<br><br>Regards,<br><br>
<span style="font-family: 'Calibri', sans-serif; font-size: 12pt;"><strong>Greg Karsten</strong></span><br>
<span style="font-family: 'Calibri', sans-serif; font-size: 10pt; font-style: italic;">Senior Production Engineer</span><br>
<span style="font-family: 'Calibri', sans-serif; font-size: 10pt; font-style: italic;">Black Rock Mining Operations</span>"""

            mail.HTMLBody = f"<html><body>{body_html}{signature_html}</body></html>"

            # Add attachment if provided
            if attachment:
                if not os.path.exists(attachment):
                    print(f"✗ Attachment not found: {attachment}", file=sys.stderr)
                    return False

                mail.Attachments.Add(attachment)

            # Resolve all recipients
            mail.Recipients.ResolveAll()

            # Send
            mail.Send()

            print("✓ Email sent successfully")
            print(f"  Subject: {subject}")
            print(f"  To: {', '.join(to_list)}")
            if cc_recipients:
                print(f"  CC: {cc_recipients}")
            if bcc_recipients:
                print(f"  BCC: {bcc_recipients}")

            return True

        except Exception as e:
            print(f"✗ Error sending email: {e}", file=sys.stderr)
            return False

    def delete_email(self, subject=None, sender=None, days_back=None, limit=10):
        """
        Delete emails from inbox based on search criteria

        Args:
            subject: Subject text to match (partial match, case-insensitive)
            sender: Sender email or name to match (partial match, case-insensitive)
            days_back: Only delete emails from last N days (optional)
            limit: Maximum number of emails to delete (default 10, safety limit)

        Returns:
            Number of emails deleted
        """
        try:
            if not subject and not sender:
                print("✗ Error: Must specify at least --subject or --sender", file=sys.stderr)
                return 0

            inbox = self.namespace.GetDefaultFolder(6)  # 6 = Inbox
            items = inbox.Items
            items.Sort("[ReceivedTime]", False)

            # Calculate cutoff date if specified
            cutoff_date = None
            if days_back:
                cutoff_date = datetime.now() - timedelta(days=days_back)

            # Find matching emails
            matches = []
            print(f"\nSearching for emails to delete...")
            if subject:
                print(f"  Subject contains: '{subject}'")
            if sender:
                print(f"  From: '{sender}'")
            if days_back:
                print(f"  Last {days_back} days")
            print(f"  Limit: {limit} emails max\n")

            for item in items:
                if len(matches) >= limit:
                    break

                try:
                    # Check date range if specified
                    if cutoff_date:
                        received_time = item.ReceivedTime
                        if received_time.tzinfo is not None:
                            received_time = received_time.replace(tzinfo=None)
                        if cutoff_date.tzinfo is not None:
                            cutoff_date = cutoff_date.replace(tzinfo=None)
                        if received_time < cutoff_date:
                            continue

                    # Check subject match
                    if subject and subject.lower() not in item.Subject.lower():
                        continue

                    # Check sender match
                    if sender:
                        sender_match = False
                        if sender.lower() in item.SenderName.lower():
                            sender_match = True
                        try:
                            if sender.lower() in item.SenderEmailAddress.lower():
                                sender_match = True
                        except:
                            pass

                        if not sender_match:
                            continue

                    # Found a match
                    matches.append({
                        'item': item,
                        'subject': item.Subject,
                        'from': item.SenderName,
                        'received': str(item.ReceivedTime)
                    })

                except Exception as e:
                    print(f"  Warning: Could not process item: {e}", file=sys.stderr)
                    continue

            if not matches:
                print("✗ No matching emails found")
                return 0

            # Show what will be deleted
            print(f"Found {len(matches)} email(s) to delete:\n")
            for i, match in enumerate(matches, 1):
                print(f"{i}. From: {match['from']}")
                print(f"   Subject: {match['subject']}")
                print(f"   Received: {match['received']}\n")

            # Delete the emails
            deleted_count = 0
            for match in matches:
                try:
                    match['item'].Delete()
                    deleted_count += 1
                except Exception as e:
                    print(f"✗ Failed to delete: {match['subject']} - {e}", file=sys.stderr)

            print(f"✓ Successfully deleted {deleted_count} email(s)")
            return deleted_count

        except Exception as e:
            print(f"✗ Error deleting emails: {e}", file=sys.stderr)
            return 0

    def create_meeting(self, subject, start_time, end_time=None, location=None,
                      attendees=None, body=None):
        """
        Create a calendar meeting

        Args:
            subject: Meeting title
            start_time: Start time (datetime object or string "YYYY-MM-DD HH:MM")
            end_time: End time (optional, defaults to 1 hour after start)
            location: Meeting location (optional)
            attendees: Comma-separated email addresses (optional)
            body: Meeting description (optional)
        """
        try:
            # Parse start time if string
            if isinstance(start_time, str):
                start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")

            # Default end time to 1 hour after start
            if end_time is None:
                end_time = start_time + timedelta(hours=1)
            elif isinstance(end_time, str):
                end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")

            # Create appointment
            meeting = self.outlook.CreateItem(1)  # 1 = AppointmentItem

            meeting.Subject = subject
            meeting.Start = start_time
            meeting.End = end_time

            if location:
                meeting.Location = location

            if body:
                meeting.Body = body

            # Add attendees
            if attendees:
                if isinstance(attendees, str):
                    attendee_list = [a.strip() for a in attendees.split(',')]
                else:
                    attendee_list = attendees

                for attendee_email in attendee_list:
                    meeting.Recipients.Add(attendee_email)

                meeting.Recipients.ResolveAll()

            meeting.Save()

            print("✓ Meeting created successfully")
            print(f"  Subject: {subject}")
            print(f"  Start: {start_time}")
            print(f"  End: {end_time}")
            if location:
                print(f"  Location: {location}")
            if attendees:
                print(f"  Attendees: {attendees}")

            return True

        except Exception as e:
            print(f"✗ Error creating meeting: {e}", file=sys.stderr)
            return False

    def delete_meeting(self, subject, start_time):
        """
        Delete a calendar meeting

        Args:
            subject: Meeting title
            start_time: Start time (datetime object or string "YYYY-MM-DD HH:MM")
                       IMPORTANT: Use LOCAL timezone (SAST +2) as displayed in Outlook UI

        Returns:
            True if deleted, False otherwise
        """
        try:
            # Parse start time if string
            if isinstance(start_time, str):
                start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")

            # Convert local time (SAST +2) to UTC for comparison
            # SAST is UTC+2, so subtract 2 hours to get UTC
            start_time_utc = start_time - timedelta(hours=2)

            calendar = self.namespace.GetDefaultFolder(9)  # 9 = Calendar
            items = calendar.Items

            found = False
            for item in items:
                try:
                    if item.Subject == subject:
                        # Verify it's the right one by checking start time
                        item_start = item.Start
                        if item_start.tzinfo is not None:
                            item_start = item_start.replace(tzinfo=None)

                        if item_start == start_time_utc.replace(tzinfo=None):
                            print(f"✓ Found: {item.Subject}")
                            print(f"  Start (SAST): {start_time}")
                            print(f"  Start (UTC): {item.Start}")
                            print(f"  Location: {item.Location}")

                            # Delete it
                            item.Delete()
                            print(f"\n✓ Meeting deleted successfully!")
                            found = True
                            break
                except Exception as e:
                    print(f"  Warning: Could not process item: {e}", file=sys.stderr)
                    continue

            if not found:
                print(f"✗ Meeting not found: {subject} at {start_time} (SAST)")
                return False

            return True

        except Exception as e:
            print(f"✗ Error deleting meeting: {e}", file=sys.stderr)
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Outlook COM API Integration Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python outlook_extractor.py emails --days 7 --limit 50
  python outlook_extractor.py calendar --days 30
  python outlook_extractor.py send-email --to "user@company.com" --subject "Title" --body "Message"
  python outlook_extractor.py delete-email --subject "spam" --limit 5
  python outlook_extractor.py delete-email --sender "noreply@example.com" --days 7 --limit 20
  python outlook_extractor.py create-meeting --subject "Meeting" --start "2025-10-25 10:00"
  python outlook_extractor.py delete-meeting --subject "Meeting" --start "2025-10-25 10:00"
  python outlook_extractor.py contacts --limit 100
  python outlook_extractor.py all
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Emails command
    emails_parser = subparsers.add_parser('emails', help='Extract emails')
    emails_parser.add_argument('--days', type=int, default=30, help='Days back to search')
    emails_parser.add_argument('--limit', type=int, default=20, help='Max emails to return')
    emails_parser.add_argument('--folder', type=str, default='Inbox', choices=['Inbox', 'Sent Items'], help='Folder to search (Inbox or Sent Items)')
    emails_parser.add_argument('--folder-search', type=str, help='Search all subfolders matching this name pattern (e.g., "Production" or "N2")')
    emails_parser.add_argument('--list-folders', action='store_true', help='List all available folders (Inbox + subfolders)')

    # Calendar command
    calendar_parser = subparsers.add_parser('calendar', help='Extract calendar events')
    calendar_parser.add_argument('--days', type=int, default=7, help='Days ahead to check')
    calendar_parser.add_argument('--limit', type=int, default=20, help='Max events to return')
    calendar_parser.add_argument('--from-week-start', action='store_true', help='Include events from Monday of current week')

    # Contacts command
    contacts_parser = subparsers.add_parser('contacts', help='Extract contacts')
    contacts_parser.add_argument('--limit', type=int, default=100, help='Max contacts to return')

    # Search contact command
    search_parser = subparsers.add_parser('search-contact', help='Search for a contact by name')
    search_parser.add_argument('name', help='Name to search for (first name, last name, or full name)')

    # Send email command
    send_parser = subparsers.add_parser('send-email', help='Send an email')
    send_parser.add_argument('--to', required=True, help='Recipient email(s)')
    send_parser.add_argument('--subject', required=True, help='Email subject')
    send_parser.add_argument('--body', required=True, help='Email body')
    send_parser.add_argument('--cc', help='CC recipients')
    send_parser.add_argument('--bcc', help='BCC recipients')
    send_parser.add_argument('--attachment', help='File path to attach')
    send_parser.add_argument('--priority', choices=['low', 'normal', 'high'],
                            default='normal', help='Email priority')

    # Delete email command
    delete_email_parser = subparsers.add_parser('delete-email', help='Delete emails from inbox')
    delete_email_parser.add_argument('--subject', help='Subject text to match (partial, case-insensitive)')
    delete_email_parser.add_argument('--sender', help='Sender name/email to match (partial, case-insensitive)')
    delete_email_parser.add_argument('--days', type=int, help='Only delete emails from last N days')
    delete_email_parser.add_argument('--limit', type=int, default=10, help='Max emails to delete (default 10)')

    # Create meeting command
    meeting_parser = subparsers.add_parser('create-meeting', help='Create a calendar meeting')
    meeting_parser.add_argument('--subject', required=True, help='Meeting title')
    meeting_parser.add_argument('--start', required=True, help='Start time (YYYY-MM-DD HH:MM)')
    meeting_parser.add_argument('--end', help='End time (YYYY-MM-DD HH:MM)')
    meeting_parser.add_argument('--location', help='Meeting location')
    meeting_parser.add_argument('--attendees', help='Comma-separated attendee emails')
    meeting_parser.add_argument('--body', help='Meeting description')

    # Delete meeting command
    delete_parser = subparsers.add_parser('delete-meeting', help='Delete a calendar meeting')
    delete_parser.add_argument('--subject', required=True, help='Meeting title')
    delete_parser.add_argument('--start', required=True, help='Start time (YYYY-MM-DD HH:MM)')

    # All command
    all_parser = subparsers.add_parser('all', help='Extract all data')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Initialize extractor
    extractor = OutlookExtractor()

    # Execute command
    if args.command == 'emails':
        # Handle --list-folders
        if args.list_folders:
            folders = extractor.list_all_folders()
            if folders:
                print("\n✓ Available Folders:\n")
                for folder_path, display_name in folders.items():
                    print(f"  {display_name}")
                    if '\\' in folder_path:
                        print(f"    → Use: --folder-search \"{folder_path.split(chr(92))[1]}\"")
                print(f"\nTotal folders: {len(folders)}")
            sys.exit(0)

        # Handle --folder-search
        if args.folder_search:
            emails = extractor.search_folders_by_name(args.folder_search, limit=args.limit, days_back=args.days)
        else:
            folder = args.folder if hasattr(args, 'folder') else 'Inbox'
            emails = extractor.get_emails(limit=args.limit, days_back=args.days, folder=folder)

        if emails:
            print(f"\nFound {len(emails)} emails:\n")
            for email in emails[:5]:  # Show first 5
                print(f"From: {email.get('From', 'Unknown')}")
                if 'To' in email:
                    print(f"To: {email['To']}")
                print(f"Subject: {email['Subject']}")
                time_field = 'SentOn' if (not args.folder_search and args.folder == 'Sent Items') else 'ReceivedTime'
                print(f"{time_field}: {email.get(time_field, 'Unknown')}")
                if 'Unread' in email:
                    print(f"Read: {not email['Unread']}")
                print(f"Attachments: {email['Attachments']}\n")

            # Save to JSON
            with open('outlook_emails.json', 'w', encoding='utf-8') as f:
                json.dump(emails, f, indent=2, ensure_ascii=False)

            print(f"✓ Saved to outlook_emails.json")
        else:
            print("No emails found.")

    elif args.command == 'calendar':
        from_week_start = getattr(args, 'from_week_start', False)
        events = extractor.get_calendar_events(days_ahead=args.days, limit=args.limit, from_week_start=from_week_start)

        if events:
            print(f"\nFound {len(events)} events:\n")
            for event in events[:5]:  # Show first 5
                print(f"Subject: {event['Subject']}")
                print(f"Start: {event['Start']}")
                print(f"End: {event['End']}")
                print(f"Location: {event['Location']}")
                print(f"Organizer: {event['Organizer']}\n")

            # Save to JSON
            with open('outlook_calendar.json', 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=2, ensure_ascii=False)

            print(f"✓ Saved to outlook_calendar.json")
        else:
            print("No events found.")

    elif args.command == 'contacts':
        contacts = extractor.get_contacts(limit=args.limit)

        if contacts:
            print(f"\nFound {len(contacts)} contacts:\n")
            for contact in contacts[:5]:  # Show first 5
                print(f"Name: {contact['Name']}")
                print(f"Email: {contact['Email']}")
                print(f"Phone: {contact['Phone']}")
                print(f"Company: {contact['Company']}\n")

            # Save to JSON
            with open('outlook_contacts.json', 'w', encoding='utf-8') as f:
                json.dump(contacts, f, indent=2, ensure_ascii=False)

            print(f"✓ Saved to outlook_contacts.json")
        else:
            print("No contacts found.")

    elif args.command == 'search-contact':
        email = extractor.search_contact(args.name)
        return 0 if email else 1

    elif args.command == 'send-email':
        success = extractor.send_email(
            to_recipients=args.to,
            subject=args.subject,
            body=args.body,
            cc_recipients=args.cc,
            bcc_recipients=args.bcc,
            attachment=args.attachment,
            priority=args.priority
        )
        return 0 if success else 1

    elif args.command == 'delete-email':
        deleted_count = extractor.delete_email(
            subject=args.subject,
            sender=args.sender,
            days_back=args.days,
            limit=args.limit
        )
        return 0 if deleted_count > 0 else 1

    elif args.command == 'create-meeting':
        success = extractor.create_meeting(
            subject=args.subject,
            start_time=args.start,
            end_time=args.end,
            location=args.location,
            attendees=args.attendees,
            body=args.body
        )
        return 0 if success else 1

    elif args.command == 'delete-meeting':
        success = extractor.delete_meeting(
            subject=args.subject,
            start_time=args.start
        )
        return 0 if success else 1

    elif args.command == 'all':
        print("\n=== OUTLOOK DATA EXTRACTION ===\n")

        emails = extractor.get_emails(limit=20, days_back=30)
        events = extractor.get_calendar_events(days_ahead=7, limit=20)
        contacts = extractor.get_contacts(limit=50)

        all_data = {
            'emails': emails,
            'calendar_events': events,
            'contacts': contacts
        }

        with open('outlook_all.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Saved to outlook_all.json")
        print(f"  - {len(emails)} emails")
        print(f"  - {len(events)} calendar events")
        print(f"  - {len(contacts)} contacts")

    return 0


if __name__ == '__main__':
    sys.exit(main())

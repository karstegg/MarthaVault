#!/usr/bin/env python3
"""
Weekly Report Setup Automation Skill

Automates steps 1-5 of the weekly report generation process:
1. Create Week XX folder
2. Find weekly report emails (N2, N3, Gloria, S&W)
3. Find Epiroc BEV report email
4. Download all attachments to Week XX folder
5. Extract N2 HEAL content to text file

Uses Outlook COM API and fiscal week calculation (July 1, 2025 = Week 1).
"""

import sys
import os
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul')
    sys.stdout.reconfigure(encoding='utf-8')

try:
    import win32com.client
except ImportError:
    print("ERROR: pywin32 not installed. Run: pip install pywin32 --upgrade", file=sys.stderr)
    sys.exit(1)


class WeeklyReportSetup:
    """Handles setup and data collection for weekly reports"""

    # Fiscal calendar configuration
    FISCAL_WEEK_1_START = datetime(2025, 7, 1)  # July 1, 2025 = Week 1

    # Email sender name and email mappings (for dual search strategy)
    SENDERS = {
        'n2': {
            'name': 'Sikelela Nzuza',
            'email': 'Sikelela.Nzuza@assmang.co.za',
            'subject_keywords': ['weekly report', 'eng report', 'nch2', 'n2'],
            'exclude_keywords': ['mobilaris', 're:', 'fwd:'],  # Exclude replies and specific topics
            'preferred_folders': ['Production\\NCH2', 'Production', 'Planners']
        },
        'n3': {
            'name': 'Sello Sease',
            'email': 'Sello.Sease@assmang.co.za',
            'subject_keywords': ['weekly report', 'eng report', 'nch3', 'n3']
        },
        'gloria': {
            'name': 'Sipho Dubazane',
            'email': 'Sipho.Dubazane@assmang.co.za',
            'subject_keywords': ['weekly report', 'eng report', 'gloria']
        },
        'shafts': {
            'name': 'Xavier Petersen',
            'email': 'Xavier.Petersen@assmang.co.za',
            'subject_keywords': ['weekly report', 'shafts', 'winders', 's&w']
        },
        'epiroc': {
            'name': 'Phillip Moller',
            'email': 'phillip.moller@epiroc.com',
            'subject_keywords': ['brmo weekly report', 'weekly report', 'bev']
        }
    }

    # Weekly reports directory
    BASE_REPORTS_DIR = r"C:\Users\10064957\OneDrive - African Rainbow Minerals\Senior Production Engineer (Acting - January 2025)\Weekly Reports"

    def __init__(self):
        """Initialize Outlook connection"""
        try:
            try:
                self.outlook = win32com.client.GetActiveObject("Outlook.Application")
            except:
                self.outlook = win32com.client.Dispatch("Outlook.Application")

            self.namespace = self.outlook.GetNamespace("MAPI")
            inbox = self.namespace.GetDefaultFolder(6)  # 6 = Inbox

            # Build list of folders to search (Inbox + ALL subfolders recursively)
            self.folders_to_search = [inbox]

            # Recursively discover all subfolders
            print("Discovering Inbox subfolders...")
            subfolder_count = self._add_subfolders_recursive(inbox, max_depth=3)
            print(f"✓ Found {subfolder_count} subfolder(s) to search")

            print(f"✓ Connected to Outlook (searching {len(self.folders_to_search)} folder(s))")
        except Exception as e:
            print(f"✗ Error connecting to Outlook: {e}", file=sys.stderr)
            sys.exit(1)

        self.found_emails = {}
        self.downloaded_files = []
        self.missing_emails = []

    def _add_subfolders_recursive(self, parent_folder, current_depth=0, max_depth=3):
        """
        Recursively discover and add all subfolders to the search list.

        Args:
            parent_folder: Outlook folder object to search within
            current_depth: Current recursion depth (for limiting depth)
            max_depth: Maximum depth to recurse (default 3 levels)

        Returns:
            Number of subfolders added
        """
        count = 0

        if current_depth >= max_depth:
            return count

        try:
            # Get all subfolders of the parent folder
            subfolders = parent_folder.Folders

            for i in range(1, subfolders.Count + 1):  # COM API uses 1-based indexing
                try:
                    subfolder = subfolders.Item(i)
                    folder_name = subfolder.Name

                    # Add this subfolder to search list
                    self.folders_to_search.append(subfolder)
                    count += 1
                    print(f"  • {folder_name}")

                    # Recursively add subfolders of this subfolder
                    nested_count = self._add_subfolders_recursive(subfolder, current_depth + 1, max_depth)
                    count += nested_count

                except Exception as e:
                    # Skip folders that can't be accessed
                    continue
        except Exception as e:
            # No subfolders or error accessing them
            pass

        return count

    @staticmethod
    def calculate_current_week():
        """
        Calculate current fiscal week number.
        Week 1 = July 1, 2025
        """
        today = datetime.now()
        days_since_start = (today - WeeklyReportSetup.FISCAL_WEEK_1_START).days
        week_num = (days_since_start // 7) + 1
        return max(1, week_num)

    @staticmethod
    def get_week_date_range(week_num):
        """
        Get start and end date for a fiscal week.
        Returns (monday, sunday) of the week.
        """
        fiscal_start = WeeklyReportSetup.FISCAL_WEEK_1_START
        days_offset = (week_num - 1) * 7
        week_start = fiscal_start + timedelta(days=days_offset)
        week_end = week_start + timedelta(days=6)
        return week_start, week_end

    @staticmethod
    def get_target_friday(week_num):
        """
        Get Friday (report send date) for a given week.
        Week runs Mon-Sun, so Friday is 4 days after week start.
        Reports are sent on the Friday OF the week being reported.
        """
        week_start, week_end = WeeklyReportSetup.get_week_date_range(week_num)
        # Week runs Mon-Sun (assuming fiscal weeks start on Monday)
        # Friday is 4 days after Monday
        # But our fiscal weeks start on Tuesday, so Friday is 3 days after
        # Actually let me recalculate: Week 17 = Oct 21 (Tue) - Oct 27 (Mon)
        # Friday Oct 24 is 3 days after Oct 21
        friday = week_start + timedelta(days=3)
        return friday

    @staticmethod
    def get_email_search_range(week_num):
        """
        Get date range for searching emails (Friday through following Monday).
        Reports are sent on Friday and processed on Monday.

        Returns:
            (start_date, end_date) tuple for email search
        """
        friday = WeeklyReportSetup.get_target_friday(week_num)
        week_start, week_end = WeeklyReportSetup.get_week_date_range(week_num)
        # Search from Friday 00:00 through end of Monday 23:59
        # Add 1 day minus 1 second to get Monday 23:59:59
        monday_end = week_end.replace(hour=23, minute=59, second=59)
        return friday, monday_end

    def prompt_week_confirmation(self, auto_week):
        """
        Prompt user to confirm the week number.

        Args:
            auto_week: Automatically calculated week number

        Returns:
            Confirmed week number
        """
        week_start, week_end = self.get_week_date_range(auto_week)
        date_range = f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}"

        prompt = f"\nDetected Week {auto_week} ({date_range})\nProceed? (Y/n): "
        response = input(prompt).strip().lower()

        if response == 'n':
            print("Setup cancelled.")
            sys.exit(0)

        return auto_week

    def create_week_folder(self, week_num):
        """
        Create Week XX folder if it doesn't exist.

        Args:
            week_num: Week number

        Returns:
            Path to week folder
        """
        week_folder = Path(self.BASE_REPORTS_DIR) / f"Week {week_num}"

        try:
            week_folder.mkdir(parents=True, exist_ok=True)
            if week_folder.exists():
                print(f"✓ Week {week_num} folder ready: {week_folder}")
                return week_folder
            else:
                print(f"✗ Failed to create Week {week_num} folder", file=sys.stderr)
                return None
        except Exception as e:
            print(f"✗ Error creating folder: {e}", file=sys.stderr)
            return None

    def find_emails_by_sender(self, sender_info, start_date, end_date):
        """
        Find emails from a specific sender across multiple folders by name or email address
        within a specific date range, with optional subject keyword filtering.
        Uses Outlook Restrict() for fast filtering at COM level.

        Args:
            sender_info: Dict with 'name', 'email', and 'subject_keywords' keys
            start_date: Start of search range (datetime)
            end_date: End of search range (datetime)

        Returns:
            List of matching email items
        """
        try:
            matches = []
            sender_name = sender_info.get('name', '')
            sender_email = sender_info.get('email', '')
            subject_keywords = sender_info.get('subject_keywords', [])

            # Normalize timezone for dates
            if start_date.tzinfo is not None:
                start_date = start_date.replace(tzinfo=None)
            if end_date.tzinfo is not None:
                end_date = end_date.replace(tzinfo=None)

            # Build Outlook filter string for fast COM-level filtering
            # Format dates as MM/DD/YYYY for Outlook filter
            start_str = start_date.strftime("%m/%d/%Y %H:%M")
            end_str = end_date.strftime("%m/%d/%Y %H:%M")

            # Restrict by date range (much faster than Python iteration)
            filter_str = f"[ReceivedTime] >= '{start_str}' AND [ReceivedTime] <= '{end_str}'"

            # Search across all configured folders (Inbox + subfolders)
            for folder in self.folders_to_search:
                items = folder.Items

                # Apply date filter using Restrict() - fast COM-level filtering
                restricted_items = items.Restrict(filter_str)
                restricted_items.Sort("[ReceivedTime]", False)

                for item in restricted_items:
                    try:
                        # Check sender by name or email (case-insensitive)
                        sender_name_match = sender_name.lower() in item.SenderName.lower() if sender_name else False
                        sender_email_match = False

                        try:
                            sender_email_match = sender_email.lower() in item.SenderEmailAddress.lower() if sender_email else False
                        except:
                            pass

                        if not (sender_name_match or sender_email_match):
                            continue

                        # Check subject keywords if provided
                        if subject_keywords:
                            subject = item.Subject.lower()
                            subject_match = any(keyword.lower() in subject for keyword in subject_keywords)
                            if not subject_match:
                                continue

                        # Check exclude keywords if provided
                        exclude_keywords = sender_info.get('exclude_keywords', [])
                        if exclude_keywords:
                            subject = item.Subject.lower()
                            is_excluded = any(keyword.lower() in subject for keyword in exclude_keywords)
                            if is_excluded:
                                continue  # Skip this email

                        # Found a match!
                        matches.append(item)
                        return matches  # Return immediately after first match

                    except Exception as e:
                        continue

            return matches

        except Exception as e:
            print(f"✗ Error searching emails: {e}", file=sys.stderr)
            return []

    def download_attachments(self, email_item, week_folder, sender_key):
        """
        Download all attachments from an email.

        Args:
            email_item: Outlook email item
            week_folder: Path to save attachments
            sender_key: Key for tracking in found_emails

        Returns:
            Number of attachments downloaded
        """
        try:
            attachments = email_item.Attachments
            count = attachments.Count

            if count == 0:
                print(f"  ℹ No attachments found")
                return 0

            downloaded = 0
            skipped_inline = 0
            for i in range(1, count + 1):
                try:
                    attachment = attachments.Item(i)
                    filename = attachment.FileName

                    # Skip inline/embedded images (they have generic names or are referenced in HTML body)
                    # Common patterns: image001.png, Outlook-xxx.png, etc.
                    is_inline_image = False
                    try:
                        # Check if this is an inline attachment (has PR_ATTACH_CONTENT_ID property)
                        # Inline attachments are embedded in the email body, not true file attachments
                        content_id = attachment.PropertyAccessor.GetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F")
                        if content_id:
                            is_inline_image = True
                    except:
                        # If property doesn't exist, check filename patterns
                        lower_filename = filename.lower()
                        if (lower_filename.startswith('image') or
                            lower_filename.startswith('outlook-')) and \
                           (lower_filename.endswith('.png') or
                            lower_filename.endswith('.jpg') or
                            lower_filename.endswith('.gif')):
                            is_inline_image = True

                    if is_inline_image:
                        skipped_inline += 1
                        continue

                    # Download actual file attachment
                    filepath = str(week_folder / filename)
                    attachment.SaveAsFile(filepath)
                    self.downloaded_files.append(filename)
                    print(f"  ✓ Downloaded: {filename}")
                    downloaded += 1

                except Exception as e:
                    print(f"  ✗ Failed to download attachment: {e}", file=sys.stderr)
                    continue

            if skipped_inline > 0:
                print(f"  ℹ Skipped {skipped_inline} inline image(s)")

            return downloaded

        except Exception as e:
            print(f"✗ Error accessing attachments: {e}", file=sys.stderr)
            return 0

    def extract_n2_heal(self, email_item, week_folder, week_num):
        """
        Save N2 email body for Claude to parse and extract HEAL content.

        Args:
            email_item: Outlook email item
            week_folder: Path to save email body
            week_num: Week number

        Returns:
            True if successful, False otherwise
        """
        try:
            body = email_item.Body

            # Save raw email body for Claude to parse
            raw_body_filename = f"N2 Email Body - Week{week_num}.txt"
            raw_body_filepath = week_folder / raw_body_filename

            with open(raw_body_filepath, 'w', encoding='utf-8') as f:
                f.write(body)

            print(f"  ✓ Saved N2 email body: {raw_body_filename}")
            print(f"    → Claude will parse this to create N2 HEAL Page Week{week_num}.txt")
            self.downloaded_files.append(raw_body_filename)
            return True

        except Exception as e:
            print(f"  ✗ Error saving N2 email body: {e}", file=sys.stderr)
            return False

    def cleanup_downloaded_files(self, week_folder):
        """
        Remove 'Copy of' prefixes and other problematic naming from downloaded files.

        Args:
            week_folder: Path to Week XX folder

        Returns:
            Number of files renamed
        """
        renamed_count = 0
        try:
            for filename in os.listdir(week_folder):
                old_path = week_folder / filename
                new_filename = filename

                # Remove "Copy of " prefix
                if filename.startswith('Copy of '):
                    new_filename = filename.replace('Copy of ', '', 1)

                # If filename changed, rename the file
                if new_filename != filename:
                    new_path = week_folder / new_filename
                    os.rename(old_path, new_path)
                    print(f"    ✓ Renamed: {filename}")
                    print(f"           -> {new_filename}")
                    renamed_count += 1

                    # Update downloaded_files list
                    if filename in self.downloaded_files:
                        self.downloaded_files.remove(filename)
                        self.downloaded_files.append(new_filename)

        except Exception as e:
            print(f"  ⚠ Error during file cleanup: {e}", file=sys.stderr)

        return renamed_count

    def run(self, manual_week=None):
        """
        Run the weekly report setup process.

        Args:
            manual_week: Manually specified week number (optional)
        """
        print("\n" + "="*70)
        print("WEEKLY REPORT SETUP - Steps 1-5 Automation")
        print("="*70)

        # Step 1: Determine week number
        if manual_week:
            week_num = manual_week
            print(f"\n[1/5] Using manual week number: {week_num}")
        else:
            auto_week = self.calculate_current_week()
            print(f"\n[1/5] Calculating fiscal week number...")
            week_num = self.prompt_week_confirmation(auto_week)

        # Get week date range and email search range
        week_start, week_end = self.get_week_date_range(week_num)
        friday = self.get_target_friday(week_num)
        search_start, search_end = self.get_email_search_range(week_num)

        print(f"  Week dates: {week_start.strftime('%a, %b %d')} - {week_end.strftime('%a, %b %d, %Y')}")
        print(f"  Report send date (Friday): {friday.strftime('%a, %b %d, %Y')}")

        # Step 2-4: Create folder and download emails
        print(f"\n[2/5] Creating Week {week_num} folder...")
        week_folder = self.create_week_folder(week_num)
        if not week_folder:
            sys.exit(1)

        print(f"\n[3/5] Searching for weekly report emails...")
        print(f"  (Searching emails from {search_start.strftime('%a %b %d')} to {search_end.strftime('%a %b %d, %Y')})")

        # Search for each sender
        emails_to_process = [
            ('n2', 'N2 Report'),
            ('n3', 'N3 Report'),
            ('gloria', 'Gloria Report'),
            ('shafts', 'Shafts & Winders Report'),
        ]

        for key, label in emails_to_process:
            sender_info = self.SENDERS[key]
            print(f"\n  Searching for {label}...")
            print(f"    From: {sender_info['name']} ({sender_info['email']})")

            emails = self.find_emails_by_sender(sender_info, search_start, search_end)

            if emails:
                email = emails[0]
                print(f"    ✓ Found: {email.Subject}")
                print(f"    Date: {email.ReceivedTime}")
                self.found_emails[key] = email

                # Download attachments
                print(f"    Downloading {email.Attachments.Count} attachment(s)...")
                self.download_attachments(email, week_folder, key)
            else:
                print(f"    ✗ Not found")
                self.missing_emails.append(label)

        # Search for Epiroc BEV report
        print(f"\n  Searching for Epiroc BEV Report...")
        epiroc_info = self.SENDERS['epiroc']
        print(f"    From: {epiroc_info['name']} ({epiroc_info['email']})")

        epiroc_emails = self.find_emails_by_sender(epiroc_info, search_start, search_end)
        if epiroc_emails:
            email = epiroc_emails[0]
            print(f"    ✓ Found: {email.Subject}")
            print(f"    Date: {email.ReceivedTime}")
            self.found_emails['epiroc'] = email

            # Download attachments
            print(f"    Downloading {email.Attachments.Count} attachment(s)...")
            self.download_attachments(email, week_folder, 'epiroc')
        else:
            print(f"    ✗ Not found")
            self.missing_emails.append('Epiroc BEV Report')

        # Cleanup: Remove "Copy of" prefixes and normalize filenames
        print(f"\n  Cleaning up downloaded filenames...")
        renamed_count = self.cleanup_downloaded_files(week_folder)
        if renamed_count > 0:
            print(f"  ✓ Renamed {renamed_count} file(s) to remove prefixes")
        else:
            print(f"  ✓ All filenames clean")

        # Step 5: Extract N2 HEAL
        print(f"\n[4/5] Saving N2 email body for Claude to parse...")
        if 'n2' in self.found_emails:
            self.extract_n2_heal(self.found_emails['n2'], week_folder, week_num)
        else:
            print(f"  ⚠ N2 email not available, skipping HEAL extraction")

        # Summary
        print(f"\n[5/5] Setup Summary")
        print(f"  {'='*66}")
        print(f"  Week folder: {week_folder}")
        print(f"  Files downloaded: {len(self.downloaded_files)}")

        if self.downloaded_files:
            print(f"\n  Downloaded files:")
            for filename in self.downloaded_files:
                print(f"    • {filename}")

        if self.missing_emails:
            print(f"\n  ⚠ Missing emails:")
            for email in self.missing_emails:
                print(f"    • {email}")

        print(f"\n  {'='*66}")
        print(f"✓ Setup complete! Ready for data extraction (steps 6-12)")
        print(f"\n  Next steps:")
        print(f"    0. Ask Claude to parse N2 Email Body and create N2 HEAL Page Week{week_num}.txt")
        print(f"    1. Run extract-primary-equipment (N2, N3, Gloria)")
        print(f"    2. Run extract-maintenance-compliance (N2, N3, Gloria)")
        print(f"    3. Run extract-bev")
        print(f"    4. Run extract-epiroc-bev-report")
        print(f"    5. Run extract-pptx-heal (N3, Gloria, S&W)")
        print(f"    6. Run extract-shafts-winders")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Weekly Report Setup - Automate steps 1-5 of report generation'
    )
    parser.add_argument(
        '--week',
        type=int,
        help='Specify week number (optional, will prompt if not provided)'
    )

    args = parser.parse_args()

    setup = WeeklyReportSetup()
    setup.run(manual_week=args.week)


if __name__ == '__main__':
    main()

import win32com.client
from datetime import datetime, timedelta
import json

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # 6 = Inbox

# Search for email from Sikelela Nzuza with subject "FW: DT0121"
target_date = datetime(2025, 12, 2, 12, 4, 58)
search_start = target_date - timedelta(hours=2)
search_end = target_date + timedelta(hours=2)

print("Searching for email from Sikelela Nzuza with subject 'FW: DT0121'...")

found_email = None
for message in inbox.Items:
    try:
        # Check sender
        if hasattr(message, 'SenderEmailAddress'):
            sender = message.SenderEmailAddress.lower()
            if 'sikelela.nzuza' in sender or 'nzuza' in sender.lower():
                # Check subject
                subject = message.Subject if hasattr(message, 'Subject') else ""
                if 'DT0121' in subject:
                    received_time = message.ReceivedTime
                    if search_start <= received_time <= search_end:
                        found_email = message
                        break
    except Exception as e:
        continue

if found_email:
    print(f"\n{'='*80}")
    print(f"EMAIL FOUND")
    print(f"{'='*80}")
    print(f"\nFrom: {found_email.SenderName} <{found_email.SenderEmailAddress}>")
    print(f"To: {found_email.To}")
    if found_email.CC:
        print(f"CC: {found_email.CC}")
    print(f"Subject: {found_email.Subject}")
    print(f"Received: {found_email.ReceivedTime}")
    print(f"\n{'-'*80}")
    print(f"BODY:")
    print(f"{'-'*80}")
    print(found_email.Body)
    print(f"\n{'-'*80}")
    print(f"ATTACHMENTS:")
    print(f"{'-'*80}")

    if found_email.Attachments.Count > 0:
        for i, attachment in enumerate(found_email.Attachments, 1):
            print(f"\nAttachment {i}:")
            print(f"  Filename: {attachment.FileName}")
            print(f"  Size: {attachment.Size:,} bytes")
            print(f"  Type: {attachment.Type}")
    else:
        print("No attachments")

    print(f"\n{'='*80}")
else:
    print("\nEmail not found. Checking recent emails from Sikelela Nzuza...")

    count = 0
    for message in inbox.Items:
        try:
            if hasattr(message, 'SenderEmailAddress'):
                sender = message.SenderEmailAddress.lower()
                if 'sikelela' in sender or 'nzuza' in sender.lower():
                    print(f"\nFrom: {message.SenderName}")
                    print(f"Subject: {message.Subject}")
                    print(f"Received: {message.ReceivedTime}")
                    count += 1
                    if count >= 10:
                        break
        except:
            continue

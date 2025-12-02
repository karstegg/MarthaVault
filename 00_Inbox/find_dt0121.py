import win32com.client
from datetime import datetime, timedelta

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # 6 = Inbox

print("Searching for any email with 'DT0121' in subject...")

# Search last 7 days
cutoff_date = datetime.now() - timedelta(days=7)

found_emails = []
count = 0

for message in inbox.Items:
    try:
        count += 1
        if count % 100 == 0:
            print(f"Checked {count} emails...")

        # Check if received within last week
        if hasattr(message, 'ReceivedTime') and message.ReceivedTime < cutoff_date:
            continue

        # Check subject for DT0121
        subject = message.Subject if hasattr(message, 'Subject') else ""
        if 'DT0121' in subject.upper():
            found_emails.append({
                'sender': message.SenderName,
                'email': message.SenderEmailAddress if hasattr(message, 'SenderEmailAddress') else "",
                'subject': subject,
                'received': message.ReceivedTime,
                'message': message
            })

        if count >= 500:  # Limit search to recent 500 emails
            break

    except Exception as e:
        continue

print(f"\nTotal emails checked: {count}")
print(f"Found {len(found_emails)} email(s) with 'DT0121' in subject:\n")

for idx, email_info in enumerate(found_emails, 1):
    msg = email_info['message']
    print(f"\n{'='*80}")
    print(f"EMAIL {idx}")
    print(f"{'='*80}")
    print(f"From: {email_info['sender']} <{email_info['email']}>")
    print(f"To: {msg.To}")
    if msg.CC:
        print(f"CC: {msg.CC}")
    print(f"Subject: {email_info['subject']}")
    print(f"Received: {email_info['received']}")
    print(f"\n{'-'*80}")
    print(f"BODY:")
    print(f"{'-'*80}")
    print(msg.Body)
    print(f"\n{'-'*80}")
    print(f"ATTACHMENTS:")
    print(f"{'-'*80}")

    if msg.Attachments.Count > 0:
        for i, attachment in enumerate(msg.Attachments, 1):
            print(f"\nAttachment {i}:")
            print(f"  Filename: {attachment.FileName}")
            print(f"  Size: {attachment.Size:,} bytes")
            print(f"  Type: {attachment.Type}")
    else:
        print("No attachments")

print(f"\n{'='*80}")

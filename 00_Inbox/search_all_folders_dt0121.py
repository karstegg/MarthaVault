import win32com.client
from datetime import datetime, timedelta

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

def search_folder(folder, folder_path="", depth=0, max_depth=3):
    """Recursively search folders for DT0121 email"""
    if depth > max_depth:
        return []

    found_emails = []
    current_path = f"{folder_path}/{folder.Name}" if folder_path else folder.Name

    try:
        print(f"{'  ' * depth}Searching: {current_path}")

        # Search items in this folder
        cutoff_date = datetime.now() - timedelta(days=7)
        count = 0

        for message in folder.Items:
            try:
                count += 1
                if count > 200:  # Limit per folder
                    break

                if hasattr(message, 'ReceivedTime') and message.ReceivedTime < cutoff_date:
                    continue

                subject = message.Subject if hasattr(message, 'Subject') else ""
                if 'DT0121' in subject.upper():
                    found_emails.append({
                        'folder': current_path,
                        'sender': message.SenderName,
                        'email': message.SenderEmailAddress if hasattr(message, 'SenderEmailAddress') else "",
                        'subject': subject,
                        'received': message.ReceivedTime,
                        'message': message
                    })
            except:
                continue

        # Search subfolders
        if folder.Folders.Count > 0:
            for subfolder in folder.Folders:
                found_emails.extend(search_folder(subfolder, current_path, depth + 1, max_depth))

    except Exception as e:
        print(f"{'  ' * depth}Error accessing {current_path}: {e}")

    return found_emails

# Search Inbox and subfolders
print("Starting search in Inbox and subfolders...\n")
inbox = outlook.GetDefaultFolder(6)
found = search_folder(inbox)

# Also check Sent Items
print("\nSearching Sent Items...\n")
sent_items = outlook.GetDefaultFolder(5)
found.extend(search_folder(sent_items))

print(f"\n{'='*80}")
print(f"SEARCH COMPLETE - Found {len(found)} email(s)")
print(f"{'='*80}\n")

for idx, email_info in enumerate(found, 1):
    msg = email_info['message']
    print(f"\n{'='*80}")
    print(f"EMAIL {idx} - Found in: {email_info['folder']}")
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

import imaplib
import email 
from dotenv import load_dotenv
import os

load_dotenv()

address = os.getenv("Email_Address")
password = os.getenv("Email_Password")
imap_server = "imap.ethereal.email"
imap_port = 993
imap = None

try:
    # Connect and login
    imap = imaplib.IMAP4_SSL(imap_server, imap_port)
    imap.login(address, password)
    imap.select("Inbox")
    
    # Search for all emails
    _, msg_ids = imap.search(None, "ALL")
    
    # Check if inbox is empty
    if not msg_ids[0].split():
        print("Inbox is empty")
    else:
        latest_id = msg_ids[0].split()[-1]
        _, data = imap.fetch(latest_id, "(RFC822)")
        message = email.message_from_bytes(data[0][1])
        
        print(f"Message Number: {latest_id.decode()}")
        print(f"From: {message.get('From')}")
        print(f"To: {message.get('To')}")
        print(f"BCC: {message.get('BCC')}")
        print(f"Date: {message.get('Date')}")
        print(f"Subject: {message.get('Subject')}")
        print("Content:")
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                print(part.get_payload(decode=True).decode())

except imaplib.IMAP4.error as e:
    print(f"IMAP error: {e}")
except Exception as e:
    print(f"General error: {e}")
finally:
    # Always close connection even if error occurs
    if imap:
        imap.close()
        imap.logout()
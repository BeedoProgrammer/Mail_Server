from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
from dotenv import load_dotenv
import os

def send_email_secure(subject, sender, password, recipients, cc, body, smtp_server, smtp_port):
    try:
        # Create secure SSL context
        context = ssl.create_default_context()

        # Construct email
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg['Cc'] = ', '.join(cc)
        msg.attach(MIMEText(body, 'plain'))

        # Send email using secure connection
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, recipients + cc, msg.as_string())
        print("Secure email sent successfully!")

    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"General error: {e}")


# Test
load_dotenv()

subject = "Secure Update"

# Get email and password from .env file
sender = os.getenv("Email_Address")
password = os.getenv("Email_Password")

recipients = ["test1@sharebot.net", "test2@sharebot.net"]
cc = ["limeteresina@sharebot.net"]
body = "This email is sent using a secure connection."
smtp_server = "smtp.gmail.com"
smtp_port = 465

send_email_secure(subject, sender, password, recipients, cc, body, smtp_server, smtp_port)
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
import time
import logging
from email.parser import BytesParser
from email import policy
from config import USER, APP_PASSWORD, IMAP_URL, SMTP_URL, SMTP_PORT
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def connect_to_smtp():
    """Connect to the SMTP server and login."""
    server = smtplib.SMTP(SMTP_URL, SMTP_PORT)
    server.starttls()
    server.login(USER, APP_PASSWORD)
    return server

def send_email(recipient, subject, body):
    """Send an email using SMTP."""
    server = connect_to_smtp()
    message = MIMEText(body)
    message['From'] = USER
    message['To'] = recipient
    message['Subject'] = subject
    server.sendmail(USER, recipient, message.as_string())
    server.quit()
    logging.info(f"Email sent to {recipient}")

def connect_to_imap():
    """Connect to the IMAP server and login."""
    imap = imaplib.IMAP4_SSL(IMAP_URL)
    imap.login(USER, APP_PASSWORD)
    return imap

def get_unread_emails():
    """Fetch unread emails from the inbox."""
    imap = connect_to_imap()
    imap.select('inbox')
    status, response = imap.search(None, 'UNSEEN')
    unread_msg_nums = response[0].split()
    messages = []
    for e_id in unread_msg_nums:
        _, response = imap.fetch(e_id, '(RFC822)')
        for part in response:
            if isinstance(part, tuple):
                msg = email.message_from_bytes(part[1], policy=policy.default)
                messages.append(msg)
    imap.logout()
    return messages

def process_emails():
    """Process unread emails and perform actions based on content."""
    emails = get_unread_emails()
    for msg in emails:
        email_subject = msg['subject']
        email_from = msg['from']
        # Assuming you parse and handle the email content here
        logging.info(f"Processing email from {email_from} with subject {email_subject}")
        # Example sending a response
        send_email(email_from, "Re: " + email_subject, "Thank you for your email.")

if __name__ == "__main__":
    while True:
        process_emails()
        time.sleep(3)  # Check every 5 minutes

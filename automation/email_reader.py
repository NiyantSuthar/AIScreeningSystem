import imaplib
import email
from email.header import decode_header
import os



EMAIL = "Enter your email here"
APP_PASSWORD = "Enter your app password here"


def fetch_unread_applications():

    DOWNLOAD_FOLDER = "temp_resumes"

    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, APP_PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, '(UNSEEN SUBJECT "application")')
    email_ids = messages[0].split()

    if not email_ids:
        print("No unread application emails found.")
        mail.logout()
        return []

    print(f"Found {len(email_ids)} unread application emails.")

    email_data_list = []

    for email_id in email_ids:

        status, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        sender = msg.get("From")

        print("Subject:", subject)
        print("From:", sender)

        attachment_path = None

        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" in content_disposition:
                filename = part.get_filename()

                if filename and filename.lower().endswith(".pdf"):
                    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))

                    print("Downloaded:", filename)
                    attachment_path = filepath

        mail.store(email_id, '+FLAGS', '\\Seen')

        print("-" * 50)

        email_data_list.append({
            "subject": subject,
            "sender": sender,
            "attachment_path": attachment_path
        })

    mail.logout()
    return email_data_list
import os
import smtplib
import mimetypes
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

class EmailAlert:
    def __init__(self):
        self.sender = os.getenv("DWC_EMAIL")
        self.password = os.getenv("DWC_EMAIL_PASSWORD")
        self.recipients = [
            os.getenv("DWC_ALERT_EMAIL_1"),
            os.getenv("DWC_ALERT_EMAIL_2")
        ]

    def send(self, subject, message, attachments=None):
        try:
            msg = EmailMessage()
            msg["From"] = self.sender
            msg["To"] = ", ".join(self.recipients)
            msg["Subject"] = subject
            msg.set_content(message)

            if attachments:
                for path in attachments:
                    if not path or not os.path.exists(path):
                        continue
                    mime, _ = mimetypes.guess_type(path)
                    maintype, subtype = mime.split("/")
                    with open(path, "rb") as f:
                        msg.add_attachment(
                            f.read(),
                            maintype=maintype,
                            subtype=subtype,
                            filename=os.path.basename(path)
                        )

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender, self.password)
                server.send_message(msg)

            print("[EMAIL] Alert + evidence sent")

        except Exception as e:
            print("[EMAIL] Failed:", e)


import smtplib
from email.message import EmailMessage
from app.config import EMAIL_USER, EMAIL_PASS

def send_verification_email(to, token):
    msg = EmailMessage()
    msg["Subject"] = "Verify Your Email"
    msg["From"] = EMAIL_USER
    msg["To"] = to
    msg.set_content(f"Click to verify: http://localhost:8000/client/verify-email?token={token}")

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

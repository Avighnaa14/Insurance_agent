# utils/sendgrid_client.py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")  # Verified sender email

def send_email(to_email: str, subject: str, content: str):
    """Send a plain-text email via SendGrid. Returns status code."""
    if not SENDGRID_API_KEY or not FROM_EMAIL:
        raise RuntimeError("SendGrid not configured. Set SENDGRID_API_KEY and FROM_EMAIL env vars.")
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=content
    )
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    return response.status_code

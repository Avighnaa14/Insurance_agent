from twilio.rest import Client
import os

# ⚠️ You’ll set these in Render Environment Variables later
account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH")
twilio_number = os.getenv("TWILIO_PHONE")

client = Client(account_sid, auth_token)

def send_sms(to: str, body: str):
    """Send an SMS using Twilio"""
    message = client.messages.create(
        body=body,
        from_=twilio_number,
        to=to
    )
    return message.sid

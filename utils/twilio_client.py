# utils/twilio_client.py
import os
from twilio.rest import Client

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")  # your Twilio phone number in +country format

client = None
if TWILIO_SID and TWILIO_AUTH:
    client = Client(TWILIO_SID, TWILIO_AUTH)

def send_sms(to: str, body: str):
    """Send an SMS via Twilio. Returns message SID or raises."""
    if client is None:
        raise RuntimeError("Twilio client not configured. Set TWILIO_SID and TWILIO_AUTH env vars.")
    message = client.messages.create(
        body=body,
        from_=TWILIO_PHONE,
        to=to
    )
    return message.sid

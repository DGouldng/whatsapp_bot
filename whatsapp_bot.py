from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')

# Use these variables in your code


app = Flask(__name__)

# Define banned words
BANNED_WORDS = ["spam", "banword", "offensive"]

@app.route("/bot", methods=["POST"])
def whatsapp_bot():
    # Get incoming message
    incoming_msg = request.form.get("Body").strip()
    sender = request.form.get("From")

    # Create response
    resp = MessagingResponse()
    msg = resp.message()

    # Check for banned words
    if any(word in incoming_msg.lower() for word in BANNED_WORDS):
        msg.body(f"🚫 Warning: Your message contains inappropriate content!")
    else:
        msg.body("✅ Message received! Thank you for contributing to the group.")

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

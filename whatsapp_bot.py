import json
import re
from flask import Flask, request, jsonify
from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "DGould"  # Replace with your verify token

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification step
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode and token:
            if mode == "subscribe" and token == VERIFY_TOKEN:
                return challenge, 200  # Respond with the challenge to verify the endpoint
            else:
                return "Forbidden", 403
    elif request.method == 'POST':
        # Handle incoming webhook events here
        data = request.get_json()
        print("Webhook received:", data)
        return "Event received", 200


# List of admin phone numbers (replace with actual phone numbers)
admin_numbers = ['2347040968349']

# List of common spam keywords (extend as needed)
spam_keywords = ['cheap', 'offer', 'discount', 'free', 'urgent', 'limited time']

# Define the phone number for the bot
bot_phone_number = '2348107301257'

# first token I think temporary one 
# EAAHXnlhnVkUBO9mwYjHcZAWZBkowoZCCpotWmYqngbJtzLpCVBKBBjdn4hZAqcOkTwe32N0rGZB29eKYrsZBMisAO2OdPqRe4kigQeZAQsBk1aa8dsDgBW5GeVg2KSYd2jAJGRVKZCzm2oza1UnQmqzbFVzVHeZATMqEZBATyFjbx3wOrUZA4vOe6qXGQtZAan0Eel6dHYZByckIQyLX1mEgCWEquLT5JZCzRpb0ngOAp6r13638kZD

# The one I think it's permanent 
# EAAHXnlhnVkUBOwxnT9bJvYRHoSVeHECK2itvgelNcX2yR4x6om71ZAQdN1QdZBbZAEFSHjMsHLr46uBR5kH9fO371XGEGUgMtNBCSjwnpYvHyOAMOZADFAo9WUX69tmVkFXFgFT36rztdOlUlxM0RKvR0M7F0MqvRkSxkkBxcE1cJAUus92Luic7UG7ZAVpdpqAZDZD

# Function to send a message to the WhatsApp number
def send_message(to, message):
    url = "https://graph.facebook.com/v21.0/560717020449590/messages"
    headers = {
        'Authorization': 'Bearer EAAHXnlhnVkUBOwxnT9bJvYRHoSVeHECK2itvgelNcX2yR4x6om71ZAQdN1QdZBbZAEFSHjMsHLr46uBR5kH9fO371XGEGUgMtNBCSjwnpYvHyOAMOZADFAo9WUX69tmVkFXFgFT36rztdOlUlxM0RKvR0M7F0MqvRkSxkkBxcE1cJAUus92Luic7UG7ZAVpdpqAZDZD',
        'Content-Type': 'application/json'
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to check if a message is spam
def is_spam(message):
    for keyword in spam_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', message.lower()):
            return True
    return False

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print('Incoming message:', json.dumps(data, indent=2))

    # Get the sender's phone number and the message content
    sender = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    group_id = data['entry'][0]['changes'][0]['value']['messages'][0].get('group', {}).get('id', 'unknown')
    message = data['entry'][0]['changes'][0]['value']['messages'][0].get('text', {}).get('body')

    # If the message is spam, notify the admin
    if message and is_spam(message):
        # Send a notification to the sender about the spam
        send_message(sender, "Your message was flagged as spam and will not be sent to the group.")
        
        # Send a notification to the admin (replace with actual admin number)
        send_message('2347040968349', f"Alert: A potential spam message was detected: {message}")

        return jsonify({'status': 'spam detected'}), 200

    # If sender is an admin and sends "stop", stop the bot
    if sender in admin_numbers and message.lower() == "./Stop!":
        send_message(sender, "Bot stopped. I will no longer respond.")
        # Add any other logic to disable the bot if necessary
        return jsonify({'status': 'stopped'}), 200

    # Handle regular messages
    if message:
        # Respond to greeting
        if 'Hello' in message.lower():
            reply = "Hey! I'm DGould bot. How can I help you today?"
        elif 'Hi' in message.lower():
            reply = "Yeah I'm listening to you!"
        elif 'order' in message.lower():
            reply = "I can help you with your order. Please provide your order ID."
        else:
            reply = f"Thank you for your message: {message}. How can I assist you further?"

        # Send the response to the sender
        send_message(sender, reply)

    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True)

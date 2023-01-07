try:    
    import os
    import requests
    from flask import Flask, request
    from waitress import serve
except ImportError as err:
    print(f"Failed to import the required modules: {err}")

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

webhook = Flask(__name__)

@webhook.route("/", methods=["GET"])
def handle_get():
    send_message(f"GET /", TELEGRAM_CHAT_ID)
    
    return webhook.send_static_file('index.html')

@webhook.route("/sms", methods=["POST"])
def sms_reply():
    message = request.form["Body"]
    sender = request.form["From"]
    
    send_message(f"From: {sender}\n{message}", TELEGRAM_CHAT_ID)
    
    return webhook.send_static_file('index.html')

def send_message(message, chat_id):
    url = f"{TELEGRAM_API_URL}/sendMessage?text={message}&chat_id={chat_id}"
    requests.get(url)

def send_initial_message(chat_id):
    message = "Bot started"
    url = f"{TELEGRAM_API_URL}/sendMessage?text={message}&chat_id={chat_id}"
    requests.get(url)

if __name__ == "__main__":
    send_initial_message(TELEGRAM_CHAT_ID)
    serve(webhook, host='0.0.0.0', port=8080)

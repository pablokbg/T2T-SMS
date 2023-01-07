try:    
    import os
    import requests
    from flask import Flask, request, abort
    from waitress import serve
    from functools import wraps
    from twilio.request_validator import RequestValidator
except ImportError as err:
    print(f"Failed to import the required modules: {err}")

TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

webhook = Flask(__name__)

def validate_twilio_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        validator = RequestValidator(TWILIO_AUTH_TOKEN)
        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        if request_valid:
            return f(*args, **kwargs)
        else:
            return abort(403)

    return decorated_function

@webhook.route("/", methods=["GET"])
def index_webhook():
    return webhook.send_static_file('index.html')

@webhook.route("/sms", methods=["POST"])
@validate_twilio_request
def sms_reply():
    message = request.form["Body"]
    sender = request.form["From"]
    
    send_message(f"From: {sender}\n{message}", TELEGRAM_CHAT_ID)
    
    return 'SUCCESS'

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

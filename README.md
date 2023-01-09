# ![Logo](/images/T2T_logo.png) T2T SMS 
T2T SMS is a tool written in Python that allows you to forward SMS from your Twilio number to Telegram via HTTP requests.

# Capture
> ![capture](https://raw.githubusercontent.com/pablokbg/T2T-SMS/main/images/capture.png)

# Use
* Step 1: Clone the repository.
```
git clone https://github.com/pablokbg/T2T-SMS.git && cd T2T-SMS
```
* Step 2: Edit the [docker-compose.yml](https://github.com/pablokbg/T2T-SMS/blob/main/docker-compose.yml#L8-L11) file and change the environment section to your credentials.
```
environment:
 - TELEGRAM_BOT_TOKEN=123456789:AAAAAAAAAAAAAAAAAAAAAA
 - TELEGRAM_CHAT_ID=000000000
 - TWILIO_AUTH_TOKEN=abcdefghi123456789
```
* Step 3: Add the webhook in [Twilio](https://twilio.com/console/phone-numbers/incoming).
> ![webhook](https://raw.githubusercontent.com/pablokbg/T2T-SMS/main/images/webhook_twilio.jpg)

* Step 4: Launch the docker container.
```
docker-compose up -d
```

# Notes
* By default the docker container runs on port 8624, but you can change it from the [docker-compose.yml](https://github.com/pablokbg/T2T-SMS/blob/main/docker-compose.yml#L12-L13) file.
* The Telegram bot must be turned on (/start) before launching the container, as the bot works through requests.

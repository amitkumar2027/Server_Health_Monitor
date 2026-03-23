import requests
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram(message):

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        })

    except Exception as e:
        print("Telegram error:", e)


import os
import time
import random
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

PRODUCT_URL = os.environ["PRODUCT_URL"]

def notify(message):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        },
        timeout=15
    ).raise_for_status()

def check_product():
    response = requests.get(
        PRODUCT_URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for button in soup.select('button[name="add"]'):
        if not button.has_attr("disabled"):
            return True

    return False

def main():
    was_available = False

    while True:
        try:
            available = check_product()

            if available and not was_available:
                notify(
                    "🔥 AIR FORCE 1 RS BLACK POTENZIALMENTE DISPONIBILI!\n"
                    + PRODUCT_URL
                )

            was_available = available

        except Exception as error:
            print("Controllo non riuscito:", error)

        time.sleep(300)

if __name__ == "__main__":
    main()

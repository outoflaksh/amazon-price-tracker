import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_current_price(amazon_product_url: str) -> int:
    import requests
    from bs4 import BeautifulSoup

    price_tag_class = "a-price-whole"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    }
    response = requests.get(
        url=amazon_product_url,
        headers=headers,
    )

    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            current_price = int(
                soup.find("span", {"class": price_tag_class})
                .text.replace(",", "")
                .replace(".", "")
            )

            return current_price

        except AttributeError:
            raise Exception("Can't connect to the Amazon page")
    return -1


def send_message():
    from twilio.rest import Client

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    from_number = os.environ["TWILIO_PHONE_NUMBER"]
    to_number = os.environ["TO_PHONE_NUMBER"]

    message = client.messages.create(
        body="The iPhone you wanted is available at low prices!",
        from_=from_number,
        to=to_number,
    )

    return message


def price_drop_alert_job(amazon_product_url: str, check_price: int):
    curr_price = get_current_price(amazon_product_url)

    if curr_price != -1 and curr_price < check_price:
        send_message()
        return (curr_price, True)

    return (curr_price, False)

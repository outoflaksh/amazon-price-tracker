from fastapi import FastAPI
from scraper import price_drop_alert_job

import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/")
def read_index():
    return "Hello there!"


@app.get("/initiate")
def initiate_job():
    curr_price, message_sent = price_drop_alert_job(
        amazon_product_url=os.environ["AMAZON_URL"],
        check_price=49000,
    )

    return {"Current price": curr_price, "Message sent": message_sent}


@app.get("/healthcheck")
def healthcheck():
    return {"msg": "OK"}

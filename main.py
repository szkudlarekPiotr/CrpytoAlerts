import requests
from twilio.rest import Client
from datetime import date, timedelta
import os

today = date.today()
yesterday = date.today() - timedelta(days=1)

crypto_api_key = os.environ['CRYPTO_API_KEY']

crypto_params= {
    "function":"DIGITAL_CURRENCY_DAILY",
    "symbol":"BTC",
    "market":"PLN",
    "apikey":crypto_api_key
}

crypto_response = requests.get("https://www.alphavantage.co/query?", params=crypto_params)
crypto_response.raise_for_status()

BTC_data = crypto_response.json()

today_open_val = round(float(BTC_data["Time Series (Digital Currency Daily)"]
                             [str(today)]["1b. open (USD)"]),2)
yesterday_open_val = round(float(BTC_data["Time Series (Digital Currency Daily)"]
                                 [str(yesterday)]["1b. open (USD)"]),2)


news_api_key = os.environ['NEWS_API_KEY']

news_params={
    "q":"+bitcoin",
    "from":yesterday,
    "language":"en",
    "sortBy":"relevancy",
    "domains":"cryptodaily.co.uk",
    "apikey":news_api_key
}

news_response = requests.get("https://newsapi.org/v2/everything?", params=news_params)
news_response.raise_for_status()

news_data = news_response.json()

article_title = news_data["articles"][0]["title"]
article_desc = news_data["articles"][0]["description"]


t_account_sid = os.environ['TWILIO_ACCOUNT_SID']
t_auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_client = Client(t_account_sid, t_auth_token)


daily_value_shift = round(((float(today_open_val) - 
                            float(yesterday_open_val))/float(today_open_val))*100,2)
up = "☝️"
down = "👇"
emoji = lambda up,down : up if daily_value_shift > 0 else down
message_body = (f"\nToday's open value: {today_open_val} USD."
                f"\nYesterdays open val: {yesterday_open_val} USD. \nDaily shift: "
                f"{emoji(up, down)} {abs(daily_value_shift)}%. \nMost relevant article: {article_title}. \n{article_desc}")

message = twilio_client.messages.create(
    body = message_body,
    from_ = "placeholder for actual phone number",
    to = "placeholder for actual phone number"
)
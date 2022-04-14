import os
import requests
from twilio.rest import Client
from datetime import date, timedelta

TOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_KEY_ALPHA = os.environ["API_KEY_ALPHA"]
API_KEY_NEWS = os.environ["API_KEY_NEWS"]

account_sid = os.environ['twilio_account_sid']
auth_token = os.environ['twilio_auth_token']
my_number = os.environ["mobile_number"]

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": TOCK_NAME,
    "apikey": API_KEY_ALPHA,
    "slice": "month1"
}

data = requests.get(url=STOCK_ENDPOINT, params=parameters)
data_json = data.json()
yesterday_close_rate = float(data_json["Time Series (Daily)"]['2022-04-08']["4. close"])
day_before_rate = float(data_json["Time Series (Daily)"]['2022-04-07']["4. close"])

difference_between_rating = abs(yesterday_close_rate - day_before_rate)
difference_between_rating = round(difference_between_rating, 2)

difference_percentage = difference_between_rating * 100 / yesterday_close_rate
difference_percentage = round(difference_percentage, 4)

if difference_percentage > 3:
    parameters = {
        "q": "tesla",
        "from": date.today() - timedelta(days=1),
        "to": date.today(),
        "sortBy": "popularity",
        "language": "en",
        "apiKey": API_KEY_NEWS
    }
    news_data = requests.get(url=NEWS_ENDPOINT, params=parameters)
    news_data_json = news_data.json()
    news_list = []
    for i in range(3):
        news_title = news_list.append(news_data_json["articles"][i]["title"])
        news_description = news_list.append(news_data_json["articles"][i]["description"])
        news_url = news_list.append(news_data_json["articles"][i]["url"])
    if yesterday_close_rate - day_before_rate < 0:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"🔻{difference_percentage}%\n{news_list}",
            from_='+16625055192',
            to=my_number)
        print(message.status)
    else:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"🔺{difference_percentage}%\n{news_list}",
            from_='+16625055192',
            to=my_number)
        print(message.status)

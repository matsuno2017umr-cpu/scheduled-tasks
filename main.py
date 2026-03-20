import os
import requests
from twilio.rest import Client

api_key = os.environ.get("OWM_API_KEY")
MY_LAT = 3.139003
MY_LONG = 101.686852
# api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}
# api.openweathermap.org/data/2.5/forecast?lat={3.139003}&lon={101.686852}&appid={f1367254f3e7fc423b0d1179f4220408}
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
call_number = os.environ.get("CALL_NUMBER")

parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "cnt": 4
}

response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
data = response.json()
print(data["list"][0]["weather"])

nearest = data["list"][0]["weather"][0]["id"]
print("次の3時間予報:", nearest)

will_rain = False
for forecast in data["list"]:
    # dt_txt = forecast["dt_txt"]  # 例: "2026-03-19 12:00:00"
    # temp = forecast["main"]["temp"]  # 気温（units=metricなら℃）
    weather_desc = forecast["weather"][0]["id"]
    if int(weather_desc) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain!",
        from_="+18143288412",
        to=call_number
    )
    print(message.status)

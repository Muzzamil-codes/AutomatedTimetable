import requests
from datetime import datetime, timedelta

url = "https://muslimsalat.p.rapidapi.com/doha.json"

headers = {
	"X-RapidAPI-Key": "e48d3c1ff5mshcba2893797cf7fep1396dejsn0565e9c8aefd",
	"X-RapidAPI-Host": "muslimsalat.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

data = response.json()

items_dict = data.get('items', {})[0]
items_dict.pop('date_for')

for key, value in items_dict.items():
    # Parse the time string in 12-hour format and convert it to 24-hour format
    time_12_hour = datetime.strptime(value, '%I:%M %p')
    time_12_hour = time_12_hour + timedelta(minutes=10)
    time_24_hour = time_12_hour.strftime('%H:%M')
    items_dict[key] = time_24_hour

for key, value in items_dict.items():
    if key == "maghrib":
        given_time = datetime.strptime(value, '%H:%M')
        correct_time = given_time - timedelta(minutes=5)
        correct_time = correct_time.strftime('%H:%M')
        items_dict[key] = correct_time

print(items_dict)

def ti(time, delay):
    given_time = datetime.strptime(time, '%H:%M')

    # Add 30 minutes to the time
    increased_time = given_time + timedelta(minutes=delay)

    # Convert the increased time back to the string format
    increased_time = increased_time.strftime('%H:%M')
    return increased_time

def my_timetable():
    my_timetable = {
        '07:00-08:15': 'lecture time',
        '08:16-08:24': 'break',
        '08:25-09:40': 'lecture time',
        '09:41-09:49': 'break',
        f'09:50-{items_dict["dhuhr"]}': 'Side work',
        f'{items_dict["dhuhr"]}-{ti(items_dict["dhuhr"], 30)}': 'break',
        f'{ti(items_dict["dhuhr"], 30)}-{ti(items_dict["dhuhr"], 110)}': 'lecture time',
        f'{ti(items_dict["dhuhr"], 110)}-{ti(items_dict["asr"], -20)}': 'Revission',
        f'{ti(items_dict["asr"], -20)}-{ti(items_dict["asr"], 30)}': 'break',
        f'{ti(items_dict["asr"], 30)}-{items_dict["maghrib"]}': 'lecture time',
        f'{items_dict["maghrib"]}-{ti(items_dict["maghrib"], 20)}': 'break',
        f'{ti(items_dict["maghrib"], 20)}-{items_dict["isha"]}': 'lecture time',
        f'{ti(items_dict["isha"], 30)}-{ti(items_dict["isha"], 60)}': 'break',
        f'{ti(items_dict["isha"], 60)}-{ti(items_dict["isha"], 140)}': 'lecture time',
        f'{ti(items_dict["isha"], 140)}-21:40': 'Revission'
    }
    
    return my_timetable



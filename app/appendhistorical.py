from fbaseconnection import firebaseconnection
import pandas as pd
import json

db = firebaseconnection.db
temp_ref = db.reference('weather_data')


with open('month_weather.json', 'r') as f:
    d = json.load(f)
    temp_ref.set(d)

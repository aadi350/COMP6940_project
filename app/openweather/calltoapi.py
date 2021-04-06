import requests
import json
import numpy as np
import pandas as pd
import sys
from ast import literal_eval
from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import credentials, firestore, initialize_app, db
from firebase_admin import db

PORT_OF_SPAIN = '3573890'
APP_ID = '88cc48691dfee3e4171782d8419517f7'
weather_url = f'https://api.openweathermap.org/data/2.5/forecast?id={PORT_OF_SPAIN}&appid={APP_ID}'
'''
    data[list] ->   iterate
        dt
        main -> dictionary
            temp
            feels_like
            temp_min
            temp_max
            pressure
            sea_level
            grnd_level
            humidity
            temp_kf
        weather
        clouds
        wind 
        visibility
        pop
        rain -> dictionary
            3h
        sys
        dt_txt
'''


def clean_from_api(data):
    '''
        Function takes raw API response and outputs average of forecasted values for:
            temp, temp_min, temp_max, pressure, humidity and rain as a dictionary
    '''
    data = data['list']
    data_len = 0
    avg_data = dict({
        'rain': 0,
        'temp': 0,
        'temp_min': 0,
        'temp_max': 0,
        'pressure': 0,
        'humidity': 0
    })


    for day in data:    
        if 'rain' in day.keys():
            avg_data['rain'] = avg_data['rain'] + day['rain']['3h']    
        avg_data['temp'] = avg_data['temp'] + day['main']['temp']
        avg_data['temp_min'] = avg_data['temp_min'] + day['main']['temp_min']
        avg_data['temp_max'] = avg_data['temp_max'] + day['main']['temp_max']
        avg_data['pressure'] = avg_data['pressure'] + day['main']['pressure']
        avg_data['humidity'] = avg_data['humidity'] + day['main']['humidity']
        data_len += 1

    for k,v in avg_data.items():
        avg_data[k] = avg_data[k]/int(data_len)

    return avg_data

def foo(data):
    return data

def transform_data(avg_data):
    transformed = dict()
    TRANFORMS = [np.log, np.exp, foo]
    TRANFORMS_NAMES = ['log', 'exp', 'None']
    for t,n in zip(TRANFORMS, TRANFORMS_NAMES):
        pressure = t(avg_data['pressure'])
        if pressure==np.Inf:
            pressure = sys.float_info.max

        transformed_dict = dict({
            'rain': t(avg_data['rain']),
            'temp': t(avg_data['temp']),
            'temp_min': t(avg_data['temp_min']),
            'temp_max': t(avg_data['temp_max']),
            'pressure': pressure,
            'humidity': t(avg_data['humidity'])
        })
        
        transformed[n] = transformed_dict

    return transformed


def get_data():
    response = requests.get(weather_url).content
    data = literal_eval(response.decode('utf-8'))

    avg_data = clean_from_api(data)
    transformed_data = transform_data(avg_data)
    return transformed_data

cred = credentials.Certificate('crop-jedi-storage-firebase-adminsdk-scef3-882ee18ae0.json')
app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://crop-jedi-storage-default-rtdb.firebaseio.com/'
})

temp_data = get_data()

def post_data(temp_data):
    temp_ref = db.reference('weather_data')
    data = {
        datetime.today().strftime('%Y%m%d'): 
                {
                    'log': {
                        'rain': temp_data['log']['rain'],
                        'temp': temp_data['log']['temp'],
                        'temp_min': temp_data['log']['temp_min'],
                        'temp_max': temp_data['log']['temp_max'],
                        'pressure': temp_data['log']['pressure'],
                        'humidity': temp_data['log']['humidity']
                    },
                    'exp': {
                        'rain': temp_data['exp']['rain'],
                        'temp': temp_data['exp']['temp'],
                        'temp_min': temp_data['exp']['temp_min'],
                        'temp_max': temp_data['exp']['temp_max'],
                        'pressure': temp_data['exp']['pressure'],
                        'humidity': temp_data['exp']['humidity']
                    },
                    'none': {
                        'rain': temp_data['None']['rain'],
                        'temp': temp_data['None']['temp'],
                        'temp_min': temp_data['None']['temp_min'],
                        'temp_max': temp_data['None']['temp_max'],
                        'pressure': temp_data['None']['pressure'],
                        'humidity': temp_data['None']['humidity']
                    }
                }
            
            }

    temp_ref.set(data)


if __name__ == '__main__':
    temp_data = get_data()
    post_data(temp_data)
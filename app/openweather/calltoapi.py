import requests
import json
import numpy as np
import sys
from ast import literal_eval
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import credentials, initialize_app, db
from firebase_admin import db
import pickle


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

    scalers = load_scalers()
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
    '''
        Function takes raw data from API and computes mean of all weather parameters,
        multiple transformations are then done in order to scale the params 
        as determined during model building
    '''
    transformed = dict()
    TRANFORMS = [np.log, np.exp, foo]
    TRANFORMS_NAMES = ['log', 'exp', 'None']

    for t,n in zip(TRANFORMS, TRANFORMS_NAMES):
        pressure = t(avg_data['pressure'])

        if pressure==np.Inf:
            pressure = sys.float_info.max
        transformed_dict = dict({
            'rain_mean': t(avg_data['rain']),
            'temp_mean': t(avg_data['temp']),
            'temp_min': t(avg_data['temp_min']),
            'temp_max': t(avg_data['temp_max']),
            'pressure_mean': pressure,
            'humidity_mean': t(avg_data['humidity'])
        })
        


        transformed[n] = transformed_dict

    return transformed


def get_data():
    response = requests.get(weather_url).content
    data = literal_eval(response.decode('utf-8'))
    scalers = load_scalers()

    avg_data = clean_from_api(data)
    transformed_data = transform_data(avg_data)
    return transformed_data


def post_data(temp_data):
    '''
        Function first gets the database reference from Firebase corresponding
        to today's month and year, the weather parameters are posted to the database by
        means of the set functions for each given parameter. This script is meant to be run daily 
        in order to keep the weather parameters updated.

        # TODO: Possible update is to first pull the current mean value and use a 
        running average to update the values on Firebase
    '''
    temp_ref = db.reference('weather_data')
    cur_year = int(datetime.today().strftime('%Y'))
    cur_month = int(datetime.today().strftime('%m'))

    rain_mean_ref = db.reference(f'/weather_data/rain_mean/({cur_month}, {cur_year})')
    rain_mean_ref.set(temp_data['None']['rain_mean'])

    temp_max_ref = db.reference(f'/weather_data/temp_max/({cur_month}, {cur_year})')
    temp_max_ref.set(temp_data['None']['temp_max'])

    pressure_mean_ref = db.reference(f'/weather_data/pressure_mean/({cur_month}, {cur_year})')
    pressure_mean_ref.set(temp_data['None']['pressure_mean'])

    temp_min_ref = db.reference(f'/weather_data/temp_min/({cur_month}, {cur_year})')
    temp_min_ref.set(temp_data['None']['temp_min'])


    temp_min_ref = db.reference(f'/weather_data/temp_min_raw/({cur_month}, {cur_year})')
    temp_min_ref.set(temp_data['None']['temp_min'])

    return None


if __name__ == '__main__':
    cred = credentials.Certificate('crop-jedi-storage-firebase-adminsdk-scef3-882ee18ae0.json')
    app = firebase_admin.initialize_app(cred, { 'databaseURL': 'https://crop-jedi-storage-default-rtdb.firebaseio.com/'})
    temp_data = get_data()
    post_data(temp_data)
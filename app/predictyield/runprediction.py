import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import credentials, firestore, initialize_app, db
from flask import Flask, request, jsonify
import numpy as np
from modelparams import pymc3_params, lr_params, ridge_params

from datetime import date

cred = credentials.Certificate('../private/HIDDEN.json')
app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://crop-jedi-storage-default-rtdb.firebaseio.com/'
})

class OrganiseData:
    def __init__(self,):
        pass

    def filter_weather(self, weather_data):
        weather_filtered = dict()
        weather_keys = ['humidity_mean', 'humidity_var', 'pressure_mean', 'pressure_var', 'rain_mean', 'rain_var', 'temp', 'temp_max', 'temp_min']
        for weather_key in weather_keys:    
            month_current = int(date.today().strftime('%m'))
            year_current = int(date.today().strftime('%Y'))
            temp_key_data = weather_data[0][weather_key]
            # To Store retrieved data
            temp_list = []
            for temp_data in temp_key_data.items():
                ## Gets most recent year        
                if int(temp_data[0][-6:-1])>= year_current-3:
                    temp_list.append(temp_data[1])

            weather_filtered[weather_key] = temp_list

        return weather_filtered, weather_keys

    def get_weather(self):
        weather_ref = db.reference('weather_data')
        weather_data = weather_ref.get(weather_ref)
        return weather_data



class RunPrediction:
    def __init__(self):
        self.model_params = None 

    def predict_feasibility(self, weather_data):        
        print(self.predict_crop_feasibility(weather_data, pymc3_params))

    def select_model(self, model_params):
        self.model_params = model_params

    def predict_crop_feasibility(self, weather_data, model_params):
        if self.model_params is None:
            logging.warning("pymc3_params selected as default")
            self.model_params = pymc3_params
        potato_data = self._choose_crop(weather_data, crop='POTATO')
        citrus_data = self._choose_crop(weather_data, crop='CITRUS')
        peas_data = self._choose_crop(weather_data, crop='PEAS')
        
        potato = self._predict_crop_feasibility(potato_data, self.model_params['POTATO'])
        citrus = self._predict_crop_feasibility(citrus_data, self.model_params['CITRUS'])
        peas = self._predict_crop_feasibility(peas_data, self.model_params['PEAS'])

        divisor = max([potato, citrus, peas])
        potato /= divisor
        citrus /= divisor
        peas /= divisor

        return potato, citrus, peas


    def _predict_crop_feasibility(self, crop, model_params):
        crop_data, crop_keys = crop[0], crop[1]
        res = 0.0

        for crop_key in crop_keys:
            res += crop_data[crop_key] * model_params[crop_key]

        res+= model_params['intercept']
        return res

    def _choose_crop(self, weather_data, crop):
        data = dict()
        potato_keys = ['pressure_mean', 'temp_max']
        citrus_keys = ['rain_mean', 'pressure_mean', 'rain_var']
        peas_keys = ['temp_min', 'temp_max']

        if crop == 'POTATO':           
            data['pressure_mean'] = np.exp(np.mean(weather_filtered['pressure_mean']))
            data['temp_max'] = np.exp(np.mean(weather_filtered['temp_max']))

        if crop == 'CITRUS':
            data['rain_mean'] = rain_mean = np.exp(np.mean(weather_filtered['rain_mean']))
            data['pressure_mean'] = np.mean(weather_filtered['pressure_mean'])
            data['rain_var'] = np.mean(weather_filtered['rain_var'])

        if crop == 'PIGEON_PEA':            
            data['temp_min'] = np.exp(np.mean(weather_filtered['temp_min']))
            data['temp_min_raw'] = np.mean(weather_filtered['temp_min'])
            data['temp_max'] = np.mean(weather_filtered['temp_max'])

        return data, data.keys()

organisedata = OrganiseData()
weather_data = organisedata.get_weather()
weather_filtered, weather_keys = organisedata.filter_weather(weather_data)

runprediction = RunPrediction()
runprediction.predict_feasibility(weather_filtered)
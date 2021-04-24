import pandas as pd
import json
from predictyield.runprediction import OrganiseData, RunPrediction

def get_data():
    organisedata = OrganiseData()
    weather_data = organisedata.get_weather()
    weather_filtered, weather_keys = organisedata.filter_weather(weather_data)
    forecast = pd.DataFrame.from_dict(weather_filtered)
    forecast = forecast.to_json(orient="split")
    return(forecast)

def get_prediction():
    organisedata = OrganiseData()
    weather_data = organisedata.get_weather()
    weather_filtered, weather_keys = organisedata.filter_weather(weather_data)
    runprediction = RunPrediction()
    scaled_df = runprediction.forecast_prediction(weather_filtered, weather_keys)
    scaled_df = scaled_df.drop(weather_keys, axis=1)
    prediction = scaled_df.to_json(orient="split")
    return scaled_df

def filter_prediction(crop, model, prediction):
    columns = []
    if crop == '':
        columns = columns + ['3 months potato', '6 months potato', '3 months citrus', '6 months citrus', '3 months peas', '6 months peas']
        if model == '':
            columns =  columns + ['potato_pymc3', 'potato_lr', 'potato_ridge', 'citrus_pymc3', 'citrus_lr', 'citrus_ridge', 'peas_pymc3', 'peas_lr', 'peas_ridge']
        elif model == 'pymc3':
            columns =  columns + ['potato_pymc3', 'citrus_pymc3', 'peas_pymc3']
        elif model == model == 'lr':
            columns =  columns + ['potato_lr', 'citrus_lr', 'peas_lr']
        elif model == 'ridge':
            columns =  columns + ['potato_ridge', 'citrus_ridge', 'peas_ridge']

    elif crop == 'potato':
        columns = columns + ['3 months potato', '6 months potato']
        if model == '':
            columns =  columns + ['potato_pymc3', 'potato_lr', 'potato_ridge']
        elif model == 'pymc3':
            columns =  columns + ['potato_pymc3']
        elif model == model == 'lr':
            columns =  columns + ['potato_lr']
        elif model == 'ridge':
            columns =  columns + ['potato_ridge']

    elif crop == 'citrus':
        columns = columns + ['3 months citrus', '6 months citrus']
        if model == '':
            columns =  columns + ['citrus_pymc3', 'citrus_lr', 'citrus_ridge']
        elif model == 'pymc3':
            columns =  columns + ['citrus_pymc3']
        elif model == model == 'lr':
            columns =  columns + ['citrus_lr']
        elif model == 'ridge':
            columns =  columns + ['citrus_ridge']

    elif crop == 'peas':
        columns = columns + ['3 months peas', '6 months peas']
        if model == '':
            columns =  columns + ['peas_pymc3', 'peas_lr', 'peas_ridge']
        elif model == 'pymc3':
            columns =  columns + ['peas_pymc3']
        elif model == model == 'lr':
            columns =  columns + ['peas_lr']
        elif model == 'ridge':
            columns =  columns + ['peas_ridge']

    prediction = pd.DataFrame(prediction[columns], columns = columns)
    prediction = prediction.to_json(orient="split")
    return prediction    
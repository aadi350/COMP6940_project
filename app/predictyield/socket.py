import pandas as pd
from predictyield.runprediction import OrganiseData, RunPrediction

def get_data():
    organisedata = OrganiseData()
    weather_data = organisedata.get_weather()
    weather_filtered, weather_keys = organisedata.filter_weather(weather_data)
    return(weather_filtered, weather_keys)

def get_prediction():
    runprediction = RunPrediction()
    scaled_df = runprediction.forecast_prediction(weather_filtered, weather_keys)
    return scaled_df
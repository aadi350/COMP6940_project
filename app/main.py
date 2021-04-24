import firebase_admin
from flask import Flask, render_template, request, redirect
from fbaseconnection import firebaseconnection
from firebase_admin import db
import logging
import pandas as pd
from predictyield.socket import get_data, get_prediction, filter_prediction

app = Flask(__name__)

@app.route('/main/forecast')
def getForecast():
    forecast = get_data()
    return forecast

@app.route('/main/prediction', methods=['POST'])
def getPredictionData():
    params = request.json
    prediction = get_prediction()
    filtered_prediction = filter_prediction(params['crop'], params['model'], prediction)
    return(filtered_prediction)

if __name__ == '__main__':
    app.run()

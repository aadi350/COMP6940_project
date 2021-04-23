import firebase_admin
from flask import Flask, render_template, request, redirect
from fbaseconnection import firebaseconnection
from firebase_admin import db
import logging
from flask_socketio import SocketIO, emit
from predictyield.socket import get_data, get_prediction

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=['http://localhost:5000/', 'http://localhost:3000/'])


@app.route('/')
def hello():
#   temp_ref = db.reference('test')
#   temp_ref.set(data)
    # weather_filtered, weather_keys = get_data()
    # print(weather_filtered)
    # print('----------------------------------------------------------------')
    # print(weather_keys)
    return render_template('home.html')

@app.route('/home')
def test():
#   temp_ref = db.reference('test')
#   temp_ref.set(data)
    # return render_template('home.html')
    return {"message":"Working"}


@app.route('/form')
def dropdown():
    logging.warning('test')
    return render_template('form.html')


# Dummy function to submit to firebase
@app.route('/submitvalue', methods=['POST'])
def submitvalue():
    val = request.form.get('CropType')
    temp_ref = db.reference('test')
    data = {'test': {'name' : val}}
    temp_ref.set(data)
    return redirect('/') 


################Socket Paths######################
@socketio.on('test')
def test(msg):
    return ("yo")


if __name__ == '__main__':
    socketio.run(app)

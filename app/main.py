import firebase_admin
from flask import Flask, render_template, request, redirect
from fbaseconnection import firebaseconnection
from firebase_admin import db
import logging

app = Flask(__name__)


@app.route('/')
def hello():
#   temp_ref = db.reference('test')
#   temp_ref.set(data)
    return render_template('home.html')


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

if __name__ == '__main__':
    app.run(debug=True)

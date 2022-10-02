from ctypes import resize
from time import sleep
from flask import Flask, request, jsonify, render_template, redirect, flash, url_for
import numpy as np
from tensorflow import keras
import os
import sqlite3
from PIL import Image

# Work flow: Load model from storage -> use model to predict -> return results
# 3 types: damage detection (happen or not), damage classification (flood, fire, etc.), damage evaluation (minor or major damage)
app = Flask(__name__, static_url_path='/static')
model_classification = keras.models.load_model("models/damage-classification-model-real.h5")
model_detection = keras.models.load_model("models/damage-detection-model-real.h5")

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/getData')
def getAllData():
    conn = get_db_connection()
    mapData = conn.execute('SELECT * FROM mapData').fetchall()
    conn.close()
    print(mapData)
    print(type(mapData))
    # return render_template('index.html', posts=posts)
    return render_template('index.html', mapData = mapData)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        lon = request.form['lon']
        lat = request.form['lat']
        damageType = request.form['damageType']
        # minorMajor = request.form['minorMajor']

        if not lon:
            flash('Longitude is required!')
        elif not lat:
            flash('Latitude is required!')
        elif not damageType:
            flash('Damage Type is required!')
        # elif not minorMajor:
        #     flash('Damage extend is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO mapData (lon, lat, damageType, minorMajor) VALUES (?, ?, ?, ?)',
                         (lon, lat, damageType))
            conn.commit()
            conn.close()
            return redirect(url_for('getAllData'))

def classification(img):
    damage_types = np.array(sorted(['volcano', 'flooding', 'earthquake', 'fire', 'wind', 'tsunami']))
    # Load model here
    
    # Predict and return results:
    print(img.shape)
    image = np.zeros((1, 1024, 1024, 3), dtype=np.uint8)
    image[0] = img
    prediction = model_classification.predict(image).tolist()[0]
    print(prediction)
    return {damage_types[i]: prediction[i] for i in range(len(damage_types))}

def detection(img):
    arr = np.array(sorted(['disaster detected', 'no disaster detected']))
    # Load model
    
    print(img.shape)
    image = np.zeros((1, 1024, 1024, 3), dtype=np.uint8)
    image[0] = img
    prediction = model_detection.predict(image).tolist()[0]
    print(prediction)
    return {arr[i]: prediction[i] for i in range(len(arr))}



@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    
    if (request.method == 'POST'):
        if os.path.isfile('./static/files/image_1.png'):
            os.remove("./static/files/image_1.png")
        input_file = request.files["image-input"]
        if input_file.filename != '':
            input_file.save("./static/files/image_1.png")
        # import json
        image=Image.open("./static/files/image_1.png")
        resized_img = image.resize((1024,1024))
        img = np.asarray(resized_img)
        classification_data = (classification(img))
        print(classification(img))
        detection_data = detection(img)
        print(detection_data)
        # getAllData()
        return render_template("index.html",classify=(classification_data),detect=detection_data)
    else:
        # getAllData()
        return render_template("index.html")


@app.route('/map', methods=['GET', 'POST'])
@app.route('/map.html', methods=['GET', 'POST'])
def map():
    return render_template("m_2.html")

@app.route('/landing.html')
@app.route('/landing')
def landing():
    return render_template("landing.html")

if __name__ == "__main__":
    app.run(debug=True)

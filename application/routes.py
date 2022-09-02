import os
from flask import render_template, redirect, flash, request
from application import app
from application.utils import *
import pandas as pd


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if not 'file' in request.files:
            flash('No file part in request')
            return redirect(request.url)

        files = request.files.getlist('file')
        for file in files:
            if file.filename == '':
                flash('No file uploaded')
                return redirect(request.url)
            if file_valid(file.filename):
                filename = "overriden.jpg"
                file.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))
            else:
                flash('Invalid file type')
                return redirect(request.url)
        # flash('We have recived your submission . And will contact you after few Days.')
        result = predictor()
        result[0] = fruit_dict[str(result[0])]
        return render_template('predict.html', prediction_text=result)

    else:
        return render_template('home.html')

@app.route('/detection', methods=['GET', 'POST'])
def detection():
    if request.method == "POST":
        list_names = attendance()
        length = len(list_names[0])
        flash('Attendance Recorded')
        return render_template('detection_result.html',list_names=list_names,length=length)
    return render_template('detection.html')

@app.route('/monitoring', methods=['GET', 'POST'])
def monitoring():
    df = pd.read_csv('Student_sih.csv')
    print(list(df['Name']))
    return render_template('monitoring.html',labels=list(df['Name']),values=list(df.BMI))
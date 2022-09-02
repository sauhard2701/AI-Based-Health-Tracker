import csv
import pandas as pd
import numpy as np
import cv2
from application.attendance.detection import detection
from application.calculations.calorie_calc import getCalorie, getVolume
from application.calculations.create_feature import readFeatureImg
from application.calculations.testing import testing



ALLOWED_EXTENSIONS = ['jpg']
UPLOADS_FOLDER = 'application/uploads/'
fruit_dict = {
  '1.0': "Apple",
  '2.0': "Banana",
  '3.0': "Beans",
  '4.0': "Carrot",
  '5.0': "Cheese",
  '6.0': "Orange",
  '7.0': "Onion",
  '8.0': "Pasta",
  '9.0': "Tomato",
  '10.0': "Cucumber",
  '11.0': "Sauce",
  '12.0': "kiwi",
  '13.0': "Capsicum",
  '14.0': "Watermelon",
}

def file_valid(file):
  return '.' in file and \
    file.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def predictor():
    obj = testing()
    result = obj.run()
    return result
  
def attendance():
    obj = detection()
    obj.run()
    df = pd.read_csv('Attendance.csv')
    return [list(df.Name),list(df.Time)]


    
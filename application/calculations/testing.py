import csv
import numpy as np
import cv2
import os
from application.calculations.calorie_calc import getCalorie, getVolume
from application.calculations.create_feature import readFeatureImg


class testing():
    def __init__(self):
        self.svm_model = cv2.ml.SVM_load("svm_data.dat")
        self.feature_mat = []
        self.pix_cm = 0
        self.fruit_contours = []
        self.fruit_areas = 0.0
        self.fruit_volumes = 0.0
        self.fruit_mass = 0.0
        self.fruit_calories = 0
        self.skin_areas = 0.0
        self.fruit_calories_100grams = 0
        self.img_path = "application/uploads/overriden.jpg"
        
        
    def get_features(self):
        self.feature_mat, self.fruit_areas, self.skin_areas, self.fruit_contours, self.pix_cm = readFeatureImg(self.img_path)
        self.testData = np.float32(self.feature_mat).reshape(-1, 94)

    def calories(self):
        self.result = self.svm_model.predict(self.testData)[1]

        # calculate calories
        self.fruit_volumes = getVolume(self.result[0], self.fruit_areas,
                            self.skin_areas, self.pix_cm, self.fruit_contours)
        self.fruit_mass, self.fruit_calories, self.fruit_calories_100grams = getCalorie(self.result[0], self.fruit_volumes)

    def run(self):
        self.get_features()
        self.calories()
        if (self.fruit_volumes == None):
            data = [str(self.result[0][0]), "None", "None", "None", str(self.fruit_calories_100grams)]
        else:
            data = [str(self.result[0][0]), str(self.fruit_volumes),str(self.fruit_mass), str(self.fruit_calories),str(self.fruit_calories_100grams)]
        return data 


    
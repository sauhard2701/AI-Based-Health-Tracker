import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import csv
# from PIL import ImageGrab



class detection():
    def __init__(self):
        self.nameList = []
        path = 'application/uploads/images/ImagesAttendance'
        images = []
        self.classNames = []
        myList = os.listdir(path)
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])
        self.encodeListKnown = self.findEncodings(images)

    def findEncodings(self,images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList
    
    def markAttendance(self,name):
        with open('Attendance.csv','a+') as f:
            if name not in self.nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')

    def run(self):
        cap = cv2.VideoCapture(0)
 
        while(cap.isOpened()):
            success, img = cap.read()
            imgS = cv2.resize(img,(0,0),None,0.25,0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
            for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
                matches = face_recognition.compare_faces(self.encodeListKnown,encodeFace)
                faceDis = face_recognition.face_distance(self.encodeListKnown,encodeFace)
                matchIndex = np.argmin(faceDis)
                if faceDis[matchIndex]< 0.50:
                    name = self.classNames[matchIndex].upper()
                    if name not in self.nameList:
                        self.markAttendance(name)
                        self.nameList.append(name)
                else: 
                    name = 'Unknown'
                    #print(name)
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            cv2.imshow('Webcam',img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


from sklearn.neighbors import KNeighborsClassifier

import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))  # Create an speech object
    speak.Speak(str1)                   # Speaks the string str1
# Open the default camera (usually the built-in camera)
cap = cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

#to load the names.pkl and faces.pkl file in the knn classifier
with open ('data/names.pkl','rb') as f:
        LABLES=pickle.load(f)
#Load the faces.pkl file
with open ('data/faces_data.pkl','rb') as f:
        FACES=pickle.load(f)

knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES,LABLES)
#add canvas to the camera
imgBackground=cv2.imread("background.png")
#insert data in cvs file as 
COL_Name =['Name', 'Date']

print("Model Loaded")
attendance_taken=False
attendance_recorded=False
while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    #convert the xml file to BGR2RGBa
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #detection of faces
    faces=facedetect.detectMultiScale(gray,1.3 ,5)
    for(x,y,w,h) in faces:
        #croping the face  and adding it to our dataset
        crop_img=frame[y:y+h, x:x+w, :]
        #resize the crop image and reshape to pass it tp ml in single vector
        resized_img=cv2.resize(crop_img,(50,50)).flatten().reshape(1,-1)
        #predict the label of the face using kNN algorithm
        output=knn.predict(resized_img)
        #instance for time and datetime
        ts=time.time()
        date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp=datetime.fromtimestamp(ts).strftime("%H-%M-%S")
        exist=os.path.isfile("Attendance/Attendance_" + date +".csv")
        #insert a rectangle
        cv2.rectangle(frame,(x,y),(x+w,y+h),((0,0,255)),1)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
        cv2.rectangle(frame, (x,y-30),(x+w,y),(50,50,255),-1)
        #put text to display the  name of the person
        cv2.putText(frame,str(output[0]),(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,50),1)
        #draw rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        attendance=[str(output[0])+" "+date+" "+timestamp]
    #insert the background frame
    imgBackground[150:150 +480, 48:48 +640]=frame
    # Display the frame
    cv2.imshow('Camera', imgBackground)
    # Wait for a key press and close the window if 'q' is pressed
    k=cv2.waitKey(1)
    if k== ord('o') and not attendance_taken and not attendance_recorded:
        speak("Attendance taken..")
        time.sleep(5)
        attendance_taken=True
        
        if exist:
            with open("Attendance/Attendance_" +  date + ".csv", "a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(attendance)
                csvfile.close()
        else:
            with open(r"Attendance\Attendance_" + date + ".csv","w+")as csvFile:
                writer=csv.writer(csvFile)
                writer.writerow(COL_Name)
                writer.writerow(attendance)
                csvFile.close()
    elif k== ord('o') and attendance_taken and not attendance_recorded:
        speak("Attendance has already been taken.")
    #if k== ord('o') and not attendance_taken :
     #   speak("Attendance Taken..")
      #  time.sleep(5)
       # if attendance_taken:speak("Attendance has already been taken.")
            #with open("Attendance/Attendance_" + date + ".csv","+a") as csvfile:
             #   writer=csv.writer(csvfile)
              #  writer.writerow(attendance)
               # csvfile.close()
        #attendance_taken =True
        # if exist:
        #     with open("Attendance/Attendance_" + date + ".csv","+a") as csvfile:
        #         writer=csv.writer(csvfile)
        #         writer.writerow(COL_Name)
        #         writer.writerow(attendance)
        #         csvfile.close()
    if k== ord('q'):
        break
# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()


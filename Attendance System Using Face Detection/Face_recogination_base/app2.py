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
COL_Name =['Name','Time','First_in', 'Last_out']

print("Model Loaded")
attendance_taken=False
attendance_recorded=False
first_in = None
last_out = None
face_attendance = {}
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
        exist=os.path.isfile("Attendance/Attendance2_" + date +".csv")
        #insert a rectangle
        cv2.rectangle(frame,(x,y),(x+w,y+h),((0,0,255)),1)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
        cv2.rectangle(frame, (x,y-30),(x+w,y),(50,50,255),-1)
        #put text to display the  name of the person
        cv2.putText(frame,str(output[0]),(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,50),1)
        #draw rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        attendance=[str(output[0])+" "+date+" "+timestamp]
        if exist:
            with open("Attendance/Attendance2_" +  date + ".csv", "r") as csvfile:
                reader=csv.reader(csvfile)
                existing_attendance = list(reader)
                csvfile.close()
            for row in existing_attendance:
                if row and row[0] == output[0]:
                    if first_in is None:
                        first_in = timestamp
                    last_out = timestamp
                    if output[0] in face_attendance:
                        face_attendance[output[0]][1] =last_out
                    else:
                        face_attendance[output[0]] = [first_in, last_out]
                    break
            else:
                with open("Attendance/Attendance2_" +  date + ".csv", "a") as csvfile:
                    writer=csv.writer(csvfile)
                    writer.writerow(attendance)
                    if first_in is None:
                        first_in = timestamp
                        face_attendance[output[0]] = [first_in, None]
                    else:
                        last_out = timestamp
                        face_attendance[output[0]] = [first_in, last_out]
                    csvfile.close()
        else:
            with open(r"Attendance/Attendance2_" + date + ".csv","w+")as csvFile:
                writer=csv.writer(csvFile)
                writer.writerow(COL_Name)
                writer.writerow(attendance)
                if first_in is None:
                    first_in = timestamp
                    face_attendance[output[0]] = [first_in, None]
                else:
                    last_out = timestamp
                    face_attendance[output[0]].append(last_out)
                csvFile.close()
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
    elif k== ord('o') and attendance_taken and not attendance_recorded:
        speak("Attendance has already been taken.")
    if k== ord('q'):
        break
# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()


with open("Attendance/Attendance2_" + date + ".csv", "w+") as csvfile:
    writer = csv.writer(csvfile)
    for name, attendance in face_attendance.items():
        if attendance[1] is not None:
            first_out_row = [name + " " + date + " " + attendance[0]]
            last_in_row = [name + " " + date + " " + attendance[1]]
            writer.writerow(first_out_row)
            writer.writerow(last_in_row)
        else:
            first_out_row = [name + " " + date + " " + attendance[0]]
            writer.writerow(first_out_row)
    csvfile.close()
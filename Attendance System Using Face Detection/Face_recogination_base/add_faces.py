import cv2
import pickle
import numpy as np
import os
# Open the default camera (usually the built-in camera)
cap = cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

faces_data=[]
i=0
#To get the user name.
name=input("Enter your name: ")
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
        #resize the crop image
        resized_img=cv2.resize(crop_img,(50,50))
        #condition if the image is not present in the dataset
        if len(faces_data)<=100 and i%10==0:
            faces_data.append(resized_img)
            #print("Added")
        i=i+1
        #to find the face detect with  the webcam
        cv2.putText(frame,str(len(faces_data)),(50,50),cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 5)
        #draw rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # Display the frame
    cv2.imshow('Camera', frame)
    # Wait for a key press and close the window if 'q' is pressed
    k=cv2.waitKey(1)
    if k== ord('q') or len(faces_data)==100:
        break
# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
#save the data into pickle format
#its for names.pickle file
#convert the data into numpy array
faces_data=np.asarray(faces_data)
faces_data=faces_data.reshape(100, -1)
#create a pickle file if not present 
if 'names.pkl' not in os.listdir('data/'):
    names=[name]*100
    #save the names in the pickel file
    with open ('data/names.pkl','wb') as f:
        pickle.dump(names,f)
# to add new user to the pickle file
else:
    with open ('data/names.pkl','rb') as f:
        names=pickle.load(f)
    names=names+[name]*100
    with open ('data/names.pkl','wb') as f:
        pickle.dump(names,f)
#For Face detection into pickle file
if 'faces_data.pkl' not in os.listdir('data/'):
    #save the names in the pickle file
    with open ('data/faces_data.pkl','wb') as f:
        pickle.dump(faces_data,f)
# to add new user face to the pickle file
else:
    with open ('data/faces_data.pkl','rb') as f:
        faces=pickle.load(f)
    faces=np.append(faces, faces_data, axis=0)
    with open ('data/faces_data.pkl','wb') as f:
        pickle.dump(faces,f)

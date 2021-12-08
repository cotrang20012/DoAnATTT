
#%%
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from gtts import gTTS
import os
import playsound
import cv2
import face_recognition
import os
import numpy as np
import threading
import tkinter as tk
from datetime import date, datetime
from tkinter import filedialog
from functools import partial
root = Tk()
frm = ttk.Frame(root,padding=100)
frm.grid()
#%%
UserLst = {"Brad":"123","Emma":"321","Robert":"robert"}

def validateLogin(username, password):
	
    try:
        if UserLst[username.get()] == password.get():
            messagebox.showinfo("","Welcome " + username.get())
        # pass
        #
    except:
        messagebox.showinfo("","Please try again")
    finally:
        pass

def FacialRecognitionWithWebcam():
    ## duyệt từng hình ảnh có trong thư mục và encode các đặc tính của nó sau đó đưa vào một list để lưu trữ
    path = 'C:\\Users\\khoa9\\Documents\\GitHub\\DoAnATTT\\rieng tu\\HinhAnh'
    listofImg = []
    listofName = []

    
    listofImgInDir = os.listdir(path)

    for img in listofImgInDir: #duyệt từng hình ảnh trong thư mục và lưu lại vào list hình ảnh và tên
        currentImg =  cv2.imread(f'{path}/{img}')
        listofImg.append(currentImg)
        listofName.append(os.path.splitext(img)[0])

    def Encoding(listofImg): #duyệt từng hình ảnh trong list và encode nó 
        listEncode = []
        for img in listofImg:
            imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(imgRGB)[0]
            listEncode.append(encode)
        return listEncode

    listKnowEncode = Encoding(listofImg)
    ##

    #lấy hình ảnh từ webcam
    webcam = cv2.VideoCapture(0)
    while True:
        #đọc khung ảnh hiện tại từ webcam
        place_holder,frame = webcam.read()

        #tạo một bản sao nhỏ của khung hình đang đọc
        frameS = cv2.resize(frame,(0,0),None,0.25,0.25)
        rgb_img = cv2.cvtColor(frameS,cv2.COLOR_BGR2RGB)
        #chuyển tấm hình sang dạng trắng đen
        #grayscaled_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #chuyển bản sao nhỏ sang dạng rgb
        
        #rgb_img1 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        #encode các đặc tính ở khuôn mặt được đưa vào
        frameSCurrentFrame = face_recognition.face_locations(rgb_img)
        encodingCurrentFrame = face_recognition.face_encodings(rgb_img,frameSCurrentFrame)
        
        #so sánh khuôn mặt trong webcam với các khuôn mặt có sẵn
        for encodingCurrent, faceCorCurrent in zip(encodingCurrentFrame,frameSCurrentFrame):
            cv2.rectangle(frame,(faceCorCurrent[3]*4,faceCorCurrent[0]*4),(faceCorCurrent[1]*4,faceCorCurrent[2]*4),(255,0,255),2)
            matches = face_recognition.compare_faces(listKnowEncode,encodingCurrent) #so sánh
            faceDis = face_recognition.face_distance(listKnowEncode,encodingCurrent) #tính toán sự khác biệt giữa bức ảnh đc đưa vào và ảnh trong thư mục
            matchIndex = np.argmin(faceDis)  #phải lấy khuôn mặt có độ lệch nhỏ nhất (gần giống với khuôn mặt trong thư mục nhất)
            if matches[matchIndex]:
                #cv2.destroyAllWindows()
                Name = listofName[matchIndex]
                messagebox.showinfo("","Welcome " + Name)
                # x,y,w,h =  faceCorCurrent
                # x,y,w,h = x*4,y*4,w*4,h*4
                
                # cv2.putText(frame,Name,(h+6,w-6),cv2.FONT_ITALIC,1,(0,255,0),2)                


        #xem hình ảnh
        cv2.imshow('Face Detection',frame)
        key = cv2.waitKey(1) #tạm dừng chương trình
        if key == 27: #nhấn ESC để dừng chương trình
            break
usernameLabel = Label(root, text="User Name").grid(row=0, column=0)
username = StringVar()
usernameEntry = Entry(root, textvariable=username).grid(row=0, column=1)  

#password label and password entry box
passwordLabel = Label(root,text="Password").grid(row=1, column=0)  
password = StringVar()
passwordEntry = Entry(root, textvariable=password, show='*').grid(row=1, column=1)  

# ttk.Button(frm,text="Đăng nhập khác",command= FacialRecognitionWithWebcam).grid(column=0,row =0)
# ttk.Button(frm,text="quit",command=root.destroy).grid(column=1,row =0)
validateLogin = partial(validateLogin, username, password)

#login button
loginButton = Button(root, text="Login", command=validateLogin).grid(row=4, column=0)  
loginButtonFace = Button(root,text="FaceId",command=FacialRecognitionWithWebcam).grid(row=4,column=1)
'''Label(root,text = "Đăng nhập").pack()

def myClick():
    myLabel = Label(root, text = "Hello " + e.get())
    myLabel.pack()
myButton = Button(root, command = myClick)
myButton.pack()
'''

root.mainloop()
# %%

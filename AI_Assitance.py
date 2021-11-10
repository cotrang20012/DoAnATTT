import speech_recognition as sr
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

root = tk.Tk()
root.withdraw()

##
def FacialRecognitionWithWebcam():
    ## duyệt từng hình ảnh có trong thư mục và encode các đặc tính của nó sau đó đưa vào một list để lưu trữ
    path = 'HinhAnh'
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

    #Nạp dữ liệu đã được train sẵn để nhận diện khuôn mặt trực diện (haar cascade algorithm)
    face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #Classifier là một detector, để nhận diện khuôn mặt

    #lấy hình ảnh từ webcam
    webcam = cv2.VideoCapture(0)

    while True:
        #đọc khung ảnh hiện tại từ webcam
        place_holder,frame = webcam.read()

        #tạo một bản sao nhỏ của khung hình đang đọc
        frameS = cv2.resize(frame,(0,0),None,0.25,0.25)

        #chuyển tấm hình sang dạng trắng đen
        grayscaled_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #chuyển bản sao nhỏ sang dạng rgb
        rgb_img = cv2.cvtColor(frameS,cv2.COLOR_BGR2RGB)

        #phát hiện khuôn mặt và mắt
        face_cordianate = face_data.detectMultiScale(grayscaled_img)

        #encode các đặc tính ở khuôn mặt được đưa vào
        frameSCurrentFrame = face_recognition.face_locations(rgb_img)
        encodingCurrentFrame = face_recognition.face_encodings(rgb_img,frameSCurrentFrame)
    
        #vẽ hình chữ nhật xung quanh khuôn mặt
        for (x,y,w,h) in face_cordianate:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            
        #so sánh khuôn mặt trong webcam với các khuôn mặt có sẵn
        for encodingCurrent, faceCorCurrent in zip(encodingCurrentFrame,frameSCurrentFrame):
            matches = face_recognition.compare_faces(listKnowEncode,encodingCurrent) #so sánh
            faceDis = face_recognition.face_distance(listKnowEncode,encodingCurrent) #tính toán sự khác biệt giữa bức ảnh đc đưa vào và ảnh trong thư mục
            matchIndex = np.argmin(faceDis)  #phải lấy khuôn mặt có độ lệch nhỏ nhất (gần giống với khuôn mặt trong thư mục nhất)
            if matches[matchIndex]:
                x,y,w,h =  faceCorCurrent
                x,y,w,h = x*4,y*4,w*4,h*4
                Name = listofName[matchIndex].upper()
                cv2.putText(frame,Name,(h+6,w-6),cv2.FONT_ITALIC,1,(0,255,0),2)
                if(Name != ""):
                    result = "Tên người trong ảnh là "+ Name
                    threading.Thread(speak(result)).start()

        #xem hình ảnh
        cv2.imshow('Face Detection',frame)
        key = cv2.waitKey(1) #tạm dừng chương trình
        if key == 27: #nhấn ESC để dừng chương trình
            break
    cv2.destroyAllWindows()

def FacialRecognitionWithImage(text):
    Name = ''
    ## duyệt từng hình ảnh có trong thư mục và encode các đặc tính của nó sau đó đưa vào một list để lưu trữ
    path = 'HinhAnh'
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

    #Nạp dữ liệu đã được train sẵn để nhận diện khuôn mặt trực diện (haar cascade algorithm)
    face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #Classifier là một detector, để nhận diện khuôn mặt

    #lấy hình ảnh từ webcam
    img = cv2.imread(f"{text}")

    #chuyển tấm hình sang dạng trắng đen
    grayscaled_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #chuyển bản sao nhỏ sang dạng rgb
    rgb_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    #phát hiện khuôn mặt và mắt
    face_cordianate = face_data.detectMultiScale(grayscaled_img)

    #encode các đặc tính ở khuôn mặt được đưa vào
    frameSCurrentFrame = face_recognition.face_locations(rgb_img)
    encodingCurrentFrame = face_recognition.face_encodings(rgb_img,frameSCurrentFrame)
    
    #vẽ hình chữ nhật xung quanh khuôn mặt
    for (x,y,w,h) in face_cordianate:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            
        #so sánh khuôn mặt trong webcam với các khuôn mặt có sẵn
    for encodingCurrent, faceCorCurrent in zip(encodingCurrentFrame,frameSCurrentFrame):
        matches = face_recognition.compare_faces(listKnowEncode,encodingCurrent) #so sánh
        faceDis = face_recognition.face_distance(listKnowEncode,encodingCurrent) #tính toán sự khác biệt giữa bức ảnh đc đưa vào và ảnh trong thư mục
        matchIndex = np.argmin(faceDis)  #phải lấy khuôn mặt có độ lệch nhỏ nhất (gần giống với khuôn mặt trong thư mục nhất)
        if matches[matchIndex]:
            x,y,w,h =  faceCorCurrent
            x,y,w,h = x*4,y*4,w*4,h*4
            Name = listofName[matchIndex].upper()
            cv2.putText(img,Name,(h+6,w-6),cv2.FONT_ITALIC,1,(0,255,0),2)    
      
    return Name
        #xem hình ảnh

def ShowWebcam():
    webcam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    while True:
        place_holder,frame = webcam.read()
        cv2.imshow('webcam',frame)
        key = cv2.waitKey(1) #tạm dừng chương trình
        if key == 27: #nhấn ESC để dừng chương trình
            break
    cv2.destroyAllWindows()
##

r = sr.Recognizer()
def speak(text):
    tts = gTTS(text=text, lang='vi')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

while True:
    with sr.Microphone() as source:
        print("Tinh chỉnh âm thanh nền trong 3 giây")
        r.adjust_for_ambient_noise(source,3)
        print("Thu âm trong 3 giây")
        ThuAm = r.record(source,3)
        try:
            text = r.recognize_google(ThuAm,language='vi')
            print(text)
        except:
            text =""
            
        text = text.lower()
        if text =="":
            AI_Assitant = "Xin lỗi tôi nghe không rõ"
            speak(AI_Assitant)
        elif "xin chào" in text:
            AI_Assitant = "Xin chào"
            speak(AI_Assitant)
        elif "hôm nay là ngày mấy" in text:
            time = datetime.now()
            AI_Assitant = time.strftime("Hôm nay là ngày %d tháng %m năm %y")
            speak(AI_Assitant)
        elif "mấy giờ" in text:
            time = datetime.now()
            AI_Assitant = time.strftime("%H:%M:%S")
            speak(AI_Assitant)
        elif "bật webcam" in text:
            speak("Bật webcam, muốn tắt vui lòng bấm ESC")
            FacialRecognitionWithWebcam()
        elif "mở thư mục" in text:
            speak("Mở thư mục và chọn file hình ảnh muốn nhận diện")
            path = filedialog.askopenfilenames()[0]
            resultName = FacialRecognitionWithImage(path)
            if resultName == "":
                speak("Không nhận diện được người trong ảnh hoặc người trong ảnh không có trong tập dữ liệu")
            else:
                result = "Tên người trong ảnh là "+ resultName
                speak(result)
        elif "nhận diện khuôn mặt qua hình ảnh" in text:
            AI_Assitant = "Hãy nhập tên hình ảnh và đảm bảo hình ảnh có trong thư mục"
            speak(AI_Assitant)  
            text = input("Tên hình ảnh: ")        #ex: RDJ.jpg
            resultName = FacialRecognitionWithImage(text)
            if resultName == "":
                speak("Không nhận diện được người trong ảnh hoặc người trong ảnh không có trong tập dữ liệu")
            else:
                result = "Tên người trong ảnh là "+ resultName
                speak(result)
        else:
            AI_Assitant ="Bạn vui lòng nói lại"
            speak(AI_Assitant)
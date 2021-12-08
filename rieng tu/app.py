import face_recognition

from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
# Import kivy UX components
from kivy.uix.image import AsyncImage, Image
from kivymd.uix.button import MDRaisedButton
#from kivy.uix.image import Image
# Import other kivy stuff
from kivy.graphics.texture import Texture
# Import other dependencies
import cv2
import os
import numpy as np

def FacialRecognitionWithWebcam(frame):
    ## duyệt từng hình ảnh có trong thư mục và encode các đặc tính của nó sau đó đưa vào một list để lưu trữ
    path = 'assets'
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
    

  
    frameS = cv2.resize(frame,(0,0),None,0.25,0.25)
    rgb_img = cv2.cvtColor(frameS,cv2.COLOR_BGR2RGB)
       
    frameSCurrentFrame = face_recognition.face_locations(rgb_img)
    encodingCurrentFrame = face_recognition.face_encodings(rgb_img,frameSCurrentFrame)
        
        #so sánh khuôn mặt trong webcam với các khuôn mặt có sẵn
    for encodingCurrent, faceCorCurrent in zip(encodingCurrentFrame,frameSCurrentFrame):
        cv2.rectangle(frame,(faceCorCurrent[3]*4,faceCorCurrent[0]*4),(faceCorCurrent[1]*4,faceCorCurrent[2]*4),(255,0,255),2)
        matches = face_recognition.compare_faces(listKnowEncode,encodingCurrent) #so sánh
        faceDis = face_recognition.face_distance(listKnowEncode,encodingCurrent) #tính toán sự khác biệt giữa bức ảnh đc đưa vào và ảnh trong thư mục
        matchIndex = np.argmin(faceDis)  #phải lấy khuôn mặt có độ lệch nhỏ nhất (gần giống với khuôn mặt trong thư mục nhất)
        if matches[matchIndex]:
            x,y,w,h =  faceCorCurrent
            x,y,w,h = x*4,y*4,w*4,h*4
            Name = listofName[matchIndex].upper()
            cv2.putText(frame,Name,(h+6,w-6),cv2.FONT_ITALIC,1,(0,255,0),2)                

    return frame
        #xem hình ảnh
       # cv2.imshow('Face Detection',frame)
        

class TheLabApp(MDApp):

    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        self.image = Image()
        layout.add_widget(self.image)
        self.captureBtn = MDRaisedButton(
            text="Capture",
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(None, None))
        self.captureBtn.bind(on_press=self.take_picture)
        layout.add_widget(self.captureBtn)
        self.displayImage = Image()
        layout.add_widget(self.displayImage)
        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.load_video, 1.0/30.0)
        return layout

   
    
    def load_video(self, *args):
        ret, frame = self.capture.read()
        # Frame initialize
        self.image_frame = frame
        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

    def take_picture(self,*args):
        frame = FacialRecognitionWithWebcam(self.image_frame)
        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.displayImage.texture = texture
if __name__ == '__main__':
    TheLabApp().run()
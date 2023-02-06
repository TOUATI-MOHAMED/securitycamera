from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import cv2
import winsound

ui,_=loadUiType('pyqt-security-cam.ui')

class MainApp(QMainWindow,ui):
    volume = 500
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.MONITORING.clicked.connect(self.start_monitoring)
        self.VOLUME.clicked.connect(self.set_volume)
        self.EXIT.clicked.connect(self.close_window) 
        self.VOLUMESLIDER.setVisible(False)
        self.VOLUMESLIDER.valueChanged.connect(self.set_volume_level)

    def start_monitoring(self):
        print("Start monitoring button clicked")
        webcam = cv2.VideoCapture(0)
        while True:
            _,im1 = webcam.read()
            _,im2 = webcam.read()
            diff = cv2.absdiff(im1,im2)
            gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),0)
            _,thresh = cv2.threshold(blur, 20,255,cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh,None,iterations=3)
            countours,_=cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for c in countours:
                if cv2.contourArea(c) <5000:
                    continue
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(im1,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.imwrite('captured.jpg',im1)
                image = QImage('captured.jpg')
                pm = QPixmap.fromImage(image)
                self.CAMWINDOW.setPixmap(pm)
                winsound.Beep(self.volume,100)
            cv2.imshow("Opencv-Security-Camera",im1)
            
            key = cv2.waitKey(10)
            if key == 27:
                break
        webcam.release() 
        cv2.destroyAllWindows()   

    def set_volume(self):
        self.VOLUMESLIDER.setVisible(True)
        print("Set volume button clicked")

    def close_window(self):
        self.close()

    def set_volume_level(self):
        self.VOLUMELEVEL.setText(str(self.VOLUMESLIDER.value()//10))
        self.volume = self.VOLUMESLIDER.value() * 10
        cv2.waitKey(1000)
        self.VOLUMESLIDER.setVisible(False)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()    


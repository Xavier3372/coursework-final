from ctypes import alignment
from re import A
import sys
import random
from textwrap import wrap
from tkinter import W
from PySide6 import QtCore, QtWidgets, QtGui
from cv2 import QRCodeDetector
from matplotlib.widgets import Widget
from autocorrect import *


a = 0
translatedText = "futher"

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        global translatedText

        super().__init__()
        self.setWindowTitle("Translator")
        
        self.setGeometry(83,35,1100,700)

        
        self.startbutton = QtWidgets.QPushButton("Start",self)
        self.nextWord = QtWidgets.QPushButton("New Word",self)  
        self.endbutton = QtWidgets.QPushButton("End",self)
        self.scr = QtWidgets.QPushButton("Screen",self)

        self.text = QtWidgets.QLabel(translatedText,self)
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setWordWrap(True)
        self.text.move(70,430)
        self.text.resize(1000,100)


        self.scr.resize(800,450) #placeholder for screen
        self.scr.move(150,0)


        self.endbutton.resize(100,100)
        self.endbutton.move(850,550)


        self.startbutton.resize(100,100)
        self.startbutton.move(150,550)
        '''self.startbutton.setStyleSheet(
            "border-style: outset;"
            "border-radius : 50;" 
            "border-width: 10px;"
            "border-color: red;")'''
        
        self.nextWord.resize(100,100)


       
        
        #self.text = QtWidgets.QLabel(
         #   "Press the button", alignment=QtCore.Qt.AlignCenter) 
        '''self.layout = QtWidgets.QHBoxLayout(self) #
        self.layout.addWidget(self.startbutton)
        self.layout.addWidget(self.endbutton) '''
        self.startbutton.clicked.connect(self.startcamera)
        self.endbutton.clicked.connect(self.endcamera)
        self.nextWord.clicked.connect(self.nextword)

    def updatetext(self):
        global translatedText
        self.text.setText(translatedText)
            

    def camera(self):
        global a 
        print(a)
        if a == 1:
            print("start")
        if a == 2:
            print("stop")
        
    def startcamera(self): # what button does
        global a
        if a != 1:

            print("started")
            a = 1
            self.camera()

    def endcamera(self):
        global a
        if a == 1:
            a = 2
            print("ended")
            self.camera()

    def nextword(self):
        global translatedText
        translatedText = (autoCorrect(translatedText)[0])
        self.updatetext()

    def putwordhere(letter):
        global translatedText
        translatedText += letter



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())

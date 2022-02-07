from ctypes import alignment
from re import A
import sys
from textwrap import wrap
from tkinter import W
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)
from cv2 import QRCodeDetector
from matplotlib.widgets import Widget
from autocorrect import *
import os
import detection as dt

import cv2

a = 0
translatedText = "futher"

model_path = 'model/asl_model'
predicted_char = "nothing"


class Thread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.status = True

    def run(self):
        while self.status:
            frame = dt.detectImg()

            color_frame = cv2.cvtColor(frame[0], cv2.COLOR_BGR2RGB)

            h, w, ch = color_frame.shape
            img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)
            scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)

            self.updateFrame.emit(scaled_img)
        sys.exit(-1)


class Window(QMainWindow):
    def __init__(self):
        global translatedText

        super().__init__()
        self.setWindowTitle("Translator")

        self.setGeometry(83, 35, 1100, 700)
        self.th = Thread(self)
        self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)

        self.startbutton = QPushButton("Start", self)
        self.nextWord = QPushButton("New Word", self)
        self.endbutton = QPushButton("End", self)
        self.scr = QPushButton("Screen", self)

        self.text = QLabel(translatedText, self)
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setWordWrap(True)
        self.text.move(70, 430)
        self.text.resize(1000, 100)

        self.scr.resize(800, 450)  # placeholder for screen
        self.scr.move(150, 0)

        self.endbutton.resize(100, 100)
        self.endbutton.move(850, 550)

        self.endbutton.resize(100, 100)
        self.endbutton.move(850, 550)

        self.startbutton.resize(100, 100)
        self.startbutton.move(150, 550)
        self.startbutton.setStyleSheet(
            "background-image : url(xavier_angy.jpg);")
        '''self.startbutton.setStyleSheet(
            "border-style: outset;"
            "border-radius : 50;" 
            "border-width: 10px;"
            "border-color: red;")'''

        self.nextWord.resize(100, 100)

        # self.text = QtWidgets.QLabel(
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

    def startcamera(self):  # what button does
        global a
        if a != 1:

            print("started")
            a = 1
            self.camera()
            self.th.start()

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
    app = QApplication()
    w = Window()
    w.show()
    sys.exit(app.exec())

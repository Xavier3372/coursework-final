from ctypes import alignment
import sys
import random
from textwrap import wrap
from tkinter import W
from PySide6 import QtCore, QtWidgets, QtGui
from cv2 import QRCodeDetector
from matplotlib.widgets import Widget


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Translator")
        
        self.setGeometry(83,35,1200,700)

        self.translatedText = ""
        self.startbutton = QtWidgets.QPushButton("Start",self) 
        self.endbutton = QtWidgets.QPushButton("End",self)
        self.scr = QtWidgets.QPushButton("Screen",self)
        self.text = QtWidgets.QLabel("text goes here",self)
        self.scr.resize(960,540) #placeholder for screen
        self.scr.move(120,0)
        self.endbutton.resize(100,100)
        self.endbutton.move(950,550)
        self.startbutton.resize(100,100)
        self.startbutton.move(150,550)
        self.text.move(550,550)
        #self.text = QtWidgets.QLabel(
         #   "Press the button", alignment=QtCore.Qt.AlignCenter) 
        '''self.layout = QtWidgets.QHBoxLayout(self) #
        self.layout.addWidget(self.startbutton)
        self.layout.addWidget(self.endbutton) '''

        self.startbutton.clicked.connect(self.startcamera)
        self.endbutton.clicked.connect(self.endcamera)
    
    def updatetext(self,pain):
        
        if pain == "start":
            print("start")
            if pain == "end":
                print("end")    
    def startcamera(self): # what button does
        self.updatetext("start")
    def endcamera(self):
        self.updatetext("end")
    

    
    

        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())

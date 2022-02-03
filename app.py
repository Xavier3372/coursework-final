from ctypes import alignment
import sys
import random
from textwrap import wrap
from tkinter import W
from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Translator")
        self.translatedText = ""
        self.count = 0
        self.startbutton = QtWidgets.QPushButton("Start")
        self.startbutton = QtWidgets.QPushButton("Stop")
        self.text = QtWidgets.QLabel(
            "Press the button", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.addL)

    @QtCore.Slot()
    def addL(self):
        self.count += 1
        self.translatedText = self.translatedText + "L" * self.count
        self.text.setText(self.translatedText)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())

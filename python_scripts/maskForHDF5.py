'''######################################################################
# File Name: maskForHDF5.py
# Project:
# Version:
# Creation Date: 2017/04/11
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import libs.makeHDF5
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QVBoxLayout, QPushButton, QApplication
import sys
import numpy as np


class maskHDF5():
    def __init__(self, frequency, filename, data):
        self._dict = dict()
        unit = 1.0 / frequency
        self.setitem("timestamps_unit", unit)
        self._dict["author_affiliation"] = "Institute for Physical and Theoretical Chemistry, Goethe-University Frankfurt"
        self._dict["detectors"] = "no idea"
        self._filename = filename
        self._data = data
        self.maskWindow()

    def setitem(self, name, text):
        self._dict[name] = text

    def getitem(self, name):
        return self._dict[name]

    def maskWindow(self):
        win = QWidget()

        label1 = QLabel("author")
        label2 = QLabel("institute")
        label3 = QLabel("sample")
        label4 = QLabel("buffer")
        label5 = QLabel("dyes")
        label6 = QLabel("description")

        line1 = QLineEdit()
        line1.setPlaceholderText("Your name")
        line2 = QLineEdit()
        line2.setPlaceholderText("Institute for Physical and Theoretical Chemistry, Goethe-University Frankfurt")
        line3 = QLineEdit()
        line3.setPlaceholderText("Sample name")
        line4 = QLineEdit()
        line4.setPlaceholderText("Buffer name")
        line5 = QLineEdit()
        line5.setPlaceholderText("Dye names, separated by comma")
        line6 = QLineEdit()
        line6.setPlaceholderText("detailed description")

        line1.textChanged.connect(lambda name, text: self.setitem("author", text))
        line2.textChanged.connect(lambda name, text: self.setitem("author_affiliation", text))
        line3.textChanged.connect(lambda name, text: self.setitem("sample_name", text))
        line4.textChanged.connect(lambda name, text: self.setitem("buffer_name", text))
        line5.textChanged.connect(lambda name, text: self.setitem("dye_names", text))
        line6.textChanged.connect(lambda name, text: self.setitem("description", text))

        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.saveFile)

        vbox = QVBoxLayout()
        vbox.addWidget(label1)
        vbox.addWidget(line1)
        vbox.addWidget(label2)
        vbox.addWidget(line2)
        vbox.addWidget(label3)
        vbox.addWidget(line3)
        vbox.addWidget(label4)
        vbox.addWidget(line4)
        vbox.addWidget(label5)
        vbox.addWidget(line5)
        vbox.addWidget(label6)
        vbox.addWidget(line6)
        vbox.addWidget(saveButton)

        # group = QGroupBox()
        # group.setLayout(vbox)

        # box = QVBoxLayout()
        # box.addLayout(group)

        win.setLayout(vbox)
        win.setWindowTitle("hdf5 mask")
        win.show()

    def saveFile(self):
        libs.makeHDF5.makeHDF5(self._dict, self._data, self._filename)

if __name__ == '__main__':
    data = np.zeros([4, 4])
    app = QApplication(sys.argv)
    maskHDF5(100, "test", data)
    app.exec_()
    sys.exit()
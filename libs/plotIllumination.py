'''######################################################################
# File Name: plotIllumination.py
# Project: ALEX
# Version:
# Creation Date: 2017/07/30
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import numpy as np
from matplotlib import pyplot as plt
import libs.dictionary
# from matplotlib.backends.backend_pdf import PdfPages


class plotIllumination():
    def __init__(self):
        self._dict = libs.dictionary.UIsettings()
        self._t = np.arange(0, 101, 1)
        self._green = np.zeros([101])
        self._red = np.zeros([101])

    def refreshSettings(self, dictionary):
        self._dict_a = dictionary

    def plot(self, fname):
        self._greenPercent = self._dict.getitem("laser percentage1")
        print(self._greenPercent)
        self._greenAmp = self._dict.getitem("lpower green")
        self._redAmp = self._dict.getitem("lpower red")

        self._green[1:self._greenPercent + 1] = (self._greenAmp)
        self._red[self._greenPercent + 1:-1] = (self._redAmp)

        plt.plot(self._t, self._green, linestyle='--', drawstyle='steps')
        plt.plot(self._t, self._red, linestyle='--', drawstyle='steps')
        plt.axis([-10, 120, -10, 120])
        plt.xlabel("percentage of illumination")
        plt.ylabel("percentage of laser intensity")
        fname = str(fname + '.png')
        plt.savefig(fname)
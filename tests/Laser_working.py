'''######################################################################
# File Name: rectWave.py
# Project:
# Version:
# Creation Date: 2017/02/09
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import numpy as np
from scipy import signal
from PyDAQmx import *
import libs.dictionary


class GenerateSignal():
    def __init__(self):
        self._sampFreq = 100
        self._t = np.linspace(0, 1, self._sampFreq, endpoint=False)
        self._redP = np.zeros([self._sampFreq, 1])
        self._greenP = np.zeros([self._sampFreq, 1])
        self._sig1 = np.zeros([self._sampFreq, 1])
        self._sig2 = np.zeros([self._sampFreq, 1])
        self._silence = np.zeros([self._sampFreq, 1])
        self._duty = 0.49
        self.read = int32()
        # self.read = ctypes.c_int32()
        self._dict = libs.dictionary.UIsettings()
        self.redAmp = self._dict.getitem("lpower red")
        self.greenAmp = self._dict.getitem("lpower green")
        self._freq = self._dict.getitem("laser frequency")

    def refreshSettings(self, diction):
        self._dict_a = diction

    def calcSignal(self):
        self.silenceAPD()
        phi = np.pi
        self._redP = (self.redAmp / 100.0) * 2.5 * signal.square(2.0 * np.pi * 1.0 * self._t, self._duty) + (self.redAmp / 100.0) * 2.5
        self._greenP = (self.greenAmp / 100.0) * 2.5 * signal.square(2.0 * np.pi * 1.0 * self._t + phi, self._duty) + (self.greenAmp / 100.0) * 2.5
        self._data = np.concatenate((self._redP, self._greenP, self._silence))

    def silenceAPD(self):
        phi = np.pi
        self._sig1 = 2.5 * 1.0 * signal.square(2.0 * np.pi * 1.0 * (self._t + 0.01), 0.009) + 2.5
        self._sig2 = 2.5 * 1.0 * signal.square(2.0 * np.pi * 1.0 * (self._t + 0.01) + phi, 0.009) + 2.5
        self._silence = self._sig1 + self._sig2

    def ALEXLaser(self):

        self.analog_output = Task()
        self.analog_output.CreateAOVoltageChan("Dev1/ao0", " ", -10.0, 10.0, DAQmx_Val_Volts, None)
        self.analog_output.CreateAOVoltageChan("Dev1/ao1", " ", -10.0, 10.0, DAQmx_Val_Volts, None)
        self.analog_output.CreateAOVoltageChan("Dev1/ao2", " ", -10.0, 10.0, DAQmx_Val_Volts, None)

        self.analog_output.CfgSampClkTiming(" ", self._freq * self._sampFreq, DAQmx_Val_Rising, DAQmx_Val_ContSamps, self._sampFreq)
        self.analog_output.CfgDigEdgeStartTrig("/Dev1/ctr0out", DAQmx_Val_Rising)

        self.analog_output.WriteAnalogF64(self._sampFreq, 0, -1, DAQmx_Val_GroupByChannel, self._data, byref(self.read), None)
        self.analog_output.StartTask()

    def startLaser(self):
        print("laser started")
        self.silenceAPD()
        self.calcSignal()
        self.ALEXLaser()

    def stopLaser(self):
        self.analog_output.StopTask()
        self.analog_output.ClearTask()

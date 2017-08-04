'''######################################################################
# File Name: AnalogOutput.py
# Project: ALEX
# Version:
# Creation Date: 2017_07_13
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import numpy as np
import time
from PyDAQmx import *
import libs.dictionary


class GenerateSignal():
    def __init__(self):
        self._sampFreq = 2
        self._dict = libs.dictionary.UIsettings()
        self._freq = self._dict.getitem("laser frequency")
        self._red = np.zeros([2])
        self._green = np.zeros([2])
        self.read = int32()

    def refreshSettings(self, dictionary):
        self._dict._a = dictionary

    def Intensities(self):
        self.redAmp = self._dict._a.getitem("lpower red")
        self.greenAmp = self._dict._a.getitem("lpower green")

        self._red[:] = (self.redAmp * 5.0 / 100.0)
        self._green[:] = (self.greenAmp * 5.0 / 100.0)
        self._data = np.concatenate((self._red, self._green))

    def AnalogChannels(self):
        self.analog_output = Task()
        self.analog_output.CreateAOVoltageChan(physicalChannel="Dev1/ao0",
                                               nameToAssignToChannel="",
                                               minVal=-10.0,
                                               maxVal=10.0,
                                               units=DAQmx_Val_Volts,
                                               customScaleName=None)
        self.analog_output.CreateAOVoltageChan(physicalChannel="Dev1/ao1",
                                               nameToAssignToChannel="",
                                               minVal=-10.0,
                                               maxVal=10.0,
                                               units=DAQmx_Val_Volts,
                                               customScaleName=None)

        self.analog_output.CfgSampClkTiming(source="",
                                            rate=self._freq,
                                            activeEdge=DAQmx_Val_Rising,
                                            sampleMode=DAQmx_Val_FiniteSamps,
                                            sampsPerChan=self._sampFreq)
        self.analog_output.CfgDigEdgeStartTrig(triggerSource="/Dev1/RTSI2",
                                               triggerEdge=DAQmx_Val_Rising)

        self.analog_output.WriteAnalogF64(numSampsPerChan=self._sampFreq,
                                          autoStart=0,
                                          timeout=-1,
                                          dataLayout=DAQmx_Val_GroupByChannel,
                                          writeArray=self._data,
                                          sampsPerChanWritten=byref(self.read),
                                          reserved=None)

        self.analog_output.StartTask()

    def startAnalog(self):
        self.Intensities()
        self.AnalogChannels()

    def stopAnalog(self):
        self.analog_output.StopTask()
        self.analog_output.ClearTask()
        self._data[:] = 0
        self.AnalogChannels()
        time.sleep(0.1)
        self.analog_output.StopTask()
        self.analog_output.ClearTask()

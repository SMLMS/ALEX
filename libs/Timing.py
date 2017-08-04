'''######################################################################
# File Name: Timing.py
# Project: ALEX
# Version:
# Creation Date: 2017/07/21
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from PyDAQmx import *
import libs.dictionary


class SampleClock():
    def __init__(self):
        self._dict = libs.dictionary.UIsettings()

    def refreshSettings(self, dictionary):
        self._dict._a = dictionary

    def Pulse(self):
        self._timingPuls = Task()
        self._timingPuls.CreateCOPulseChanFreq(counter="Dev1/ctr0",
                                               nameToAssignToChannel="",
                                               units=DAQmx_Val_Hz,
                                               idleState=DAQmx_Val_Low,
                                               initialDelay=0.0,
                                               freq=self._freq,
                                               dutyCycle=0.50)
        self._timingPuls.CfgImplicitTiming(DAQmx_Val_ContSamps, 10000)
        self._timingPuls.ExportSignal(signalID=DAQmx_Val_CounterOutputEvent,
                                      outputTerminal="/Dev2/RTSI0, /Dev1/RTSI2")
        self._timingPuls.SetExportedCtrOutEventOutputBehavior(DAQmx_Val_Pulse)

    def startClock(self):
        self._freq = self._dict._a.getitem("laser frequency")
        self.Pulse()
        self._timingPuls.StartTask()

    def stopClock(self):
        self._timingPuls.StopTask()
        self._timingPuls.ClearTask()
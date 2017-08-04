'''######################################################################
# File Name: Illumination.py
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
import libs.AnalogOutput


class Illumination():
    def __init__(self):
        self._dict = libs.dictionary.UIsettings()
        self._analog = libs.AnalogOutput.GenerateSignal()

    def refreshSettings(self, dictionary):
        self._dict._a = dictionary
        self._analog.refreshSettings(self._dict._a)

    def calcSignal(self):
        self._percentHighGreen = (self._dict._a.getitem("laser percentageG") / 100.0)
        self._percentHighRed = (self._dict._a.getitem("laser percentageR") / 100.0)
        self._frequency = self._dict._a.getitem("laser frequency")
        self._highTime = (1.0 / self._frequency) * self._percentHighGreen
        self._lowTime = (1.0 / self._frequency) * self._percentHighRed
        self._initialDelay_red = self._highTime
        self._highSil = 0.01 / 100000
        self._lowSil = (1 / self._frequency) - (self._highSil)
        self._initialDelay_sil1 = self._highTime - (0.3 * self._highSil)
        self._initialDelay_sil2 = self._initialDelay_red - (0.3 * self._highSil)

    def startIllumination(self):
        self.calcSignal()
        self._analog.startAnalog()

        self._green = Task()
        self._green.CreateCOPulseChanTime(counter="Dev2/ctr4",
                                          nameToAssignToChannel="",
                                          units=DAQmx_Val_Seconds,
                                          idleState=DAQmx_Val_Low,
                                          initialDelay=0.00,
                                          lowTime=self._lowTime,
                                          highTime=self._highTime)
        self._green.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)

        self._red = Task()
        self._red.CreateCOPulseChanTime(counter="Dev2/ctr5",
                                        nameToAssignToChannel="",
                                        units=DAQmx_Val_Seconds,
                                        idleState=DAQmx_Val_Low,
                                        initialDelay=self._initialDelay_red,
                                        lowTime=self._highTime,
                                        highTime=self._lowTime)
        self._red.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)

        self._sil1 = Task()
        self._sil1.CreateCOPulseChanTime(counter="Dev2/ctr6",
                                         nameToAssignToChannel="",
                                         units=DAQmx_Val_Seconds,
                                         idleState=DAQmx_Val_Low,
                                         initialDelay=self._initialDelay_sil1,
                                         lowTime=self._lowSil,
                                         highTime=self._highSil)
        self._sil1.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)

        self._sil2 = Task()
        self._sil2.CreateCOPulseChanTime(counter="Dev2/ctr7",
                                         nameToAssignToChannel="",
                                         units=DAQmx_Val_Seconds,
                                         idleState=DAQmx_Val_Low,
                                         initialDelay=self._initialDelay_sil2,
                                         lowTime=self._lowSil,
                                         highTime=self._highSil)
        self._sil2.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)

        self.triggerIllumination()

        self._green.StartTask()
        self._red.StartTask()
        self._sil1.StartTask()
        self._sil2.StartTask()

    def triggerIllumination(self):
        self._green.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
        self._red.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
        self._sil1.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
        self._sil2.SetArmStartTrigType(data=DAQmx_Val_DigEdge)

        self._green.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
        self._red.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
        self._sil1.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
        self._sil2.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)

        self._green.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")
        self._red.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")
        self._sil1.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")
        self._sil2.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")

    def stopIllumination(self):
        self._green.StopTask()
        self._red.StopTask()
        self._sil1.StopTask()
        self._sil2.StopTask()

        self._green.ClearTask()
        self._red.ClearTask()
        self._sil1.ClearTask()
        self._sil2.ClearTask()

        self._analog.stopAnalog()

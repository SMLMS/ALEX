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


class Timing:
    """
    This class configures the pulse train, which serves as trigger signal
    and as sample clock for the analog signal. The pulse train is created
    on the 6713 card, which should be 'Device 1'.
    """
    def __init__(self):
        self._dict = dict()
        self._timingPuls = None
        self._freq = 0

    def refreshSettings(self, dictionary):
        self._dict.update(dictionary)

    def InitClock(self):
        """
        The timing pulse gets exported to RTSI 0 on Dev2 as trigger signal for the counter tasks
        and to RTSI 2 on Dev1 as sample clock for the analog output task.
        """
        self._freq = self._dict["laser frequency"]

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
        self._timingPuls.StartTask()

    def stopClock(self):
        self._timingPuls.StopTask()
        self._timingPuls.ClearTask()

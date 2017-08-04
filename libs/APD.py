'''######################################################################
# File Name: TimestampingCounters.py
# Project: ALEX
# Version:
# Creation Date: 2017_07_13
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from PyDAQmx import *
import ctypes
import numpy as np
# import cProfile


class TimestampingCounters():
    def __init__(self, readArraySize, N):
        self._sampNumber = readArraySize
        self._N = N
        self._buffer = int(1e8)    # 1e8 is possible, no more
        self._value1 = np.zeros([self._sampNumber], dtype=ctypes.c_uint32())
        self._value2 = np.zeros([self._sampNumber], dtype=ctypes.c_uint32())
        self._roll1 = np.zeros([self._sampNumber], dtype=ctypes.c_uint32())
        self._roll2 = np.zeros([self._sampNumber], dtype=ctypes.c_uint32())
        self._data = np.zeros([self._sampNumber, 2])
        self._read = int32()

    """
    def do_cprofile(func):
        def profiled_func(*args, **kwargs):
            profile = cProfile.Profile()
            try:
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                return result
            finally:
                profile.print_stats()
        return profiled_func
    """

    # @do_cprofile
    def startCounting(self):
        # 4 counters are set up, all counting edges, source terminal of counter 0 and 2 is 100MHzTimebase,
        # source terminal of 1 and 3 is their output terminal. The last function assembles all needed functions
        # and starts the tasks. This function should be called from the 'Counter.py' class.
        if self._N == 1:
            self.InitializeCounter1()
            self.SamplingCounter1()
            self.ArmStartCounter1()
            self._rollover1.StartTask()
            self._counter1.StartTask()
        else:
            self.InitializeCounter2()
            self.SamplingCounter2()
            self.ArmStartCounter2()
            self._rollover2.StartTask()
            self._counter2.StartTask()
        # Important note for arm start trigger: Always start trigger pulse AFTER counter tasks, else NO SYNC!

    def InitializeCounter1(self):
        self._counter1 = Task()
        self._counter1.CreateCICountEdgesChan(counter="Dev2/ctr0",
                                              nameToAssignToChannel="",
                                              edge=DAQmx_Val_Rising,
                                              initialCount=0,
                                              countDirection=DAQmx_Val_CountUp)
        self._counter1.SetCICountEdgesTerm("", "/Dev2/100MHzTimebase")

        self._rollover1 = Task()
        self._rollover1.CreateCICountEdgesChan(counter="Dev2/ctr1",
                                               nameToAssignToChannel="",
                                               edge=DAQmx_Val_Rising,
                                               initialCount=0,
                                               countDirection=DAQmx_Val_CountUp)
        self._rollover1.SetCICountEdgesTerm("", "/Dev2/PFI32")

    def InitializeCounter2(self):
        self._counter2 = Task()
        self._counter2.CreateCICountEdgesChan(counter="Dev2/ctr2",
                                              nameToAssignToChannel="",
                                              edge=DAQmx_Val_Rising,
                                              initialCount=0,
                                              countDirection=DAQmx_Val_CountUp)
        self._counter2.SetCICountEdgesTerm("", "/Dev2/100MHzTimebase")

        self._rollover2 = Task()
        self._rollover2.CreateCICountEdgesChan(counter="Dev2/ctr3",
                                               nameToAssignToChannel="",
                                               edge=DAQmx_Val_Rising,
                                               initialCount=0,
                                               countDirection=DAQmx_Val_CountUp)
        self._rollover2.SetCICountEdgesTerm("", "/Dev2/PFI24")

    def SamplingCounter1(self):
        # Sampling of all four counters is set to sample clock,
        # all are sampled by the signal of their APD respectively.
        # The signal should be received by the source terminal.
        self._counter1.CfgSampClkTiming(sampsPerChan=self._buffer,              # This is sampsPerChanToAcquire argument
                                        source="/Dev2/PFI39",
                                        rate=10000000,
                                        activeEdge=DAQmx_Val_Rising,
                                        sampleMode=DAQmx_Val_ContSamps)
        # The next function sets the task to ignore sample pulses, that came faster than the task can handle.
        # This might be the case when a fluorophore enters the volume, also it means in this case we lose all photon events that are coming in faster than 100MHz.
        self._counter1.SetSampClkOverrunBehavior(data=DAQmx_Val_IgnoreOverruns)

        # Duplication prevention for the rollover counters
        self._rollover1.SetCIDupCountPrevent("/Dev2/ctr1", True)
        self._rollover1.CfgSampClkTiming(sampsPerChan=self._buffer,              # This is sampsPerChanToAcquire argument
                                         source="/Dev2/PFI35",
                                         rate=10000000,
                                         activeEdge=DAQmx_Val_Rising,
                                         sampleMode=DAQmx_Val_ContSamps)
        self._rollover1.SetSampClkOverrunBehavior(data=DAQmx_Val_IgnoreOverruns)

        # The terminal count signal of counters 0 and 2 is routed to the output terminals
        # of counters 1 and 3 respectively. Output behavior is 'puls' (not toggle).
        # This is important because only rising edges get counted.
        self._counter1.ExportSignal(signalID=DAQmx_Val_CounterOutputEvent,
                                    outputTerminal="/Dev2/PFI32")
        self._counter1.SetExportedCtrOutEventOutputBehavior(DAQmx_Val_Pulse)

    def SamplingCounter2(self):
        self._counter2.CfgSampClkTiming(source="/Dev2/PFI31",
                                        rate=10000000,
                                        activeEdge=DAQmx_Val_Rising,
                                        sampleMode=DAQmx_Val_ContSamps,
                                        sampsPerChan=self._buffer)
        self._counter2.SetSampClkOverrunBehavior(data=DAQmx_Val_IgnoreOverruns)

        self._rollover2.SetCIDupCountPrevent("/Dev2/ctr3", True)
        self._rollover2.CfgSampClkTiming(source="/Dev2/PFI27",
                                         rate=10000000,
                                         activeEdge=DAQmx_Val_Rising,
                                         sampleMode=DAQmx_Val_ContSamps,
                                         sampsPerChan=self._buffer)
        self._rollover2.SetSampClkOverrunBehavior(data=DAQmx_Val_IgnoreOverruns)

        self._counter2.ExportSignal(signalID=DAQmx_Val_CounterOutputEvent,
                                    outputTerminal="/Dev2/PFI24")
        self._counter2.SetExportedCtrOutEventOutputBehavior(DAQmx_Val_Pulse)

    def ArmStartCounter1(self):
        # Arm start trigger makes the counters wait for an external signal.
        # signal could be the timing task from 6713 (over RTSI). But counters should
        # always be started first, otherwise they wait for the next edge
        # or infinitely.
        self._counter1.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
        self._rollover1.SetArmStartTrigType(data=DAQmx_Val_DigEdge)

        self._counter1.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
        self._rollover1.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)

        self._counter1.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")
        self._rollover1.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")

    def ArmStartCounter2(self):
        self._counter2.SetArmStartTrigType(data=DAQmx_Val_DigEdge)
        self._rollover2.SetArmStartTrigType(data=DAQmx_Val_DigEdge)

        self._counter2.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)
        self._rollover2.SetDigEdgeArmStartTrigEdge(data=DAQmx_Val_Rising)

        self._counter2.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")
        self._rollover2.SetDigEdgeArmStartTrigSrc(data="/Dev2/RTSI0")

    # @do_cprofile
    def readAPD(self):
        if self._N == 1:
            self.actualCounting(self._rollover1, self._roll1)
            self.actualCounting(self._counter1, self._value1)
            self._data[:, 1] = self._roll1[:]
            self._data[:, 0] = self._value1[:]
        else:
            self.actualCounting(self._rollover2, self._roll2)
            self.actualCounting(self._counter2, self._value2)
            self._data[:, 1] = self._roll2[:]
            self._data[:, 0] = self._value2[:]
        return self._data

    def actualCounting(self, task, readArray):
        task.ReadCounterU32(numSampsPerChan=self._sampNumber,
                            timeout=200.0,
                            readArray=readArray,
                            arraySizeInSamps=self._sampNumber + 1,
                            sampsPerChanRead=self._read,
                            reserved=None)
        return readArray

    def stopCounting(self):
        # Stop and clear tasks
        if self._N == 1:
            self._rollover1.StopTask()
            self._counter1.StopTask()
            self._rollover1.ClearTask()
            self._counter1.ClearTask()
        else:
            self._rollover2.StopTask()
            self._counter2.StopTask()
            self._rollover2.ClearTask()
            self._counter2.ClearTask()
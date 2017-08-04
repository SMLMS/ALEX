'''######################################################################
# File Name: Counter.py
# Project: ALEX
# Version:
# Creation Date: 2017/03/13
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import libs.APD
import numpy as np
from multiprocessing import Process
# import cProfile


class Counter(Process):
    def __init__(self, running, dataQ, readArraySize, N):
        super(Counter, self).__init__()
        self.daemon = True
        self._running = running
        self._dataQ = dataQ
        self._readArraySize = readArraySize
        self._data = np.zeros([self._readArraySize, 2], dtype=int)    # this statement doesnt update arraySize otherwise
        self._N = N
        self._apd = libs.APD.TimestampingCounters(self._readArraySize, self._N)

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
    def run(self):
        # run() is obligatory for subprocesses. Strangely it gets called by start()
        # This function calls refresh functions, starts counting
        self._apd.startCounting()
        self.Measurement()
        print("Counter %i sent all data and exits." % ((self._N)))

    # @do_cprofile
    def Measurement(self):
        while self._running.is_set():
            self._data = self._apd.readAPD()
            self._dataQ.put(self._data)
        self._apd.stopCounting()
        self._dataQ.put('STOP')

    def __del__(self):
        print("Counter class instance %i has been removed." % ((self._N)))

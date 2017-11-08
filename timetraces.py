'''######################################################################
# File Name: timetraces.py
# Project: ALEX
# Version:
# Creation Date: 07/11/2017
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import numpy as np
import pathlib
import tables
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser(description="Shows timetraces of hdf's.")
parser.add_argument("--d", type=str, help="Enter directory")
args = parser.parse_args()
directory = pathlib.Path(args.d)


def correctRollover(t1, t2):
    int_32 = (2**32) - 1
    t1[:, 0] = t1[:, 0] + (int_32 * t1[:, 1])
    t2[:, 0] = t2[:, 0] + (int_32 * t2[:, 1])
    return t1, t2


def binnedTrace(array):
    trace = []
    n = 1
    bins = 0
    for i in range(len(array)):
        bins += 1
        if array[i] >= (n * 1e6):
            trace.append(bins)
            n += 1
            bins = 0
        if array[i] == array[-1]:
            trace.append(bins)
            n += 1
            bins = 0
    return trace, n - 1

filename = str(directory / 'smALEX_APD1.hdf')
f = tables.open_file(filename, 'r')
green_trace = np.array(f.root.timestamps[:, :], dtype=np.int64)
f.flush()
f.close()

filename = str(directory / 'smALEX_APD2.hdf')
f = tables.open_file(filename, 'r')
red_trace = np.array(f.root.timestamps[:, :], dtype=np.int64)
f.flush()
f.close()

green_trace, red_trace = correctRollover(green_trace, red_trace)

green_trace, num1 = binnedTrace(green_trace[:, 0])
green_trace[:] = [x / 10 for x in green_trace]
num1 = np.arange(num1)

red_trace, num2 = binnedTrace(red_trace[:, 0])
red_trace[:] = [x / 10 for x in red_trace]
num2 = np.arange(num2)

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax1.plot(num1, green_trace, 'g')
ax1.set_ylabel('kHz')
ax1.set_xlabel('10 ms')

ax2 = fig.add_subplot(2, 1, 2)
ax2.set_xlabel('10 ms')
ax2.set_ylabel('kHz')
ax2.plot(num2, red_trace, 'r')

fig.subplots_adjust(hspace=0.5)
plt.show()
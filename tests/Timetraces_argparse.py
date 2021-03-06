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


def correct2(t):
    int_32 = (2**32) - 1
    n = 0
    dt = t[0, 0]
    for i in range(1, len(t)):
        if t[i, 0] < dt:
            n += 1
        dt = t[i, 0]
        t[i, 0] += n * int_32
    return t


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
        # if array[i] == array[-1]:
        #     trace.append(bins)
        #     n += 1
        #     bins = 0
    return trace, n - 1


def binnedTrace1(array):
    n_bin = int(np.floor((array[-1] - array[0]) / (1e6)))
    print(n_bin, array[-1])
    trace = np.zeros([n_bin, 1], dtype=np.int64)
    j = 0
    for i in range(len(trace)):
        bins = 0
        t_m = (i + 1) * 1e6
        while (array[j] < t_m):    # and (array[j] >= t_m - (1e5)):
            bins += 1
            j += 1
        trace[i] = bins
    return trace, n_bin


filename = str(directory / 'smALEX_APD1.hdf')
f = tables.open_file(filename, 'r')
green_trace = np.array(f.root.timestamps[:, :], dtype=np.float)
f.flush()
f.close()

filename = str(directory / 'smALEX_APD2.hdf')
f = tables.open_file(filename, 'r')
red_trace = np.array(f.root.timestamps[:, :], dtype=np.float)
f.flush()
f.close()

green_trace, red_trace = correctRollover(green_trace, red_trace)
# green_trace = correct2(green_trace)
# red_trace = correct2(red_trace)

green_trace, num1 = binnedTrace(green_trace[:, 0])
green_trace[:] = [x / 10.0 for x in green_trace]   # 10 ms bins
# green_trace[:] = [x * 10.0 for x in green_trace]   # 100 us bins
num1 = np.arange(num1)

red_trace, num2 = binnedTrace(red_trace[:, 0])
red_trace[:] = [x / 10.0 for x in red_trace]
# red_trace[:] = [x * 10.0 for x in red_trace]   # 100 us bins
num2 = np.arange(num2)

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax1.plot(num1, green_trace, 'g')
ax1.set_ylabel('kHz')
ax1.set_xlabel('ms')

ax2 = fig.add_subplot(2, 1, 2)
ax2.set_xlabel('ms')
ax2.set_ylabel('kHz')
ax2.plot(num2, red_trace, 'r')

fig.subplots_adjust(hspace=0.5)
plt.show()

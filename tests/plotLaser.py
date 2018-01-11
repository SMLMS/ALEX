'''######################################################################
# File Name:
# Project:
# Version:
# Creation Date:
# Created By:
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import numpy as np
import matplotlib.pyplot as plt


freq = 102
t = np.arange(0, 2.04, 0.02)
redP = np.zeros([freq, 1])
greenP = np.zeros([freq, 1])
sig1 = np.zeros([freq, 1])
sig2 = np.ones([freq, 1])


greenP[1:26] = 4
greenP[51:76] = 4
redP[26:51] = 3.5
redP[76:101] = 3.5
sig2[:] *= 5
sig2[25:27] = 0
sig2[75:77] = 0
sig2[50:52] = 0
sig2[100:] = 0
sig2[:2] = 0
sig1[0] = 100
sig1[1:] = 5

fig, ax = plt.subplots()
ax.step(t, greenP, color='green', linestyle='-')
ax.step(t, redP, color='red', linestyle='-')
ax.step(t, sig2, color='black', linestyle='--')
ax.yaxis.set_ticks_position('both')
plt.tick_params(axis='y', which='both', labelleft='off', labelright='off')

plt.show()

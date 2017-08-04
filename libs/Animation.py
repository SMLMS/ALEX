'''######################################################################
# File Name: Animation.py
# Project: ALEX
# Version:
# Creation Date: 2017/03/16
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
from matplotlib import pyplot, animation
from matplotlib.lines import Line2D
import seaborn as sns


class Animation():
    def __init__(self, animDataQ1, animDataQ2, signal):
        self._animDataQ1 = animDataQ1
        self._animDataQ2 = animDataQ2
        self._signal = signal
        self._dt = 0.1
        self._tdata = [0]
        self._greenData = [0]
        self._redData = [0]
        self._greenLine = 0
        self._redLine = 0
        self._figure = pyplot.figure()
        self.anim = 0
        self._axLimit = 1e8

    def run(self):
        self.plot()

    def plot(self):
        # pyplot.style.use('seaborn-deep')
        sns.set()
        ax = self._figure.add_subplot(111)

        self._greenLine = Line2D([], [], color='black')
        self._redLine = Line2D([], [], color='black')

        ax.add_line(self._greenLine)
        ax.add_line(self._redLine)

        ax.set_xlim(0, 10)
        ax.set_ylim(-self._axLimit, self._axLimit)

        ax.set_xlabel("time in [s]")
        ax.set_ylabel("counts")

    def plot2(self):
        pyplot.style.use('seaborn-deep')

        ax_green = self._figure.add_subplot(2, 1, 1)
        ax_red = self._figure.add_subplot(2, 1, 2)

        self._greenLine = Line2D([], [], color='black')
        self._redLine = Line2D([], [], color='black')

        ax_green.add_line(self._greenLine)
        ax_red.add_line(self._redLine)

        ax_green.set_xlim(0, 10)
        ax_red.set_xlim(0, 10)
        ax_green.set_ylim(-30, 10000000)
        ax_red.set_ylim(1000000, -30)

        ax_green.set_xlabel("time in [s]")
        ax_red.set_xlabel("time in [s]")
        ax_green.set_ylabel("counts")
        ax_red.set_ylabel("counts")

        ax_green.set_title("Green channel")
        ax_red.set_title("Red channel")

        # pyplot.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        self._figure.subplots_adjust(left=0.2, bottom=0.1, right=0.8, top=0.9, wspace=0.1, hspace=0.8)

    def initAnimation(self):
        self._greenLine.set_data([], [])
        self._redLine.set_data([], [])
        return self._greenLine, self._redLine,

    def updateAnimation(self, i):
        if self._tdata[-1] > 10:
            self._tdata = [0]
            self._greenData = [self._greenData[-1]]
            self._redData = [self._redData[-1]]
        try:
            green = float(1e8) * self._animDataQ1.get(timeout=1.0)
            red = float(1e8) * (-1) * self._animDataQ2.get(timeout=1.0)
            x = [int(green), int(red)]
            self._signal.displayRates.emit(x)

            self._greenData.append(green)
            self._redData.append(red)
            self._tdata.append(self._tdata[-1] + self._dt)
        except:
            print("error getting data for animation")
            pass

        self._greenLine.set_data(self._tdata, self._greenData)
        self._redLine.set_data(self._tdata, self._redData)
        return self._greenLine, self._redLine,

    def animate(self):
        self.anim = animation.FuncAnimation(self._figure, self.updateAnimation, init_func=self.initAnimation, frames=100, interval=100, blit=True, repeat=True)
        pyplot.show()

    def __del__(self):
        print("Animation class instance removed")

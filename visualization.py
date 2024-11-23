import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
from pyqtgraph.opengl import GLViewWidget, GLGridItem, GLLinePlotItem

class Waveform3D(GLViewWidget):
    def __init__(self, parent=None):
        super(Waveform3D, self).__init__(parent)
        self.setWindowTitle('3D Waveform')
        self.show()
        self.setCameraPosition(distance=40)
        self.grid = GLGridItem()
        self.addItem(self.grid)
        self.waveform_plot = GLLinePlotItem(color=(1, 0, 0, 1), width=2, antialias=True)
        self.addItem(self.waveform_plot)

    def update_plot(self, data):
        if data is not None:
            print("Waveform data received for 3D plotting:", data)  # Debug statement
            length = len(data)
            x = np.linspace(0, 20, length)
            y = np.zeros(length)
            z = data[:length]  # Ensure lengths match
            points = np.vstack([x, y, z]).T  # Ensure lengths match
            print(f"Plotting points: {points}")  # Debug statement
            self.waveform_plot.setData(pos=points)
        else:
            print("No data received for 3D waveform plotting.")  # Debug statement

class Spectrum3D(GLViewWidget):
    def __init__(self, parent=None):
        super(Spectrum3D, self).__init__(parent)
        self.setWindowTitle('3D Spectrum')
        self.show()
        self.setCameraPosition(distance=40)
        self.grid = GLGridItem()
        self.addItem(self.grid)
        self.spectrum_plot = GLLinePlotItem(color=(0, 1, 0, 1), width=2, antialias=True)
        self.addItem(self.spectrum_plot)

    def update_plot(self, data):
        if data is not None:
            print("Spectrum data received for 3D plotting:", data)  # Debug statement
            length = len(data)
            freqs = np.fft.fftfreq(length)
            x = freqs[:length]
            y = np.zeros(length)
            z = data[:length]  # Ensure lengths match
            points = np.vstack([x, y, z]).T  # Ensure lengths match
            print(f"Plotting points: {points}")  # Debug statement
            self.spectrum_plot.setData(pos=points)
        else:
            print("No data received for 3D spectrum plotting.")  # Debug statement

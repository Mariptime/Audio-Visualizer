# visualization.py

import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout

class Waveform(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)
        self.plot_data = self.plot_widget.plot(pen='r')  # Set the plot line color to red
        self.plot_widget.setYRange(-3000, 3000)
        self.plot_widget.setLabel('left', 'Amplitude')
        self.plot_widget.setLabel('bottom', 'Time')
        self.plot_widget.showGrid(x=True, y=True)

    def update(self, waveform):
        self.plot_data.setData(waveform)

    def reset(self):
        self.plot_data.clear()

class Spectrum(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)
        self.plot_data = self.plot_widget.plot(pen='g')  # Set the plot line color to green
        self.plot_widget.setLogMode(y=True)
        self.plot_widget.setLabel('left', 'Magnitude (dB)')
        self.plot_widget.setLabel('bottom', 'Frequency (Hz)')
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setXRange(0, 22000)  # Set x-axis range to 0 to 22,000 Hz
        self.plot_widget.setYRange(6, 0)  # Set x-axis range to 0 to 22,000 Hz


    def update(self, freqs, spectrum):
        self.plot_data.setData(freqs, spectrum)

    def reset(self):
        self.plot_data.clear()  # Clear the plot data
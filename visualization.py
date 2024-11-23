# visualization.py

import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout

class Waveform(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)
        self.plot_data = self.plot_widget.plot()

    def update(self, waveform):
        self.plot_data.setData(waveform)

class Spectrum(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)
        self.plot_data = self.plot_widget.plot()

    def update(self, spectrum):
        self.plot_data.setData(spectrum)

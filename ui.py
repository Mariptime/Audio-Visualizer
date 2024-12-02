# ui.py

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QPushButton, QComboBox, QVBoxLayout, QWidget
from audio_processing import AudioInput, ProcessingEngine
from visualization import Waveform, Spectrum
from PyQt5.QtCore import QTimer
import threading

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.audio_input = AudioInput()
        self.stream = None
        self.file_data = None
        self.file_path = None
        self.processing_engine = ProcessingEngine()
        self.waveform_view = Waveform(self)
        self.spectrum_view = Spectrum(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Music Waveform Visualizer")
        self.waveform_view.setGeometry(10, 10, 400, 300)
        self.spectrum_view.setGeometry(420, 10, 400, 300)
        self.setGeometry(100, 100, 840, 400)

        # Adding input source selection
        self.input_source = QComboBox(self)
        self.input_source.setGeometry(10, 320, 150, 30)
        self.input_source.addItem("Microphone")
        self.input_source.addItem("Audio File")
        self.input_source.setCurrentIndex(0)  # Set default to "Microphone"
        self.input_source.currentIndexChanged.connect(self.change_input_source)

        # Initialize microphone stream
        self.stream = self.audio_input.get_mic_stream()
        self.processing_engine.stream = self.stream
        print("Microphone stream initialized")

        # Adding a button to load audio files
        self.load_file_btn = QPushButton('Load Audio File', self)
        self.load_file_btn.setGeometry(170, 320, 150, 30)
        self.load_file_btn.clicked.connect(self.load_audio_file)
        self.load_file_btn.setEnabled(False)
        
        # Create reset button
        self.reset_button = QPushButton('Reset Graph View', self)
        self.reset_button.setGeometry(330, 320, 150, 30)
        self.reset_button.clicked.connect(self.reset_graph_view) 

        self.show()
        
    def reset_graph_view(self):
        self.waveform_view.reset()
        self.spectrum_view.reset()

    def change_input_source(self, index):
        if index == 0:
            self.load_file_btn.setEnabled(False)
            self.stream = self.audio_input.get_mic_stream()
            self.processing_engine.stream = self.stream
            self.file_data = None
            self.file_path = None
            self.audio_input.stop_audio_playback()
            print("Microphone stream initialized")
        elif index == 1:
            self.load_file_btn.setEnabled(True)
            if self.stream is not None:
                self.stream.close()
                self.processing_engine.stream = None
            print("File input enabled")

    def load_audio_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Audio File", "", "Audio Files (*.wav *.flac *.ogg *.mp3)", options=options)
        if file_name:
            samplerate = self.audio_input.get_file_stream(file_name)
            self.file_data = True
            self.file_path = file_name
            self.processing_engine.stream = None  # Clear the mic stream
            print(f"Loaded file: {file_name}")
            # Start playing audio in a separate thread
            playback_thread = threading.Thread(target=self.audio_input.play_audio_file, args=(file_name,))
            playback_thread.start()
            

    def run(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_visuals)
        self.timer.start(50)  # Adjusted interval to 50ms
        sys.exit(self.app.exec_())

    def update_visuals(self):
        waveform = None
        samplerate = 44100  # Replace with the actual sample rate of your audio input
        if self.input_source.currentText() == "Microphone":
            if self.stream:
                waveform = self.processing_engine.get_waveform(source='mic')
                print("Microphone waveform:", waveform)
        elif self.file_data:
            chunk = self.audio_input.read_file_chunk()
            if chunk is not None:
                waveform = self.processing_engine.get_waveform(source='file', file_data=chunk)
                print("File waveform:", waveform)
            else:
                print("End of file reached")
    
        if waveform is not None:
            # Apply threshold to the waveform to filter out noise
            threshold = 500
            waveform = self.processing_engine.apply_threshold(waveform, threshold)
    
            freqs, spectrum = self.processing_engine.get_spectrum(waveform, samplerate)
            if spectrum is not None:
                self.waveform_view.update(waveform)
                self.spectrum_view.update(freqs, spectrum)
            else:
                print("No valid spectrum data")
                
    def closeEvent(self, event):
            self.audio_input.stop_audio_playback()  # Stop audio playback when closing the window
            event.accept()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.run()
    sys.exit(app.exec_())
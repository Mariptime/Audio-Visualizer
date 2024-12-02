# ui.py

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QPushButton, QComboBox, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
import threading
from audio_processing import AudioInput, ProcessingEngine
from visualization import Waveform, Spectrum

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
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setGeometry(100, 100, 1280, 720)

        # Main layout
        main_layout = QVBoxLayout()

        # Create a horizontal layout for the plot views (waveform and spectrum)
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.waveform_view)
        plot_layout.addWidget(self.spectrum_view)

        # Add plot layout to main layout
        main_layout.addLayout(plot_layout)

        # Create a horizontal layout for control buttons (input source, load file, and reset)
        control_layout = QHBoxLayout()

        # Adding input source selection
        self.input_source = QComboBox(self)
        self.input_source.addItem("Microphone")
        self.input_source.addItem("Audio File")
        self.input_source.setCurrentIndex(0)  # Set default to "Microphone"
        self.input_source.currentIndexChanged.connect(self.change_input_source)
        control_layout.addWidget(self.input_source)
        
        # Initialize microphone stream
        self.stream = self.audio_input.get_mic_stream()
        self.processing_engine.stream = self.stream
        print("Microphone stream initialized")

        # Adding a button to load audio files
        self.load_file_btn = QPushButton('Load Audio File', self)
        self.load_file_btn.clicked.connect(self.load_audio_file)
        self.load_file_btn.setEnabled(False)
        control_layout.addWidget(self.load_file_btn)

        # Create reset button and place it to the right
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.Reset)
        control_layout.addWidget(self.reset_button, alignment=Qt.AlignRight)

        # Add control layout to main layout
        main_layout.addLayout(control_layout)

        # Set the main layout to the window
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.show()

    def Reset(self):
        # Reset any ongoing audio playback or graph updates
        if self.timer.isActive():
            self.timer.stop()
        if self.stream:
            self.audio_input.stop_audio_playback()  # Reset playback from microphone

        # Reset the visuals
        self.file_data = None
        self.waveform_view.reset()
        self.spectrum_view.reset()
        print("Graphs Cleared.")

    def change_input_source(self, index):
        if self.timer.isActive():
            self.timer.stop()
        
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
        self.timer.start(50)

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
        samplerate = 44100  # Replace with actual sample rate
        if self.input_source.currentText() == "Microphone":
            if self.stream:
                waveform = self.processing_engine.get_waveform(source='mic')
                print(f"Microphone waveform: length={len(waveform) if waveform is not None else 'None'}")
        elif self.file_data:
            chunk = self.audio_input.read_file_chunk()
            if chunk is not None:
                waveform = self.processing_engine.get_waveform(source='file', file_data=chunk)
                print(f"File waveform: length={len(waveform) if waveform is not None else 'None'}")
            else:
                self.file_data = None  # Reset further updates
                print("End of audio file reached.")
                self.Reset()
                return
        
        if waveform is not None:
            # Apply threshold to remove noise
            threshold = 50
            waveform = self.processing_engine.apply_threshold(waveform, threshold)
            print(f"Filtered waveform: length={len(waveform)}")

            # Generate spectrum
            freqs, spectrum = self.processing_engine.get_spectrum(waveform, samplerate)
            if freqs is not None and spectrum is not None:
                if len(freqs) != len(spectrum):
                    print(f"Skipping update: freqs={len(freqs)}, spectrum={len(spectrum)}")
                    return
                print(f"Spectrum data: freqs={len(freqs)}, spectrum={len(spectrum)}")
                self.waveform_view.update(waveform)
                self.spectrum_view.update(freqs, spectrum)
            else:
                print("No valid spectrum data")
                
    def closeEvent(self, event):
        self.audio_input.stop_audio_playback()  # Reset audio playback when closing the window
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.run()
    sys.exit(app.exec_())

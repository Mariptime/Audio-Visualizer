# audio_processing.py

import pyaudio
import numpy as np
import soundfile as sf
import sounddevice as sd

class AudioInput:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None

    def get_mic_stream(self, input_device_index=None):
        if self.stream is not None:
            self.stream.close()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=44100,
                                  input=True,
                                  frames_per_buffer=2048,
                                  input_device_index=input_device_index)
        return self.stream

    def get_file_stream(self, file_path):
        self.file_data, self.samplerate = sf.read(file_path, dtype='int16')
        self.file_position = 0
        return self.samplerate

    def read_file_chunk(self, chunk_size=2048):
        if self.file_position >= len(self.file_data):
            return None
        end = min(self.file_position + chunk_size, len(self.file_data))
        chunk = self.file_data[self.file_position:end]
        self.file_position = end
        return chunk

    def play_audio_file(self, file_path):
        data, samplerate = sf.read(file_path, dtype='int16')
        sd.play(data, samplerate)
        sd.wait()
        
    def stop_audio_playback(self):
        sd.stop()

class ProcessingEngine:
    def __init__(self):
        self.stream = None
        self.file_data = None
        self.file_position = 0

    def get_waveform(self, source='mic', file_data=None):
        if source == 'mic':
            try:
                data = self.stream.read(2048)
                waveform = np.frombuffer(data, dtype=np.int16)
            except Exception as e:
                print(f"Error reading mic stream: {e}")
                return None
        elif source == 'file' and file_data is not None:
            waveform = file_data
        return waveform

    def get_spectrum(self, waveform):
        if waveform is not None:
            spectrum = np.fft.fft(waveform)
            return np.abs(spectrum)
        return None

    def apply_threshold(self, waveform, threshold=500):
        # Create a mutable copy of the waveform array
        mutable_waveform = np.copy(waveform)
        # Apply a simple threshold filter to remove low amplitude noise
        mutable_waveform[abs(mutable_waveform) < threshold] = 0
        return mutable_waveform

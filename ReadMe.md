# Music Waveform Visualizer

This project is a Music Waveform Visualizer built using PyQt5 and pyqtgraph. It allows users to visualize audio waveforms and spectrums in real-time.

## Features

- Real-time audio waveform visualization
- Real-time audio spectrum visualization
- Reset button to reset the graph views to default

## Requirements

- Python 3.10

## Libraries
- pyaudio
- pyqtgraph
- PyQt5
- numpy
- scipy
- soundfile
- sounddevice
- PyOpenGL
- PyOpenGL_accelerate

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/Mariptime/Audio-Visualizer.git
    cd music-waveform-visualizer
    ```

2. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```
    python ui.py
    ```

2. Select the input source (e.g., Microphone) from the dropdown menu.

3. Click the "Reset Graph View" button to reset the waveform and spectrum views to default.

## Project Structure

- `ui.py`: Contains the main application code and UI setup.
- `audio_processing.py`: Contains the audio processing logic.
- `visualization.py`: Contains the waveform and spectrum visualization classes.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
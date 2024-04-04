# Image-to-Text-to-Speech (ITTS) Converter

ITTS Converter is a Python application that captures images from a webcam, extracts text from the captured images using the Google Cloud Vision API, performs text-to-speech conversion using the pyttsx3 library, and provides functionality to play, pause, save, or delete the audio transcription through voice commands using the Vosk ASR model.

## Requirements

- Python 3.x
- OpenCV (`pip install opencv-python`)
- Google Cloud Vision API client (`pip install google-cloud-vision`)
- Pyttsx3 (`pip install pyttsx3`)
- Pygame (`pip install pygame`)
- Vosk ASR model (`pip install vosk`)
- Pyaudio (`pip install pyaudio`)

## Usage

1. Ensure all required dependencies are installed. For reference, directly install dependencies using requirements.txt
2. Run the `main.py` script.
3. The application will capture an image from the webcam on the press of space key, extract text from the image, convert the text to speech, and play the audio transcription.
4. Once audio playback stops, you can use following voice commands recognized by vosk:
   - "Quit" or "Close" to quit the program.
   - "Scan again" or "Try again" to scan another document or to perform another detection.
   - "Play recent" to play the last audio transcription when no transcription is being played
5. You can use voice commands recognized by the Vosk ASR model to control the playback:
   - "Pause" or "Stop" to pause the audio.
   - "Resume" or "Start" to start playing the audio.
   - "Exit and remove" or "Exit remove" to remove last captured image and it corresponding transcribed audio file.
   - "Exit and keep" or "Exit keep" to keep last captured image and it corresponding transcribed audio file and scan again.
6. Whenever prompted a question, you can answer it in "yes" or "no" to perform relevant task.
7. Follow the on-screen prompts and voice commands to interact with the application.

## Contributing

Contributions to improve the functionality, usability, or documentation of the ITTS Converter project are welcome! If you have any suggestions, bug reports, or feature requests, please feel free to open an issue or submit a pull request.

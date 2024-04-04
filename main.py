import os
import glob
import cv2
from google.cloud import vision
import pyttsx3
import pygame
from pygame import mixer
from uuid import uuid4
from vosk import Model, KaldiRecognizer
import pyaudio
import sys

model = Model('vosk-model-small-en-in-0.4/vosk-model-small-en-in-0.4')
recognizer = KaldiRecognizer(model, 16000)

def get_recent_file(folder_path):
    os.chdir(folder_path)
    files = glob.glob('*')
    if not files:
        print("No files found in the folder.")
        return None
    most_recent_file = max(files, key=os.path.getmtime)
    most_recent_file_name = os.path.basename(most_recent_file)
    return most_recent_file_name

def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open the camera.")
        return
    while True:
        ret, frame = cap.read()
        cv2.imshow('Say Capture', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            image_path = f"temp/images/{str(uuid4())[:4]}.jpg"
            cv2.imwrite(image_path, frame)
            # print(f"Image saved as {image_path}")
            break
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return image_path

def voice_commands():
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()
    while True:
        voice = stream.read(4096)
        if recognizer.AcceptWaveform(voice):
            text = recognizer.Result()
            command = text[14:-3]
            print('command ====> ', command)
            return command

def stop_audio():
    mixer.music.stop()

def pause():
    mixer.music.pause()

def unpause():
    mixer.music.unpause()

def save_file(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')      
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 200)
    outfile = f"temp/temp{str(uuid4())[:4]}.wav"
    engine.save_to_file(text, outfile)
    engine.runAndWait()
    return outfile

def detect_text(path):
    client = vision.ImageAnnotatorClient()
    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        complete_text = ' '.join(texts[0].description.split('\n'))
        print('Texts:', complete_text)
        output = save_file(complete_text)
        # print("Text saved --- > ", output)
        return output
    else:
        print('No text detected in the image.')

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

def delete_file(file_path, image_path):
    # print('file_path ==========>  ', file_path)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            os.remove(image_path)
            # print(f"File '{file_path}' and '{image_path}' deleted successfully.")
            print('Deleted')
            return True
        else:
            print(f"File '{file_path}' not found.")
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def main():
    try:
        engine = pyttsx3.init()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./application_default_credentials.json"
        # image_path = 'book.jpg'
        image_path = capture_image()
        file = detect_text(image_path)
        if file:
            mixer.init()
            mixer.music.load(file)
            mixer.music.play()
            while True:
                commands = voice_commands()
                if ('stop' in commands) or ('pause' in commands):
                    pause() 
                elif ('resume' in commands) or ('start' in commands):
                    unpause()    
                elif ('exit and remove' in commands) or ('exit remove' in commands) or ('exit' in commands and 'remove' in commands):
                    stop_audio()
                    mixer.music.stop()
                    mixer.quit()
                    print('You choose to delete the file.')
                    engine.say('You choose to delete the file.')
                    engine.runAndWait()
                    delete_file(str(file), str(image_path))
                    engine.say('Deleted.')
                    engine.runAndWait()
                    print('Want to detect more ? - Yes or no')
                    engine.say('Want to detect more ? ')
                    engine.runAndWait()
                    while (' ' in commands) or ('yes' not in commands) or (commands is None):
                        commands_1 = voice_commands()
                        if 'yes' in commands_1:
                            print('Ok, scan again')
                            engine.say('Ok, scan again')
                            engine.runAndWait()
                            main()
                        elif 'no' in commands_1:
                            print('Thank you ! Exiting')
                            engine.say('Thank you ! Exiting')
                            engine.runAndWait()
                            sys.exit(0)          
                elif ('exit and keep' in commands) or ('exit' in commands and 'keep' in commands):
                    print('You choose to save the file. Thank you!')
                    engine.say('You choose to save the file. Thank you!')
                    engine.runAndWait()
                    print('Want to detect more? - Yes or no')
                    engine.say('Want to detect more?')
                    engine.runAndWait()
                    while (' ' in commands) or ('yes' not in commands) or (commands is None):
                        commands_1 = voice_commands()
                        if 'yes' in commands_1:
                            print('Ok, Scan again')
                            engine.say('Ok, Scan again')
                            engine.runAndWait()
                            main()
                        elif 'no' in commands_1:
                            print('Thank you ! Exiting')
                            engine.say('Thank you ! Exiting')
                            engine.runAndWait()
                            sys.exit(0) 
                elif ('quit' in commands) or ('close' in commands):
                    if mixer.get_busy == True:
                        mixer.music.stop()
                        mixer.quit()
                    print('Thank you ! Exiting')
                    engine.say('Thank you! Exiting')
                    engine.runAndWait()
                    sys.exit(0)
                elif (commands == 'scan again') or (commands == 'try again'):
                    print('Ok, Try again !')
                    engine.say('Ok, Try again !')
                    engine.runAndWait()
                    main()
                elif (commands == 'play recent') or ('play' in commands and 'recent' in commands):
                    print('Ok, Playing the most recent transcription !')
                    engine.say('Ok, Playing the most recent transcription !')
                    engine.runAndWait()
                    recent_path = get_recent_file('temp')
                    recent_path = f'temp/{recent_path}'
                    if mixer.get_busy == False:
                        try:
                            mixer.init()
                            mixer.music.load(recent_path)
                            mixer.music.play()
                        except Exception as e:
                            engine.say('Playing recent transcription failed')
                            engine.runAndWait()

        else:
            print('No text found, try again')
            engine.say('No text found, try again')
            engine.runAndWait()
            main()

    except pygame.error:
        print('File not found')
        engine.say('Looks like you removed the last file')
        engine.runAndWait()
        print('Want to detect more ? - Yes or No')
        engine.say('Want to detect more ?')
        engine.runAndWait()
        commands = voice_commands()
        while (' ' in commands) or ('yes' not in commands) or (commands is None):
            commands_1 = voice_commands()
            if 'yes' in commands_1:
                print('Ok, scan again')
                engine.say('Ok, scan again')
                engine.runAndWait()
                main()
            elif 'no' in commands_1:
                print('Thank you ! Exiting')
                engine.say('Thank you ! Exiting')
                engine.runAndWait()
                sys.exit(0)
            elif (commands_1 == 'quit') or ('quit' in commands_1):
                print('Thank you ! Exiting')
                engine.say('Thank you ! Exiting')
                engine.runAndWait()
                sys.exit(0)                
    except Exception as e:
        print('Error -------> ', e)
        engine.say('Something went wrong !')
        engine.runAndWait()
        
if __name__ == "__main__":
    main()



import os
from pynput import keyboard
import time
import pyaudio
import wave
import sched
import sys
import pyttsx3
import time
import wave
from googletrans import Translator
import pandas as pd

import pyaudio
import pyperclip as clip
import speech_recognition as sr
from pynput.keyboard import Listener, KeyCode
from pynput.keyboard import Key, Controller
from fuzzywuzzy import process


voice_commands = pd.read_csv("commands.csv").set_index('voice_command').to_dict()['result']

current_directory = os.path.dirname(os.path.realpath("__file__")) + "/"
data_directory = os.path.join(current_directory, 'data')
wav_file = f"{data_directory}/new_recording.wav"
ideas_file = f"{data_directory}/ideas.csv"
current_directory, data_directory

def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return (in_data, pyaudio.paContinue)

class MyListener(keyboard.Listener):
    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None
        self.wf = wave.open(wav_file, 'wb')
        self.wf.setnchannels(CHANNELS)
        self.wf.setsampwidth(p.get_sample_size(FORMAT))
        self.wf.setframerate(RATE)
    def on_press(self, key):
        if key == keyboard.Key.ctrl:
            self.key_pressed = True
        return True

    def on_release(self, key):
        if key == keyboard.Key.ctrl:
            self.key_pressed = False
        return True

def recorder():
    global started, p, stream, frames

    if listener.key_pressed and not started:
        # Start the recording
        try:
            stream = p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK,
                             stream_callback = callback)
            print("Stream active:", stream.is_active())
            started = True
            print("start Stream")
        except:
            raise

    elif not listener.key_pressed and started:
        print("Stop recording")
        stream.stop_stream()
        stream.close()
        p.terminate()
        listener.wf.writeframes(b''.join(frames))
        listener.wf.close()
        return
    # Reschedule the recorder function in 100 ms.
    task.enter(0.1, 1, recorder, ())

def react_to_recording():
    try:
        r = sr.Recognizer()
        audio_file = sr.AudioFile(wav_file)
        with audio_file as source:
            audio = r.record(source)
        command = r.recognize_google(audio)
        print(command)
        return command
    except:
        pass

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', "com.apple.speech.synthesis.voice.yuna") # KO: com.apple.speech.synthesis.voice.yuna # Hindi: com.apple.speech.synthesis.voice.lekha
    engine.startLoop(False)
    engine.say(text)
    engine.iterate()
    time.sleep(0.10*len(text))
    engine.endLoop()

def my_translation(response):
    try:
        translator = Translator()
        response = translator.translate(response, src='en', dest='ko').pronunciation # hi, ja, ko
    except:
        pass
    return response

def respond_to_command(text):
    if text == "":
        return
    print(text)
    if text.startswith("python"):
        python_logic(text)
    else:
        regular_logic(text)

def python_logic(text):
    if "if" in text:
        text = """if condition:
    pass
else:
    pass"""
    clip.copy(text)
    time.sleep(0.25)
    keyboard2 = Controller()
    keyboard2.press(Key.cmd.value)
    keyboard2.press('v')

def regular_logic(text):
    clip.copy(text)
    time.sleep(0.25)
    keyboard2 = Controller()
    keyboard2.press(Key.cmd.value)
    keyboard2.press('v')

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
while True:
    p = pyaudio.PyAudio()
    frames = []
    listener = MyListener()
    listener.start()
    started = False
    stream = None
    print("Press and hold the 'ctrl' key to begin recording")
    print("Release the 'ctrl' key to end recording")
    task = sched.scheduler(time.time, time.sleep)
    task.enter(0.1, 1, recorder, ())
    task.run()
    command = react_to_recording()
    command = "" if command == None else command.lower()
    response = command
    if command.startswith("python"):
        best_match = process.extractOne(command, voice_commands.keys())[0]
        response = voice_commands.get(best_match, command)
    respond_to_command(response)
    # response = my_translation(response)
    # speak_text(response)
    previously_listening = False

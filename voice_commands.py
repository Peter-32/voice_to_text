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
import pandas as pd

import pyaudio
import pyautogui as g
import pyperclip as clip
import speech_recognition as sr
from pynput.keyboard import Listener, KeyCode
from pynput.keyboard import Key, Controller

g.size()
g.FAILSAFE = True
g.PAUSE = 0

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
    engine.startLoop(False)
    engine.say(text)
    engine.iterate()
    time.sleep(0.10*len(text))
    engine.endLoop()
    
def append_ideas_to_list(text):
    if text == "":
        return
    clip.copy(text)
    time.sleep(1)
    print(text)
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
    append_ideas_to_list(response)
    # speak_text(response)
    previously_listening = False
    



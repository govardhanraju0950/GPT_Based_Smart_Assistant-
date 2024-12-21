import openai
from apikey import api_data 
import os
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import pyttsx3
import webbrowser
import tempfile
import speech_recognition as sr

Model = "gpt-4o"
client = openai.OpenAI(api_key=api_data)

# GPT-4 Response Function
def Reply(question):
    completion = client.chat.completions.create(
        model=Model,
        messages=[
            {'role':"system","content":"You are a helpful assistant"},
            {'role':'user','content':question}
        ],
        max_tokens=200
    )
    answer = completion.choices[0].message.content
    return answer 

# Text to Speech Engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

speak("Hello, how are you?")

# Capture Audio with Sounddevice
def takeCommand():
    try:
        print('Listening .......')
        fs = 44100  # Sample rate
        seconds = 5  # Duration
        print("Recording for 5 seconds...")
        audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

        # Save audio to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            wav.write(temp_audio.name, fs, audio)
            temp_audio_path = temp_audio.name

        # Use Recognizer
        r = sr.Recognizer()
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = r.record(source)
            query = r.recognize_google(audio_data, language='en-in')
            print("User Said: {} \n".format(query))
            return query.lower()
    except Exception as e:
        print("Say that again .....")
        return "none"

if __name__ == '__main__':
    while True: 
        query = takeCommand()
        if query == 'none':
            continue

        ans = Reply(query)
        print(ans)
        speak(ans)

        # Specific Browser Related Tasks 
        if "open youtube" in query: 
            webbrowser.open('www.youtube.com')
        if "open google" in query: 
            webbrowser.open('www.google.com')
        if "bye" in query:
            break

import pyttsx3
import datetime
import speech_recognition as s
import requests
from bs4 import BeautifulSoup
from utils.location import get_location

# python text to speech with inbuilt windows voices
speak_engine = pyttsx3.init('sapi5')
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[1].id)


# Speak function for python to speak something
def speak(audio):
    speak_engine.say(audio)
    speak_engine.runAndWait()


# Wish me first
def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour <= 12:
        speak("Good Morning Sir")
    elif 12 < hour <= 18:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")


# Get temperature
def get_temperature():
    search = f'temperature in {get_location()}'
    url = f'https://www.google.com/search?q={search}'
    response = requests.get(url)
    data = BeautifulSoup(response.text,"html.parser")
    to_speak = data.find("div",class_="BNeawe").text
    speak(f'current {search} is {to_speak}')


# Take command
def get_command():
    listerner = s.Recognizer()
    with s.Microphone() as source:
        speak("How may i help you!")
        listerner.pause_threshold = 1
        audio = listerner.record(source,duration=5)

        try:
            query = listerner.recognize_google(audio,language="en-in")
            lower_query = str(query.lower())
            if lower_query.find("weather") >= 0:
                get_temperature()
        except:
            speak("Some error occured")


# main function
if __name__ == "__main__":
    wish_me()
    get_command()
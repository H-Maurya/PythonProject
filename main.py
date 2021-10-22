import pyttsx3  # python text to speech module
import datetime  # python datetime module
import speech_recognition as s  # google speech_recognition library
import requests  # working with apis
import bs4  # package to parse html and xml data
from utils.location import get_location  # using own module
import wikipedia  # wikipedia api module for searching query
from utils.email import sendMail  # using own module

# python text to speech with inbuilt windows voices
speak_engine = pyttsx3.init('sapi5')
# getting all voices present in windows machine
voices = speak_engine.getProperty('voices')
# setting voice
speak_engine.setProperty('voice', voices[1].id)


# Speak function for python to speak something
def speak(audio):
    # speaks the string audio
    speak_engine.say(audio)
    # runs and waits
    speak_engine.runAndWait()


# Wish me first
def wish_me():
    # first getting time
    hour = int(datetime.datetime.now().hour)
    # if time between 0 to 12 say Good Morning
    if 0 <= hour <= 12:
        speak("Good Morning Sir")
    # if time between 12 to 18 say Good Afternoon
    elif 12 < hour <= 18:
        speak("Good Afternoon Sir")
    # else say Good Evening
    else:
        speak("Good Evening Sir")
    speak("Your voice assistant is ready to serve you!")


# End wish
def end_wish():
    hour = int(datetime.datetime.now().hour)
    # if night time say Good Night
    if 18 < hour < 24:
        speak("Good Night!! Hope we meet soon")
    # else say this
    else:
        speak("Have a nice day, sir")


# Get temperature
def get_temperature():
    # search query and getting current location
    search = f'temperature in {get_location()}'
    # searching google for current temperature
    url = f'https://www.google.com/search?q={search}'
    # get request to url
    response = requests.get(url)
    # playing with Html data
    data = bs4.BeautifulSoup(response.text,"html.parser")
    # extracting temperature from data
    to_speak = data.find("div",class_="BNeawe").text
    # output results
    speak(f'current {search} is {to_speak}')


# Take command
def get_command():
    # initialising speech recogniser
    listeners = s.Recognizer()
    # activating microphone as source
    with s.Microphone() as source:
        # wait for 1 second if no sound detected
        listeners.pause_threshold = 1
        # microphone as source getting data
        audio = listeners.record(source, duration=2)
        try:
            # get text from speech using google
            source_data = listeners.recognize_google(audio, language="en-in")
            # to lowercase
            lower_query = str(source_data.lower())
            return lower_query
        except Exception as e:
            # if exception print it
            print(e)
            speak("Could you please say it again")
            # if spoken nothing return none
            return None


# getting a valid command
def get_not_empty_command():
    message = get_command()
    # while message is null retake input
    while message is None:
        message = get_command()
    # if message becomes not null return
    return message


# wikipedia command
def search_wiki():
    speak("What you want to search ?")
    # getting query to search
    search = get_not_empty_command()
    # searching query via wikipedia api
    result = wikipedia.summary(search, sentences=2)
    # providing information to user
    speak(f"According to wikipedia {result}")


# send mails
def send_email():
    speak("To whom you want to send mail")
    # email receivers name input
    receiver = get_not_empty_command()
    # dictionary containing predefined emails
    receiver_data = {"me": "mihirwaykole1703@yahoo.com"}
    if receiver in receiver_data:
        speak("Tell me what message to send")
        # message to send input
        message = get_not_empty_command()
        # sending email
        sendMail(receiver_data[receiver], message)
    else:
        speak("Sender not in list try saying email address")
        # get sender email id
        email = get_not_empty_command()
        speak("Tell me what message to send")
        # message to send input
        message = get_not_empty_command()
        # sending email
        sendMail(email, message)


# main function
if __name__ == "__main__":
    # wishing the user
    wish_me()
    when_to_close = True
    # if user said exit we will exit
    while when_to_close:
        speak("How may i help you!")
        query = get_not_empty_command()
        # searching wikipedia
        if 'wikipedia' in query:
            search_wiki()
        # to know temperature
        elif 'temperature today' in query:
            get_temperature()
        # for emailing
        elif 'email' in query:
            send_email()
        # for exiting
        elif 'exit' in query:
            when_to_close = False
    # wish user good night if it is night else good day
    end_wish()

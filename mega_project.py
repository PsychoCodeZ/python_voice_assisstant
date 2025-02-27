import speech_recognition as sr
import webbrowser 
import pyttsx3
import music_library
import requests
import google.generativeai as genai
from gtts import gTTS
import pygame
import os

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "Enter you own"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()
def speak(text): # this is use to speak in aa better form
    tts = gTTS(text)
    tts.save("temp.mp3") 
    # Initialize the mixer module
    pygame.mixer.init()
    
    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")
    
    # Play the MP3 file
    pygame.mixer.music.play()
    
    # Keep the script running until the music stops
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  
    
    pygame.mixer.music.unload()   # this is use to stop the music      
    os.remove("temp.mp3")  # this is use to remove the file after the work is done
    

def gemini_ai(command):
       genai.configure(api_key="make your own")
       model = genai.GenerativeModel("gemini-1.5-flash")
       response = model.generate_content(command)
       speak(response.text)

def processCommand(c):
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("www.google.com")
    elif "open youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("www.youtube.com")   
    elif "open facebook" in c.lower():
        speak("Opening Facebook")
        webbrowser.open("www.facebook.com")   
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = music_library.music[song]  # this is the link to the song which is stored in the music_library.py file in bracket it is the key of the song
        webbrowser.open(link)
    elif "open linkedin" in c.lower():
        speak("Opening LinkedIn")
        webbrowser.open("www.linkedin.com")  
    elif "news" in c.lower():
        speak("Opening news")
        r = requests.get(f"http://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")  
        if r.status_code == 200:
            # parse the json response
            data = r.json()
            # extract the news articles
            articles = data.get('articles', [])
            if not articles:
             speak("Sorry, no news articles available right now.")
            
            # print the headlines
            for article in articles:
                speak(article['title'])
        
        else:
            print(f"Failed to fetch news. Status code: {r.status_code}")
    else:
        # if the command is not recognized        
        # let gemini handle the command
        gemini_ai(c)

if __name__ == '__main__':
    speak("Initializing Jarvis.....")
    while True:
        # listen for the wake word "didi"
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        try:
            command = recognizer.recognize_google(audio)
            if "jarvis" in command.lower():
                speak("hey sijju...")
                # listen for the command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except Exception as e:
            print("An error occurred: {0}".format(e))

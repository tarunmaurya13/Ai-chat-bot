import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import google.generativeai as genai
from gtts import gTTS
import pygame
import os
import time

# Initialize Recognizer & TTS Engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "28ba6dfafb114cd2b46dddfc5af8378f"  # Replace with your News API key
gemini_api_key = "AIzaSyDHNMsx1l0ZQTj3bsZU7w6-HpvtX3cffpE"  # Replace with your Gemini API key

# Configure Gemini AI
genai.configure(api_key=gemini_api_key)

def speak(text):
    """Text-to-Speech using gTTS & Pygame"""
    if not text:
        return  # Prevent empty speech attempts

    print(f"Jarvis: {text}")  # Debugging print

    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    """Uses Gemini AI API to generate responses"""
    model = genai.GenerativeModel("AIzaSyDHNMsx1l0ZQTj3bsZU7w6-HpvtX3cffpE")

    try:
        response = model.generate_content(command)
        if response and hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content
        else:
            return "Sorry, I couldn't process that request."
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "There was an issue connecting to Gemini AI."

def processCommand(c):
    """Processes voice commands"""
    c = c.lower()

    if "open google" in c:
        speak("Opening Google...")
        webbrowser.open("https://google.com")

    elif "open facebook" in c:
        speak("Opening Facebook...")
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c:
        speak("Opening YouTube...")
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c:
        speak("Opening LinkedIn...")
        webbrowser.open("https://linkedin.com")

    elif "news" in c:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={"28ba6dfafb114cd2b46dddfc5af8378f"}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])

                if articles:
                    speak("Here are the latest news headlines:")
                    for article in articles[:5]:  # Read only the top 5 news headlines
                        speak(article['title'])
                else:
                    speak("No news articles found.")
            else:
                speak("Failed to fetch news.")
        except Exception as e:
            print(f"News API Error: {e}")
            speak("There was an issue fetching the news.")

    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("\nListening for 'Jarvis' wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

            word = recognizer.recognize_google(audio).lower()
            print(f"You said: {word}")  # Debugging print

            if word == "jarvis":
                speak("Yes, how can I help?")

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    print("Listening for command...")
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio).lower()
                print(f"Command received: {command}")  # Debugging print
                
                processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Speech Recognition error: {e}")
        except Exception as e:
            print(f"Error: {e}")

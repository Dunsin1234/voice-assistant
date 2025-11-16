import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyjokes
import sys
import time

engine=None

def setjarvisvoice(engine):
    voices=engine.getProperty("voices")
    chosen=None
    for v in voices:
        try:
            name=v.name.lower()
        except:
            name=str(v.id).lower()
        if "male" in name:
            chosen=v
            break
    if chosen is None and len(voices)>0:
        chosen=voices[0]
    if chosen is not None:
        try:
            engine.setProperty("voice",chosen.id)
        except:
            pass
    engine.setProperty("rate",140)
    engine.setProperty("volume",1.0)

def speak(text):
    print(f"Assistant: {text}")
    global engine
    if engine is None:
        return
    try:
        ssml_text=f'<pitch middle="-6">{text}</pitch>'
        engine.say(ssml_text)
        engine.runAndWait()
    except Exception as e:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e2:
            print("Audio output not supported in this environment.")

def wishuser():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good morning!")
    elif hour>=12 and hour<18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your voice assistant. How can I help you today?")

def takecommand():
    r=sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold=1
            audio=r.listen(source,timeout=5,phrase_time_limit=8)
        try:
            print("Recognizing...")
            command=r.recognize_google(audio,language="en-US")
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("I didn't catch that, please say it again.")
            return "none"
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return "none"
        except Exception:
            speak("I didn't catch that, please say it again.")
            return "none"
    except Exception:
        try:
            return input("Mic not available — type your command: ").lower()
        except Exception:
            return "exit"

def runassistant():
    wishuser()
    while True:
        command=takecommand()
        if command is None:
            continue
        if command.strip()=="":
            continue

        if "wikipedia" in command:
            speak("Searching Wikipedia...")
            query=command.replace("wikipedia","").strip()
            if query=="":
                speak("Please tell me what to search on Wikipedia.")
                continue
            try:
                result=wikipedia.summary(query,sentences=2)
                speak(result)
            except Exception:
                speak("I couldn't find that on Wikipedia.")

        elif "open youtube" in command:
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")

        elif "open google" in command:
            speak("Opening Google...")
            webbrowser.open("https://www.google.com")

        elif "open stackoverflow" in command or "stack overflow" in command:
            speak("Opening Stack Overflow...")
            webbrowser.open("https://stackoverflow.com")

        elif "joke" in command or "tell me a joke" in command:
            try:
                joke=pyjokes.get_joke()
                speak(joke)
            except Exception:
                speak("I couldn't fetch a joke right now.")

        elif "time" in command or "what time" in command:
            now=datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {now}")

        elif command in ["exit","quit","stop","bye","goodbye"]:
            speak("Goodbye!")
            break

        else:
            speak("Sorry, I didn't understand that. Try again.")

if __name__=="__main__":
    try:
        engine=pyttsx3.init()
        setjarvisvoice(engine)
    except Exception:
        engine=None
        print("Warning: TTS engine could not be initialized. Audio output may be unavailable.")
    try:
        runassistant()
    except KeyboardInterrupt:
        speak("Shutting down. Goodbye!")
        try:
            sys.exit(0)
        except:
            pass

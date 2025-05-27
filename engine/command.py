import pyttsx3
import speech_recognition as sr
import eel
import time
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id) # 3 voices in my system [0]-female, [1]-male, [2]-female
    engine.setProperty('rate', 174) #speed of the voice
    eel.DisplayMessage(text)
    engine.say(text) #speak according to the given text
    engine.runAndWait() #delay while speaking 

def takecommand():

    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source)

        audio=r.listen(source, 10,20)
    try:
        print("Recognizing")
        query=r.recognize_google(audio,language='en-in')
        print(f"User said: {query}")
        time.sleep(2)
        
    except Exception as e:
        return ""
    return query.lower()
@eel.expose
def allCommands():
    query=takecommand()
    print(query)

    if "open" in query:
        from engine.features import openCommand
        openCommand(query)
    elif "on youtube" in query:
        from engine.features import PlayYoutube
        PlayYoutube(query)

    else:
        print("Not running")

    eel.ShowHood()
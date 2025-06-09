import pyttsx3
import speech_recognition as sr
import eel
import time
import engine.features as features
from engine.search_files import findAndOpenFile 

engine = pyttsx3.init()

def speak(text):
    if features.interrupt_flag:
        print("[Speak] Interrupted before speaking.")
        return

    text = str(text)
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)

    eel.DisplayMessage(text)
    eel.receiverText(text)

    engine.say(text)

    # Run and wait but allow interrupt by checking flag
    try:
        engine.runAndWait()
    except RuntimeError:
        print("[Speak] Runtime error in pyttsx3")

    if features.interrupt_flag:
        engine.stop()
        print("[Speak] Interrupted during speech.")


def takecommand():

    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        eel.DisplayMessage('listening....')
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source)

        audio=r.listen(source, 10,6)
    try:
        print("Recognizing")
        eel.DisplayMessage('recognizing....')
        query=r.recognize_google(audio,language='en-in')
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        
    except Exception as e:
        return ""
    return query.lower()
    
@eel.expose
def allCommands(message=1):
    import engine.features as features
    features.interrupt_flag = False  # reset before new command

    if message==1:
        query=takecommand()
        print(query)
        eel.senderText(query)
    else:
        query=message
        eel.senderText(query)

    query = query.lower()

    try:
        if features.interrupt_flag:
            return
        
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            message = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    message = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    message = 'call'
                else:
                    message = 'video call'
                    
                whatsApp(contact_no, query, message, name)
        elif "temperature" in query or "weather" in query:
            from engine.features import getTemperature    
            getTemperature(query)
        
        elif "open file" in query or "search file" in query or "find file" in query:
            print(f"[DEBUG] Recognized file open/search command: '{query}'")
            findAndOpenFile(query)


        else:
            from engine.features import chatBot
            features.interrupt_flag = False
            chatBot(query)
    except:
        print("Error")

    eel.ShowHood()
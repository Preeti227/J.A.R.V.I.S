import pyttsx3
import speech_recognition as sr
import eel
import time
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id) # 3 voices in my system [0]-female, [1]-male, [2]-female
    engine.setProperty('rate', 174) #speed of the voice
    #eel.DisplayMessage(text)
    engine.say(text) #speak according to the given text
    eel.receiverText(text) #jarvis will speak the chatbox message
    engine.runAndWait() #delay while speaking 

def takecommand():

    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source)

        audio=r.listen(source, 10,6)
    try:
        print("Recognizing")
        query=r.recognize_google(audio,language='en-in')
        print(f"User said: {query}")
        time.sleep(2)
        
    except Exception as e:
        return ""
    return query.lower()
@eel.expose
def allCommands(message=1):
    if message==1:
        query=takecommand()
        print(query)
        eel.senderText(query)
    else:
        query=message
        eel.senderText(query)

    try:

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

        else:
            print("Not running")
    except:
        print("Error")

    eel.ShowHood()
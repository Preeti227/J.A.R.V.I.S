import os
import re
from shlex import quote
import struct
import subprocess
import time
import webbrowser
import eel
import pvporcupine
import pyaudio
import pyautogui
import requests

from engine.config import ASSISTANT_NAME
import requests
import sqlite3
import pywhatkit as kit
from engine.helper import extract_yt_term, remove_words
import engine.features as features
from engine.search_files import findAndOpenFile

interrupt_flag = False


con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def cancelExecution():
    print("Cancel execution called!")
    features.interrupt_flag = True
    from engine.command import engine
    engine.stop()       # Immediately stop any speaking
    eel.ShowHood()


def openCommand(query):
    from engine.command import speak,takecommand

    if features.interrupt_flag:
        print("Execution interrupted!")
        return

    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")



def PlayYoutube(query):
    from engine.command import speak

    if features.interrupt_flag:
        print("Execution interrupted!")
        return
    search_term=extract_yt_term(query)
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Sorry, I couldn't understand what to play on YouTube.")

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

 #find contacts       
def findContact(query):
    from engine.command import speak
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    from engine.command import speak

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

#Chatbot using gemini
import google.generativeai as genai
def chatBot(query):

    from engine.command import speak

    # Immediately exit if interrupted
    if features.interrupt_flag:
        print("Execution interrupted")
        return

    from engine.credentials import API_KEY
 
    genai.configure(api_key=API_KEY)

    try:
        user_input = query.lower()
        model = genai.GenerativeModel('gemini-1.5-flash') 
        chat = model.start_chat(history=[]) 

        # Double-check interrupt before sending
        if features.interrupt_flag:
            print("Execution interrupted before sending message!")
            return

        response = chat.send_message(user_input)

        if features.interrupt_flag:
            print("Execution interrupted after response, before speaking!")
            return

        reply = response.text.strip()        
        print(reply)
        speak(reply) 
        
        return reply

    except Exception as e:
        print(f"ChatBot Error: {str(e)}")
        speak("Sorry, I couldn't get a response from Gemini.")
        return "Error"

#Temperature feature
def getTemperature(query=None):
    from engine.command import speak, takecommand
    if features.interrupt_flag:
        print("Execution interrupted!")
        return
    city = None
    
    if query:
        # Extract city name from text query
        city = query.lower()
        for word in ["temperature", "in", "what's", "what is", "tell me", "the", "of", "jarvis"]:
            city = city.replace(word, "")
        city = city.strip()
    
    if not city:
        speak("Which city's temperature would you like to know?")
        city = takecommand()
        if not city:
            speak("Sorry, I didn't catch the city name.")
            return
    
    from engine.credentials import api_key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url).json()
        if response.get("cod") == 200:
            temp = response["main"]["temp"]
            condition = response["weather"][0]["description"]
            speak(f"The temperature in {city.title()} is {temp} degree Celsius with {condition}.")
        else:
            speak("City not found or unable to get weather data.")
    except Exception as e:
        print("Weather API error:", e)
        speak("Sorry, I couldn't fetch the temperature right now.")

def makeCall(name, mobileNo):
    from engine.command import speak
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    #command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    command = 'adb shell service call phone 1 s16 "tel:'+mobileNo
    os.system(command)





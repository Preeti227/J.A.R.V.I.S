import re
from engine.command import speak
from engine.config import ASSISTANT_NAME
import os
import pywhatkit as kit

def openCommand(query):
    query=query.replace(ASSISTANT_NAME,"")
    query=query.replace("open","")
    query=query.lower()

    if query!="":
        speak("Opening"+query)
        os.system('start '+query)
    else:
        speak("Not found")

def PlayYoutube(query):
    search_term=extract_yt_term(query)
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Sorry, I couldn't understand what to play on YouTube.")

def extract_yt_term(command):
    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name; otherwise, return None
    return match.group(1) if match else None

import os
import webbrowser
import eel
from engine.command import *

def start():
    #print("Starting Eel frontend...", flush=True)
    eel.init("www")

    try:
        webbrowser.open("http://localhost:8000/index.html")
    except Exception as e:
        print("Browser failed to open:", e)

    eel.start('index.html', mode=None, host='localhost', block=False)

    while True:
        eel.sleep(1)  # Keep the process alive

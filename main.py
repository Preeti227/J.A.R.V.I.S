import os
import webbrowser
import eel
from engine.command import *

def start():
    #print("Starting Eel frontend...", flush=True)
    eel.init("www")

    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)
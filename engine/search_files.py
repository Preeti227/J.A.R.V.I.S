import os
import re
import eel



# Default path to search in
DEFAULT_SEARCH_PATH = r"C:\Users\parth"

# Function to search files recursively
def search_files(filename, search_path=DEFAULT_SEARCH_PATH):
    matches = []
    print(f"Walking directory: {search_path}")
    
    for root, dirs, files in os.walk(search_path):
        for file in files:
            #print(f"[DEBUG] Found file: {file}")
            if filename.lower() in file.lower():
                full_path = os.path.join(root, file)
                #print(f"[MATCHED] {full_path}")
                matches.append(full_path)

    return matches

# Extract the filename from query like "open file main.pdf"
def extract_filename(query):
    # Flexible regex: captures filename after open/search and optional filler words
    pattern = r"(?:open|search|find)(?:\s+(?:the|my|a))?\s+(?:file\s+)?(.+\.\w+)"
    match = re.search(pattern, query, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""


# Main exposed function to be called from JS or handler
@eel.expose
def findAndOpenFile(query):
    from engine.command import speak
    #print(f"[DEBUG] findAndOpenFile called with query: '{query}'")
    
    filename = extract_filename(query)
    print(f"Extracted filename: '{filename}'")
    
    if not filename:
        print("No filename specified in query.")        
        eel.DisplayMessage("Please specify the filename to open.")
        speak("No filename specified in query")
        return

    print(f"Searching for '{filename}' in '{DEFAULT_SEARCH_PATH}'")
    eel.DisplayMessage(f"Searching for '{filename}'")
    results = search_files(filename)

    if results:
        path_to_open = os.path.abspath(results[0])
        #print(f"[DEBUG] Attempting to open: {path_to_open}")

        if os.path.exists(path_to_open):
            try:
                os.startfile(path_to_open)
                print("File opened successfully.")                
                eel.DisplayMessage(f"Opening file: {os.path.basename(path_to_open)}")
                speak("File opened successfully")
            except Exception as e:
                print(f"[ERROR] Failed to open file: {e}")
                eel.DisplayMessage(f"Error: Could not open file: {e}")
                speak(f"[ERROR] Failed to open file: {e}")
        else:
            print(f"[ERROR] File does not exist: {path_to_open}")            
            eel.DisplayMessage("File path does not exist.")
            speak(f"[ERROR] File does not exist: {path_to_open}")
    else:
        print("File not found!")
        eel.DisplayMessage("File not found.")
        speak("File not found")

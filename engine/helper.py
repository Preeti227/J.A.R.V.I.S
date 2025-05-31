import re


def extract_yt_term(command):

    # Extensive list of patterns
    patterns = [
        r'play\s+(.*?)\s+on\s+youtube',
        r'play\s+(.*?)\s+youtube',
        r'play\s+(.*?)\s+video',
        r'can you play\s+(.*?)\s+on\s+youtube',
        r'i want to play\s+(.*?)\s+on\s+youtube',
        r'could you play\s+(.*?)\s+on\s+youtube',
        r'would you play\s+(.*?)\s+on\s+youtube',
        r'please play\s+(.*?)\s+on\s+youtube',
        r'search\s+for\s+(.*?)\s+on\s+youtube',
        r'look\s+up\s+(.*?)\s+on\s+youtube',
        r'show me\s+(.*?)\s+on\s+youtube',
        r'find\s+(.*?)\s+on\s+youtube',
        r'play\s+the\s+song\s+(.*?)\s+on\s+youtube',
        r'play\s+the\s+video\s+(.*?)\s+on\s+youtube',
        r'play\s+the\s+(.*?)\s+on\s+youtube',
        r'play\s+(.*?)\s+from\s+youtube',
        r'play\s+(.*)'  # fallback pattern
    ]
#Looping through the patterns possible
    for pattern in patterns:
        # Use re.search to find the match in the command
        match = re.search(pattern, command, re.IGNORECASE)
        # If a match is found, return the extracted song name; otherwise, return None
        if match:
            return match.group(1).strip()

    return None


def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string

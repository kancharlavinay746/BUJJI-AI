import webbrowser
import subprocess
import datetime
from voice.speak import speak

def execute(command):

    command = command.lower()

    if "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        return True

    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        return True

    elif "chrome" in command:
        speak("Opening Chrome")
        webbrowser.open("https://google.com")
        return True

    elif "notepad" in command:
        speak("Opening Notepad")
        subprocess.Popen("notepad.exe")
        return True

    elif "calculator" in command:
        speak("Opening Calculator")
        subprocess.Popen("calc.exe")
        return True

    elif "time" in command:
        current = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current}")
        return True

    elif "exit" in command:
        speak("Goodbye")
        exit()

    return False
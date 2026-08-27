import os
import subprocess
import webbrowser
from urllib.parse import quote
import shutil
import re


class CommandHandler:

    def __init__(self):
        print("Command Handler loaded.")


    # =========================================================
    # OPEN APPLICATION
    # =========================================================

    def open_application(self, app_name):

        app_name = app_name.lower().strip()

        applications = {

            "chrome": [
                "chrome.exe"
            ],

            "google chrome": [
                "chrome.exe"
            ],

            "edge": [
                "msedge.exe"
            ],

            "microsoft edge": [
                "msedge.exe"
            ],

            "notepad": [
                "notepad.exe"
            ],

            "calculator": [
                "calc.exe"
            ],

            "calc": [
                "calc.exe"
            ],

            "explorer": [
                "explorer.exe"
            ],

            "file explorer": [
                "explorer.exe"
            ],

            "paint": [
                "mspaint.exe"
            ],

            "task manager": [
                "taskmgr.exe"
            ]
        }

        if app_name not in applications:

            return False

        executable = applications[app_name][0]

        try:

            subprocess.Popen(
                executable,
                shell=True
            )

            print(
                f"✅ Opened {app_name}"
            )

            return True

        except Exception as e:

            print(
                f"❌ Could not open {app_name}"
            )

            print(e)

            return False


    # =========================================================
    # OPEN WEBSITE
    # =========================================================

    def open_website(self, website):

        website = website.lower().strip()

        websites = {

            "youtube":
                "https://www.youtube.com",

            "google":
                "https://www.google.com",

            "gmail":
                "https://mail.google.com",

            "github":
                "https://github.com",

            "chatgpt":
                "https://chatgpt.com",

            "instagram":
                "https://www.instagram.com",

            "facebook":
                "https://www.facebook.com"
        }

        if website not in websites:

            return False

        try:

            webbrowser.open(
                websites[website]
            )

            print(
                f"✅ Opened {website}"
            )

            return True

        except Exception as e:

            print(
                f"❌ Could not open {website}"
            )

            print(e)

            return False


    # =========================================================
    # SEARCH WEB
    # =========================================================

    def search_web(self, query):

        query = query.strip()

        if not query:

            return False

        url = (
    "https://www.google.com/search?q="
    + quote(query)
)
        

        webbrowser.open(url)

        print(
            f"🔎 Searching Google for: {query}"
        )

        return True


    # =========================================================
    # HANDLE COMMAND
    # =========================================================

    def handle(self, command):

        if not command:

            return False

        command = command.lower().strip()

        print()
        print(
            f"⚙️ Processing command: {command}"
        )


        # =====================================================
        # EXIT
        # =====================================================

        if command in [
            "exit",
            "quit",
            "stop",
            "shutdown assistant"
        ]:

            print(
                "👋 BUJJI shutting down..."
            )

            return "EXIT"


        # =====================================================
        # OPEN APPLICATION
        # =====================================================

        if command.startswith("open "):

            target = command[
                len("open "):
            ].strip()


            # Try application first

            if self.open_application(
                target
            ):

                return True


            # Try website

            if self.open_website(
                target
            ):

                return True


            # If neither worked,
            # search the web

            print(
                f"🔎 '{target}' not found as an app."
            )

            return self.search_web(
                target
            )


        # =====================================================
        # SEARCH
        # =====================================================

        search_patterns = [
            r"search for (.+)",
            r"search (.+)",
            r"google (.+)",
            r"look up (.+)"
        ]

        for pattern in search_patterns:

            match = re.match(
                pattern,
                command
            )

            if match:

                query = match.group(1)

                return self.search_web(
                    query
                )


        # =====================================================
        # OPEN YOUTUBE
        # =====================================================

        if "youtube" in command:

            return self.open_website(
                "youtube"
            )


        # =====================================================
        # OPEN GOOGLE
        # =====================================================

        if "google" in command:

            return self.open_website(
                "google"
            )


        # =====================================================
        # UNKNOWN COMMAND
        # =====================================================

        print(
            "⚠️ I don't understand that command yet."
        )

        return False


# =============================================================
# TEST COMMAND HANDLER
# =============================================================

if __name__ == "__main__":

    handler = CommandHandler()

    print()
    print("Command Handler Test")
    print("=" * 40)

    while True:

        command = input(
            "Enter command: "
        )

        result = handler.handle(
            command
        )

        if result == "EXIT":

            break
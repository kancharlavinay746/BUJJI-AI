import json
import re

from brain.ai_manager import ai_manager

from actions.app_index import launch_application

from actions.apps import (
    open_file_explorer,
    open_cmd,
    open_powershell,
    open_task_manager,
)

from actions.browser import (
    open_youtube,
    open_google,
)

from actions.system import (
    open_settings,
)


class Router:

    def __init__(self):
        print("🔀 BUJJI Intelligent Router initialized.")

    # =====================================================
    # AI CLASSIFICATION
    # =====================================================

    def classify(self, command):

        prompt = f"""
You are BUJJI, a Windows desktop AI command router.

Understand the user's natural-language command.

Return ONLY valid JSON.

Allowed intents:

OPEN_APP
OPEN_WEBSITE
SYSTEM_ACTION
GENERAL_AI

Rules:

1. OPEN_APP means the user wants to launch an installed
   Windows application.

2. OPEN_WEBSITE means the user wants a website opened.

3. SYSTEM_ACTION means the user wants a Windows/system
   action.

4. GENERAL_AI means the user is asking a question or
   requesting normal AI assistance.

Examples:

User: "open spotify"
JSON:
{{"intent":"OPEN_APP","target":"spotify"}}

User: "please launch discord"
JSON:
{{"intent":"OPEN_APP","target":"discord"}}

User: "can you start visual studio code"
JSON:
{{"intent":"OPEN_APP","target":"visual studio code"}}

User: "open youtube"
JSON:
{{"intent":"OPEN_WEBSITE","target":"youtube"}}

User: "search google"
JSON:
{{"intent":"OPEN_WEBSITE","target":"google"}}

User: "open task manager"
JSON:
{{"intent":"SYSTEM_ACTION","target":"task manager"}}

User: "open file explorer"
JSON:
{{"intent":"SYSTEM_ACTION","target":"file explorer"}}

User: "open command prompt"
JSON:
{{"intent":"SYSTEM_ACTION","target":"command prompt"}}

User: "open powershell"
JSON:
{{"intent":"SYSTEM_ACTION","target":"powershell"}}

User: "open settings"
JSON:
{{"intent":"SYSTEM_ACTION","target":"settings"}}

User: "what is machine learning?"
JSON:
{{"intent":"GENERAL_AI","target":""}}

User command:
{command}

Return ONLY JSON.
"""

        try:

            response = ai_manager.ask(
                prompt
            )

            print(
                f"🧠 AI classification: {response}"
            )

            # Remove markdown code fences if AI adds them
            response = re.sub(
                r"```json|```",
                "",
                response
            ).strip()

            result = json.loads(
                response
            )

            if not isinstance(
                result,
                dict
            ):

                raise ValueError(
                    "AI returned invalid JSON object."
                )

            return result

        except Exception as e:

            print(
                f"❌ Classification error: {e}"
            )

            return {
                "intent": "GENERAL_AI",
                "target": ""
            }

    # =====================================================
    # SYSTEM ACTIONS
    # =====================================================

    def system_action(self, target):

        target = target.lower().strip()

        if "task manager" in target:

            open_task_manager()

            return "Opening Task Manager."

        if (
            "file explorer" in target
            or "explorer" in target
        ):

            open_file_explorer()

            return "Opening File Explorer."

        if (
            "command prompt" in target
            or target == "cmd"
        ):

            open_cmd()

            return "Opening Command Prompt."

        if "powershell" in target:

            open_powershell()

            return "Opening PowerShell."

        if "settings" in target:

            open_settings()

            return "Opening Windows Settings."

        return None

    # =====================================================
    # WEBSITE ACTION
    # =====================================================

    def website_action(self, target):

        target = target.lower().strip()

        if "youtube" in target:

            open_youtube()

            return "Opening YouTube."

        if "google" in target:

            open_google()

            return "Opening Google."

        # Unknown website:
        # open Google so the user can search it.

        open_google()

        return f"Opening Google to search for {target}."

    # =====================================================
    # MAIN ROUTER
    # =====================================================

    def route(self, command):

        command = command.strip()

        if not command:

            return "I didn't hear a command."

        print()
        print("=" * 60)
        print(
            f"🎤 BUJJI COMMAND: {command}"
        )
        print("=" * 60)

        result = self.classify(
            command
        )

        intent = result.get(
            "intent",
            "GENERAL_AI"
        )

        target = result.get(
            "target",
            ""
        )

        print(
            f"🎯 Intent: {intent}"
        )

        print(
            f"🎯 Target: {target}"
        )

        # =================================================
        # OPEN APPLICATION
        # =================================================

        if intent == "OPEN_APP":

            if not target:

                return (
                    "Which application "
                    "should I open?"
                )

            print(
                f"🚀 Application request: {target}"
            )

            success = launch_application(
                target
            )

            if success:

                return f"Opening {target}."

            # Application doesn't exist.
            # Browser fallback.

            print(
                f"🌐 {target} was not found."
            )

            open_google()

            return (
                f"I couldn't find {target} "
                "installed on this computer, "
                "so I opened Google."
            )

        # =================================================
        # WEBSITE
        # =================================================

        if intent == "OPEN_WEBSITE":

            return self.website_action(
                target
            )

        # =================================================
        # SYSTEM
        # =================================================

        if intent == "SYSTEM_ACTION":

            response = self.system_action(
                target
            )

            if response:

                return response

        # =================================================
        # GENERAL AI
        # =================================================

        print(
            "🤖 Sending to AI..."
        )

        return ai_manager.ask(
            command
        )


# =========================================================
# GLOBAL ROUTER
# =========================================================

router = Router()
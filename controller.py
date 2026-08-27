from voice.microphone import Microphone
from voice.vad import VoiceActivityDetector
from voice.whisper import WhisperEngine
from voice.wakeword import WakeWordDetector

from brain.router import router


class AssistantController:

    def __init__(self):

        print()
        print("🧠 Initializing BUJJI...")
        print()

        # ==============================================
        # VOICE COMPONENTS
        # ==============================================

        print("🎙️ Initializing microphone...")

        self.microphone = Microphone()

        print("🔊 Initializing voice activity detector...")

        self.vad = VoiceActivityDetector()

        print("🧠 Loading Faster-Whisper...")

        self.whisper = WhisperEngine()

        print("🎯 Initializing wake-word detector...")

        self.wakeword = WakeWordDetector()

        # ==============================================
        # STATE
        # ==============================================

        self.running = True

        print()
        print("✅ BUJJI initialized successfully.")

    # ==================================================
    # REMOVE WAKE WORD
    # ==================================================

    def remove_wake_word(self, text):

        if not text:

            return ""

        wake_words = [
            "bujji",
            "budgie",
            "budji",
            "budgy",
            "buddhi",
            "puji",
            "boojie",
            "booji"
        ]

        words = text.split()

        remaining = []

        for word in words:

            cleaned = word.lower().strip(
                ".,!?;:'\""
            )

            if cleaned not in wake_words:

                remaining.append(word)

        return " ".join(
            remaining
        ).strip()

    # ==================================================
    # LISTEN
    # ==================================================

    def listen(self):

        print(
            "🎤 Listening..."
        )

        try:

            audio = self.vad.record_until_silence(
                self.microphone
            )

        except Exception as e:

            print(
                f"❌ VAD error: {e}"
            )

            return ""

        if audio is None:

            return ""

        if len(audio) == 0:

            return ""

        print(
            "🧠 Transcribing..."
        )

        try:

            text = self.whisper.transcribe(
                audio
            )

        except Exception as e:

            print(
                f"❌ Whisper error: {e}"
            )

            return ""

        return text.strip()

    # ==================================================
    # EXIT COMMAND
    # ==================================================

    def is_exit_command(self, command):

        command_lower = command.lower().strip()

        exit_commands = [

            "exit",
            "quit",
            "stop",
            "stop bujji",
            "shutdown bujji",
            "exit bujji",
            "quit bujji"

        ]

        return command_lower in exit_commands

    # ==================================================
    # EXECUTE COMMAND
    # ==================================================

    def execute_command(self, command):

        if not command:

            return

        print()
        print(
            "⚡ Sending command to router..."
        )

        print(
            f"🔀 Command: {command}"
        )

        try:

            response = router.route(
                command
            )

        except Exception as e:

            print()
            print(
                f"❌ Router error: {e}"
            )

            return

        print()
        print(
            "🤖 BUJJI:"
        )

        print(
            response
        )

        print()

    # ==================================================
    # MAIN LOOP
    # ==================================================

    def run(self):

        print()
        print("=" * 60)
        print("                 BUJJI")
        print("=" * 60)
        print()
        print(
            "💤 BUJJI is sleeping."
        )
        print(
            "🎯 Say 'Bujji' to wake me."
        )
        print()
        print("=" * 60)

        # ==============================================
        # START MICROPHONE
        # ==============================================

        try:

            self.microphone.start()

        except Exception as e:

            print()
            print(
                "❌ BUJJI could not start the microphone."
            )

            print(
                f"Error: {e}"
            )

            return

        # ==============================================
        # CONTINUOUS ASSISTANT LOOP
        # ==============================================

        try:

            while self.running:

                print()
                print(
                    "🎤 Waiting for speech..."
                )

                # --------------------------------------
                # Listen
                # --------------------------------------

                text = self.listen()

                if not text:

                    continue

                print()
                print(
                    f"👂 Heard: {text}"
                )

                # --------------------------------------
                # Wake word
                # --------------------------------------

                if not self.wakeword.detect(text):

                    print(
                        "💤 Wake word not detected."
                    )

                    continue

                # --------------------------------------
                # BUJJI ACTIVATED
                # --------------------------------------

                print()
                print(
                    "🟢 BUJJI ACTIVATED!"
                )

                # --------------------------------------
                # Remove wake word
                # --------------------------------------

                command = self.remove_wake_word(
                    text
                )

                # --------------------------------------
                # Command in same sentence
                # --------------------------------------

                if command:

                    print(
                        f"🗣️ Command: {command}"
                    )

                # --------------------------------------
                # User only said BUJJI
                # --------------------------------------

                else:

                    print()
                    print(
                        "👂 I'm listening for your command..."
                    )

                    command = self.listen()

                    if not command:

                        print(
                            "💤 No command received."
                        )

                        continue

                    print(
                        f"🗣️ Command: {command}"
                    )

                # --------------------------------------
                # EXIT
                # --------------------------------------

                if self.is_exit_command(
                    command
                ):

                    print()
                    print(
                        "👋 Shutting down BUJJI..."
                    )

                    self.running = False

                    break

                # --------------------------------------
                # EXECUTE
                # --------------------------------------

                self.execute_command(
                    command
                )

                # --------------------------------------
                # Return to listening
                # --------------------------------------

                print()
                print(
                    "💤 Returning to sleep..."
                )

        except KeyboardInterrupt:

            print()
            print(
                "⌨️ Keyboard interrupt received."
            )

            self.running = False

        except Exception as e:

            print()
            print(
                f"❌ BUJJI main loop error: {e}"
            )

        finally:

            self.microphone.stop()

            print()
            print("=" * 60)
            print("🔴 BUJJI STOPPED")
            print("=" * 60)


# ======================================================
# BACKWARD COMPATIBILITY
# ======================================================

BujjiController = AssistantController
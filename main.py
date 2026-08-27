from voice.whisper import WhisperEngine
from actions.command_handler import CommandHandler


def main():

    print()
    print("=" * 60)
    print("🤖 BUJJI AI ASSISTANT")
    print("=" * 60)
    print()

    # Load speech recognition
    whisper = WhisperEngine()

    # Load action system
    handler = CommandHandler()

    print()
    print("✅ BUJJI is ready.")
    print()
    print("Try saying:")
    print("  Open Chrome")
    print("  Open YouTube")
    print("  Open Notepad")
    print("  Open Calculator")
    print("  Search Python tutorials")
    print()
    print("Press CTRL+C to stop.")
    print("=" * 60)


    # =====================================================
    # MAIN ASSISTANT LOOP
    # =====================================================

    while True:

        try:

            # ---------------------------------------------
            # Listen
            # ---------------------------------------------

            command = whisper.listen()

            if not command:
                continue


            # ---------------------------------------------
            # Display what BUJJI heard
            # ---------------------------------------------

            print()
            print(f"👤 USER: {command}")


            # ---------------------------------------------
            # Execute command
            # ---------------------------------------------

            result = handler.handle(command)


            # ---------------------------------------------
            # Exit
            # ---------------------------------------------

            if result == "EXIT":

                print()
                print("👋 BUJJI shutting down.")
                break


        except KeyboardInterrupt:

            print()
            print()
            print("👋 BUJJI stopped.")
            break


        except Exception as e:

            print()
            print("❌ BUJJI ERROR:")
            print(e)


# =========================================================
# START BUJJI
# =========================================================

if __name__ == "__main__":
    main()
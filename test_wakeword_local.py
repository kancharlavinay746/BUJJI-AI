from voice.wakeword import WakeWordDetector


wake = WakeWordDetector()


tests = [
    "Hey Bujji",
    "Hey budgie",
    "Bujji open task manager",
    "Puji open task manager",
    "Hello computer",
    "Open Chrome",
]


for text in tests:

    result = wake.detect(text)

    print(
        f"{text:35} -> {result}"
    )
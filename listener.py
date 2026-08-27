from voice.microphone import Microphone
from voice.vad import VoiceActivityDetector
from voice.whisper import WhisperEngine


class Listener:

    def __init__(self):
        self.microphone = Microphone()
        self.vad = VoiceActivityDetector()
        self.whisper = WhisperEngine()

    def listen(self):

        self.microphone.start()

        audio = self.vad.record_until_silence(
            self.microphone
        )

        self.microphone.stop()

        text = self.whisper.transcribe(audio)

        return text.lower()
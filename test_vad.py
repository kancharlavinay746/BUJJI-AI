from voice.microphone import Microphone
from voice.vad import VoiceActivityDetector

mic = Microphone()
vad = VoiceActivityDetector()

mic.start()

audio = vad.record_until_silence(mic)

mic.stop()

print("Captured samples:", len(audio))
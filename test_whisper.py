from voice.microphone import Microphone
from voice.vad import VoiceActivityDetector
from voice.whisper import WhisperEngine

mic = Microphone()
vad = VoiceActivityDetector()
whisper = WhisperEngine()

mic.start()

audio = vad.record_until_silence(mic)

mic.stop()

text = whisper.transcribe(audio)

print("\nRecognized Text:")
print(text)
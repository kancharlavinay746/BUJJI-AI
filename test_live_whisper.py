import time
import numpy as np
import sounddevice as sd

from voice.whisper import WhisperEngine


SAMPLE_RATE = 16000
CHANNELS = 1

print("=" * 60)
print("🎙️ BUJJI DIRECT WHISPER MICROPHONE TEST")
print("=" * 60)

whisper = WhisperEngine()

print()
print("Speak a sentence after the recording starts.")
print("Example:")
print("    Bujji, open Notepad")
print("    Bujji, open YouTube")
print("    What is machine learning?")
print()
print("Press CTRL+C to stop.")
print()


def record_audio(seconds=5):
    print("🔴 Recording for 5 seconds...")

    audio = sd.rec(
        int(seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32"
    )

    sd.wait()

    print("🟢 Recording finished.")

    return audio.flatten()


try:

    while True:

        input("Press ENTER, then speak...")

        audio = record_audio(5)

        if audio.size == 0:
            print("❌ No audio captured.")
            continue

        peak = float(np.max(np.abs(audio)))
        rms = float(np.sqrt(np.mean(audio ** 2)))

        print()
        print(f"📊 Audio peak : {peak:.4f}")
        print(f"📊 Audio RMS  : {rms:.4f}")

        if peak < 0.01:
            print("⚠️ Microphone signal is extremely low.")

        print("🧠 Sending audio to GPU Whisper...")

        text = whisper.transcribe(audio)

        print()
        print("==========================================")
        print("👂 WHISPER RESULT:")
        print(text)
        print("==========================================")
        print()

except KeyboardInterrupt:

    print()
    print("🛑 Test stopped.")
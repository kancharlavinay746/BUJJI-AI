import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np


SAMPLE_RATE = 16000
DURATION = 5


print("🎙️ Recording for 5 seconds...")
print("Speak clearly!")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32"
)

sd.wait()

audio = audio.flatten()

# Measure original volume
rms = np.sqrt(np.mean(audio ** 2))

print(f"Original RMS: {rms:.6f}")

# Automatic gain
target_rms = 0.05

if rms > 0:

    gain = target_rms / rms

    # Limit gain so background noise isn't amplified excessively
    gain = min(gain, 8.0)

    audio = audio * gain

# Prevent clipping
audio = np.clip(audio, -1.0, 1.0)

print(f"Applied gain: {gain:.2f}x")

wav.write(
    "test_recording.wav",
    SAMPLE_RATE,
    np.int16(audio * 32767)
)

print("✅ Recording saved as test_recording.wav")
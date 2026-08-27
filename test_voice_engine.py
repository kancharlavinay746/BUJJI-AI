import sounddevice as sd
import numpy as np
import pyttsx3
from faster_whisper import WhisperModel


SAMPLE_RATE = 16000
RECORD_SECONDS = 5


print("=" * 60)
print("        BUJJI VOICE ENGINE TEST")
print("=" * 60)

print("\n🧠 Loading Faster-Whisper small multilingual model...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("✅ Whisper model loaded.")


# --------------------------------------------------
# RECORD
# --------------------------------------------------

print("\n🎤 Speak now...")
print(f"⏱️ Recording for {RECORD_SECONDS} seconds...")

audio = sd.rec(
    int(RECORD_SECONDS * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32"
)

sd.wait()

print("✅ Recording complete.")


# --------------------------------------------------
# PREPROCESS
# --------------------------------------------------

audio = audio.flatten()

audio = audio - np.mean(audio)

peak = np.max(np.abs(audio))

if peak > 0:
    audio = audio / peak * 0.85

audio = np.clip(audio, -1.0, 1.0)


# --------------------------------------------------
# WHISPER
# --------------------------------------------------

print("\n🧠 Processing speech...")

segments, info = model.transcribe(
    audio,
    task="transcribe",
    beam_size=5,
    best_of=5,
    temperature=0.0,
    condition_on_previous_text=False,
    vad_filter=True,
    vad_parameters={
        "min_silence_duration_ms": 500,
        "speech_pad_ms": 250
    }
)


# --------------------------------------------------
# LANGUAGE + TEXT
# --------------------------------------------------

print(
    f"\n🌐 Detected language: "
    f"{info.language} "
    f"({info.language_probability:.2f})"
)

text_parts = []

for segment in segments:

    text = segment.text.strip()

    if text:
        text_parts.append(text)


text = " ".join(text_parts).strip()


print("\n" + "=" * 60)

if text:

    print(f"📝 YOU SAID:")
    print(text)

else:

    print("❌ No speech detected.")


print("=" * 60)


# --------------------------------------------------
# TEXT TO SPEECH
# --------------------------------------------------

if text:

    print("\n🔊 BUJJI speaking...")

    engine = pyttsx3.init()

    engine.setProperty(
        "rate",
        165
    )

    engine.say(
        f"I heard you say: {text}"
    )

    engine.runAndWait()

    print("✅ Voice response complete.")


print("\n✅ Voice engine test finished.")
import os
import assemblyai as aai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ASSEMBLYAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "ASSEMBLYAI_API_KEY was not found in .env"
    )

aai.settings.api_key = api_key

print("✅ AssemblyAI connected.")

config = aai.TranscriptionConfig(
    speech_model=aai.SpeechModel.best,
    language_code="en"
)

transcriber = aai.Transcriber(
    config=config
)

print("🎧 Transcribing test_recording.wav...")

transcript = transcriber.transcribe(
    "test_recording.wav"
)

if transcript.status == aai.TranscriptStatus.error:

    print("❌ Transcription failed:")
    print(transcript.error)

else:

    print()
    print("Recognized Text:")
    print(transcript.text)
from google.cloud import speech_v1


class GoogleSpeechRecognizer:

    def __init__(self):

        print("🌐 Initializing Google Speech-to-Text...")

        self.client = speech_v1.SpeechClient()

        print("✅ Google Speech-to-Text ready.")

    def transcribe(self, audio_bytes):

        audio = speech_v1.RecognitionAudio(
            content=audio_bytes
        )

        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-IN",
            audio_channel_count=1,
            enable_automatic_punctuation=True,
            model="latest_long"
        )

        response = self.client.recognize(
            config=config,
            audio=audio
        )

        results = []

        for result in response.results:

            if result.alternatives:

                text = result.alternatives[0].transcript

                results.append(text)

        return " ".join(results).strip()
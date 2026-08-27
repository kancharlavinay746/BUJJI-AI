import numpy as np
import time


class VoiceActivityDetector:

    def __init__(
        self,
        silence_threshold=0.005,
        silence_duration=1.8,
        min_recording_duration=0.5
    ):

        self.silence_threshold = silence_threshold

        self.silence_duration = silence_duration

        self.min_recording_duration = (
            min_recording_duration
        )

    def record_until_silence(self, mic):

        print("🎤 Waiting for speech...")

        audio_chunks = []

        speech_started = False

        silence_start = None

        start_time = None

        while True:

            chunk = mic.read()

            if chunk is None:
                continue

            chunk = np.asarray(
                chunk,
                dtype=np.float32
            )

            # Calculate volume
            volume = np.sqrt(
                np.mean(
                    np.square(chunk)
                )
            )

            # ==================================
            # SPEECH START
            # ==================================

            if not speech_started:

                if volume > self.silence_threshold:

                    speech_started = True

                    start_time = time.time()

                    print(
                        "🟢 Speech detected..."
                    )

                    audio_chunks.append(chunk)

                continue

            # ==================================
            # SPEECH CONTINUES
            # ==================================

            audio_chunks.append(chunk)

            # ==================================
            # SPEECH PRESENT
            # ==================================

            if volume > self.silence_threshold:

                silence_start = None

            # ==================================
            # SILENCE DETECTED
            # ==================================

            else:

                if silence_start is None:

                    silence_start = time.time()

                silence_time = (
                    time.time()
                    - silence_start
                )

                recording_time = (
                    time.time()
                    - start_time
                )

                # Don't stop too quickly
                if (
                    silence_time
                    >= self.silence_duration
                    and recording_time
                    >= self.min_recording_duration
                ):

                    print(
                        "🔴 End of speech..."
                    )

                    break

        if not audio_chunks:

            return np.array(
                [],
                dtype=np.float32
            )

        return np.concatenate(
            audio_chunks
        )
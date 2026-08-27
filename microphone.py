import sounddevice as sd
import numpy as np


SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 1024


class Microphone:

    def __init__(self, device=None):

        self.sample_rate = SAMPLE_RATE
        self.channels = CHANNELS
        self.block_size = BLOCK_SIZE

        # None = Windows default microphone
        # We can specify a device later if necessary.
        self.device = device

        self.stream = None

    def start(self):

        print("🎙️ Starting microphone...")

        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=np.float32,
                blocksize=self.block_size,
                device=self.device,
                latency="low"
            )

            self.stream.start()

            print("🎙️ Microphone started.")

        except Exception as e:

            print("❌ Could not start microphone.")
            print(f"Error: {e}")

            self.stream = None

            raise

    def read(self):

        if self.stream is None:
            return None

        try:

            audio, overflowed = self.stream.read(
                self.block_size
            )

            if overflowed:
                print(
                    "⚠️ Microphone buffer overflow"
                )

            # Convert to one-dimensional float32 array
            audio = np.asarray(
                audio,
                dtype=np.float32
            ).flatten()

            # Remove DC offset
            audio = audio - np.mean(audio)

            # Prevent accidental clipping
            audio = np.clip(
                audio,
                -1.0,
                1.0
            )

            return audio

        except Exception as e:

            print(
                f"⚠️ Microphone read error: {e}"
            )

            return np.zeros(
                self.block_size,
                dtype=np.float32
            )

    def stop(self):

        if self.stream is not None:

            print("🎙️ Stopping microphone...")

            try:
                self.stream.stop()
                self.stream.close()

            except Exception as e:

                print(
                    f"⚠️ Error stopping microphone: {e}"
                )

            finally:

                self.stream = None

            print("🎙️ Microphone stopped.")
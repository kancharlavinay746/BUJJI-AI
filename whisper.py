import numpy as np
import sounddevice as sd

from scipy.signal import resample_poly
from faster_whisper import WhisperModel


# ============================================================
# BUJJI CONFIGURATION
# ============================================================

MIC_DEVICE = 12

# Native microphone rate
MIC_SAMPLE_RATE = 48000

# Whisper input rate
WHISPER_SAMPLE_RATE = 16000

CHANNELS = 1

# Record up to 6 seconds
MAX_RECORD_SECONDS = 6


# ============================================================
# WHISPER CONFIGURATION
# ============================================================

MODEL_NAME = "small"

DEVICE = "cuda"

COMPUTE_TYPE = "float16"


# ============================================================
# AUDIO SETTINGS
# ============================================================

# Minimum useful signal
MIN_PEAK = 0.015
MIN_RMS = 0.0008

# Amount of silence to keep around speech
SILENCE_PADDING = 0.25


# ============================================================
# WHISPER ENGINE
# ============================================================

class WhisperEngine:

    def __init__(self):

        print()
        print("=" * 60)
        print("BUJJI - ADVANCED WHISPER ENGINE")
        print("=" * 60)

        print(f"Microphone       : {MIC_DEVICE}")
        print(f"Capture rate     : {MIC_SAMPLE_RATE} Hz")
        print(f"Whisper rate     : {WHISPER_SAMPLE_RATE} Hz")
        print(f"Model            : {MODEL_NAME}")
        print(f"Device           : {DEVICE}")
        print(f"Compute type     : {COMPUTE_TYPE}")

        print("=" * 60)
        print()

        print("Loading Faster-Whisper...")

        self.model = WhisperModel(
            MODEL_NAME,
            device=DEVICE,
            compute_type=COMPUTE_TYPE
        )

        print("✅ Whisper loaded")
        print("✅ NVIDIA GPU enabled")
        print()


    # ========================================================
    # RECORD AUDIO
    # ========================================================

    def record_audio(self):

        print()
        print("🎤 Listening...")
        print("Speak your command now.")

        audio = sd.rec(
            int(
                MAX_RECORD_SECONDS *
                MIC_SAMPLE_RATE
            ),
            samplerate=MIC_SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            device=MIC_DEVICE
        )

        sd.wait()

        audio = audio.flatten()

        return audio


    # ========================================================
    # AUDIO ANALYSIS
    # ========================================================

    def analyze_audio(self, audio):

        peak = float(
            np.max(
                np.abs(audio)
            )
        )

        rms = float(
            np.sqrt(
                np.mean(
                    audio ** 2
                )
            )
        )

        print()
        print("AUDIO LEVEL")
        print("-" * 30)
        print(f"Peak : {peak:.6f}")
        print(f"RMS  : {rms:.6f}")

        return peak, rms


    # ========================================================
    # REMOVE DC OFFSET
    # ========================================================

    def remove_dc(self, audio):

        audio = audio - np.mean(audio)

        return audio.astype(
            np.float32
        )


    # ========================================================
    # FIND SPEECH REGION
    # ========================================================

    def find_speech_region(self, audio):

        print()
        print("🔎 Detecting speech region...")

        # Work with absolute amplitude
        envelope = np.abs(audio)

        # Smooth envelope
        window_size = int(
            MIC_SAMPLE_RATE * 0.02
        )

        if window_size < 1:
            window_size = 1

        kernel = np.ones(
            window_size,
            dtype=np.float32
        ) / window_size

        smoothed = np.convolve(
            envelope,
            kernel,
            mode="same"
        )

        # Adaptive threshold
        noise_floor = np.percentile(
            smoothed,
            20
        )

        threshold = max(
            noise_floor * 3.0,
            0.008
        )

        speech_indices = np.where(
            smoothed > threshold
        )[0]

        if len(speech_indices) == 0:

            print("⚠️ No speech region detected.")

            return None

        start = speech_indices[0]
        end = speech_indices[-1]

        # Add padding
        padding = int(
            SILENCE_PADDING *
            MIC_SAMPLE_RATE
        )

        start = max(
            0,
            start - padding
        )

        end = min(
            len(audio),
            end + padding
        )

        speech = audio[
            start:end
        ]

        print(
            f"Speech region: "
            f"{start / MIC_SAMPLE_RATE:.2f}s "
            f"→ "
            f"{end / MIC_SAMPLE_RATE:.2f}s"
        )

        print(
            f"Speech duration: "
            f"{len(speech) / MIC_SAMPLE_RATE:.2f}s"
        )

        return speech


    # ========================================================
    # LIGHT AUDIO NORMALIZATION
    # ========================================================

    def normalize_audio(self, audio):

        peak = np.max(
            np.abs(audio)
        )

        if peak <= 0:

            return audio

        # Only modest gain
        # Don't aggressively amplify noise.

        target = 0.5

        gain = target / peak

        gain = min(
            gain,
            2.0
        )

        audio = audio * gain

        audio = np.clip(
            audio,
            -1.0,
            1.0
        )

        return audio.astype(
            np.float32
        )


    # ========================================================
    # PREPARE WHISPER AUDIO
    # ========================================================

    def prepare_whisper_audio(self, audio):

        print()
        print("🔄 Preparing audio for Whisper...")

        audio = resample_poly(
            audio,
            1,
            3
        )

        audio = audio.astype(
            np.float32
        )

        print(
            f"Whisper samples: "
            f"{len(audio)}"
        )

        return audio


    # ========================================================
    # TRANSCRIBE
    # ========================================================

    def transcribe(self, audio):

        print()
        print("🧠 Whisper decoding...")
        print("🚀 NVIDIA GTX 1650")

        segments, info = self.model.transcribe(

            audio,

            language="en",

            # Better decoding
            beam_size=5,

            best_of=5,

            patience=1.0,

            # Prevent previous commands
            # from influencing this command
            condition_on_previous_text=False,

            # VAD
            vad_filter=True,

            vad_parameters={
                "min_silence_duration_ms": 350,
                "speech_pad_ms": 250
            },

            # Reduce hallucination
            no_speech_threshold=0.6,

            log_prob_threshold=-1.0,

            compression_ratio_threshold=2.4,

            # Deterministic decoding
            temperature=0.0
        )

        results = []

        for segment in segments:

            text = segment.text.strip()

            if text:

                results.append(text)

        return " ".join(
            results
        ).strip()


    # ========================================================
    # COMPLETE LISTEN
    # ========================================================

    def listen(self):

        # ---------------------------------------------
        # Record
        # ---------------------------------------------

        audio = self.record_audio()


        # ---------------------------------------------
        # Remove DC
        # ---------------------------------------------

        audio = self.remove_dc(
            audio
        )


        # ---------------------------------------------
        # Analyze
        # ---------------------------------------------

        peak, rms = self.analyze_audio(
            audio
        )


        # ---------------------------------------------
        # Reject silence
        # ---------------------------------------------

        if (
            peak < MIN_PEAK
            or
            rms < MIN_RMS
        ):

            print()
            print("⚠️ Recording is too quiet.")
            print("Please speak closer to the microphone.")

            return ""


        # ---------------------------------------------
        # Find speech
        # ---------------------------------------------

        speech = self.find_speech_region(
            audio
        )

        if speech is None:

            return ""


        # ---------------------------------------------
        # Normalize lightly
        # ---------------------------------------------

        speech = self.normalize_audio(
            speech
        )


        # ---------------------------------------------
        # Convert 48 kHz → 16 kHz
        # ---------------------------------------------

        whisper_audio = self.prepare_whisper_audio(
            speech
        )


        # ---------------------------------------------
        # Whisper
        # ---------------------------------------------

        text = self.transcribe(
            whisper_audio
        )


        # ---------------------------------------------
        # Result
        # ---------------------------------------------

        print()
        print("=" * 60)
        print("🧠 HEARD:")
        print(repr(text))
        print("=" * 60)

        return text


# ============================================================
# TEST PROGRAM
# ============================================================

if __name__ == "__main__":

    whisper = WhisperEngine()

    print()
    print("BUJJI is ready.")
    print()

    while True:

        try:

            text = whisper.listen()

            if text:

                print()
                print("USER:", text)

            else:

                print()
                print("⚠️ Nothing recognized.")

            print()

            command = input(
                "Press ENTER to speak again "
                "or type EXIT to stop: "
            )

            if command.strip().lower() == "exit":

                print()
                print("BUJJI stopped.")
                break

        except KeyboardInterrupt:

            print()
            print()
            print("BUJJI stopped.")
            break

        except Exception as e:

            print()
            print("❌ ERROR:")
            print(e)
            break
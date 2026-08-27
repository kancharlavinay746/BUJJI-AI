import re


class WakeWordDetector:

    def __init__(self):

        print("🎯 Initializing wake-word detector...")

        # English / Roman variations
        self.wake_words = {
            "bujji",
            "budji",
            "budgie",
            "budgy",
            "buddhi",
            "puji",
            "booji",
            "boojie",
        }

        # Hindi / Devanagari variations that Whisper may produce
        self.wake_words_devanagari = {
            "बुज्जी",
            "बुजी",
            "बुज्जि",
            "बुजजी",
            "बूजी",
            "बूज्जी",
        }

        print("🟢 Bujji wake-word detector ready.")

    def normalize(self, text):

        if not text:
            return ""

        text = text.lower()

        # Remove punctuation
        text = re.sub(
            r"[.,!?;:'\"।,!?]",
            " ",
            text
        )

        # Normalize multiple spaces
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def detect(self, text):

        if not text:
            return False

        normalized = self.normalize(text)

        words = normalized.split()

        # ---------------------------------------
        # English / Roman detection
        # ---------------------------------------

        for word in words:

            if word in self.wake_words:
                return True

        # ---------------------------------------
        # Devanagari detection
        # ---------------------------------------

        for word in words:

            if word in self.wake_words_devanagari:
                return True

        # ---------------------------------------
        # More tolerant matching
        #
        # Handles things like:
        # "bujji,"
        # "heybujji"
        # ---------------------------------------

        compact = normalized.replace(" ", "")

        for wake_word in self.wake_words:

            if wake_word in compact:
                return True

        return False
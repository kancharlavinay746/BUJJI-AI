from faster_whisper import WhisperModel

models = ["tiny", "base", "small"]

for model_name in models:

    print("\n" + "=" * 50)
    print("Testing model:", model_name)
    print("=" * 50)

    model = WhisperModel(
        model_name,
        device="cpu",
        compute_type="int8"
    )

    segments, info = model.transcribe(
        "test_recording.wav",
        language="en",
        beam_size=5,
        best_of=5,
        temperature=0.0,
        condition_on_previous_text=False,
        vad_filter=False
    )

    text = " ".join(
        segment.text.strip()
        for segment in segments
    )

    print("Recognized:", text)
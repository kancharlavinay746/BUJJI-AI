from voice.microphone import Microphone

mic = Microphone()

mic.start()

print("Microphone started...")
print("Reading audio...")

for i in range(20):
    data = mic.read()
    print(f"Chunk {i+1}: {len(data)} samples")

mic.stop()

print("Microphone stopped.")
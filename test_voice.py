from voice.listener import listen

while True:
    text = listen()
    print(f"\nRecognized: {text}")
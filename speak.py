import edge_tts
import asyncio
import pygame
import os

VOICE = "en-US-JennyNeural"   # Change this voice name

async def speak_async(text):
    filename = "voice.mp3"

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicate.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    pygame.mixer.quit()
    os.remove(filename)


def speak(text):
    asyncio.run(speak_async(text))

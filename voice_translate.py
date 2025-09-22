import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import os

def play_audio(file):
    """Play audio file using pygame (cross-platform safe)."""
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # wait until playback finishes
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

def voice_translate(src_lang="en", dest_lang="hi"):
    recognizer = sr.Recognizer()
    translator = Translator()

    with sr.Microphone() as source:
        print("🎤 Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            # Speech → Text
            text = recognizer.recognize_google(audio, language=src_lang)
            print(f"🗣 You said: {text}")

            # Translation
            translated = translator.translate(text, src=src_lang, dest=dest_lang)
            print(f"🌍 Translated: {translated.text}")

            # Text → Speech
            tts = gTTS(translated.text, lang=dest_lang)
            filename = "translated.mp3"
            tts.save(filename)

            # Play audio with pygame
            play_audio(filename)
            os.remove(filename)

        except Exception as e:
            print("❌ Error:", e)

if __name__ == "__main__":
    # Example: English → Hindi
    voice_translate(src_lang="en", dest_lang="fr")

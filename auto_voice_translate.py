import sounddevice as sd
import wavio
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import os

def record_audio(filename="input.wav", duration=5, fs=44100):
    """Record audio from mic and save to WAV"""
    print("🎤 Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wavio.write(filename, recording, fs, sampwidth=2)
    print("✅ Recording complete")

def play_audio(file):
    """Play audio file using pygame"""
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

def auto_translate(dest_lang="en"):
    recognizer = sr.Recognizer()
    translator = Translator()

    # Step 1: Record voice
    record_audio("input.wav", duration=5)

    # Step 2: Speech → Text (Google ASR, language-independent)
    with sr.AudioFile("input.wav") as source:
        audio = recognizer.record(source)
        try:
            # Try recognition without forcing language (auto detect from Translate later)
            text = recognizer.recognize_google(audio)
            print(f"🗣 Detected Speech: {text}")

            # Step 3: Translate (auto-detect source language)
            translated = translator.translate(text, dest=dest_lang)
            print(f"🌍 Detected Language: {translated.src}")
            print(f"➡️ Translated ({dest_lang}): {translated.text}")

            # Step 4: Text → Speech
            tts = gTTS(translated.text, lang=dest_lang)
            filename = "translated.mp3"
            tts.save(filename)
            play_audio(filename)
            os.remove(filename)

        except Exception as e:
            print("❌ Error:", e)

if __name__ == "__main__":
    # Auto-detect spoken language → Translate → English voice output
    auto_translate(dest_lang="fr")

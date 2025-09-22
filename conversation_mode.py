import sounddevice as sd
import wavio
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import os

# 🌍 Language mapping (ISO codes)
LANGUAGES = {
    "tamil": ("ta", "ta-IN"),
    "english": ("en", "en-US"),
    "german": ("de", "de-DE"),
    "french": ("fr", "fr-FR"),
    "japanese": ("ja", "ja-JP"),
    "spanish": ("es", "es-ES"),
    "hindi": ("hi", "hi-IN")
}

def record_audio(filename="input.wav", duration=5, fs=44100):
    print("🎤 Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wavio.write(filename, recording, fs, sampwidth=2)
    return filename

def play_audio(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

def translate_and_speak(src_lang, dest_lang, duration=5):
    recognizer = sr.Recognizer()
    translator = Translator()

    filename = record_audio(duration=duration)
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)

        try:
            recog_locale = LANGUAGES[src_lang][1]
            text = recognizer.recognize_google(audio, language=recog_locale)
            print(f"🗣 [{src_lang}] {text}")

            trans_code = LANGUAGES[dest_lang][0]
            translated = translator.translate(text, src=LANGUAGES[src_lang][0], dest=trans_code)
            print(f"🌍 [{dest_lang}] {translated.text}")

            tts = gTTS(translated.text, lang=trans_code)
            out_file = "translated.mp3"
            tts.save(out_file)
            play_audio(out_file)
            os.remove(out_file)

        except Exception as e:
            print("❌ Error:", e)

if __name__ == "__main__":
    print("🔄 Multi-language Conversation Mode (Ctrl+C to stop)")
    print("Available:", ", ".join(LANGUAGES.keys()))

    src = input("👉 Enter source language: ").strip().lower()
    dest = input("👉 Enter target language: ").strip().lower()

    if src not in LANGUAGES or dest not in LANGUAGES:
        print("❌ Language not supported.")
        exit()

    while True:
        print(f"\n👤 Speak in {src.capitalize()}")
        translate_and_speak(src_lang=src, dest_lang=dest, duration=5)

        print(f"\n👤 Speak in {dest.capitalize()}")
        translate_and_speak(src_lang=dest, dest_lang=src, duration=5)

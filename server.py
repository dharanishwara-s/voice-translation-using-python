from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from googletrans import Translator
from gtts import gTTS
import os

app = Flask(__name__)
translator = Translator()

@app.route("/voice", methods=["POST"])
def voice():
    # When someone calls your Twilio number
    resp = VoiceResponse()
    resp.say("Hello! Please speak after the beep. I will translate your voice.", voice="alice")
    resp.record(
        action="/handle-recording",
        transcribe=True,
        transcribe_callback="/handle-transcription"
    )
    return Response(str(resp), mimetype="application/xml")

@app.route("/handle-transcription", methods=["POST"])
def handle_transcription():
    text = request.form["TranscriptionText"]
    print("🎤 Caller said:", text)

    # Translate (English -> German as example)
    translated = translator.translate(text, src="en", dest="de").text
    print("🌍 Translated:", translated)

    # Generate speech
    tts = gTTS(translated, lang="de")
    filename = "output.mp3"
    tts.save(filename)

    # (Here, you’d host the MP3 on a server or Twilio’s `Play` can fetch it)
    # For demo, just show translation
    return "OK"

@app.route("/handle-recording", methods=["POST"])
def handle_recording():
    return "Recording received"

if __name__ == "__main__":
    app.run(port=5000, debug=True)

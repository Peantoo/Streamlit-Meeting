import os
import base64
import tempfile
from flask import Flask, request, render_template, jsonify
import speech_recognition as sr
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")
USERNAME = os.environ.get("APP_USERNAME")
PASSWORD = os.environ.get("APP_PASSWORD")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            return render_template("main.html")
        else:
            return "Invalid credentials. Please try again."
    return render_template("login.html")

@app.route("/end_meeting", methods=["POST"])
def end_meeting():
    try:
        audio_data = request.form['audio']
        audio_data = audio_data.split(",")[1]
        audio_data = base64.b64decode(audio_data)

        with tempfile.TemporaryFile() as audio_file:
            audio_file.write(audio_data)
            audio_file.seek(0)

            r = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio = r.record(source)
            transcript = r.recognize_google(audio)

        prompt = f"Summarize the following meeting transcript: {transcript}"
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )

        summary = response.choices[0].text.strip()
        return jsonify(summary=summary)

    except Exception as e:
        # Add proper error logging
        print(e)
        return jsonify(error="An error occurred while processing the audio."), 500

if __name__ == "__main__":
    app.run()
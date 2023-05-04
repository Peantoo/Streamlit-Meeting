import os
from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import openai
import requests
from pydub import AudioSegment

app = Flask(__name__)

# Comment out the following two lines if running locally
# username = os.environ.get('USERNAME')
# password = os.environ.get('PASSWORD')

# Uncomment the following two lines and replace them with your credentials when running locally
username = "dustin"
password = "password"

openai.api_key = "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"

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    auth = request.authorization
    if not auth or not (auth.username == username and auth.password == password):
        return authenticate()

    return render_template('main.html')

@app.route('/end_meeting', methods=['POST'])
def end_meeting():
    audio_data = request.files['file']
    audio_format = audio_data.filename.split('.')[-1]

    audio = AudioSegment.from_file(audio_data, format=audio_format)
    audio = audio.set_channels(1)  # Convert to mono
    audio.export("temp.wav", format="wav")

    recognizer = sr.Recognizer()

    with sr.AudioFile("temp.wav") as source:
        audio = recognizer.record(source)

    try:
        transcript = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return jsonify(error="Speech recognition failed. Please try again.")
    
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=f"Summarize the following meeting: {transcript}",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    summary = response.choices[0].text.strip()
    return jsonify(summary=summary)

def authenticate():
    message = {'message': 'Authorization required'}
    resp = jsonify(message)
    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
    return resp

if __name__ == '__main__':
    # Comment out the following line if running on Heroku
    app.run(debug=True)
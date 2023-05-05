import requests
from transformers import pipeline
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

APIKEY = os.environ.get("HF_API_KEY")
# Speech-to-text
API_URL = "https://api-inference.huggingface.co/models/jonatasgrosman/wav2vec2-large-xlsr-53-english"
headers = {"Authorization": APIKEY}

def query(audio_data):
    response = requests.post(API_URL, headers=headers, data=audio_data)
    return response.json()

# Summarization
summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum")

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Read the file into memory
    audio_data = BytesIO(file.read())

    transcription_output = query(audio_data.getvalue())
    transcription_text = transcription_output['text']
    summary_output = summarizer(transcription_text)
    summary_text = summary_output[0]['summary_text']

    return jsonify({'transcription': transcription_text, 'summary': summary_text}), 200
    
if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error: {e}")

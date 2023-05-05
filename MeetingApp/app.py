import requests
from transformers import pipeline
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Speech-to-text
API_URL = "https://api-inference.huggingface.co/models/jonatasgrosman/wav2vec2-large-xlsr-53-english"
headers = {"Authorization": "Bearer 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"}

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

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    with open(file_path, 'rb') as f:
        audio_data = f.read()

    transcription_output = query(audio_data)
    transcription_text = transcription_output['text']
    summary_output = summarizer(transcription_text)
    summary_text = summary_output[0]['summary_text']

    os.remove(file_path)

    return jsonify({'transcription': transcription_text, 'summary': summary_text}), 200

if __name__ == '__main__':
    app.run(debug=True)
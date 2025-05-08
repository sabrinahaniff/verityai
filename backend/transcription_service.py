from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from audio_processing import transcribe_audio
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty file'}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Transcribe the audio
        transcription = transcribe_audio(file_path)
        os.remove(file_path)

        return jsonify({'transcription': transcription, 'sentiment': 'N/A', 'score': 0.0})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

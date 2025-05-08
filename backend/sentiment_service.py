from flask import Flask, request, jsonify
from flask_cors import CORS
from sentiment_analysis import analyze_sentiment

app = Flask(__name__)
CORS(app)

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment_route():
    try:
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        sentiment_result = analyze_sentiment(text)
        return jsonify({'sentiment': sentiment_result['label'], 'score': sentiment_result['score']})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

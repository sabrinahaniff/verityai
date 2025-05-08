import pandas as pd
from transformers import pipeline

# Initialize the sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

THRESHOLD = 0.7

def analyze_sentiment(text):
    try:
        result = sentiment_analyzer(text)[0]
        label = result['label']
        score = result['score']

        # Re-label as NEUTRAL if score is below the threshold
        if score < THRESHOLD:
            label = "NEUTRAL"

        return {"label": label, "score": score}
    except Exception as e:
        return {"error": str(e)}


def analyze_sentiment_dataframe(transcription_data):
    # Ensure transcription_data is a DataFrame
    if not isinstance(transcription_data, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    if 'text' not in transcription_data.columns:
        raise KeyError("DataFrame must contain a 'text' column")

    # Apply sentiment analysis to each text entry with error handling
    results = []
    for text in transcription_data['text']:
        analysis = analyze_sentiment(text)
        results.append(analysis)

    transcription_data['sentiment'] = [res.get('label', 'ERROR') for res in results]
    transcription_data['score'] = [res.get('score', 0.0) for res in results]

    return transcription_data


if __name__ == "__main__":
    # Example usage
    sample_data = pd.DataFrame({"text": ["I love this!", "This is terrible.", "Not bad at all.", "Meh.", "Amazing product!"]})
    result = analyze_sentiment_dataframe(sample_data)
    print(result)
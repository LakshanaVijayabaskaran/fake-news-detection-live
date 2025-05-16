import tensorflow as tf
tf.config.run_functions_eagerly(True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)
CORS(app)

# Constants
MODEL_PATH = 'lstm_model.h5'
TOKENIZER_PATH = 'tokenizer.pickle'
NEWS_API_KEY = '15e26c29629f4803ac71c20f59b1f09d'
NEWS_API_URL = f'https://newsapi.org/v2/top-headlines?language=en&apiKey={NEWS_API_KEY}'
MAXLEN = 200

# Global model and tokenizer
model = load_model(MODEL_PATH)
with open(TOKENIZER_PATH, 'rb') as handle:
    tokenizer = pickle.load(handle)


def fetch_news():
    try:
        print("Fetching latest news articles...")
        response = requests.get(NEWS_API_URL)
        news_data = response.json()
        articles = news_data.get('articles', [])
        texts = []

        print(f"Fetched {len(articles)} articles.")
        for i, article in enumerate(articles):
            title = article.get('title') or ''
            description = article.get('description') or ''
            print(f"{i+1}. {title}")
            full_text = title + ' ' + description
            texts.append(full_text.strip())

        return texts
    except Exception as e:
        print("Error fetching news:", e)
        return []


def retrain_model():
    global model
    print("Starting retraining job...")

    articles = fetch_news()
    if not articles:
        print("No articles fetched. Skipping retraining.")
        return

    sequences = tokenizer.texts_to_sequences(articles)
    padded = pad_sequences(sequences, maxlen=MAXLEN)

    # Dummy labels (in production, you'd use verified labels)
    labels = np.random.randint(0, 2, len(articles))

    # Reload model fresh and recompile with new optimizer
    model = load_model(MODEL_PATH)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(padded, labels, epochs=2, batch_size=16, verbose=1)
    model.save(MODEL_PATH)
    print("Retraining complete.")


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=MAXLEN)
    prediction = model.predict(padded)[0][0]
    return jsonify({'prediction': float(prediction)})


if __name__ == '__main__':
    # Retrain every 30 seconds (use hours=6 in production)
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=retrain_model, trigger="interval", hours=1)
    scheduler.start()

    print("API is running with periodic model updates.")
    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

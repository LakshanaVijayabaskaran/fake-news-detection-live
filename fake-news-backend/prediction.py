import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# === Load model and tokenizer ===
model = load_model('lstm_model.h5')

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# === Take input from user ===
news_text = input("Please enter the news text you want to verify: ")
print("You entered:", news_text)

# === Preprocess input ===
sequence = tokenizer.texts_to_sequences([news_text])
padded = pad_sequences(sequence, maxlen=200)  # Ensure maxlen matches training

# === Predict ===
prediction = model.predict(padded)[0][0]

# === Output result ===
if prediction >= 0.5:
    print("✅ This news is likely REAL (confidence: {:.2f}%)".format(prediction * 100))
else:
    print("❌ This news is likely FAKE (confidence: {:.2f}%)".format((1 - prediction) * 100))

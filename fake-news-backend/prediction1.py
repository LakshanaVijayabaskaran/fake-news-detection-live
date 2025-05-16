import pickle
import os

# === Load the model ===
model_path = os.path.join(os.path.expanduser("~"), "Downloads", "decision_tree_model.pkl")

with open(model_path, 'rb') as f:
    model = pickle.load(f)

# === Load the vectorizer ===
vectorizer_path = os.path.join(os.path.expanduser("~"), "Downloads", "tfidf_vectorizer.pkl")

with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)

# === Take input ===
input_text = input("Please enter the news text you want to verify: ")
print("You entered:", input_text)

# === Transform text ===
input_vector = vectorizer.transform([input_text])

# === Predict ===
prediction = model.predict(input_vector)[0]

# === Output ===
if prediction == 1:
    print("✅ This news is likely REAL.")
else:
    print("❌ This news is likely FAKE.")

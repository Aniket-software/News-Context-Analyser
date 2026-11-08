
import pandas as pd
import joblib
import json
import os

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load test dataset
df = pd.read_csv("data/raw/test.tsv", sep="\t")
df = df.dropna(subset=["title", "text", "label"])

# Prepare article content
df["content"] = df["title"] + " " + df["text"]

# Load trained model and vectorizer
tfidf = joblib.load("models/tfidf_vectorizer.pkl")
model = joblib.load("models/fake_news_model.pkl")

# Transform test data
X_test = tfidf.transform(df["content"])
y_test = df["label"]

# Generate predictions
predictions = model.predict(X_test)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, predictions)

report = classification_report(
    y_test,
    predictions,
    output_dict=True
)

matrix = confusion_matrix(y_test, predictions)

# Store results
results = {
    "test_accuracy": accuracy,
    "classification_report": report,
    "confusion_matrix": matrix.tolist()
}

# Create models folder if needed
os.makedirs("models", exist_ok=True)

# Save evaluation results
with open("models/evaluation_results.json", "w") as file:
    json.dump(results, file, indent=4)

print("Evaluation results saved successfully!")
print("Test Accuracy:", round(accuracy * 100, 2), "%")
print("File: models/evaluation_results.json")


import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load cleaned validation dataset
df = pd.read_csv("data/processed/validation_cleaned.csv")

X_val = df["cleaned_content"]
y_val = df["label"]

# Load trained vectorizer and model
tfidf = joblib.load("models/tfidf_vectorizer.pkl")
model = joblib.load("models/fake_news_model.pkl")

# Transform validation data
X_val_tfidf = tfidf.transform(X_val)

# Predict
predictions = model.predict(X_val_tfidf)

# Evaluate
print("Validation Accuracy:", accuracy_score(y_val, predictions))

print("\nClassification Report:")
print(classification_report(y_val, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_val, predictions))


import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load test dataset
df = pd.read_csv("data/raw/test.tsv", sep="\t")

# Remove missing records
df = df.dropna(subset=["title", "text", "label"])

# Combine title and article text
df["content"] = df["title"] + " " + df["text"]

# Load trained vectorizer and model
tfidf = joblib.load("models/tfidf_vectorizer.pkl")
model = joblib.load("models/fake_news_model.pkl")

# Transform test data (do not fit again)
X_test = tfidf.transform(df["content"])
y_test = df["label"]

# Make predictions
predictions = model.predict(X_test)

# Evaluate model
print("Test Accuracy:", accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

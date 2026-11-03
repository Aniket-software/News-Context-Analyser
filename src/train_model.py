import pandas as pd
import joblib
import os

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer

# Load training data
df = pd.read_csv("data/processed/train_cleaned.csv")

# Remove missing and empty text
df = df.dropna(subset=["cleaned_content", "label"])
df = df[df["cleaned_content"].str.strip() != ""]

X_train = df["cleaned_content"]
y_train = df["label"]

# Load saved TF-IDF vectorizer
tfidf = joblib.load("models/tfidf_vectorizer.pkl")

# Transform text
X_train_tfidf = tfidf.transform(X_train)

# Initialize model
model = LogisticRegression(max_iter=1000)

# Train model
model.fit(X_train_tfidf, y_train)

# Training predictions
predictions = model.predict(X_train_tfidf)

# Evaluate
accuracy = accuracy_score(y_train, predictions)

print("Model Training Completed!")
print("Training Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_train, predictions))

# Save model
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/fake_news_model.pkl")

print("Model saved successfully!")
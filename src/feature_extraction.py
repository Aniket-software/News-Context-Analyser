import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

# Load processed dataset
df = pd.read_csv("data/processed/train_cleaned.csv")

# Separate text and labels
# Remove rows with missing text
df = df.dropna(subset=["cleaned_content", "label"])

# Remove empty text rows
df = df[df["cleaned_content"].str.strip() != ""]

# Separate text and labels
X = df["cleaned_content"]
y = df["label"]
# Create TF-IDF vectorizer
tfidf = TfidfVectorizer(
    max_features=5000,
    stop_words="english",
    ngram_range=(1, 2)
)

# Convert text into numerical features
X_tfidf = tfidf.fit_transform(X)

# Create models directory if it doesn't exist
os.makedirs("models", exist_ok=True)

# Save vectorizer
joblib.dump(tfidf, "models/tfidf_vectorizer.pkl")

print("TF-IDF extraction completed!")
print("Feature matrix shape:", X_tfidf.shape)
print("Number of features:", len(tfidf.get_feature_names_out()))

print("\nSample features:")
print(tfidf.get_feature_names_out()[:20])
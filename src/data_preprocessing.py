import pandas as pd
import re

def clean_text(text):

    text = str(text)

    # Convert text to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove special characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# Load training dataset
df = pd.read_csv("data/raw/train.tsv", sep="\t")

# Combine title and article text
df["content"] = df["title"] + " " + df["text"]

# Clean combined text
df["cleaned_content"] = df["content"].apply(clean_text)

# Save processed dataset
df[["cleaned_content", "label"]].to_csv(
    "data/processed/train_cleaned.csv",
    index=False
)

print("Preprocessing completed!")
print("Dataset shape:", df.shape)

print("\nOriginal text:")
print(df["content"].iloc[0][:300])

print("\nCleaned text:")
print(df["cleaned_content"].iloc[0][:300])
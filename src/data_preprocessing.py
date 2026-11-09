
import pandas as pd
import re
import os


def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess_dataset(input_path, output_path):

    df = pd.read_csv(input_path, sep="\t")

    # Preserve original row position before filtering
    df["source_index"] = df.index

    df = df.dropna(subset=["title", "text", "label"])

    df["content"] = df["title"] + " " + df["text"]

    df["cleaned_content"] = df["content"].apply(clean_text)

    df = df[df["cleaned_content"].str.strip() != ""]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df[
        ["source_index", "cleaned_content", "label"]
    ].to_csv(
        output_path,
        index=False
    )

    print("Preprocessing completed:", output_path)
    print("Dataset shape:", df.shape)


if __name__ == "__main__":

    preprocess_dataset(
        "data/raw/train.tsv",
        "data/processed/train_cleaned.csv"
    )

    preprocess_dataset(
        "data/raw/validation.tsv",
        "data/processed/validation_cleaned.csv"
    )

    preprocess_dataset(
        "data/raw/test.tsv",
        "data/processed/test_cleaned.csv"
    )

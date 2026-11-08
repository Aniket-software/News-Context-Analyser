
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Load cleaned training data
df = pd.read_csv("data/processed/train_cleaned.csv")

# Load sentence transformer model
print("Loading Sentence Transformer model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Select article text
texts = df["cleaned_content"].fillna("").tolist()

# Generate embeddings
print("Generating embeddings...")

embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True
)

# Save embeddings
os.makedirs("models", exist_ok=True)

np.save(
    "models/news_embeddings.npy",
    embeddings
)

print("\nEmbedding generation completed!")
print("Embedding shape:", embeddings.shape)
print("Number of articles:", len(texts))


import numpy as np
import pandas as pd
import faiss

from sentence_transformers import SentenceTransformer

# Load cleaned articles
df = pd.read_csv("data/processed/train_cleaned.csv")

# Load Sentence Transformer
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS index
index = faiss.read_index("models/news_faiss.index")

# Enter a sample search query
query = "The government increased fuel prices"

# Convert query into embedding
query_embedding = model.encode(
    [query],
    convert_to_numpy=True
).astype("float32")

# Normalize query embedding
faiss.normalize_L2(query_embedding)

# Search for top 5 similar articles
distances, indices = index.search(query_embedding, 5)

print("\nSearch Query:", query)
print("\nTop 5 Similar Articles:\n")

for rank, (idx, score) in enumerate(
    zip(indices[0], distances[0]), start=1
):
    print(f"Rank: {rank}")
    print(f"Similarity Score: {score:.4f}")
    print("Article:", df.iloc[idx]["cleaned_content"][:300])
    print("-" * 70)

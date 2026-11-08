
import numpy as np
import faiss
import os

# Load generated embeddings
embeddings = np.load("models/news_embeddings.npy")

# Convert embeddings to float32
embeddings = embeddings.astype("float32")

# Normalize vectors for cosine similarity
faiss.normalize_L2(embeddings)

# Get embedding dimensions
dimension = embeddings.shape[1]

# Create FAISS index
index = faiss.IndexFlatIP(dimension)

# Add embeddings to index
index.add(embeddings)

# Save FAISS index
os.makedirs("models", exist_ok=True)

faiss.write_index(
    index,
    "models/news_faiss.index"
)

print("FAISS index created successfully!")
print("Number of indexed articles:", index.ntotal)
print("Embedding dimensions:", dimension)
print("Index saved: models/news_faiss.index")

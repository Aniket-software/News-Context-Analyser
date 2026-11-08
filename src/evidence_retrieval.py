
import pandas as pd
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


class EvidenceRetriever:

    def __init__(self):

        # Load article dataset
        self.df = pd.read_csv(
            "data/processed/train_cleaned.csv"
        )

        # Load embedding model
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        # Load FAISS index
        self.index = faiss.read_index(
            "models/news_faiss.index"
        )

    def search(self, query, top_k=5):

        # Generate query embedding
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        # Normalize embedding
        faiss.normalize_L2(query_embedding)

        # Search FAISS
        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for idx, score in zip(indices[0], scores[0]):

            if idx == -1:
                continue

            results.append({
                "article": self.df.iloc[idx]["cleaned_content"],
                "similarity": float(score),
                "label": int(self.df.iloc[idx]["label"])
            })

        return results


if __name__ == "__main__":

    retriever = EvidenceRetriever()

    query = "The government increased fuel prices"

    results = retriever.search(query, top_k=5)

    print("\nRetrieved Evidence:\n")

    for i, result in enumerate(results, start=1):

        print(f"Result {i}")
        print("Similarity:", round(result["similarity"], 4))
        print("Dataset Label:", result["label"])
        print("Article:", result["article"][:300])
        print("-" * 60)

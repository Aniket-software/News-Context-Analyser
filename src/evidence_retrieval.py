
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer


class EvidenceRetriever:

    def __init__(self):

        self.df = pd.read_csv(
            "data/processed/train_cleaned.csv"
        )

        self.original_df = pd.read_csv(
            "data/raw/train.tsv",
            sep="\t"
        )

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.index = faiss.read_index(
            "models/news_faiss.index"
        )

    def search(self, query, top_k=5):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for idx, score in zip(indices[0], scores[0]):

            if idx == -1:
                continue

            cleaned_row = self.df.iloc[idx]

            source_index = int(
                cleaned_row["source_index"]
            )

            original_row = self.original_df.iloc[
                source_index
            ]

            title = str(original_row["title"])
            original_text = str(original_row["text"])

            # Preserve original numbers and punctuation
            full_article = title + "\n\n" + original_text

            results.append({

                "title": title,

                "date": str(original_row["date"]),

                "subject": str(original_row["subject"]),

                "article": full_article,

                "similarity": float(score),

                "label": int(cleaned_row["label"])

            })

        return results


import pandas as pd
from transformers import pipeline

from evidence_retrieval import EvidenceRetriever


CLAIM = (
    "North Korea experienced rising fuel prices "
    "after UN sanctions."
)


print("Loading evidence retriever...")
retriever = EvidenceRetriever()

print("\nLoading NLI model...")
nli_model = pipeline(
    "text-classification",
    model="cross-encoder/nli-deberta-v3-small"
)

# Retrieve the first article
evidence = retriever.search(CLAIM, top_k=1)[0]

# Load its cleaned version
df = pd.read_csv(
    "data/processed/train_cleaned.csv"
)

cleaned_row = df[
    df["source_index"] == retriever.original_df[
        retriever.original_df["title"] == evidence["title"]
    ].index[0]
].iloc[0]

cleaned_article = cleaned_row["cleaned_content"]
original_article = evidence["article"]


def check_nli(name, article):

    result = nli_model(
        {
            "text": article,
            "text_pair": CLAIM
        },
        top_k=None,
        truncation=True,
        max_length=512
    )

    scores = {
        item["label"]: item["score"]
        for item in result
    }

    print(f"\n{name}")
    print("-" * 45)

    for label, score in scores.items():
        print(f"{label}: {score:.4%}")


print("\nComparing the same article...")
check_nli("ORIGINAL ARTICLE", original_article)
check_nli("CLEANED ARTICLE", cleaned_article)


# Test only the opening sentences containing the key evidence
import re

article_body = original_article.split("\n\n", 1)[-1]

sentences = re.split(
    r'(?<=[.!?])\s+',
    article_body
)

focused_passage = " ".join(sentences[:3])

check_nli(
    "FOCUSED EVIDENCE PASSAGE",
    focused_passage
)

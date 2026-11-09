
from evidence_retrieval import EvidenceRetriever


retriever = EvidenceRetriever()

claim = (
    "North Korea experienced rising fuel prices "
    "after UN sanctions."
)

results = retriever.search(claim, top_k=5)

print("\nCLAIM:")
print(claim)

print("\nRETRIEVED EVIDENCE:")
print("=" * 70)

for i, item in enumerate(results, start=1):

    print(f"\nEvidence {i}")
    print("Title:", item["title"])
    print("Date:", item["date"])
    print("Subject:", item["subject"])
    print("Similarity:", round(item["similarity"], 4))

    label = "Real" if item["label"] == 1 else "Fake"
    print("Dataset Label:", label)

    print("Article:", item["article"][:300])
    print("-" * 70)

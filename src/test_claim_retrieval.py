
from evidence_retrieval import EvidenceRetriever

# Initialize retriever
retriever = EvidenceRetriever()

# Example claim
claim = "North Korea experienced rising fuel prices after UN sanctions."

# Retrieve relevant articles
results = retriever.search(claim, top_k=5)

print("\nCLAIM:")
print(claim)

print("\nRETRIEVED EVIDENCE:\n")

for i, result in enumerate(results, start=1):

    print(f"Evidence {i}")
    print("Similarity:", round(result["similarity"], 4))

    label = "Real" if result["label"] == 1 else "Fake"
    print("Dataset Label:", label)

    print("Article:", result["article"][:400])
    print("-" * 70)

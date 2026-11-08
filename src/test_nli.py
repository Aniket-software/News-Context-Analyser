from transformers import pipeline

print("Loading NLI model...")

nli_model = pipeline(
    "text-classification",
    model="cross-encoder/nli-deberta-v3-small"
)

# Evidence from an article
premise = (
    "Gasoline and diesel prices rose sharply in North Korea "
    "after the United Nations imposed new sanctions."
)

# Claim to verify
hypothesis = (
    "North Korea experienced rising fuel prices after UN sanctions."
)

# Compare evidence with claim
results = nli_model(
    {
        "text": premise,
        "text_pair": hypothesis
    },
    top_k=None
)

print("\nNLI ANALYSIS")
print("=" * 50)

for result in results:
    print(
        result["label"],
        ":",
        round(result["score"] * 100, 2),
        "%"
    )
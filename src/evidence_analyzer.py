
import re
from transformers import pipeline


class EvidenceAnalyzer:

    def __init__(self):

        print("Loading NLI model...")

        self.nli_model = pipeline(
            "text-classification",
            model="cross-encoder/nli-deberta-v3-small"
        )

    def create_passages(self, article, sentences_per_passage=3):

        # Remove the headline and retain the article body
        article_body = article.split("\n\n", 1)[-1]

        sentences = re.split(
            r'(?<=[.!?])\s+',
            article_body.strip()
        )

        sentences = [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]

        passages = []

        # Create overlapping groups of sentences
        for i in range(0, len(sentences), 2):

            passage = " ".join(
                sentences[i:i + sentences_per_passage]
            )

            if passage:
                passages.append(passage)

        return passages

    def analyze_evidence(self, claim, evidence):

        results = []

        for item in evidence:

            article = item["article"]

            passages = self.create_passages(article)

            passage_results = []

            for passage in passages:

                prediction = self.nli_model(
                    {
                        "text": passage,
                        "text_pair": claim
                    },
                    top_k=None,
                    truncation=True,
                    max_length=512
                )

                scores = {
                    result["label"]: result["score"]
                    for result in prediction
                }

                passage_results.append({
                    "passage": passage,
                    "scores": scores
                })

            if not passage_results:
                continue

            # Find the passage with the strongest
            # entailment or contradiction score
            best_result = max(
                passage_results,
                key=lambda result: max(
                    result["scores"].get("entailment", 0),
                    result["scores"].get("contradiction", 0)
                )
            )

            scores = best_result["scores"]

            strongest_stance_score = max(
                scores.get("entailment", 0),
                scores.get("contradiction", 0)
            )

            # A weak non-neutral score is not enough
            # to classify the evidence as supporting
            # or contradicting the claim.
            if strongest_stance_score < 0.50:
                stance = "neutral"
            else:
                stance = max(
                    scores,
                    key=scores.get
                )

            results.append({

                # Original article metadata
                "title": item.get("title", "Untitled article"),
                "date": item.get("date", "Date unavailable"),
                "subject": item.get("subject", "Unknown category"),

                # Original article
                "article": article,

                # Retrieval information
                "similarity": item["similarity"],
                "dataset_label": item["label"],

                # Best matching evidence passage
                "evidence_passage": best_result["passage"],

                # NLI assessment
                "stance": stance,
                "nli_scores": scores

            })

        return results

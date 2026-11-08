from transformers import pipeline


class EvidenceAnalyzer:

    def __init__(self):

        print("Loading NLI model...")

        self.nli_model = pipeline(
            "text-classification",
            model="cross-encoder/nli-deberta-v3-small"
        )

    def analyze_evidence(self, claim, evidence):

        results = []

        for item in evidence:

            premise = item["article"]

            prediction = self.nli_model(
                {
                    "text": premise,
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

            stance = max(
                scores,
                key=scores.get
            )

            results.append({
                "article": premise,
                "similarity": item["similarity"],
                "dataset_label": item["label"],
                "stance": stance,
                "nli_scores": scores
            })

        return results
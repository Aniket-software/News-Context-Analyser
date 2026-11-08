
import joblib

from evidence_retrieval import EvidenceRetriever
from evidence_analyzer import EvidenceAnalyzer


class ClaimAnalyzer:

    def __init__(self):

        print("Loading Claim Analyzer...")

        self.retriever = EvidenceRetriever()
        self.evidence_analyzer = EvidenceAnalyzer()

        # Load trained ML model
        self.tfidf = joblib.load(
            "models/tfidf_vectorizer.pkl"
        )

        self.classifier = joblib.load(
            "models/fake_news_model.pkl"
        )

    def analyze_claim(self, claim):

        # 1. ML prediction
        claim_vector = self.tfidf.transform([claim])

        prediction = self.classifier.predict(
            claim_vector
        )[0]

        probabilities = self.classifier.predict_proba(
            claim_vector
        )[0]

        # 2. Retrieve relevant evidence
        evidence = self.retriever.search(
            claim,
            top_k=5
        )

        # 3. Analyze evidence using NLI
        analyzed_evidence = (
            self.evidence_analyzer.analyze_evidence(
                claim,
                evidence
            )
        )

        # 4. Count evidence stances
        stance_summary = {
            "entailment": 0,
            "contradiction": 0,
            "neutral": 0
        }

        for item in analyzed_evidence:

            stance_summary[item["stance"]] += 1

        # 5. Prepare final analysis
        return {
            "claim": claim,

            "ml_prediction": (
                "Real" if prediction == 1 else "Fake"
            ),

            "ml_confidence": float(max(probabilities)),

            "retrieved_evidence": analyzed_evidence,

            "total_evidence": len(analyzed_evidence),

            "stance_summary": stance_summary
        }


if __name__ == "__main__":

    analyzer = ClaimAnalyzer()

    claim = (
        "North Korea experienced rising fuel prices "
        "after UN sanctions."
    )

    result = analyzer.analyze_claim(claim)

    print("\nCLAIM ANALYSIS")
    print("=" * 60)

    print("Claim:", result["claim"])

    print("ML Prediction:", result["ml_prediction"])

    print(
        "ML Confidence:",
        round(result["ml_confidence"] * 100, 2),
        "%"
    )

    print(
        "Evidence Retrieved:",
        result["total_evidence"]
    )

    # Overall evidence summary
    print("\nOVERALL EVIDENCE SUMMARY")
    print("-" * 40)

    for stance, count in result["stance_summary"].items():

        print(f"{stance}: {count}")

    # Individual evidence analysis
    print("\nINDIVIDUAL EVIDENCE ANALYSIS")
    print("=" * 60)

    for i, item in enumerate(
        result["retrieved_evidence"],
        start=1
    ):

        label = (
            "Real"
            if item["dataset_label"] == 1
            else "Fake"
        )

        print(f"\nEvidence {i}")

        print("Dataset Label:", label)

        print(
            "Similarity:",
            round(item["similarity"], 4)
        )

        print("NLI Stance:", item["stance"])

        print("NLI Scores:")

        for stance, score in item["nli_scores"].items():

            print(
                f"  {stance}: {score * 100:.2f}%"
            )

        print("Article:", item["article"][:300])

        print("-" * 60)

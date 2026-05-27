from datetime import datetime
from monitoring.axiom_setup import axiom, DATASET


def log_prediction(
    prediction,
    latency,
    geography,
    psi_scores: dict = None,
    credit_score=None,
    age=None,
    balance=None,
    salary=None,
    tenure=None
):

    event = {
        "_time": datetime.utcnow().isoformat(),
        "prediction": prediction,
        "latency_ms": latency,
        "geography": geography,
        "credit_score": credit_score,
        "age": age,
        "balance": balance,
        "salary": salary,
        "tenure": tenure,
    }

    if psi_scores:
        for feature, psi_val in psi_scores.items():
            event[f"psi_{feature}"] = psi_val

    axiom.ingest_events(
        dataset=DATASET,
        events=[event]
    )
import numpy as np

def compute_psi(reference: list[float], production: list[float], bins: int = 10) -> float:
    """
    Compute PSI between a reference distribution and current production data.
    PSI < 0.1  → no significant shift
    PSI 0.1–0.2 → moderate shift (monitor closely)
    PSI > 0.2  → significant shift (investigate / retrain)
    """
    ref = np.array(reference)
    prod = np.array(production)

    breakpoints = np.percentile(ref, np.linspace(0, 100, bins + 1))
    breakpoints[0] = -np.inf
    breakpoints[-1] = np.inf

    ref_counts  = np.histogram(ref,  bins=breakpoints)[0]
    prod_counts = np.histogram(prod, bins=breakpoints)[0]

    ref_pct  = np.where(ref_counts  == 0, 1e-6, ref_counts  / len(ref))
    prod_pct = np.where(prod_counts == 0, 1e-6, prod_counts / len(prod))

    psi_value = np.sum((prod_pct - ref_pct) * np.log(prod_pct / ref_pct))
    return float(round(psi_value, 4))
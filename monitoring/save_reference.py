# scripts/save_reference.py
import json, pandas as pd

df = pd.read_csv("data/train.csv")

reference = {
    "CreditScore":     df["CreditScore"].tolist(),
    "Age":             df["Age"].tolist(),
    "Balance":         df["Balance"].tolist(),
    "EstimatedSalary": df["EstimatedSalary"].tolist(),
    "Tenure":          df["Tenure"].tolist(),
}

with open("monitoring/reference.json", "w") as f:
    json.dump(reference, f)

print("Reference distributions saved.")
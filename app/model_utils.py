"""
Model loading and prediction logic.

The model must be loaded ONCE at module level, NOT inside the predict function.
"""
import pickle
import numpy as np
import pandas as pd
import logging

with open('./data/model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('./data/transformer.pkl', 'rb') as file:
    transformer = pickle.load(file)

def preprocess(features: list[float]) -> list[float]:
    """
    Takes raw features and applies necessary preprocessing (e.g. scaling).
    """
    columns = [
        "CreditScore",
        "Geography",
        "Gender",
        "Age",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "IsActiveMember",
        "EstimatedSalary"
    ]

    df = pd.DataFrame([features], columns=columns)

    processed_features = transformer.transform(df)
    return processed_features

def predict_churn(features: list[float]) -> int:
    """
    Takes a list of raw feature values and returns a churn prediction (0 or 1).
    """
    # TODO 3: Preprocess the features
    processed_features = preprocess(features)
    
    # TODO 4: Use model.predict() on processed_features to get a prediction and return it as an int
    #         Hint: model.predict() expects a 2D array
    processed_features = np.array(processed_features).reshape(1, -1)
    prediction = model.predict(processed_features)
    return int(prediction[0])


if __name__ == "__main__":
    # TODO 5: Replace with sample features that match your model
    sample = [650,"France","Female",35,5,50000,2,1,1,75000]
    print(f"Input:      {sample}")
    print(f"Prediction: {predict_churn(sample)}")

from locust import HttpUser, task, between
import random


class LoadTestUser(HttpUser):

    wait_time = between(1, 2)

    @task
    def predict(self):

        payload = {
            "CreditScore": random.randint(300, 900),

            "Geography": random.choice([
                "France",
                "Germany",
                "Spain"
            ]),

            "Gender": random.choice([
                "Male",
                "Female"
            ]),

            "Age": random.randint(18, 80),

            "Tenure": random.randint(0, 10),

            "Balance": round(
                random.uniform(0, 250000),
                2
            ),

            "NumOfProducts": random.randint(1, 4),

            "HasCrCard": random.choice([0, 1]),

            "IsActiveMember": random.choice([0, 1]),

            "EstimatedSalary": round(
                random.uniform(10000, 200000),
                2
            )
        }

        self.client.post(
            "/predict",
            json=payload
        )
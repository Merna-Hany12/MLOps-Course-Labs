from locust import HttpUser, task, between

class LoadTestUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def predict(self):
        self.client.post(
            "/predict",
            json={
                "CreditScore": 650,
                "Geography": "France",
                "Gender": "Female",
                "Age": 35,
                "Tenure": 5,
                "Balance": 50000,
                "NumOfProducts": 2,
                "HasCrCard": 1,
                "IsActiveMember": 1,
                "EstimatedSalary": 75000
            }
        )
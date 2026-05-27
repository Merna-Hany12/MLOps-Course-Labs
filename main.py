"""
Churn Prediction API

Run with:
    litestar --app main:app run --reload
Then open:
    http://localhost:8000/schema/swagger
"""

from litestar import Litestar,get,post
from pydantic import BaseModel
from monitoring.metrics import log_prediction
import time
from app.logger_setup import setup_logging
from app.model_utils import predict_churn
from typing import Dict, Any
import json
from monitoring.psi import compute_psi

logger = setup_logging()


# ---------------------------------------------------------------------------
# Request Schema
# ---------------------------------------------------------------------------
from pydantic import BaseModel

class ChurnRequest(BaseModel):
    CreditScore: float
    Geography: str
    Gender: str
    Age: float
    Tenure: float
    Balance: float
    NumOfProducts: float
    HasCrCard: float
    IsActiveMember: float
    EstimatedSalary: float


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@get("/")
async def index() -> str:
    logger.info("Home endpoint accessed")
    return "Welcome to the Churn Prediction API!"

@get("/health")
async def health() -> dict:
    logger.info("Health endpoint accessed")
    return {"status": "healthy"}



# Load reference distributions once at startup
with open("monitoring/reference.json") as f:
    REFERENCE = json.load(f)

# Rolling buffer — collect requests in memory, flush PSI every N requests
_psi_buffer: dict[str, list[float]] = {k: [] for k in REFERENCE}
PSI_BATCH_SIZE = 50  # compute PSI every 50 requests

@post("/predict")
async def predict(data: ChurnRequest) -> Dict[str, Any]:
    start = time.time()

    features = [
        data.CreditScore, data.Geography, data.Gender,
        data.Age, data.Tenure, data.Balance,
        data.NumOfProducts, data.HasCrCard,
        data.IsActiveMember, data.EstimatedSalary
    ]

    prediction = predict_churn(features)
    latency = (time.time() - start) * 1000

    # Accumulate numeric features into the buffer
    _psi_buffer["CreditScore"].append(data.CreditScore)
    _psi_buffer["Age"].append(data.Age)
    _psi_buffer["Balance"].append(data.Balance)
    _psi_buffer["EstimatedSalary"].append(data.EstimatedSalary)
    _psi_buffer["Tenure"].append(data.Tenure)

    # Compute PSI once we have enough samples
    psi_scores = None
    if len(_psi_buffer["CreditScore"]) >= PSI_BATCH_SIZE:
        psi_scores = {
            feature: compute_psi(REFERENCE[feature], _psi_buffer[feature])
            for feature in REFERENCE
        }
        logger.info(f"PSI scores: {psi_scores}")
        # Reset buffer after computing
        for k in _psi_buffer:
            _psi_buffer[k].clear()

    log_prediction(
        prediction=prediction,
        latency=latency,
        geography=data.Geography,
        psi_scores=psi_scores,
        credit_score=data.CreditScore,
        age=data.Age,
        balance=data.Balance,
        salary=data.EstimatedSalary,
        tenure=data.Tenure,
    )

    return {"prediction": prediction}
# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = Litestar(
    route_handlers=[index,health,predict],
)

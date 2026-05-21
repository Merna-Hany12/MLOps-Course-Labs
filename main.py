"""
Churn Prediction API

Run with:
    litestar --app main:app run --reload
Then open:
    http://localhost:8000/schema/swagger
"""

from litestar import Litestar,get,post
from pydantic import BaseModel

from app.logger_setup import setup_logging
from app.model_utils import predict_churn
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
@post("/predict")
async def predict(data:ChurnRequest)-> dict:
    features = [
        data.CreditScore,
        data.Geography,
        data.Gender,
        data.Age,
        data.Tenure,
        data.Balance,
        data.NumOfProducts,
        data.HasCrCard,
        data.IsActiveMember,
        data.EstimatedSalary
    ]
    prediction=predict_churn(features)

    logger.info(f"Input features: {features}")
    logger.info(f"Prediction result: {prediction}")
    return {"prediction": prediction}

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = Litestar(
    route_handlers=[index,health,predict],
)

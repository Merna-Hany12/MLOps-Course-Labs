import os
from axiom_py import Client

axiom = Client(
    token=os.getenv("AXIOM_TOKEN")
)

DATASET = os.getenv("AXIOM_DATASET")
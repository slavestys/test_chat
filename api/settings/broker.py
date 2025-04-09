import os

BROKER_URL = os.getenv("BROKER_URL", default="localhost:9092")
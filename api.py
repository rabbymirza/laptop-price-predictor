import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Laptop Price Predictor API")

# Model Load
pipe = joblib.load("model/pipe.joblib")


class LaptopInput(BaseModel):
    company: str
    typename: str
    ram: int
    weight: float
    touchscreen: int
    ips: int
    ppi: float
    cpu: str
    hdd: int
    ssd: int
    gpu: str
    os: str


@app.get("/")
def home():
    return {"message": "Welcome to Laptop Price Prediction API!"}


@app.post("/predict")
def predict_price(data: LaptopInput):
    # Model train korar somoy jei column name chilo, thik seivabe DataFrame toiri kora:
    query = pd.DataFrame(
        [
            {
                "Company": data.company,
                "TypeName": data.typename,
                "Ram": data.ram,
                "Weight": data.weight,
                "Touchscreen": data.touchscreen,
                "IPS": data.ips,
                "ppi": data.ppi,
                "Cpu brand": data.cpu,
                "HDD": data.hdd,
                "SSD": data.ssd,
                "Gpu brand": data.gpu,
                "os": data.os,
            }
        ]
    )

    # Predict log price and convert to actual price
    prediction = pipe.predict(query)
    predicted_price = np.exp(prediction[0])

    return {"predicted_price_bdt": round(float(predicted_price), 2)}
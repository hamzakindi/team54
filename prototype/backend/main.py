from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path

app = FastAPI(title="Diabetes Prediction API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
MODEL_PATH = Path("../dataset/diabetes-prediction-model.joblib")
model = joblib.load(MODEL_PATH)

# Define feature names
FEATURE_NAMES = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

class PredictionInput(BaseModel):
    pregnancies: float
    glucose: float
    bloodPressure: float
    skinThickness: float
    insulin: float
    bmi: float
    diabetesPedigreeFunction: float
    age: float

    class Config:
        schema_extra = {
            "example": {
                "pregnancies": 1,
                "glucose": 103,
                "bloodPressure": 30,
                "skinThickness": 38,
                "insulin": 83,
                "bmi": 43.3,
                "diabetesPedigreeFunction": 0.183,
                "age": 33
            }
        }

@app.post("/predict")
async def predict(data: PredictionInput):
    try:
        # Convert input data to DataFrame
        input_data = pd.DataFrame(
            [[
                data.pregnancies,
                data.glucose,
                data.bloodPressure,
                data.skinThickness,
                data.insulin,
                data.bmi,
                data.diabetesPedigreeFunction,
                data.age
            ]],
            columns=FEATURE_NAMES
        )
        
        # Make prediction
        prediction = model.predict(input_data)
        probability = model.predict_proba(input_data)
        
        return {
            "prediction": int(prediction[0]),
            "probability": float(probability[0][1]),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
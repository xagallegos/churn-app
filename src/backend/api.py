from fastapi import FastAPI, Depends, Security, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from pydantic import BaseModel
import uvicorn
import pickle

class FeaturesModel(BaseModel):
    SeniorCitizen: int
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    gender_Female: bool
    gender_Male: bool
    Partner_No: bool
    Partner_Yes: bool
    Dependents_No: bool
    Dependents_Yes: bool
    PhoneService_No: bool
    PhoneService_Yes: bool
    MultipleLines_No: bool
    MultipleLines_No_phone_service: bool
    MultipleLines_Yes: bool
    InternetService_DSL: bool
    InternetService_Fiber_optic: bool
    InternetService_No: bool
    OnlineSecurity_No: bool
    OnlineSecurity_No_internet_service: bool
    OnlineSecurity_Yes: bool
    OnlineBackup_No: bool
    OnlineBackup_No_internet_service: bool
    OnlineBackup_Yes: bool
    DeviceProtection_No: bool
    DeviceProtection_No_internet_service: bool
    DeviceProtection_Yes: bool
    TechSupport_No: bool
    TechSupport_No_internet_service: bool
    TechSupport_Yes: bool
    StreamingTV_No: bool
    StreamingTV_No_internet_service: bool
    StreamingTV_Yes: bool
    StreamingMovies_No: bool
    StreamingMovies_No_internet_service: bool
    StreamingMovies_Yes: bool
    Contract_Month_to_month: bool
    Contract_One_year: bool
    Contract_Two_year: bool
    PaperlessBilling_No: bool
    PaperlessBilling_Yes: bool
    PaymentMethod_Bank_transfer: bool
    PaymentMethod_Credit_card: bool
    PaymentMethod_Electronic_check: bool
    PaymentMethod_Mailed_check: bool

app = FastAPI()

API_KEY = "ChurnModel-2024$*"
API_KEY_NAME = "api_key"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_query: str = Security(api_key_query)):
    if api_key_query == API_KEY:
        return api_key_query
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

@app.on_event("startup")
def load_model():
    import mlflow
    global logged_model

    mlflow.set_tracking_uri('https://dagshub.com/xagallegos/churn-app.mlflow')
    logged_model = 'runs:/c83fd81e4f8c43f18b23ddc2ed180e6a/ada_boost_classifier'
    logged_model = mlflow.pyfunc.load_model(logged_model)

@app.get("/api/v1/classify")
def classify(features_model: FeaturesModel, api_key: str = Depends(get_api_key)):
    import pandas as pd
    features = [val for val in features_model.__dict__.values()]

    prediction = logged_model.predict([features])

    label_dict = {
        0: "Not churn",
        1: "Churn"
    }

    return {"prediction": label_dict[int(prediction[0])]}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=5000, log_level="info")

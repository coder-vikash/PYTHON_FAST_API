from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd
import os


# Check whether model file exists
print(os.path.exists("model.pkl"))

# Load the ML model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)


# Create FastAPI app
app = FastAPI()


# City lists
tier_1_cities = [
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Chennai",
    "Kolkata",
    "Hyderabad",
    "Pune"
]

tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna",
    "Ranchi", "Visakhapatnam", "Coimbatore", "Bhopal",
    "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur",
    "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun",
    "Mysore", "Jabalpur", "Guwahati",
    "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli",
    "Belgaum", "Salem", "Vijayawada",
    "Tiruchirappalli", "Bhavnagar", "Gwalior",
    "Dhanbad", "Bareilly", "Aligarh", "Gaya",
    "Kozhikode", "Warangal", "Kolhapur",
    "Bilaspur", "Jalandhar", "Noida",
    "Guntur", "Asansol", "Siliguri"
]


# User Input Schema
class UserInput(BaseModel):

    age: Annotated[
        int,
        Field(..., gt=0, lt=120,
              description="Age of the user")
    ]

    weight: Annotated[
        float,
        Field(..., gt=0,
              description="Weight of the user")
    ]

    height: Annotated[
        float,
        Field(..., gt=0, lt=2.5,
              description="Height of the user in meters")
    ]

    income_lpa: Annotated[
        float,
        Field(..., gt=0,
              description="Annual salary in LPA")
    ]

    smoker: Annotated[
        bool,
        Field(...,
              description="Is the user a smoker?")
    ]

    city: Annotated[
        str,
        Field(...,
              min_length=1,
              max_length=120,
              description="City of the user")
    ]

    occupation: Annotated[
        Literal[
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job"
        ],
        Field(...,
              description="Occupation of the user")
    ]

    # BMI Calculation
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    # Lifestyle Risk Calculation
    @computed_field
    @property
    def lifestyle_risk(self) -> str:

        if self.smoker and self.bmi > 30:
            return "high"

        elif self.smoker or self.bmi > 27:
            return "medium"

        else:
            return "low"

    # Age Group Calculation
    @computed_field
    @property
    def age_group(self) -> str:

        if self.age < 25:
            return "young"

        elif self.age < 45:
            return "adult"

        elif self.age < 60:
            return "middle_age"

        else:
            return "senior"

    # City Tier Calculation
    @computed_field
    @property
    def city_tier(self) -> int:

        if self.city in tier_1_cities:
            return 1

        elif self.city in tier_2_cities:
            return 2

        else:
            return 3


# Prediction API
@app.post("/predict")
def predict_premium(data: UserInput):

    # Create DataFrame for prediction
    input_df = pd.DataFrame([{

        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation

    }])

    # Make prediction
    prediction = model.predict(input_df)[0]

    # Return response
    return JSONResponse(
        status_code=200,
        content={
            "predicted_category": str(prediction)
        }
    )
from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal,Optional
import json

app = FastAPI()


# ------------------------- Patient Model ------------------------- #

class Patient(BaseModel):
    id: Annotated[
        str,
        Field(
            ...,
            description="Unique ID of the patient",
            example="P002"
        )
    ]

    name: Annotated[
        str,
        Field(
            ...,
            description="Full name of the patient",
            example="Rahul Kumar"
        )
    ]

    city: Annotated[
        str,
        Field(
            ...,
            description="City where the patient lives",
            example="Noida"
        )
    ]

    age: Annotated[
        int,
        Field(
            ...,
            gt=0,
            description="Age of the patient in years",
            example=25
        )
    ]

    gender: Annotated[
        Literal["male", "female", "others"],
        Field(
            ...,
            description="Gender of the patient",
            example="male"
        )
    ]

    height: Annotated[
        float,
        Field(
            ...,
            gt=0,
            description="Height of the patient in meters",
            example=1.75
        )
    ]

    weight: Annotated[
        float,
        Field(
            ...,
            gt=0,
            description="Weight of the patient in kilograms",
            example=70.5
        )
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


class PatientUpdate(BaseModel):
    name: str | None = None
    city: str | None = None
    age: int | None = Field(default=None, gt=0)
    gender: Literal["male", "female", "others"] | None = None
    height: float | None = Field(default=None, gt=0)
    weight: float | None = Field(default=None, gt=0)
# ------------------------- File Functions ------------------------- #

def load_data():
    try:
        with open("patient.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_data(data):
    with open("patient.json", "w") as f:
        json.dump(data, f, indent=4)


# ------------------------- Routes ------------------------- #

@app.get("/")
def hello():
    return {"message": "Hello World"}


@app.get("/about")
def about():
    return {"message": "This is about page"}


@app.get("/view")
def view():
    return load_data()


@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ...,
        description="ID of the patient",
        example="P002"
    )
):
    data = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


@app.get("/sort")
def sort_patient(
    sort_by: str = Query(
        ...,
        description="Sort by height, weight or bmi"
    ),
    order: str = Query(
        "asc",
        description="Sorting order: asc or desc"
    )
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Choose from {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Order must be asc or desc"
        )

    data = load_data()

    reverse = order == "desc"

    sorted_data = sorted(
        data.values(),
        key=lambda patient: patient.get(sort_by, 0),
        reverse=reverse
    )

    return sorted_data


@app.post("/create-patient", status_code=201)
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail="Patient already exists"
        )

    patient_data = patient.model_dump()

    patient_id = patient_data.pop("id")

    data[patient_id] = patient_data

    save_data(data)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Patient created successfully",
            "patient": patient_data
        }
    )

@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient ID not found"
        )

    existing_patient_info = data[patient_id]

    # Only update the fields sent by the client
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    existing_patient_info.update(updated_patient_info)

    # Remove old computed fields if present
    existing_patient_info.pop("bmi", None)
    existing_patient_info.pop("verdict", None)

    # Add id back temporarily
    existing_patient_info["id"] = patient_id

    # Recalculate BMI and verdict
    patient_obj = Patient(**existing_patient_info)

    # Save everything except id
    data[patient_id] = patient_obj.model_dump(
        exclude={"id"},
        mode="json"
    )

    save_data(data)

    return {
        "message": "Patient updated successfully",
        "patient": data[patient_id]
    }


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    # Load existing data
    data = load_data()

    # Check if patient exists
    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Delete patient
    del data[patient_id]

    # Save updated data
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient deleted successfully",
            "deleted_patient": {
                "id": patient_id,
                
            }
        }
    )

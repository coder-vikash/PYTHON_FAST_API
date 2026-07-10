from fastapi import FastAPI,Path,HTTPException
import json
app = FastAPI()

def load_data():
    with open("patient.json","r") as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {"message": "Hello World"}

@app.get('/about')
def about():
    return {"message": "This is about page "}

@app.get('/view')
def view():
    data= load_data()

    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str = Path(...,description="ID of the patient in the DB", example="P002" )):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="patient not found")

from fastapi import FastAPI, Query, HTTPException

@app.get("/sort")
def sort_patient(
    sort_by: str = Query(
        ...,
        description="Sort by height, weight or bmi"
    ),
    order: str = Query(
        "asc",
        description="asc or desc"
    )
):
    valid_field = ["height", "weight", "bmi"]

    if sort_by not in valid_field:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Select from {valid_field}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Order must be asc or desc"
        )

    data = load_data()

    reverse = True if order == "desc" else False

    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse
    )

    return sorted_data
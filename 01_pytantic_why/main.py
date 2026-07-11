from pydantic import BaseModel
from typing import List, Dict

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    patient_alergy: List[str]
    marrage: bool
    patient_contactNo: Dict[str, str]


def Patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.marrage)
    print(patient.patient_alergy)
    print(patient.patient_contactNo)


Patient_info = {
    "name": "vikash",
    "age": 25,
    "weight": 68.5,
    "marrage": True,
    "patient_alergy": ["Dust", "Pollen"],
    "patient_contactNo": {
        "mobile": "1234567876",
        "home": "9876543210"
    }
}

patient1 = Patient(**Patient_info)

Patient_data(patient1)
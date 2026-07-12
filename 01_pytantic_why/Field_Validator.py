from pydantic import BaseModel,EmailStr,Field,field_validator
from typing import List, Dict,Optional,Annotated

class Patient(BaseModel):
    name :Annotated[
        str,
        Field(
            max_length=50,
            title="Name of the Patient",
            description="Give the name of the patient in less than 50 characters."
        )
    ]
    age: int= Field(gt=0, lt=120),
    email:EmailStr
    weight: Annotated[float, Field(ge=0,strict=True)]
    patient_alergy:Optional[List[str]]= None
    marrage: bool
    patient_contactNo: Dict[str, str]


    @field_validator("email")
    @classmethod
    def email_validator(cls,value):
        valid_domain= ["hdfc.com","icici.com","axis.com"]

        domain_name= value.split("@")[-1]

        if domain_name not in valid_domain:
            raise ValueError("Not a valid domain")
        return value
    

    @field_validator("name")
    @classmethod
    def Upper_Name(cls,value):
        return value.upper()

def Patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.weight)
    print(patient.marrage)
    print(patient.patient_alergy)
    print(patient.patient_contactNo)


Patient_info = {
    "name": "vikash",
    "age": 34,
    "email":"vk@axis.com",
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
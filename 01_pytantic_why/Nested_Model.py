from pydantic import BaseModel

class Address(BaseModel):

    city:str
    state:str
    pincode:str

class Patient(BaseModel):
    name:str
    age:int
    gender:str
    address:Address


address_disc = {'city' :"noida","state": "Greater Noida" ,"state":"UP", "pincode": "201310" }

address1 = Address(**address_disc)

patient_desc = {'name' :"Vikash ","age": 44, "gender":"male", "address": address1 }

patient_info = Patient(**patient_desc)

temp = patient_info.model_dump()

print(patient_info)
print(temp)
print("patient name:",patient_info.name)
print("patient age:",patient_info.age)

print("patient city:",patient_info.address.city)
print("patient state:",patient_info.address.state)

print("patient pincode:",patient_info.address.pincode)


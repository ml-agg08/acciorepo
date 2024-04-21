from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from fastapi import FastAPI, Form

app=FastAPI()

# Define a Pydantic model to validate the data
class Patient(BaseModel):
    name: str
    email: str

# Route to handle the form submission
@app.post("/submit_patient_details/")
async def submit_patient_details(name: str = Form(...), email: str = Form(...)):
    # Create a patient instance
    patient = Patient(name=name, email=email)
    # Append patient data to the JSON file
    file_path = 'patients.json'
    if os.path.exists(file_path):
        with open(file_path, 'r+') as file:
            data = json.load(file)  # Load existing data
            data.append(patient.dict())  # Append new data
            file.seek(0)  # Move to the start of file
            json.dump(data, file, indent=4)  # Write updated data
    else:
        with open(file_path, 'w') as file:
            json.dump([patient.dict()], file, indent=4)  # Create new file with data
    
    return {"message": "Patient details submitted successfully"}

# Run the application using Uvicorn
if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
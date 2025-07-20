from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import json
import os
from typing import Optional, Dict, Any

app = FastAPI(title="Patient Management System", 
              description="A comprehensive system for managing patient data, appointments, and medical records",
              version="1.0.0")

# Pydantic models for request/response validation
class Patient(BaseModel):
    name: str
    city: str
    age: int
    gender: str
    height: float
    weight: float
    bmi: Optional[float] = None
    verdict: Optional[str] = None

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None

def get_file_path():
    """Get the absolute path to patients.json file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'patients.json')

def load_data():
    """Load patient data from JSON file"""
    try:
        with open(get_file_path(), 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error reading patient data")

def save_data(data):
    """Save patient data to JSON file"""
    try:
        with open(get_file_path(), 'w') as file:
            json.dump(data, file, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")

def calculate_bmi(height: float, weight: float) -> float:
    """Calculate BMI given height (in meters) and weight (in kg)"""
    return round(weight / (height ** 2), 2)

def get_bmi_verdict(bmi: float) -> str:
    """Determine BMI verdict based on BMI value"""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def generate_patient_id(data: dict) -> str:
    """Generate a new patient ID"""
    if not data:
        return "P001"
    
    max_id = max([int(pid[1:]) for pid in data.keys()])
    return f"P{str(max_id + 1).zfill(3)}"

# API Endpoints

@app.get("/", tags=["Home"])
def root():
    """Welcome message for the Patient Management System"""
    return {
        "message": "Welcome to Patient Management System",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "This welcome message",
            "GET /about": "System information",
            "GET /patients": "View all patients",
            "GET /patients/{patient_id}": "View specific patient",
            "POST /patients": "Add new patient",
            "PUT /patients/{patient_id}": "Update patient",
            "DELETE /patients/{patient_id}": "Delete patient",
            "GET /patients/city/{city}": "Get patients by city",
            "GET /patients/stats": "Get patient statistics"
        }
    }

@app.get("/about", tags=["Home"])
def about():
    """Information about the system"""
    return {
        "message": "A full-fledged Patient Management System for managing patient data, appointments, and medical records.",
        "features": [
            "Add, update, delete patient records",
            "Automatic BMI calculation",
            "Search patients by city",
            "Patient statistics",
            "Data validation and error handling"
        ],
        "author": "Patient Management System v1.0"
    }

@app.get("/patients", tags=["Patients"])
def get_all_patients():
    """Retrieve all patients"""
    data = load_data()
    if not data:
        return {"message": "No patients found", "patients": {}}
    return {"total_patients": len(data), "patients": data}

@app.get("/patients/{patient_id}", tags=["Patients"])
def get_patient(patient_id: str):
    """Retrieve a specific patient by ID"""
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"patient_id": patient_id, "patient_data": data[patient_id]}

@app.post("/patients", tags=["Patients"], status_code=status.HTTP_201_CREATED)
def add_patient(patient: Patient):
    """Add a new patient"""
    data = load_data()
    
    # Generate new patient ID
    patient_id = generate_patient_id(data)
    
    # Calculate BMI and verdict
    bmi = calculate_bmi(patient.height, patient.weight)
    verdict = get_bmi_verdict(bmi)
    
    # Create patient record
    patient_data = {
        "name": patient.name,
        "city": patient.city,
        "age": patient.age,
        "gender": patient.gender,
        "height": patient.height,
        "weight": patient.weight,
        "bmi": bmi,
        "verdict": verdict
    }
    
    # Add to data and save
    data[patient_id] = patient_data
    save_data(data)
    
    return {
        "message": "Patient added successfully",
        "patient_id": patient_id,
        "patient_data": patient_data
    }

@app.put("/patients/{patient_id}", tags=["Patients"])
def update_patient(patient_id: str, patient_update: PatientUpdate):
    """Update an existing patient"""
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Update only provided fields
    patient_data = data[patient_id]
    update_data = patient_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        patient_data[field] = value
    
    # Recalculate BMI if height or weight changed
    if "height" in update_data or "weight" in update_data:
        patient_data["bmi"] = calculate_bmi(patient_data["height"], patient_data["weight"])
        patient_data["verdict"] = get_bmi_verdict(patient_data["bmi"])
    
    data[patient_id] = patient_data
    save_data(data)
    
    return {
        "message": "Patient updated successfully",
        "patient_id": patient_id,
        "patient_data": patient_data
    }

@app.delete("/patients/{patient_id}", tags=["Patients"])
def delete_patient(patient_id: str):
    """Delete a patient"""
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    deleted_patient = data.pop(patient_id)
    save_data(data)
    
    return {
        "message": "Patient deleted successfully",
        "deleted_patient_id": patient_id,
        "deleted_patient_data": deleted_patient
    }

@app.get("/patients/city/{city}", tags=["Search"])
def get_patients_by_city(city: str):
    """Get all patients from a specific city"""
    data = load_data()
    city_patients = {
        pid: patient for pid, patient in data.items() 
        if patient.get("city", "").lower() == city.lower()
    }
    
    if not city_patients:
        return {"message": f"No patients found in {city}", "patients": {}}
    
    return {
        "city": city,
        "total_patients": len(city_patients),
        "patients": city_patients
    }

@app.get("/patients/stats", tags=["Statistics"])
def get_patient_statistics():
    """Get comprehensive patient statistics"""
    data = load_data()
    
    if not data:
        return {"message": "No patients found for statistics"}
    
    # Calculate statistics
    total_patients = len(data)
    ages = [p["age"] for p in data.values()]
    bmis = [p["bmi"] for p in data.values()]
    
    # Gender distribution
    gender_stats = {}
    for patient in data.values():
        gender = patient["gender"]
        gender_stats[gender] = gender_stats.get(gender, 0) + 1
    
    # City distribution
    city_stats = {}
    for patient in data.values():
        city = patient["city"]
        city_stats[city] = city_stats.get(city, 0) + 1
    
    # BMI verdict distribution
    verdict_stats = {}
    for patient in data.values():
        verdict = patient["verdict"]
        verdict_stats[verdict] = verdict_stats.get(verdict, 0) + 1
    
    return {
        "total_patients": total_patients,
        "age_statistics": {
            "average_age": round(sum(ages) / len(ages), 1),
            "min_age": min(ages),
            "max_age": max(ages)
        },
        "bmi_statistics": {
            "average_bmi": round(sum(bmis) / len(bmis), 2),
            "min_bmi": min(bmis),
            "max_bmi": max(bmis)
        },
        "gender_distribution": gender_stats,
        "city_distribution": city_stats,
        "bmi_verdict_distribution": verdict_stats
    }

# Keep the original view endpoint for backward compatibility
@app.get("/view", tags=["Legacy"])
def view():
    """Legacy endpoint - use /patients instead"""
    data = load_data()
    return data
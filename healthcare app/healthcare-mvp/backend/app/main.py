# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
from datetime import datetime, date, time
import uuid

# Import from current directory
#from .database import get_db, get_snowflake_connection
from . import models, schemas
from .ocr_processor_simple import ocr_processor  # Simple version

app = FastAPI(title="Healthcare MVP API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ============ PATIENT ENDPOINTS ============
@app.post("/patients/", response_model=schemas.PatientResponse)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.query(models.Patient).filter(models.Patient.email == patient.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.get("/patients/", response_model=List[schemas.PatientResponse])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients

@app.get("/patients/{patient_id}", response_model=schemas.PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# ============ DOCTOR ENDPOINTS ============
@app.get("/doctors/", response_model=List[schemas.DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    # Check if we have doctors, if not create some
    doctors = db.query(models.Doctor).all()
    if not doctors:
        # Create sample doctors
        sample_doctors = [
            models.Doctor(name="Dr. Rajesh Kumar", specialization="Cardiologist", hospital="Apollo Hospital", consultation_fee=800),
            models.Doctor(name="Dr. Priya Sharma", specialization="Dermatologist", hospital="Fortis Hospital", consultation_fee=600),
            models.Doctor(name="Dr. Amit Patel", specialization="Orthopedist", hospital="Max Hospital", consultation_fee=700),
            models.Doctor(name="Dr. Anjali Singh", specialization="Pediatrician", hospital="Medanta", consultation_fee=500),
            models.Doctor(name="Dr. Rohan Verma", specialization="General Physician", hospital="AIIMS", consultation_fee=400),
        ]
        db.add_all(sample_doctors)
        db.commit()
        doctors = sample_doctors
    return doctors

# ============ APPOINTMENT ENDPOINTS ============
@app.post("/appointments/", response_model=schemas.AppointmentResponse)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    # Check if patient exists
    patient = db.query(models.Patient).filter(models.Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Check if doctor exists
    doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Create appointment
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    
    # Add doctor info to response
    from sqlalchemy.orm import joinedload
    db_appointment = db.query(models.Appointment)\
        .options(joinedload(models.Appointment.doctor))\
        .filter(models.Appointment.id == db_appointment.id)\
        .first()
    
    return db_appointment

@app.get("/appointments/patient/{patient_id}", response_model=List[schemas.AppointmentResponse])
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    from sqlalchemy.orm import joinedload
    appointments = db.query(models.Appointment)\
        .options(joinedload(models.Appointment.doctor))\
        .filter(models.Appointment.patient_id == patient_id)\
        .all()
    return appointments

# ============ MEDICAL RECORDS ENDPOINTS ============
@app.post("/medical-records/upload/")
async def upload_medical_record(
    patient_id: int = Form(...),
    doctor_id: Optional[int] = Form(None),
    appointment_id: Optional[int] = Form(None),
    record_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate patient exists
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Generate unique filename
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
    unique_filename = f"{patient_id}_{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Process with SIMPLE OCR (no Tesseract needed)
    # For now, just create mock extracted data
    extracted_data = ocr_processor.parse_medical_report(f"Uploaded: {file.filename}")
    
    # Save to database
    db_record = models.MedicalRecord(
        patient_id=patient_id,
        doctor_id=doctor_id,
        appointment_id=appointment_id,
        record_type=record_type,
        file_name=file.filename,
        file_path=file_path,
        extracted_data=extracted_data
    )
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return {
        "message": "File uploaded successfully",
        "record_id": db_record.id,
        "filename": file.filename,
        "extracted_data": extracted_data
    }

@app.get("/medical-records/patient/{patient_id}", response_model=List[schemas.MedicalRecordResponse])
def get_patient_records(patient_id: int, db: Session = Depends(get_db)):
    records = db.query(models.MedicalRecord)\
        .filter(models.MedicalRecord.patient_id == patient_id)\
        .order_by(models.MedicalRecord.uploaded_at.desc())\
        .all()
    return records

@app.get("/medical-records/{record_id}")
def get_record_details(record_id: int, db: Session = Depends(get_db)):
    record = db.query(models.MedicalRecord).filter(models.MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    # Check if file exists
    file_exists = os.path.exists(record.file_path) if record.file_path else False
    
    return {
        "record": record,
        "file_exists": file_exists,
        "download_url": f"http://localhost:8000/download/{os.path.basename(record.file_path)}" if record.file_path else None
    }

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    from fastapi.responses import FileResponse
    return FileResponse(file_path, filename=filename)

# ============ HEALTH CHECK ============
@app.get("/")
def read_root():
    return {"message": "Healthcare MVP API is running!", "status": "healthy"}

@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    try:
        # Try to query patients
        count = db.query(models.Patient).count()
        return {"database": "connected", "patient_count": count}
    except Exception as e:
        return {"database": "error", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
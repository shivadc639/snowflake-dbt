# backend/app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import date, time, datetime
from typing import Optional, List, Dict, Any

class PatientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    dob: date

class PatientResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    dob: date
    created_at: datetime
    
    class Config:
        from_attributes = True

class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    hospital: str
    consultation_fee: int
    
    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: str  # Changed from 'time' to 'str' for easier frontend handling
    symptoms: Optional[str] = ""

class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: str
    status: str
    symptoms: Optional[str]
    created_at: datetime
    doctor: DoctorResponse
    
    class Config:
        from_attributes = True

class MedicalRecordResponse(BaseModel):
    id: int
    patient_id: int
    record_type: str
    file_name: str
    extracted_data: Optional[Dict[str, Any]]
    uploaded_at: datetime
    
    class Config:
        from_attributes = True
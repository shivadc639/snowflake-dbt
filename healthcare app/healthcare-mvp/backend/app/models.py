# backend/app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, Date, Time, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(15))
    dob = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100))
    hospital = Column(String(200))
    consultation_fee = Column(Integer, default=500)

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    status = Column(String(20), default="scheduled")
    symptoms = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    patient = relationship("Patient")
    doctor = relationship("Doctor")

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    record_type = Column(String(50))
    file_name = Column(String(255))
    file_path = Column(String(500))
    extracted_data = Column(JSON)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    patient = relationship("Patient")
    doctor = relationship("Doctor", foreign_keys=[doctor_id])
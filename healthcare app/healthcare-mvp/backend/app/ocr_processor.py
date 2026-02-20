# backend/app/ocr_processor_simple.py
import json
import re
import random

class SimpleOCRProcessor:
    """Simple text parser for demo - no external dependencies needed"""
    
    def extract_from_image(self, image_path: str) -> str:
        # Mock data for demo
        mock_data = [
            "PATIENT: JOHN DOE\nAGE: 45\nDATE: 2024-01-15\nTEST: BLOOD TEST\nBP: 120/80\nGLUCOSE: 95\nCHOLESTEROL: 180",
            "Medical Report\nPatient: Sarah Smith\nDate: 2024-01-10\nDoctor: Dr. Johnson\nFindings: All parameters within normal range\nRecommendations: Annual checkup",
            "LAB REPORT\nPatient ID: P12345\nName: Robert Brown\nTest Date: 2024-01-05\nHbA1c: 5.8%\nWBC: 7.2\nRBC: 4.8",
            "X-Ray Report\nPatient: Maria Garcia\nDate: 2024-01-12\nFindings: No acute cardiopulmonary abnormality\nImpression: Normal chest x-ray",
            "Prescription\nPatient: David Lee\nDate: 2024-01-08\nMedications:\n1. Amoxicillin 500mg - 1 tab every 8 hours for 7 days\n2. Paracetamol 500mg - as needed for fever"
        ]
        return random.choice(mock_data)
    
    def extract_from_pdf(self, pdf_path: str) -> str:
        # Same mock data for PDF
        return self.extract_from_image(pdf_path)
    
    def parse_medical_report(self, text: str) -> dict:
        """Simple regex parser for medical reports"""
        result = {
            "patient_name": "Unknown",
            "test_date": "Unknown",
            "test_type": "Medical Report",
            "results": {},
            "notes": "",
            "summary": text[:150] + "..." if len(text) > 150 else text
        }
        
        # Parse patient name
        name_patterns = [
            r'PATIENT[:]?\s*([A-Z\s]+)',
            r'Patient[:]?\s*([A-Za-z\s]+)',
            r'Name[:]?\s*([A-Za-z\s]+)'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result["patient_name"] = match.group(1).strip()
                break
        
        # Parse date
        date_patterns = [
            r'DATE[:]?\s*(\d{4}-\d{2}-\d{2})',
            r'Date[:]?\s*(\d{2}/\d{2}/\d{4})',
            r'Test Date[:]?\s*([A-Za-z0-9\-\s]+)'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result["test_date"] = match.group(1).strip()
                break
        
        # Parse test type
        if 'blood' in text.lower():
            result["test_type"] = "Blood Test"
        elif 'x-ray' in text.lower() or 'xray' in text.lower():
            result["test_type"] = "X-Ray"
        elif 'prescription' in text.lower():
            result["test_type"] = "Prescription"
        elif 'lab' in text.lower():
            result["test_type"] = "Lab Report"
        
        # Parse common medical values
        medical_patterns = [
            (r'BP[:]?\s*(\d+/\d+)', 'Blood Pressure'),
            (r'GLUCOSE[:]?\s*(\d+)', 'Glucose'),
            (r'SUGAR[:]?\s*(\d+)', 'Blood Sugar'),
            (r'HbA1c[:]?\s*([\d.]+%)', 'HbA1c'),
            (r'CHOLESTEROL[:]?\s*(\d+)', 'Cholesterol'),
            (r'WBC[:]?\s*([\d.]+)', 'White Blood Cells'),
            (r'RBC[:]?\s*([\d.]+)', 'Red Blood Cells'),
            (r'HEMOGLOBIN[:]?\s*([\d.]+)', 'Hemoglobin'),
        ]
        
        for pattern, name in medical_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result["results"][name] = match.group(1)
        
        # Extract notes/findings
        if 'findings' in text.lower():
            start = text.lower().find('findings')
            end = text.lower().find('recommendations') if 'recommendations' in text.lower() else len(text)
            result["notes"] = text[start:end].strip()
        
        return result

# Create instance
ocr_processor = SimpleOCRProcessor()
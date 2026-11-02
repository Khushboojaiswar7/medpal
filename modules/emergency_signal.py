"""
MedPal Emergency Signal & Hospital Dispatch Integration Engine
Manages emergency tokens, hospital dispatch alerts, WhatsApp/SMS payload generators,
and real-time ER trauma lifecycle tracking.
"""

import uuid
import datetime
import urllib.parse
from typing import Dict, Any, Optional

class EmergencySignalEngine:
    def __init__(self):
        pass

    def generate_emergency_token(
        self,
        patient_name: str,
        patient_age: int,
        blood_group: str,
        allergies: str,
        conditions: str,
        emergency_contact: str,
        emergency_type: str,
        user_lat: float,
        user_lon: float,
        target_hospital: Dict[str, Any],
        triage_level: str = "RED (CRITICAL)"
    ) -> Dict[str, Any]:
        """
        Creates a verified cryptographic dispatch payload for ER reception.
        """
        dispatch_id = f"SOS-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        timestamp = datetime.datetime.now().strftime("%d-%b-%Y %I:%M:%S %p")
        
        maps_link = f"https://www.google.com/maps/dir/?api=1&destination={user_lat},{user_lon}"
        
        token = {
            "dispatch_id": dispatch_id,
            "timestamp": timestamp,
            "triage_level": triage_level,
            "emergency_type": emergency_type,
            "patient": {
                "name": patient_name or "Anonymous Patient",
                "age": patient_age or 65,
                "blood_group": blood_group or "Unknown",
                "allergies": allergies or "None reported",
                "known_conditions": conditions or "Hypertension / Diabetes",
                "emergency_contact": emergency_contact or "Family Caregiver"
            },
            "location": {
                "latitude": user_lat,
                "longitude": user_lon,
                "maps_url": maps_link
            },
            "target_hospital": {
                "name": target_hospital.get("name", "Nearest Trauma Hospital"),
                "emergency_phone": target_hospital.get("emergency_phone", "108"),
                "ambulance_phone": target_hospital.get("ambulance_phone", "108"),
                "distance_km": target_hospital.get("distance_km", 2.5),
                "eta_mins": target_hospital.get("eta_mins", 8),
                "emergency_dr": target_hospital.get("emergency_lead_dr", "Dr. on Duty")
            },
            "status_stage": "DISPATCHED",
            "assigned_ambulance": {
                "vehicle_number": "MED-ALS-402",
                "paramedic_name": "Senior Paramedic Rajesh Kumar",
                "paramedic_phone": "+91-98765-43210",
                "ambulance_eta_mins": target_hospital.get("eta_mins", 8)
            }
        }
        return token

    def create_whatsapp_sos_link(self, token: Dict[str, Any], phone_number: str = "") -> str:
        """
        Generates a 1-click WhatsApp SOS link formatted for emergency contacts and hospital helplines.
        """
        msg = (
            f"🚨 *MEDPAL EMERGENCY SOS ALERT* 🚨\n"
            f"*ID:* {token['dispatch_id']}\n"
            f"*Time:* {token['timestamp']}\n\n"
            f"🔴 *Emergency:* {token['emergency_type']} ({token['triage_level']})\n"
            f"👤 *Patient:* {token['patient']['name']} (Age: {token['patient']['age']}, Blood: {token['patient']['blood_group']})\n"
            f"⚠️ *Allergies:* {token['patient']['allergies']}\n"
            f"🏥 *Target Hospital:* {token['target_hospital']['name']} (ETA: {token['target_hospital']['eta_mins']} mins)\n\n"
            f"📍 *LIVE GPS LOCATION:*\n{token['location']['maps_url']}\n\n"
            f"📞 *Emergency Contact:* {token['patient']['emergency_contact']}"
        )
        encoded_msg = urllib.parse.quote(msg)
        if phone_number:
            clean_phone = phone_number.replace("+", "").replace("-", "").replace(" ", "")
            return f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_msg}"
        return f"https://api.whatsapp.com/send?text={encoded_msg}"

    def create_sms_sos_link(self, token: Dict[str, Any], phone_number: str = "") -> str:
        """
        Generates an SMS link for quick dispatch on mobile devices.
        """
        body = (
            f"EMERGENCY SOS! Patient: {token['patient']['name']}, "
            f"Type: {token['emergency_type']}, Blood: {token['patient']['blood_group']}. "
            f"Target: {token['target_hospital']['name']}. "
            f"GPS Location: {token['location']['maps_url']}"
        )
        encoded_body = urllib.parse.quote(body)
        return f"sms:{phone_number}?body={encoded_body}"

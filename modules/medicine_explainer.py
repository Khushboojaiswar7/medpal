"""
MedPal Medicine & Prescription Explainer Engine
Designed specifically for Elderly and Low-Literacy users.
Translates complex medical prescriptions into intuitive visual routines,
plain-language guidance, and automated drug-interaction safety checks.
"""

import re
from typing import List, Dict, Any, Optional
from PIL import Image
from modules.mock_data import MEDICINE_DATABASE

try:
    import pytesseract
    HAS_PYTESSERACT = True
except ImportError:
    HAS_PYTESSERACT = False

# Known dangerous drug pairs for interaction checking
DRUG_INTERACTIONS = [
    {
        "drugs": ["aspirin", "ibuprofen"],
        "severity": "HIGH",
        "warning": "Taking Aspirin and Ibuprofen together significantly increases the risk of stomach bleeding and ulcers."
    },
    {
        "drugs": ["aspirin", "warfarin"],
        "severity": "CRITICAL",
        "warning": "Both medicines thin the blood. Combining them without close doctor monitoring can cause severe internal bleeding."
    },
    {
        "drugs": ["amlodipine", "simvastatin"],
        "severity": "MODERATE",
        "warning": "Amlodipine increases blood levels of Simvastatin, raising the risk of muscle pain and weakness."
    },
    {
        "drugs": ["metformin", "alcohol"],
        "severity": "HIGH",
        "warning": "Alcohol combined with Metformin can cause dangerously low blood sugar and lactic acidosis."
    },
    {
        "drugs": ["paracetamol", "alcohol"],
        "severity": "HIGH",
        "warning": "Drinking alcohol while taking Paracetamol strains and damages the liver."
    }
]

class MedicineExplainer:
    def __init__(self, triage_engine=None):
        self.triage_engine = triage_engine
        self.db = MEDICINE_DATABASE

    def extract_text_from_image(self, image: Image.Image) -> str:
        """
        Attempts OCR on uploaded prescription image.
        """
        if not HAS_PYTESSERACT:
            return "OCR engine (pytesseract) is not configured in this environment."
        try:
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            return f"Could not read text from image automatically: {str(e)}"

    def parse_prescription_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Scans prescription text and identifies recognized medications,
        matching them against the simplified database and extracting dosage cues.
        """
        text_lower = text.lower()
        matched_meds = []

        for med_key, med_info in self.db.items():
            matched = False
            # Check generic name
            if med_key in text_lower or med_info["generic_name"].lower() in text_lower:
                matched = True
            # Check brand names
            for brand in med_info["brand_names"]:
                if brand.lower() in text_lower:
                    matched = True
                    break

            if matched:
                med_entry = dict(med_info)
                # Check timing mentions in prescription
                # e.g., 1-0-1 (morning and night), 1-1-1 (thrice), OD (once), BD (twice), TDS (thrice), HS (bedtime)
                morning = med_info["timings"]["morning"]
                afternoon = med_info["timings"]["afternoon"]
                night = med_info["timings"]["night"]

                if "1-0-0" in text_lower or "morning" in text_lower or "od" in text_lower:
                    morning = True
                    afternoon = False
                    night = False
                elif "1-0-1" in text_lower or "bd" in text_lower or "twice" in text_lower:
                    morning = True
                    afternoon = False
                    night = True
                elif "1-1-1" in text_lower or "tds" in text_lower or "thrice" in text_lower:
                    morning = True
                    afternoon = True
                    night = True
                elif "0-0-1" in text_lower or "hs" in text_lower or "bedtime" in text_lower:
                    morning = False
                    afternoon = False
                    night = True

                med_entry["active_timings"] = {
                    "morning": morning,
                    "afternoon": afternoon,
                    "night": night
                }
                matched_meds.append(med_entry)

        # Fallback if text contains unlisted medicines
        if not matched_meds and text.strip():
            # Create a generic breakdown for user's text
            matched_meds.append({
                "generic_name": "Custom Prescribed Medication",
                "brand_names": [text.strip()[:30]],
                "category": "Prescription Treatment",
                "simple_purpose": f"Medication specified in prescription: '{text.strip()[:60]}...'",
                "elderly_explanation": "Please take this medication exactly as directed by your doctor. Drink water and take with or after meals unless told otherwise.",
                "standard_dose": "As prescribed by physician",
                "timings": {
                    "morning": True,
                    "afternoon": False,
                    "night": True,
                    "frequency_note": "Twice daily with meals"
                },
                "active_timings": {"morning": True, "afternoon": False, "night": True},
                "food_relation": "After Food",
                "food_relation_icon": "🥗",
                "water_instructions": "Take with 1 full glass of water.",
                "warnings": ["Check with your pharmacist if you have any questions.", "Keep away from children."],
                "side_effects": ["Consult doctor if any unusual rash or discomfort occurs."],
                "pill_appearance": "Standard prescribed tablet/capsule."
            })

        return matched_meds

    def check_drug_interactions(self, detected_meds: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Cross-references detected medicines against dangerous drug interaction database.
        """
        interactions_found = []
        med_names = [m["generic_name"].lower() for m in detected_meds] + \
                    [brand.lower() for m in detected_meds for brand in m.get("brand_names", [])]

        for rule in DRUG_INTERACTIONS:
            d1, d2 = rule["drugs"][0], rule["drugs"][1]
            has_d1 = any(d1 in name for name in med_names)
            has_d2 = any(d2 in name for name in med_names)
            if has_d1 and has_d2:
                interactions_found.append(rule)

        return interactions_found

    def generate_elderly_friendly_summary(self, meds: List[Dict[str, Any]], language: str = "English") -> str:
        """
        Generates a simplified, 5th-grade reading level spoken summary.
        """
        if not meds:
            return "No medications currently loaded. Please type medicine names or upload a prescription."

        if language == "Hindi":
            lines = ["नमस्ते! यहाँ आपकी दवाओं का आसान विवरण है:"]
            for idx, m in enumerate(meds, 1):
                purpose = m.get("hindi_purpose", m["simple_purpose"])
                time_str = []
                if m.get("active_timings", {}).get("morning"): time_str.append("सुबह (Morning 🌅)")
                if m.get("active_timings", {}).get("afternoon"): time_str.append("दोपहर (Afternoon ☀️)")
                if m.get("active_timings", {}).get("night"): time_str.append("रात (Night 🌙)")
                time_text = " और ".join(time_str) if time_str else "जरूरत पड़ने पर"

                lines.append(
                    f"\n{idx}. **{m['generic_name']}**:\n"
                    f"   - **काम:** {purpose}\n"
                    f"   - **कब लेना है:** {time_text}\n"
                    f"   - **भोजन:** {m['food_relation']} {m['food_relation_icon']}\n"
                    f"   - **पानी:** {m['water_instructions']}"
                )
            return "\n".join(lines)
        else:
            lines = ["Hello! Here is your clear, easy-to-follow medicine guide:"]
            for idx, m in enumerate(meds, 1):
                time_str = []
                if m.get("active_timings", {}).get("morning"): time_str.append("Morning (Breakfast 🌅)")
                if m.get("active_timings", {}).get("afternoon"): time_str.append("Afternoon (Lunch ☀️)")
                if m.get("active_timings", {}).get("night"): time_str.append("Night (Dinner/Bedtime 🌙)")
                time_text = " & ".join(time_str) if time_str else "As needed"

                lines.append(
                    f"\n{idx}. **{m['generic_name']}** *(Brands: {', '.join(m['brand_names'][:2])})*:\n"
                    f"   - **Why you take it:** {m['elderly_explanation']}\n"
                    f"   - **When to take:** {time_text}\n"
                    f"   - **Food:** {m['food_relation']} {m['food_relation_icon']}\n"
                    f"   - **Drink with:** {m['water_instructions']}\n"
                    f"   - **Important:** {m['warnings'][0]}"
                )
            return "\n".join(lines)

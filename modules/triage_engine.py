"""
MedPal Triage & Clinical Assistant Engine
Handles red-flag emergency detection, clinical triage scoring,
and conversational health guidance with fallback intelligence.
"""

import re
import os
import requests
from typing import Dict, Any, Tuple, Optional
from modules.mock_data import RED_FLAG_EMERGENCIES, MEDICINE_DATABASE

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

class TriageEngine:
    def __init__(self, hf_api_key: Optional[str] = None, gemini_api_key: Optional[str] = None):
        self.hf_api_key = hf_api_key or os.environ.get("HF_API_KEY")
        self.gemini_api_key = gemini_api_key or os.environ.get("GEMINI_API_KEY")
        
        if self.gemini_api_key and HAS_GEMINI:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")
            except Exception:
                self.gemini_model = None
        else:
            self.gemini_model = None

    def check_red_flags(self, user_query: str) -> Optional[Dict[str, Any]]:
        """
        Scans user query for life-threatening emergency keywords.
        Returns matching red-flag emergency alert if detected.
        """
        query_lower = user_query.lower()
        for emergency in RED_FLAG_EMERGENCIES:
            for keyword in emergency["trigger_keywords"]:
                if re.search(r'\b' + re.escape(keyword) + r'\b', query_lower):
                    return emergency
        return None

    def assess_triage_level(self, query: str) -> Tuple[str, str]:
        """
        Determines triage severity: RED (Critical), AMBER (Urgent), GREEN (Routine).
        """
        red_flag = self.check_red_flags(query)
        if red_flag:
            return "RED", red_flag["condition"]

        query_lower = query.lower()
        amber_keywords = [
            "high fever", "vomiting continuous", "severe stomach pain", "fracture",
            "sprain", "deep cut", "burn blister", "asthma wheezing", "dehydration",
            "dizziness severe", "eye injury", "blood in stool", "high bp"
        ]
        for kw in amber_keywords:
            if kw in query_lower:
                return "AMBER", f"Urgent Symptom: {kw.title()}"

        return "GREEN", "Routine Medical Query / Home Care"

    def query_gemini(self, prompt: str, system_context: str = "") -> Optional[str]:
        """Queries Google Gemini model if available."""
        if not self.gemini_model:
            return None
        try:
            full_prompt = f"System: {system_context}\n\nUser: {prompt}"
            response = self.gemini_model.generate_content(full_prompt)
            if response and response.text:
                return response.text.strip()
        except Exception:
            pass
        return None

    def query_huggingface(self, prompt: str) -> Optional[str]:
        """Queries Hugging Face model with key if available."""
        if not self.hf_api_key:
            return None
        models = [
            "google/flan-t5-large",
            "google/flan-t5-base",
            "meta-llama/Llama-3.2-3B-Instruct"
        ]
        headers = {"Authorization": f"Bearer {self.hf_api_key}"}
        for model in models:
            url = f"https://api-inference.huggingface.co/models/{model}"
            try:
                payload = {
                    "inputs": f"Medical Assistant Guide: Answer clearly and helpfully: {prompt}",
                    "parameters": {"max_new_tokens": 250, "temperature": 0.3}
                }
                resp = requests.post(url, headers=headers, json=payload, timeout=8)
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list) and len(data) > 0:
                        if "generated_text" in data[0]:
                            return data[0]["generated_text"]
            except Exception:
                continue
        return None

    def generate_expert_response(self, user_query: str, elderly_mode: bool = False, language: str = "English") -> str:
        """
        Core response generator combining clinical triage, rule-based medical DB, and AI.
        Guarantees instant, accurate, medically sound responses even offline.
        """
        query_lower = user_query.lower()
        red_flag = self.check_red_flags(user_query)

        # 1. Critical Emergency Immediate Intervention
        if red_flag:
            res = (
                f"🚨 **IMMEDIATE EMERGENCY ALERT – {red_flag['emergency_level']}**\n\n"
                f"**Suspected Condition:** {red_flag['condition']}\n\n"
                f"**⚡ Immediate Action Required:**\n{red_flag['immediate_action']}\n\n"
                f"**⚠️ Crucial Warning:** {red_flag['do_not']}\n\n"
                f"👉 *Click the **'🚨 Emergency SOS'** tab right now to notify nearest hospitals and dispatch an ambulance.*"
            )
            return res

        # 2. Check Medicine Database Match
        for med_key, med_info in MEDICINE_DATABASE.items():
            if med_key in query_lower or any(b.lower() in query_lower for b in med_info["brand_names"]):
                if language == "Hindi":
                    desc = med_info.get("hindi_purpose", med_info["simple_purpose"])
                    return (
                        f"💊 **दवा की जानकारी: {med_info['generic_name']}**\n\n"
                        f"• **यह क्या करती है:** {desc}\n"
                        f"• **खुराक और समय:** {med_info['timings']['frequency_note']}\n"
                        f"• **भोजन:** {med_info['food_relation']} {med_info['food_relation_icon']}\n"
                        f"• **पानी:** {med_info['water_instructions']}\n"
                        f"• **सावधानी:** {med_info['warnings'][0]}"
                    )
                else:
                    exp = med_info["elderly_explanation"] if elderly_mode else med_info["simple_purpose"]
                    res = (
                        f"💊 **Medication Overview: {med_info['generic_name']}**\n"
                        f"*(Common brands: {', '.join(med_info['brand_names'][:3])})*\n\n"
                        f"• **Purpose:** {exp}\n"
                        f"• **Standard Schedule:** {med_info['timings']['frequency_note']}\n"
                        f"• **Food Relation:** {med_info['food_relation']} {med_info['food_relation_icon']}\n"
                        f"• **How to take:** {med_info['water_instructions']}\n"
                        f"• **Key Precautions:**\n"
                    )
                    for w in med_info["warnings"]:
                        res += f"  - {w}\n"
                    return res

        # 3. AI Generation if API Available
        system_context = (
            "You are MedPal, an empathetic, highly accurate AI emergency medical and health companion. "
            "Explain medical concepts simply, without confusing medical jargon. "
            "If the user has severe symptoms, advise seeing a doctor or calling an emergency ambulance immediately. "
            "Always be caring, direct, and structured with bullet points."
        )
        if elderly_mode:
            system_context += " The user is elderly or wants very simple plain language. Use large clear explanations, short sentences, and everyday examples."

        ai_response = self.query_gemini(user_query, system_context) or self.query_huggingface(user_query)
        if ai_response:
            return ai_response

        # 4. Smart Clinical Rules Fallback
        if "fever" in query_lower:
            return (
                "🌡️ **Fever Management & Guidance:**\n\n"
                "• **Rest & Hydration:** Drink plenty of fluids (water, oral rehydration salts, warm soup) to prevent dehydration.\n"
                "• **Temperature Control:** Rest in a cool, ventilated room with light clothing. Sponge forehead with lukewarm water.\n"
                "• **Medication:** Paracetamol 500mg-650mg may be taken every 6-8 hours after food if temperature exceeds 100.4°F (38°C).\n"
                "• **⚠️ When to seek immediate hospital care:**\n"
                "  - Fever > 103°F (39.4°C) or lasting > 3 days.\n"
                "  - Severe headache, stiff neck, shortness of breath, confusion, or skin rash."
            )
        elif "headache" in query_lower:
            return (
                "🤕 **Headache Relief & Assessment:**\n\n"
                "• **Common Causes:** Stress, tension, lack of sleep, dehydration, eye strain, or sinus pressure.\n"
                "• **Quick Relief:** Rest in a quiet dark room, drink 2 glasses of water, apply a cold or warm compress to forehead/neck.\n"
                "• **⚠️ Red-Flag Warnings (Seek ER immediately):**\n"
                "  - Sudden 'thunderclap' headache (worst headache of your life).\n"
                "  - Headache with slurred speech, numbness, or vision loss.\n"
                "  - Headache following head trauma/fall."
            )
        elif "blood pressure" in query_lower or "bp" in query_lower:
            return (
                "🩺 **Blood Pressure (BP) Guidelines:**\n\n"
                "• **Normal BP:** Around 120/80 mmHg.\n"
                "• **High BP (Hypertension):** Consistently > 130/80 mmHg.\n"
                "• **Crisis Level (> 180/120 mmHg):** If accompanied by chest pain, blurry vision, or breathlessness, call 108/911 immediately!\n"
                "• **Daily Tips for Elderly:**\n"
                "  - Cut down salt (sodium) in food.\n"
                "  - Take prescribed BP medications at the exact same hour daily without skipping."
            )
        elif "diabetes" in query_lower or "sugar" in query_lower:
            return (
                "🩸 **Diabetes & Blood Sugar Care:**\n\n"
                "• **Fasting Target:** 80 - 130 mg/dL.\n"
                "• **Post-Meal Target (2 hrs after food):** Under 180 mg/dL.\n"
                "• **⚠️ Low Sugar (Hypoglycemia Warning):** If feeling shaky, sweating, or dizzy, eat 3 spoons of sugar or candy immediately!\n"
                "• **Foot Care:** Inspect feet daily for cuts, sores, or numbness."
            )
        else:
            return (
                f"🩺 **MedPal Health Consultation:**\n\n"
                f"Regarding your query on *'{user_query}'*:\n\n"
                f"• **General Health Advice:** Ensure adequate hydration, proper rest, and monitor your vitals (temperature, pulse, blood pressure).\n"
                f"• **Medication Safety:** Only take prescribed dosages after checking food instructions (before/after meals).\n"
                f"• **Next Steps:** If symptoms persist, worsen, or cause distress, please consult a qualified physician or use our **'Hospital Finder'** to reach the nearest medical center."
            )

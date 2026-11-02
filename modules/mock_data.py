"""
MedPal Mock and Reference Database
Contains comprehensive curated data for hospitals, emergency response contacts,
medicine knowledge base, elderly-friendly explanations, and first-aid protocols.
"""

# Major real-world hospitals with emergency trauma centers and GPS coordinates
HOSPITALS_DATABASE = [
    {
        "id": "hosp_001",
        "name": "Apollo Emergency & Multi-Specialty Hospital",
        "type": "Level 1 Trauma & Multi-Specialty",
        "city": "Hyderabad",
        "address": "Road No. 72, Film Nagar, Jubilee Hills, Hyderabad",
        "lat": 17.4156,
        "lon": 78.4125,
        "emergency_phone": "+91-40-23607777",
        "ambulance_phone": "1066",
        "icu_beds_available": 14,
        "blood_bank": True,
        "cardiac_cath_lab": True,
        "rating": 4.8,
        "emergency_lead_dr": "Dr. Ramesh Varma (Trauma Chief)"
    },
    {
        "id": "hosp_002",
        "name": "AIIMS Emergency & Trauma Center",
        "type": "Apex Government Trauma Center",
        "city": "New Delhi",
        "address": "Ansari Nagar, Ring Road, New Delhi",
        "lat": 28.5672,
        "lon": 77.2100,
        "emergency_phone": "+91-11-26588500",
        "ambulance_phone": "102",
        "icu_beds_available": 22,
        "blood_bank": True,
        "cardiac_cath_lab": True,
        "rating": 4.9,
        "emergency_lead_dr": "Dr. Ananya Sen (Emergency Head)"
    },
    {
        "id": "hosp_003",
        "name": "Fortis Memorial Critical Care & Trauma Hospital",
        "type": "Level 1 Multi-Specialty Hospital",
        "city": "Gurugram",
        "address": "Sector 44, Opposite HUDA City Centre, Gurugram",
        "lat": 28.4595,
        "lon": 77.0725,
        "emergency_phone": "+91-124-4962200",
        "ambulance_phone": "105010",
        "icu_beds_available": 9,
        "blood_bank": True,
        "cardiac_cath_lab": True,
        "rating": 4.7,
        "emergency_lead_dr": "Dr. Siddharth Nair (Critical Care)"
    },
    {
        "id": "hosp_004",
        "name": "Manipal Emergency & Super Specialty Hospital",
        "type": "Tertiary Care & Trauma",
        "city": "Bengaluru",
        "address": "98 HAL Old Airport Rd, Kodihalli, Bengaluru",
        "lat": 12.9592,
        "lon": 77.6534,
        "emergency_phone": "+91-80-25024444",
        "ambulance_phone": "080-22221111",
        "icu_beds_available": 11,
        "blood_bank": True,
        "cardiac_cath_lab": True,
        "rating": 4.8,
        "emergency_lead_dr": "Dr. Pradeep Rao (ER Director)"
    },
    {
        "id": "hosp_005",
        "name": "Kokilaben Dhirubhai Ambani Emergency Hospital",
        "type": "Level 1 Trauma Care",
        "city": "Mumbai",
        "address": "Rao Saheb Achutrao Patwardhan Marg, Andheri West, Mumbai",
        "lat": 19.1311,
        "lon": 72.8252,
        "emergency_phone": "+91-22-30696969",
        "ambulance_phone": "022-30999999",
        "icu_beds_available": 16,
        "blood_bank": True,
        "cardiac_cath_lab": True,
        "rating": 4.9,
        "emergency_lead_dr": "Dr. Meera Kulkarni (Trauma Lead)"
    },
    {
        "id": "hosp_006",
        "name": "KIMS Emergency & General Hospital",
        "type": "General & Urgent Care Hospital",
        "city": "Secunderabad",
        "address": "1-8-31/1, Minister Rd, Krishna Nagar Colony, Secunderabad",
        "lat": 17.4375,
        "lon": 78.4870,
        "emergency_phone": "+91-40-44885000",
        "ambulance_phone": "108",
        "icu_beds_available": 7,
        "blood_bank": True,
        "cardiac_cath_lab": True,
        "rating": 4.6,
        "emergency_lead_dr": "Dr. K. Srinivas (ER Physician)"
    },
    {
        "id": "hosp_007",
        "name": "Max Super Speciality Hospital & Trauma Care",
        "type": "Multi-Specialty & Critical Care",
        "city": "Saket, New Delhi",
        "address": "1, 2, Press Enclave Marg, Saket, New Delhi",
        "lat": 28.5284,
        "lon": 77.2114,
        "emergency_phone": "+91-11-26515050",
        "ambulance_phone": "1055",
        "icu_beds_available": 18,
        "blood_bank": True,
        "cardiac_cath_lab": True,
        "rating": 4.8,
        "emergency_lead_dr": "Dr. Vikram Ahuja (Emergency Chief)"
    },
    {
        "id": "hosp_008",
        "name": "City Care Community 24x7 Emergency Clinic",
        "type": "Community Urgent Care Center",
        "city": "General",
        "address": "Central Medical Enclave, Main Boulevard",
        "lat": 17.3850,
        "lon": 78.4867,
        "emergency_phone": "112",
        "ambulance_phone": "108",
        "icu_beds_available": 4,
        "blood_bank": False,
        "cardiac_cath_lab": False,
        "rating": 4.4,
        "emergency_lead_dr": "Dr. Sarah Johnson (Medical Officer)"
    }
]

# Universal Emergency Contact Numbers
EMERGENCY_NUMBERS = {
    "India": {"Ambulance": "108", "Police": "100", "National Emergency": "112", "Disaster": "1077"},
    "USA": {"National Emergency": "911", "Poison Control": "1-800-222-1222"},
    "UK": {"Emergency": "999", "Non-Emergency NHS": "111"},
    "Europe": {"Universal Emergency": "112"}
}

# Simplified Medicine Knowledge Base for Elderly / Low-Literacy users
MEDICINE_DATABASE = {
    "paracetamol": {
        "generic_name": "Paracetamol (Acetaminophen)",
        "brand_names": ["Crocin", "Dolo 650", "Calpol", "Tylenol", "Panadol"],
        "category": "Pain & Fever Reducer",
        "simple_purpose": "Helps bring down fever and relieves mild to moderate body pain or headaches.",
        "hindi_purpose": "यह दवा बुखार कम करने और सिरदर्द या शरीर दर्द को ठीक करने के लिए है।",
        "elderly_explanation": "Take this when you feel hot with fever or have body pain. Do not take on an empty stomach. Drink plenty of water.",
        "standard_dose": "500mg - 650mg every 6 to 8 hours as needed (Max 3-4 tablets a day)",
        "timings": {
            "morning": False,
            "afternoon": False,
            "night": False,
            "frequency_note": "Take only when fever or pain is present (minimum 6 hours gap between doses)"
        },
        "food_relation": "After Food",
        "food_relation_icon": "🥗",
        "water_instructions": "Drink with 1 full glass of clean water.",
        "warnings": [
            "Do NOT drink alcohol while taking this medicine.",
            "Do NOT take more than 4 tablets in 24 hours (can damage liver).",
            "Check if your cold medicine already has Paracetamol/Acetaminophen."
        ],
        "side_effects": ["Rare, but can cause mild stomach upset if taken without food."],
        "pill_appearance": "White oval or round tablet."
    },
    "metformin": {
        "generic_name": "Metformin Hydrochloride",
        "brand_names": ["Glycomet", "Glucophage", "Obimet", "Riomet"],
        "category": "Sugar / Diabetes Medicine",
        "simple_purpose": "Lowers your blood sugar (glucose) levels and helps your body use insulin better.",
        "hindi_purpose": "यह दवा खून में शुगर (मधुमेह) को नियंत्रित रखने के लिए है।",
        "elderly_explanation": "This keeps your blood sugar normal. ALWAYS take it right with your meal or after finishing food so your tummy doesn't get upset.",
        "standard_dose": "500mg or 850mg or 1000mg with meals",
        "timings": {
            "morning": True,
            "afternoon": False,
            "night": True,
            "frequency_note": "Usually taken twice a day: with breakfast and with dinner"
        },
        "food_relation": "With or After Food",
        "food_relation_icon": "🍽️",
        "water_instructions": "Swallow whole with food and water. Do not crush.",
        "warnings": [
            "Never skip meals after taking this medicine.",
            "If you feel dizzy, sweaty, or shaky (low sugar), eat 1-2 sugar candies or fruit juice immediately.",
            "Tell your doctor if you have kidney problems."
        ],
        "side_effects": ["Loose motions or gas when starting (usually goes away in a week)."],
        "pill_appearance": "White capsule-shaped tablet."
    },
    "amlodipine": {
        "generic_name": "Amlodipine Besylate",
        "brand_names": ["Norvasc", "Amlong", "Amtas", "Stamlo"],
        "category": "Blood Pressure (BP) Medicine",
        "simple_purpose": "Relaxes your blood vessels so your heart pumps easily and your Blood Pressure stays normal.",
        "hindi_purpose": "यह दवा हाई ब्लड प्रेशर (बीपी) को सामान्य रखने के लिए है।",
        "elderly_explanation": "This protects your heart and brain from high pressure. Take it every day at the same fixed time (best in the morning).",
        "standard_dose": "5mg or 10mg once daily",
        "timings": {
            "morning": True,
            "afternoon": False,
            "night": False,
            "frequency_note": "Take once a day in the morning"
        },
        "food_relation": "Before or After Food",
        "food_relation_icon": "🥗",
        "water_instructions": "Take with 1 glass of water every morning.",
        "warnings": [
            "Do NOT stop taking suddenly even if you feel completely fine.",
            "Stand up slowly from bed or chair to avoid dizziness.",
            "Avoid grapefruit or grapefruit juice."
        ],
        "side_effects": ["Mild ankle swelling or lightheadedness when standing up quickly."],
        "pill_appearance": "Small white or light yellow tablet."
    },
    "atorvastatin": {
        "generic_name": "Atorvastatin Calcium",
        "brand_names": ["Lipitor", "Atorva", "Storvas", "Tonact"],
        "category": "Cholesterol & Heart Protection",
        "simple_purpose": "Reduces bad cholesterol and fat in your blood vessels to protect against heart attacks.",
        "hindi_purpose": "यह दवा खून में कोलेस्ट्रॉल और चर्बी कम करने के लिए है।",
        "elderly_explanation": "This cleans the fat from your heart arteries. The liver makes cholesterol at night, so take this pill at bedtime.",
        "standard_dose": "10mg, 20mg, or 40mg at bedtime",
        "timings": {
            "morning": False,
            "afternoon": False,
            "night": True,
            "frequency_note": "Take once daily at night before sleeping"
        },
        "food_relation": "After Dinner / Bedtime",
        "food_relation_icon": "🌙",
        "water_instructions": "Swallow with water at bedtime.",
        "warnings": [
            "Do not consume alcohol.",
            "If you experience severe unexplained muscle pain or weakness, notify your doctor."
        ],
        "side_effects": ["Mild muscle soreness or digestive change."],
        "pill_appearance": "White oval coated tablet."
    },
    "pantoprazole": {
        "generic_name": "Pantoprazole Sodium",
        "brand_names": ["Pan 40", "Pantocid", "Protonix", "Pantodac"],
        "category": "Acidity & Gas Relief",
        "simple_purpose": "Reduces acid production in the stomach, curing heartburn, burning chest, and stomach ulcers.",
        "hindi_purpose": "यह दवा पेट में गैस, जलन और एसिडिटी को खत्म करने के लिए है।",
        "elderly_explanation": "Take this FIRST THING in the morning, 30 minutes BEFORE eating breakfast. It forms a protective shield in your stomach.",
        "standard_dose": "40mg once daily in morning",
        "timings": {
            "morning": True,
            "afternoon": False,
            "night": False,
            "frequency_note": "Take 30-45 minutes before morning breakfast"
        },
        "food_relation": "Before Food (Empty Stomach)",
        "food_relation_icon": "⏳",
        "water_instructions": "Swallow whole with plain water on empty stomach. Do not chew.",
        "warnings": [
            "Must be taken BEFORE eating food for it to work properly.",
            "Do not crush or break the tablet."
        ],
        "side_effects": ["Very safe; rarely headache or mild stomach rumble."],
        "pill_appearance": "Yellow oval coated tablet."
    },
    "amoxicillin": {
        "generic_name": "Amoxicillin & Clavulanate",
        "brand_names": ["Augmentin", "Mox", "Amoxil", "Novamox", "Moxikind"],
        "category": "Antibiotic (Bacterial Infection Fighter)",
        "simple_purpose": "Kills harmful bacteria causing throat, chest, ear, skin, or urine infections.",
        "hindi_purpose": "यह एक एंटीबायोटिक दवा है जो संक्रमण (इन्फेक्शन) पैदा करने वाले कीटाणुओं को मारती है।",
        "elderly_explanation": "This kills the bad bacteria causing your infection. Complete the full course (e.g. 5 days) even if you feel better after 2 days!",
        "standard_dose": "500mg or 625mg twice or thrice daily for 5-7 days",
        "timings": {
            "morning": True,
            "afternoon": True,
            "night": True,
            "frequency_note": "Every 8 or 12 hours depending on prescription"
        },
        "food_relation": "After Food",
        "food_relation_icon": "🥗",
        "water_instructions": "Take with meals and plenty of water.",
        "warnings": [
            "DO NOT STOP halfway – finish all tablets prescribed by doctor.",
            "If you get skin rash, hives, or swelling, stop immediately and seek emergency care (allergic reaction)."
        ],
        "side_effects": ["Mild loose stools or nausea."],
        "pill_appearance": "White/red capsule or large white tablet."
    },
    "aspirin": {
        "generic_name": "Aspirin (Acetylsalicylic Acid)",
        "brand_names": ["Ecosprin", "Disprin", "Bayer Aspirin", "Loprin"],
        "category": "Blood Thinner & Heart Guard",
        "simple_purpose": "Prevents blood clots from blocking heart or brain vessels in elderly and cardiac patients.",
        "hindi_purpose": "यह दवा खून को पतला रखने और हार्ट अटैक से बचाने के लिए है।",
        "elderly_explanation": "This makes your blood smooth and prevents blood clots in your heart. Always take after food so it doesn't hurt your stomach.",
        "standard_dose": "75mg or 150mg once daily after main meal",
        "timings": {
            "morning": False,
            "afternoon": True,
            "night": False,
            "frequency_note": "Once daily, usually after lunch"
        },
        "food_relation": "After Food",
        "food_relation_icon": "🥗",
        "water_instructions": "Take with a full glass of water after food.",
        "warnings": [
            "Never take on an empty stomach.",
            "Watch out for unusual bleeding or dark black stools.",
            "Inform dentist or surgeon before any procedure that you take Aspirin."
        ],
        "side_effects": ["Stomach irritation if taken without food."],
        "pill_appearance": "Small round white tablet."
    },
    "telmisartan": {
        "generic_name": "Telmisartan",
        "brand_names": ["Telma", "Micardis", "Telpres", "Telsar"],
        "category": "Blood Pressure (BP) & Kidney Shield",
        "simple_purpose": "Relaxes blood vessels, lowers blood pressure, and protects kidneys in diabetics.",
        "hindi_purpose": "यह दवा उच्च रक्तचाप (High BP) को नियंत्रित करने के लिए है।",
        "elderly_explanation": "Protects your blood vessels and heart. Take once every day at the same morning hour.",
        "standard_dose": "40mg or 80mg once daily",
        "timings": {
            "morning": True,
            "afternoon": False,
            "night": False,
            "frequency_note": "Take once a day in the morning"
        },
        "food_relation": "Before or After Food",
        "food_relation_icon": "🥗",
        "water_instructions": "Drink with a glass of water.",
        "warnings": [
            "Check BP regularly.",
            "Do not consume potassium supplements without doctor advice."
        ],
        "side_effects": ["Dizziness when standing up suddenly."],
        "pill_appearance": "White or pinkish oblong tablet."
    }
}

# Red-Flag Emergency Symptoms Knowledge Base
RED_FLAG_EMERGENCIES = [
    {
        "trigger_keywords": ["chest pain", "heart attack", "crushing chest", "left arm pain", "radiating jaw pain", "tightness in chest", "angina"],
        "emergency_level": "RED (CRITICAL)",
        "condition": "Possible Acute Coronary Syndrome / Heart Attack",
        "immediate_action": "🚨 CRITICAL MEDICAL EMERGENCY: Call Emergency Services (108 / 911 / 112) or dispatch MedPal Hospital Signal immediately. Sit down, keep calm, loosen tight clothing. If not allergic, chew 300mg Aspirin if advised by emergency doctor.",
        "do_not": "Do NOT drive yourself to the hospital. Do NOT delay or wait for pain to pass."
    },
    {
        "trigger_keywords": ["cannot breathe", "severe breathlessness", "gasping for air", "choking", "blue lips", "unable to speak", "asthma attack severe"],
        "emergency_level": "RED (CRITICAL)",
        "condition": "Severe Respiratory Distress / Airway Obstruction",
        "immediate_action": "🚨 CRITICAL AIRWAY EMERGENCY: Sit upright, lean slightly forward. Use rescue inhaler (Salbutamol) immediately if asthmatic. Call ambulance immediately.",
        "do_not": "Do NOT lie down flat. Do NOT give water if choking."
    },
    {
        "trigger_keywords": ["slurred speech", "face drooping", "arm weakness", "sudden numbness", "stroke", "paralysis", "loss of vision sudden"],
        "emergency_level": "RED (CRITICAL)",
        "condition": "Suspected Acute Stroke (FAST Protocol)",
        "immediate_action": "🚨 STROKE ALERT: Time is brain! Note the EXACT time symptoms started. Call emergency ambulance immediately so the hospital stroke team is ready.",
        "do_not": "Do NOT give food, water, or aspirin until evaluated in ER."
    },
    {
        "trigger_keywords": ["unconscious", "passed out", "unresponsive", "fainted and not waking", "seizure continuous", "convulsion"],
        "emergency_level": "RED (CRITICAL)",
        "condition": "Loss of Consciousness / Status Epilepticus",
        "immediate_action": "🚨 CRITICAL: Check breathing. Place in Recovery Position (on side). Clear airway. Call Emergency Dispatch immediately.",
        "do_not": "Do NOT put anything in the person's mouth. Do NOT hold down a seizing person."
    },
    {
        "trigger_keywords": ["severe bleeding", "arterial spurting", "heavy blood loss", "stab wound", "deep cut bleeding heavily"],
        "emergency_level": "RED (CRITICAL)",
        "condition": "Severe Hemorrhage / Massive Bleeding",
        "immediate_action": "🚨 Apply firm, continuous direct pressure with clean cloth or gauze. Elevate the bleeding limb if possible. Dispatch emergency signal.",
        "do_not": "Do NOT remove soaked cloth; place more on top. Do NOT remove embedded objects."
    }
]

# First Aid Quick Protocols
FIRST_AID_PROTOCOLS = {
    "Heart Attack": {
        "icon": "❤️‍🩹",
        "steps": [
            "Call Emergency (108 / 911 / 112) or trigger MedPal SOS.",
            "Have the person sit down, rest, and keep calm (do NOT let them walk).",
            "Loosen tight clothing around neck and waist.",
            "If the person is conscious and not allergic to aspirin, have them chew one 300mg uncoated aspirin tablet.",
            "If the person becomes unconscious and stops normal breathing, begin CPR immediately (100-120 chest compressions per minute)."
        ],
        "warning": "Never ignore chest pressure lasting longer than 5 minutes."
    },
    "Stroke (FAST)": {
        "icon": "🧠",
        "steps": [
            "F - Face Drooping: Ask them to smile. Does one side droop?",
            "A - Arm Weakness: Ask them to raise both arms. Does one drift down?",
            "S - Speech Difficulty: Ask them to repeat a simple sentence. Is it slurred?",
            "T - Time to Call 108/911: Call emergency ambulance immediately if any sign is present!",
            "Note the exact time symptoms started for the hospital stroke team."
        ],
        "warning": "Do not give food, water, or aspirin."
    },
    "Choking": {
        "icon": "🫁",
        "steps": [
            "Ask: 'Are you choking? Can you speak or cough?'",
            "If they can cough forcefully, encourage coughing.",
            "If they cannot speak or breathe, perform Heimlich Maneuver (Abdominal Thrusts):",
            "Stand behind the person, wrap arms around waist.",
            "Make a fist just above their navel, grasp with other hand, and give quick upward thrusts.",
            "For unconscious victim: Lower to ground and begin CPR."
        ],
        "warning": "Do not perform blind finger sweeps in the mouth."
    },
    "Burns (Heat/Hot Liquid)": {
        "icon": "🔥",
        "steps": [
            "Immediately cool the burn under gentle running cool tap water for 15-20 minutes.",
            "Remove tight items (rings, watches, bracelets) before area swells.",
            "Cover loosely with a sterile non-stick bandage or clean plastic cling film.",
            "Take Paracetamol for pain relief if needed."
        ],
        "warning": "Do NOT apply ice, butter, oil, or toothpaste to burns. Do NOT pop blisters."
    },
    "Severe Bleeding": {
        "icon": "🩸",
        "steps": [
            "Wear gloves or clean plastic bags if available.",
            "Apply FIRM, DIRECT pressure over the wound with a clean cloth, towel, or gauze.",
            "Maintain pressure without lifting the cloth for at least 10 minutes.",
            "If blood soaks through, add another cloth on top; do not remove the first layer.",
            "Elevate the injured limb above heart level if no fracture is suspected."
        ],
        "warning": "If bleeding is spurting or won't stop, seek immediate emergency care."
    },
    "Low Blood Sugar (Hypoglycemia)": {
        "icon": "🍬",
        "steps": [
            "Signs: Trembling, sweating, extreme hunger, confusion, dizziness.",
            "Follow the 15-15 Rule: Give 15 grams of fast-acting sugar immediately (3 teaspoons sugar in water, half cup fruit juice, or 3 hard candies).",
            "Wait 15 minutes, check blood sugar or observe symptoms.",
            "If still low, repeat with another 15g of sugar.",
            "Once normal, eat a small carbohydrate snack (slice of bread or biscuit)."
        ],
        "warning": "If the person is drowsy or unconscious, do NOT force liquids into their mouth; call emergency."
    }
}

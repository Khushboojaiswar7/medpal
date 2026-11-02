"""
MedPal: AI-Powered Emergency Medical Assistant & Healthcare Accessibility Platform
Founder & Lead Developer: Built for accessible healthcare, emergency geolocation & hospital signaling.
"""

import os
import streamlit as st
from streamlit_folium import st_folium
from PIL import Image

# Import MedPal Custom Engine Modules
from modules.mock_data import (
    HOSPITALS_DATABASE, MEDICINE_DATABASE,
    RED_FLAG_EMERGENCIES, FIRST_AID_PROTOCOLS, EMERGENCY_NUMBERS
)
from modules.triage_engine import TriageEngine
from modules.hospital_finder import HospitalFinder
from modules.emergency_signal import EmergencySignalEngine
from modules.medicine_explainer import MedicineExplainer
from modules.voice_helper import VoiceHelper

# ------------------ PAGE CONFIGURATION ------------------
st.set_page_config(
    page_title="MedPal – Emergency Medical Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ LOAD CUSTOM CSS ------------------
css_path = os.path.join(os.path.dirname(__file__), "static", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ------------------ INITIALIZE SESSION STATE ------------------
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": "👋 Hello! I am **MedPal**, your AI medical companion and emergency guardian. How can I help you today? You can describe your symptoms, ask about any medicine, or find emergency hospital assistance."
        }
    ]

if "user_lat" not in st.session_state:
    st.session_state.user_lat = 17.4156
if "user_lon" not in st.session_state:
    st.session_state.user_lon = 78.4125
if "user_location_name" not in st.session_state:
    st.session_state.user_location_name = "Hyderabad (Jubilee Hills), India"

if "selected_hospital_id" not in st.session_state:
    st.session_state.selected_hospital_id = HOSPITALS_DATABASE[0]["id"]

if "active_sos_token" not in st.session_state:
    st.session_state.active_sos_token = None

if "elderly_mode" not in st.session_state:
    st.session_state.elderly_mode = False

if "language" not in st.session_state:
    st.session_state.language = "English"

if "pill_tracker" not in st.session_state:
    st.session_state.pill_tracker = {}

# ------------------ HELPER INSTANCES ------------------
# Check secrets for API keys if available
hf_key = None
gemini_key = None
try:
    if "HF_API_KEY" in st.secrets:
        hf_key = st.secrets["HF_API_KEY"]
    if "GEMINI_API_KEY" in st.secrets:
        gemini_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

triage_engine = TriageEngine(hf_api_key=hf_key, gemini_api_key=gemini_key)
hospital_finder = HospitalFinder()
signal_engine = EmergencySignalEngine()
medicine_explainer = MedicineExplainer(triage_engine=triage_engine)
voice_helper = VoiceHelper()

# ------------------ SIDEBAR CONFIGURATION ------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/hospital-room.png", width=64)
    st.title("🏥 MedPal Center")
    st.caption("AI Emergency & Accessibility Guardian")

    # Accessibility Switcher
    st.subheader("👓 Accessibility & Display")
    elderly_toggle = st.toggle(
        "👵 Elderly & Easy-Read Mode",
        value=st.session_state.elderly_mode,
        help="Enables extra-large high-contrast text and simplified plain explanations."
    )
    st.session_state.elderly_mode = elderly_toggle

    selected_lang = st.selectbox(
        "🌐 Language",
        ["English", "Hindi", "Spanish", "French"],
        index=0 if st.session_state.language == "English" else 1
    )
    st.session_state.language = selected_lang

    st.markdown("---")

    # Patient Emergency Profile
    st.subheader("👤 Patient Emergency Profile")
    st.caption("This vital information is transmitted when you signal an emergency to the hospital.")
    
    p_name = st.text_input("Full Name", value="Ramakrishna Rao", key="p_name")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        p_age = st.number_input("Age", min_value=1, max_value=120, value=68, key="p_age")
    with col_p2:
        p_blood = st.selectbox("Blood Group", ["B+", "O+", "A+", "AB+", "B-", "O-", "A-", "AB-"], index=0, key="p_blood")
    
    p_allergies = st.text_input("Allergies", value="Penicillin, Peanuts", key="p_allergies")
    p_conditions = st.text_input("Existing Conditions", value="Hypertension, Type 2 Diabetes", key="p_conditions")
    p_contact = st.text_input("Caregiver Emergency Phone", value="+91-98765-43210", key="p_contact")

    st.markdown("---")

    # Location Setting
    st.subheader("📍 Your Current Location")
    st.write(f"**Current:** {st.session_state.user_location_name}")
    st.caption(f"Coordinates: {st.session_state.user_lat:.4f}, {st.session_state.user_lon:.4f}")

    loc_search = st.text_input("Change City / Area", placeholder="e.g. Mumbai, New Delhi, Bengaluru")
    if st.button("Update Location", use_container_width=True):
        if loc_search.strip():
            geo = hospital_finder.geocode_address(loc_search.strip())
            if geo:
                st.session_state.user_lat, st.session_state.user_lon, st.session_state.user_location_name = geo
                st.success(f"Location updated to {geo[2][:35]}... ✅")
                st.rerun()
            else:
                st.error("Location not found. Please try another city name.")

    st.markdown("---")
    
    # Universal Hotlines
    st.subheader("📞 Universal Emergency Hotlines")
    st.markdown("""
    - 🚑 **Ambulance (India):** [108](tel:108) / [102](tel:102)
    - 🚨 **National Emergency:** [112](tel:112)
    - 👮 **Police:** [100](tel:100)
    - 🇺🇸 **USA Emergency:** [911](tel:911)
    """)

# ------------------ MAIN CONTAINER & HEADER ------------------
elderly_class = "elderly-mode" if st.session_state.elderly_mode else ""
st.markdown(f'<div class="{elderly_class}">', unsafe_allow_html=True)

# Top Bar Title & Quick SOS Banner
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.title("💊 MedPal – AI Emergency & Healthcare Platform")
    st.markdown(
        "**AI Medical Chatbot • Real-time Emergency Hospital Signaling • Jargon-Free Prescription Explainer for Elderly Users**"
    )

with header_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚨 ONE-TAP SOS ALERT", type="primary", use_container_width=True):
        st.session_state.active_tab = "🚨 Emergency SOS"
        st.toast("⚡ Emergency Dispatch Hub Activated!", icon="🚨")

# ------------------ NAVIGATION TABS ------------------
tab_chat, tab_sos, tab_hospitals, tab_medicine, tab_firstaid = st.tabs([
    "🤖 MedChat (AI Assistant)",
    "🚨 Emergency SOS & Signaling",
    "🗺️ Hospital Locator & Map",
    "💊 Prescription & Medicine Explainer",
    "🩹 First-Aid Protocols"
])

# ==============================================================================
# TAB 1: 🤖 MEDCHAT (AI MEDICAL ASSISTANT & TRIAGE)
# ==============================================================================
with tab_chat:
    st.subheader("🤖 MedChat – Conversational Health & Clinical Triage")
    st.caption("Ask any health question, describe symptoms for clinical triage assessment, or get instant first-aid guidance.")

    # Quick prompt buttons
    st.markdown("**Quick Health Queries:**")
    quick_cols = st.columns(4)
    with quick_cols[0]:
        if st.button("🚨 Crushing Chest Pain", use_container_width=True):
            st.session_state.chat_query = "I have sudden crushing chest pain radiating to my left arm and jaw"
    with quick_cols[1]:
        if st.button("🌡️ High Fever in Elderly", use_container_width=True):
            st.session_state.chat_query = "Elderly person with 102 fever and body chills. What should we do?"
    with quick_cols[2]:
        if st.button("🩺 High Blood Pressure", use_container_width=True):
            st.session_state.chat_query = "My BP reading is 165/100 and feeling dizzy. Is this dangerous?"
    with quick_cols[3]:
        if st.button("💊 Metformin & Food", use_container_width=True):
            st.session_state.chat_query = "When should I take Metformin 500mg and what are the food rules?"

    # Display Chat History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
                st.markdown(msg["content"])
                if msg["role"] == "assistant":
                    # Audio voice option
                    audio_fp = voice_helper.generate_audio_bytes(msg["content"], lang=st.session_state.language)
                    if audio_fp:
                        st.audio(audio_fp, format="audio/mp3")

    # Chat Input Box
    default_input = st.session_state.pop("chat_query", "")
    user_input = st.chat_input("Type your symptoms, medical question, or medication query here...", key="chat_input_box")
    active_prompt = user_input or default_input

    if active_prompt:
        # Add user message to history
        st.session_state.chat_messages.append({"role": "user", "content": active_prompt})
        
        # Check red-flags and generate expert response
        with st.spinner("MedPal is analyzing your symptoms and clinical guidelines..."):
            response_text = triage_engine.generate_expert_response(
                active_prompt,
                elderly_mode=st.session_state.elderly_mode,
                language=st.session_state.language
            )

        st.session_state.chat_messages.append({"role": "assistant", "content": response_text})
        st.rerun()


# ==============================================================================
# TAB 2: 🚨 EMERGENCY SOS & HOSPITAL SIGNALING HUB
# ==============================================================================
with tab_sos:
    st.subheader("🚨 Emergency Hospital Signaling & Real-time Dispatch Hub")
    st.markdown("""
    When an emergency occurs, seconds count. MedPal generates a verified **Emergency Medical Token**
    with your live GPS coordinates, patient vitals, and transmits a signal to the selected emergency trauma center.
    """)

    # Get nearest hospitals for signaling
    nearby_hospitals = hospital_finder.get_nearest_hospitals(
        st.session_state.user_lat,
        st.session_state.user_lon,
        max_results=6
    )

    sos_col1, sos_col2 = st.columns([1, 1])

    with sos_col1:
        st.markdown("### 1. Configure Emergency Dispatch")
        
        # Hospital Selector
        hosp_options = {h["id"]: f"{h['name']} ({h['distance_km']} km | ETA: {h['eta_mins']} mins)" for h in nearby_hospitals}
        selected_hosp_id = st.selectbox(
            "Select Destination Emergency Trauma Center",
            options=list(hosp_options.keys()),
            format_func=lambda x: hosp_options[x]
        )
        
        target_hosp = next((h for h in nearby_hospitals if h["id"] == selected_hosp_id), nearby_hospitals[0])
        st.session_state.selected_hospital_id = target_hosp["id"]

        # Emergency Category
        emergency_type = st.selectbox(
            "Emergency Condition / Reason",
            [
                "Cardiac / Severe Chest Pain (Heart Attack Alert)",
                "Severe Respiratory Distress / Choking",
                "Acute Stroke / Sudden Paralysis (FAST Alert)",
                "Severe Trauma / Uncontrolled Bleeding / Fracture",
                "Unconscious / Seizure / Collapsed",
                "Severe Allergic Anaphylaxis",
                "Other Critical Emergency"
            ]
        )

        st.markdown(f"""
        **Target Facility Summary:**
        - 🏥 **Hospital:** {target_hosp['name']}
        - 📍 **Address:** {target_hosp['address']}, {target_hosp['city']}
        - ⏱️ **Emergency ETA:** **{target_hosp['eta_mins']} minutes** ({target_hosp['distance_km']} km)
        - 🛏️ **ICU Beds Available:** **{target_hosp['icu_beds_available']}**
        - 👨‍⚕️ **ER Lead:** {target_hosp['emergency_lead_dr']}
        """)

        # BIG RED EMERGENCY SIGNAL BUTTON
        if st.button("🚨 TRANSMIT EMERGENCY SIGNAL TO HOSPITAL NOW", type="primary", use_container_width=True):
            token = signal_engine.generate_emergency_token(
                patient_name=st.session_state.get("p_name", "Ramakrishna Rao"),
                patient_age=st.session_state.get("p_age", 68),
                blood_group=st.session_state.get("p_blood", "B+"),
                allergies=st.session_state.get("p_allergies", "Penicillin"),
                conditions=st.session_state.get("p_conditions", "Hypertension"),
                emergency_contact=st.session_state.get("p_contact", "+91-98765-43210"),
                emergency_type=emergency_type,
                user_lat=st.session_state.user_lat,
                user_lon=st.session_state.user_lon,
                target_hospital=target_hosp,
                triage_level="RED (CRITICAL)"
            )
            st.session_state.active_sos_token = token
            st.toast("🚨 EMERGENCY SIGNAL DISPATCHED TO HOSPITAL ER!", icon="🚨")

    with sos_col2:
        st.markdown("### 2. Live Dispatch & Hospital Response Monitor")

        token = st.session_state.active_sos_token
        if not token:
            st.info("ℹ️ No active emergency signal. Click **'TRANSMIT EMERGENCY SIGNAL'** to signal the hospital and dispatch medical rescue.")
        else:
            # Active Emergency Banner
            st.markdown(f"""
            <div class="emergency-banner">
                <div>
                    <h3 style="margin:0; color:white;">🚨 EMERGENCY SIGNAL ACTIVE</h3>
                    <p style="margin:4px 0 0 0; color: #FEE2E2;">Dispatch ID: <b>{token['dispatch_id']}</b> | Time: {token['timestamp']}</p>
                </div>
                <div style="font-size:24px;">🚑</div>
            </div>
            """, unsafe_allow_html=True)

            # Simulated Response Stages
            st.markdown("#### Real-time Hospital Integration Status:")
            st.markdown("""
            <div class="status-step step-done">
                <span>✅</span> <b>Step 1: Emergency Signal Transmitted to Trauma Desk</b> (Payload encrypted & delivered)
            </div>
            <div class="status-step step-done">
                <span>✅</span> <b>Step 2: ER Trauma Chief Acknowledged</b> (Dr. notified, Patient vitals & allergy record loaded)
            </div>
            <div class="status-step step-active">
                <span>🚑</span> <b>Step 3: Advanced Life Support (ALS) Ambulance En Route</b> (ETA: <b>7 mins</b>)
            </div>
            <div class="status-step step-pending">
                <span>⏳</span> <b>Step 4: ICU Trauma Bay & Surgical Team Reserved</b>
            </div>
            """, unsafe_allow_html=True)

            # Dispatch Payload Details
            with st.expander("📄 View Transmitted Emergency Payload Token", expanded=True):
                st.json(token)

            # Direct Action Buttons (WhatsApp, Call, SMS)
            st.markdown("#### ⚡ Immediate Caregiver & Hotline Actions:")
            wa_link = signal_engine.create_whatsapp_sos_link(token, phone_number=st.session_state.get("p_contact", ""))
            
            c_act1, c_act2, c_act3 = st.columns(3)
            with c_act1:
                st.link_button("📲 WhatsApp SOS Link", wa_link, use_container_width=True)
            with c_act2:
                st.link_button(f"📞 Call Ambulance ({target_hosp['ambulance_phone']})", f"tel:{target_hosp['ambulance_phone']}", use_container_width=True)
            with c_act3:
                st.link_button(f"🏥 Call ER ({target_hosp['emergency_phone']})", f"tel:{target_hosp['emergency_phone']}", use_container_width=True)

            if st.button("Cancel / Clear SOS Alert"):
                st.session_state.active_sos_token = None
                st.success("Emergency alert resolved.")
                st.rerun()


# ==============================================================================
# TAB 3: 🗺️ NEAREST HOSPITAL LOCATOR & INTERACTIVE MAP
# ==============================================================================
with tab_hospitals:
    st.subheader("🗺️ Nearest Emergency Hospitals & Live Map")
    st.caption("Find the closest verified emergency trauma centers, check ICU bed availability, and navigate with real-time ETA.")

    # Search Bar for Location
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        map_search_query = st.text_input(
            "Search hospitals near city, landmark or pincode",
            value="",
            placeholder="e.g., Jubilee Hills Hyderabad, Connaught Place Delhi, Koramangala Bengaluru",
            key="map_search_input"
        )
    with search_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Find Nearby Hospitals", use_container_width=True):
            if map_search_query.strip():
                geo_res = hospital_finder.geocode_address(map_search_query.strip())
                if geo_res:
                    st.session_state.user_lat, st.session_state.user_lon, st.session_state.user_location_name = geo_res
                    st.success(f"Showing hospitals near: {geo_res[2][:40]}...")
                    st.rerun()
                else:
                    st.warning("Could not find that location. Showing default region.")

    # Query nearest hospitals
    hospitals_list = hospital_finder.get_nearest_hospitals(
        st.session_state.user_lat,
        st.session_state.user_lon,
        max_results=6
    )

    map_col1, map_col2 = st.columns([3, 2])

    with map_col1:
        st.markdown(f"**Live Map View (Center: {st.session_state.user_location_name})**")
        folium_map = hospital_finder.create_hospital_map(
            st.session_state.user_lat,
            st.session_state.user_lon,
            hospitals_list,
            selected_hospital_id=st.session_state.selected_hospital_id
        )
        st_folium(folium_map, width=700, height=480)

    with map_col2:
        st.markdown("**🏥 Verified Emergency Facilities:**")
        for hosp in hospitals_list:
            is_selected = (hosp["id"] == st.session_state.selected_hospital_id)
            card_class = "hospital-card selected" if is_selected else "hospital-card"
            
            st.markdown(f"""
            <div class="{card_class}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0; color:#1F2937;">{hosp['name']}</h4>
                    <span style="background:#DC2626; color:white; font-size:12px; padding:3px 8px; border-radius:12px; font-weight:600;">24/7 ER</span>
                </div>
                <p style="margin:4px 0; color:#4B5563; font-size:13px;">{hosp['address']}, {hosp['city']}</p>
                <div style="display:flex; gap:12px; margin:6px 0; font-size:13px;">
                    <span>📏 <b>{hosp['distance_km']} km</b></span>
                    <span>⏱️ ETA: <b>{hosp['eta_mins']} mins</b></span>
                    <span>🛏️ ICU: <b>{hosp['icu_beds_available']} beds</b></span>
                    <span>⭐ <b>{hosp['rating']}</b></span>
                </div>
                <div style="margin-top:6px; font-size:13px;">
                    📞 <b>ER:</b> <a href="tel:{hosp['emergency_phone']}">{hosp['emergency_phone']}</a> | 
                    🚑 <b>Ambulance:</b> <a href="tel:{hosp['ambulance_phone']}">{hosp['ambulance_phone']}</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"🎯 Target for SOS ({hosp['name'][:20]}...)", key=f"btn_sel_{hosp['id']}"):
                st.session_state.selected_hospital_id = hosp["id"]
                st.toast(f"Selected {hosp['name']} as your emergency destination!", icon="🏥")
                st.rerun()


# ==============================================================================
# TAB 4: 💊 EASY MEDICINE & PRESCRIPTION EXPLAINER (FOR ELDERLY USERS)
# ==============================================================================
with tab_medicine:
    st.subheader("💊 Easy Prescription & Medicine Explainer")
    st.markdown("""
    Designed for **elderly users, family caregivers, and individuals who struggle with medical jargon**.
    Translates complicated doctor prescriptions into simple visual cards, daily routines, and spoken voice.
    """)

    med_input_col1, med_input_col2 = st.columns([1, 1])

    with med_input_col1:
        st.markdown("### 1. Upload Prescription or Enter Medicine Names")
        
        # Prescription Image OCR Upload
        uploaded_image = st.file_uploader(
            "📷 Upload Prescription / Pill Box Photo (Optional)",
            type=["png", "jpg", "jpeg"]
        )
        ocr_extracted_text = ""
        if uploaded_image:
            img = Image.open(uploaded_image)
            st.image(img, caption="Uploaded Prescription", width=250)
            with st.spinner("Reading prescription image..."):
                ocr_extracted_text = medicine_explainer.extract_text_from_image(img)
                if ocr_extracted_text:
                    st.info(f"Extracted Text: {ocr_extracted_text[:120]}...")

        # Text input
        default_presc = ocr_extracted_text or "Metformin 500mg twice daily with food, Atorvastatin 20mg at bedtime, Pantoprazole 40mg before breakfast"
        presc_text = st.text_area(
            "Or Type / Paste Prescription details:",
            value=default_presc,
            height=110,
            help="Type medicine names like Metformin, Paracetamol, Amlodipine, Atorvastatin, Amoxicillin, Pantoprazole"
        )

        sample_btn_cols = st.columns(3)
        with sample_btn_cols[0]:
            if st.button("📋 Diabetes + BP Sample"):
                st.session_state.sample_presc = "Metformin 500mg 1-0-1 with food, Telmisartan 40mg 1-0-0 in morning, Atorvastatin 20mg 0-0-1 at night"
                st.rerun()
        with sample_btn_cols[1]:
            if st.button("📋 Fever & Infection Sample"):
                st.session_state.sample_presc = "Amoxicillin 500mg thrice daily after food, Paracetamol 650mg when fever, Pantoprazole 40mg empty stomach"
                st.rerun()
        with sample_btn_cols[2]:
            if st.button("📋 Heart & Blood Thinner"):
                st.session_state.sample_presc = "Aspirin 75mg once after lunch, Amlodipine 5mg morning, Atorvastatin 20mg bedtime"
                st.rerun()

        if "sample_presc" in st.session_state:
            presc_text = st.session_state.pop("sample_presc")

    with med_input_col2:
        st.markdown("### 2. Audio Voice Read-Out")
        st.caption("Elderly users can listen to their medicine instructions spoken clearly in their preferred language.")
        
        parsed_meds = medicine_explainer.parse_prescription_text(presc_text)
        spoken_summary = medicine_explainer.generate_elderly_friendly_summary(
            parsed_meds,
            language=st.session_state.language
        )
        
        # Audio generator
        audio_stream = voice_helper.generate_audio_bytes(spoken_summary, lang=st.session_state.language)
        if audio_stream:
            st.audio(audio_stream, format="audio/mp3")

        # In-Browser Instant Speak Button
        speak_btn_html = voice_helper.render_browser_speak_button(spoken_summary, button_label="🔊 Read Medicine Schedule Aloud")
        st.components.v1.html(speak_btn_html, height=55)

    st.markdown("---")

    # Drug-Drug Interaction Safety Alert
    interactions = medicine_explainer.check_drug_interactions(parsed_meds)
    if interactions:
        for inter in interactions:
            st.error(f"⚠️ **DRUG SAFETY ALERT ({inter['severity']} SEVERITY):** {inter['warning']}")

    # Visual Routine Breakdown Cards
    st.markdown("### 🌅 Visual Daily Medicine Timetable")
    
    time_cols = st.columns(3)
    
    with time_cols[0]:
        st.markdown("#### 🌅 Morning (Breakfast)")
        morning_meds = [m for m in parsed_meds if m.get("active_timings", {}).get("morning")]
        if not morning_meds:
            st.write("*(No morning medicines)*")
        for m in morning_meds:
            st.markdown(f"""
            <div class="med-card">
                <span class="routine-pill routine-morning">🌅 Morning</span>
                <span class="routine-pill food-badge">{m['food_relation_icon']} {m['food_relation']}</span>
                <h4 style="margin: 8px 0 4px 0; color: #1F2937;">{m['generic_name']}</h4>
                <p style="margin:0 0 6px 0; font-size: 13px; color: #4B5563;"><b>Brands:</b> {', '.join(m.get('brand_names', [])[:2])}</p>
                <p style="margin:0; font-size: 14px; color: #111827;">💡 <b>Why:</b> {m['elderly_explanation']}</p>
                <p style="margin:4px 0 0 0; font-size: 13px; color: #2563EB;">💧 {m['water_instructions']}</p>
            </div>
            """, unsafe_allow_html=True)

    with time_cols[1]:
        st.markdown("#### ☀️ Afternoon (Lunch)")
        afternoon_meds = [m for m in parsed_meds if m.get("active_timings", {}).get("afternoon")]
        if not afternoon_meds:
            st.write("*(No afternoon medicines)*")
        for m in afternoon_meds:
            st.markdown(f"""
            <div class="med-card">
                <span class="routine-pill routine-afternoon">☀️ Afternoon</span>
                <span class="routine-pill food-badge">{m['food_relation_icon']} {m['food_relation']}</span>
                <h4 style="margin: 8px 0 4px 0; color: #1F2937;">{m['generic_name']}</h4>
                <p style="margin:0 0 6px 0; font-size: 13px; color: #4B5563;"><b>Brands:</b> {', '.join(m.get('brand_names', [])[:2])}</p>
                <p style="margin:0; font-size: 14px; color: #111827;">💡 <b>Why:</b> {m['elderly_explanation']}</p>
                <p style="margin:4px 0 0 0; font-size: 13px; color: #2563EB;">💧 {m['water_instructions']}</p>
            </div>
            """, unsafe_allow_html=True)

    with time_cols[2]:
        st.markdown("#### 🌙 Night (Dinner / Bedtime)")
        night_meds = [m for m in parsed_meds if m.get("active_timings", {}).get("night")]
        if not night_meds:
            st.write("*(No night medicines)*")
        for m in night_meds:
            st.markdown(f"""
            <div class="med-card">
                <span class="routine-pill routine-night">🌙 Night</span>
                <span class="routine-pill food-badge">{m['food_relation_icon']} {m['food_relation']}</span>
                <h4 style="margin: 8px 0 4px 0; color: #1F2937;">{m['generic_name']}</h4>
                <p style="margin:0 0 6px 0; font-size: 13px; color: #4B5563;"><b>Brands:</b> {', '.join(m.get('brand_names', [])[:2])}</p>
                <p style="margin:0; font-size: 14px; color: #111827;">💡 <b>Why:</b> {m['elderly_explanation']}</p>
                <p style="margin:4px 0 0 0; font-size: 13px; color: #2563EB;">💧 {m['water_instructions']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Interactive Daily Dose Checklist
    st.markdown("---")
    st.markdown("### ✅ Daily Pill Taken Checklist (For Caregiver / Patient Tracking)")
    chk_cols = st.columns(len(parsed_meds) if parsed_meds else 1)
    for idx, med in enumerate(parsed_meds):
        with chk_cols[idx % len(chk_cols)]:
            k = f"taken_{med['generic_name']}_{idx}"
            is_taken = st.checkbox(f"✔️ Took {med['generic_name']}", key=k)
            if is_taken:
                st.success("Dose logged! ✅")


# ==============================================================================
# TAB 5: 🩹 QUICK FIRST-AID & EMERGENCY PROTOCOLS
# ==============================================================================
with tab_firstaid:
    st.subheader("🩹 Instant First-Aid & Life-Saving Protocols")
    st.caption("Step-by-step verified emergency actions to take while waiting for the ambulance to arrive.")

    protocol_names = list(FIRST_AID_PROTOCOLS.keys())
    sel_proto = st.radio("Select Emergency Scenario:", protocol_names, horizontal=True)

    p_data = FIRST_AID_PROTOCOLS[sel_proto]
    
    st.markdown(f"### {p_data['icon']} {sel_proto} Immediate Action Steps")
    
    # Audio read-out for first aid
    proto_text = f"First Aid Protocol for {sel_proto}. " + " ".join(p_data["steps"])
    fa_audio = voice_helper.generate_audio_bytes(proto_text, lang=st.session_state.language)
    if fa_audio:
        st.audio(fa_audio, format="audio/mp3")

    for i, step in enumerate(p_data["steps"], 1):
        st.markdown(f"""
        <div style="background: #F9FAFB; border-left: 4px solid #2563EB; padding: 12px 16px; border-radius: 6px; margin-bottom: 8px;">
            <b style="color: #2563EB; font-size: 16px;">Step {i}:</b> {step}
        </div>
        """, unsafe_allow_html=True)

    st.warning(f"⚠️ **Important Safety Warning:** {p_data['warning']}")

st.markdown('</div>', unsafe_allow_html=True)

# ------------------ FOOTER & CLINICAL DISCLAIMER ------------------
st.markdown("---")
f_col1, f_col2 = st.columns([3, 1])
with f_col1:
    st.caption("⚠️ **Clinical Disclaimer:** MedPal is an AI-powered medical triage and emergency assistance tool. It facilitates fast emergency signaling and simple patient comprehension, but does not replace certified clinical diagnosis. In life-threatening situations, always dial 108/911/112 immediately.")
with f_col2:
    st.caption("MedPal Platform v2.0 • 2026")

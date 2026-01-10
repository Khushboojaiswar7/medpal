import streamlit as st
import requests
from datetime import datetime

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="MedPal",
    page_icon="💊",
    layout="centered"
)

st.title("💊 MedPal – AI Health Companion")

# ------------------ LOAD API KEY ------------------
try:
    HF_API_KEY = st.secrets[""]
except Exception:
    st.error("❌ Hugging Face API key not found. Check secrets.toml")
    st.stop()

# ------------------ HUGGING FACE MODEL ------------------
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HEADERS = {
    "Authorization": f"Bearer {}"
}

def query_hf(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200}
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return "⚠️ AI service is temporarily unavailable."

# ------------------ SESSION STATE ------------------
if "med_logs" not in st.session_state:
    st.session_state.med_logs = []

if "symptom_logs" not in st.session_state:
    st.session_state.symptom_logs = []

# ------------------ MEDICATION LOG ------------------
st.subheader("📌 Log Medication")

med_name = st.text_input("Medication name")
dose = st.text_input("Dose (e.g. 500mg, 1 tablet)")

if st.button("Save Medication"):
    if med_name and dose:
        time = datetime.now().strftime("%d %b %Y • %H:%M")
        st.session_state.med_logs.append(f"{med_name} ({dose}) – {time}")
        st.success("Medication saved ✅")
    else:
        st.warning("Please enter both fields")

if st.session_state.med_logs:
    st.markdown("**Medication History:**")
    for log in st.session_state.med_logs:
        st.write("•", log)

# ------------------ SYMPTOM LOG ------------------
st.subheader("🩺 Log Symptoms / Vitals")

symptom = st.text_input("Symptom or vital (e.g. headache, BP 120/80)")

if st.button("Log Symptom"):
    if symptom:
        time = datetime.now().strftime("%d %b %Y • %H:%M")
        st.session_state.symptom_logs.append(f"{symptom} – {time}")
        st.success("Symptom logged ✅")
    else:
        st.warning("Please enter a symptom")

if st.session_state.symptom_logs:
    st.markdown("**Symptoms History:**")
    for log in st.session_state.symptom_logs:
        st.write("•", log)

# ------------------ AI CHAT ------------------
st.subheader("🤖 Ask MedPal")

question = st.text_input("Ask a general health question")

if st.button("Ask MedPal"):
    if question.strip() == "":
        st.warning("Please type a question")
    else:
        with st.spinner("MedPal is thinking..."):
            response = query_hf(question)
            st.info(response)

# ------------------ DISCLAIMER ------------------
st.markdown("---")
st.caption("⚠️ MedPal is an AI assistant and does not replace professional medical advice.")

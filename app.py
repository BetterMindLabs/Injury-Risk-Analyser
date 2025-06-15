import streamlit as st
import google.generativeai as genai

# Configure Gemini
api_key = st.secrets["api_keys"]["google_api_key"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# UI Setup
st.set_page_config(page_title="Injury-Risk Analyzer")
st.title("Injury-Risk Analyzer")
st.write("Estimate injury risk based on athlete workload and recovery metrics.")

# Input fields
training_load = st.slider("Weekly Training Load (hours)", 0, 30, 10)
session_rpe = st.slider("Session RPE (1 = very light, 10 = max effort)", 1, 10, 5)
recovery_time = st.slider("Daily Recovery Time (hours)", 0, 24, 8)
sleep_hours = st.slider("Average Sleep Per Day (hours)", 0, 12, 7)
injury_history = st.slider("Injury History Score (0 = none, 10 = frequent)", 0, 10, 3)

if st.button("Analyze Risk"):
    with st.spinner("Evaluating metrics..."):
        prompt = f"""
You are a risk classification engine trained on athletic workload datasets. Using these parameters, classify injury risk as Low, Moderate, or High. Also return a short explanation.

Input Metrics:
- Weekly Training Load: {training_load} hours
- Session RPE: {session_rpe}
- Recovery Time: {recovery_time} hrs/day
- Sleep: {sleep_hours} hrs/day
- Injury History Score: {injury_history} / 10

Format:
Risk Level: <Low | Moderate | High>  
Reason: <Short technical reasoning based on workload-recovery balance>
"""

        response = model.generate_content(prompt)
        result = response.text.strip()

        st.subheader("Risk Evaluation")
        st.text(result)

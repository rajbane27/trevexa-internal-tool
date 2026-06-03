import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime, timedelta

st.title("📅 Target Planner & Delay Forecaster")
st.caption("Generate institutional schedules and dynamically track execution slippage against deadlines.")

# Initialize Gemini
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ Gemini API Key not configured in Streamlit Secrets!")
    st.stop()

# Project Identification
project_name = st.text_input("Project Name/ID", placeholder="e.g., Sector 62 Commercial Complex")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Projected Start Date", datetime.today())
with col2:
    target_days = st.number_input("Target Duration (Days)", min_value=1, value=90)

raw_scope = st.text_area("Brief Project Scope / Executing Framework:", placeholder="e.g., 50 bored cast-in-situ piles, 1200mm diameter, depth 25m...")

if st.button("Generate Master Work Plan"):
    if not project_name or not raw_scope:
        st.warning("Please fill in the project name and execution framework details.")
    else:
        with st.spinner("Calculating sequencing, task dependencies, and targets..."):
            prompt = f"""
            You are a Senior Project Management Consultant (Primavera/MSP expert) for Trevexa Infratech Pvt Ltd.
            Generate an air-tight, rigorous project execution schedule for "{project_name}" starting on {start_date} with a strict deadline of {target_days} days.
            
            Based on this scope: {raw_scope}
            
            Provide a strictly detailed blueprint formatted with these exact markdown headers:
            1. **Master Execution Methodology**: Clear step-by-step description of how this specific construction work is executed technically.
            2. **Milestone Targets Breakdowns**: 
               - Daily expected baseline output target.
               - Weekly milestone achievements.
               - Monthly and Quarterly target parameters (if applicable within the {target_days}-day limit).
            3. **Quality Control & Sign-off Gateways**: What parameters must be checked daily before clearing work for payment.
            
            Keep the tone ultra-sharp, authoritative, and data-backed.
            """
            
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                st.success("✅ Work Plan Generated Successfully!")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error communicating with AI Engine: {e}")

st.markdown("---")
st.subheader("⏱️ Live Execution & Delay Tracker")
st.markdown("Input daily progress here to calculate timeline compounding delays or production surpluses.")

# Simulation Tracker Form
with st.form("tracking_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        date_tracked = st.date_input("Tracking Date", datetime.today())
    with c2:
        expected_qty = st.number_input("Expected Quantity Today (e.g., meters, cu.m, units)", min_value=0.1, value=10.0)
    with c3:
        actual_qty = st.number_input("Actual Quantity Achieved Today", min_value=0.0, value=8.5)
        
    submit_tracking = st.form_submit_button("Log Progress & Calculate Variance")

if submit_tracking:
    variance = actual_qty - expected_qty
    st.markdown("### 📊 Variance Analysis")
    
    if variance < 0:
        loss_pct = abs(variance) / expected_qty * 100
        st.error(f"🔴 **Slippage Detected:** You missed today's target by **{abs(variance):.2f} units** ({loss_pct:.1f}% deficit).")
        st.warning(f"💡 **Strategic Forecast:** If this daily production rate continues, your overall timeline will expand by approximately **{abs(variance)/expected_qty * 1.5:.1f} additional recovery days** per week of execution.")
    elif variance == 0:
        st.success("🟢 **On Schedule:** Exactly achieved 100% of the baseline target today.")
    else:
        gain_pct = variance / expected_qty * 100
        st.balloons()
        st.success(f"🔵 **Production Surplus:** Outperformed baseline by **{variance:.2f} units** (+{gain_pct:.1f}% efficiency). Timeline buffers are improving.")

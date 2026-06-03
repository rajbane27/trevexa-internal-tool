import streamlit as st
import google.generativeai as genai
import pandas as pd

st.title("💰 Financial Estimator & Margin Builder")
st.caption("Build industrial-grade cost estimates, calculate structural reserves, and prevent margin erosion.")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ Gemini API Key not configured in Streamlit Secrets!")
    st.stop()

project_name = st.text_input("Project Name for Financial Sheet", placeholder="e.g., Sector 62 Piling Project")

col1, col2, col3 = st.columns(3)
with col1:
    raw_material_budget = st.number_input("Estimated Material Cost (₹)", min_value=0, value=500000)
with col2:
    raw_labor_budget = st.number_input("Estimated Labor Base Cost (₹)", min_value=0, value=250000)
with col3:
    target_margin_pct = st.slider("Target Profit Margin %", min_value=5, max_value=50, value=20)

additional_details = st.text_area("Specify Machinery / Site Admin Overheads or Risk Variables:", placeholder="e.g., Requires hiring a 50-ton crane for 10 days, site power access unknown...")

if st.button("Generate Complete Financial Report"):
    if not project_name:
        st.warning("Please provide a Project Name.")
    else:
        with st.spinner("Structuring corporate P&L projections..."):
            prompt = f"""
            You are the Chief Financial Officer (CFO) of Trevexa Infratech Pvt Ltd.
            Compile a highly rigorous, itemized financial report and commercial quotation baseline for "{project_name}".
            
            Financial Baseline Metrics Inputted:
            - Base Material Costs: ₹{raw_material_budget:,}
            - Base Labor Cost Allocation: ₹{raw_labor_budget:,}
            - Desired Corporate Profit Margin: {target_margin_pct}%
            - Overhead context: {additional_details}

            Please output a comprehensive commercial analysis structured with these exact sections:
            1. **Itemized Expenditure Classification**: Group into explicit corporate buckets: CapEx (Machinery/Assets), OpEx (Fuel, Utilities, Site Admin), Direct Material Cost, and Direct Labor/Wages.
            2. **Unplanned Contingency & Safety Reserves**: Calculate and suggest an explicit risk reserve allocation (e.g., 7-12% based on the overhead risks outlined).
            3. **Final Commercial Pricing Model Summary**: Show a clearly formatted table displaying the calculated Total Cost Price, Profit Margin Amount, Risk Cushion Amount, and Final Quotation Figure to be submitted to clients.
            
            Ensure your output builds structural financial confidence and leaves no room for client negotiations to erode basic profitability thresholds.
            """
            
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                st.success("✅ Commercial Report Built!")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error calculating financials: {e}")

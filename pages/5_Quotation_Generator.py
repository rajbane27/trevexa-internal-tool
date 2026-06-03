import streamlit as st
import google.generativeai as genai

st.title("📄 Institutional Quotation & BOQ Generator")
st.caption("Convert raw parameters, structural drawings data, or quantity notes into legally defensive commercial offers.")

# Initialize Gemini API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ Gemini API Key not configured in Streamlit Secrets!")
    st.stop()

# Project Info
col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("Client Organization / Authority Name", placeholder="e.g., State Highway Authority / Reliance Infra")
with col2:
    project_ref = st.text_input("Project Reference / Tender ID", placeholder="e.g., TX-INFRA/2026/B-402")

# Input Handling Section
st.subheader("📥 Input Project Requirements & Quantities")
st.markdown("Paste raw specifications, text summaries, or copied cells from your Excel/PDF files below:")

raw_specs = st.text_area(
    "Raw Technical Specifications & Quantity Data Block", 
    height=250,
    placeholder="Example:\n- Excavation in soil up to 3m depth: Approx 1500 Cu.M\n- PCC 1:4:8 placement - 120 Cu.M\n- Structural steel fabrication for pillars - 45 Metric Tons\n- Logistics timeline: Must finish within 45 days before monsoon starts."
)

# Custom T&C Additions
with st.expander("🛡️ Advanced Contractual Guardrails (Optional)"):
    payment_terms = st.text_input("Mobilization Advance / Payment Milestone Terms", value="10% Mobilization Advance, 80% running account bills within 15 days of billing, 10% retention money released after defect liability period.")
    price_escalation = st.checkbox("Include Steel/Cement Price Escalation Clause", value=True)
    force_majeure = st.checkbox("Include Standard Force Majeure & Extension of Time (EOT) protections", value=True)

if st.button("Generate Air-Tight Commercial Proposal"):
    if not client_name or not raw_specs:
        st.warning("Please specify at least the Client Name and provide technical scope/quantity data.")
    else:
        with st.spinner("Compiling institutional BOQ and legal terms..."):
            
            escalation_text = "If prices of steel, cement, or fuel escalate by more than 5% during execution, rates shall be adjusted based on the Wholesale Price Index (WPI)." if price_escalation else ""
            
            prompt = f"""
            You are the Principal Legal Counsel and Chief Commercial Officer for Trevexa Infratech Pvt Ltd.
            Draft a completely professional, legally sound, and air-tight commercial quotation and Bill of Quantities (BOQ) for "{client_name}" under Reference ID "{project_ref}".
            
            Raw Scope and Quantity Inputs:
            {raw_specs}
            
            Configured Commercial Safeguards:
            - Payment Terms: {payment_terms}
            - Price Escalation: {escalation_text}
            - Include standard high-level construction Force Majeure, Extension of Time (EOT) rules, and structural site readiness requirements.
            
            Format your entire response using clear Markdown with these specific sections:
            1. **EXECUTIVE COVER LETTER**: A formal, corporate-grade introductory letter addressed to the client, outlining Trevexa's operational commitment.
            2. **STRUCTURED BILL OF QUANTITIES (BOQ)**: Transform the raw data into a clean, markdown-formatted table with columns: [S.No, Item Description, Unit, Quantity, Estimated Rate (Base), Total Amount]. (Estimate reasonable, market-competitive civil engineering rates if exact values are omitted in the text block).
            3. **STRATEGIC TERMS & CONDITIONS (T&C)**: Explicitly map out the payment milestones, required site infrastructure to be provided by the client (e.g., unhindered site access, water/power sources), work completion deadlines, and penalty caps for client-driven delays.
            4. **DEFENSIVE CLAUSES**: Write out detailed legal clauses for Price Escalation and Force Majeure to ensure Trevexa is protected from financial losses due to inflation or unexpected external events.
            
            The tone must be authoritative, highly polished, and leave absolutely no room for ambiguity or exploitation by the client's procurement department.
            """
            
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                
                st.success("✅ Commercial Proposal & BOQ Compiled Successfully!")
                st.markdown("---")
                st.markdown(response.text)
                
                # Downloadable Artifact
                st.download_button(
                    label="📥 Download Quotation Document",
                    data=response.text,
                    file_name=f"Trevexa_Quotation_{project_ref if project_ref else 'Draft'}.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error generating contract framework: {e}")

import streamlit as st
import google.generativeai as genai

st.title("🔍 AI Scope & Missing Detail Audit")
st.caption("Establish absolute technical authority. Upload raw discussions to discover hidden technical gaps.")

# 1. Fetch API Key securely from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ Gemini API Key not configured in Streamlit Secrets! Check your Advanced Settings.")
    st.stop()

# 2. Project Raw Input
project_name = st.text_input("Project Name/Location ID", placeholder="e.g., Sector 62 Commercial Complex Piling Work")
raw_notes = st.text_area(
    "Paste Raw Discussion Notes / Client Initial Requirements:", 
    height=250,
    placeholder="Type or paste everything you know about the project here (even if unorganized)..."
)

if st.button("Generate Technical Audit"):
    if not project_name or not raw_notes:
        st.warning("Please provide both a project name and some discussion details.")
    else:
        with st.spinner("Analyzing like a veteran strategist... Please wait."):
            
            # Construct a highly targeted system prompt to make you sound ultra-expert
            prompt = f"""
            You are the Chief Civil Engineer and Strategic Risk Officer for Trevexa Infratech Pvt Ltd. 
            The user is a brilliant young executive who needs to present absolute technical dominance to a client or contractor. 
            Analyze the following raw project notes for "{project_name}" and produce a highly sharp, professional evaluation.

            Format your response exactly with these sections:
            1. **Executive Summary of Scope**: Summarize the work concisely but professionally.
            2. **The "Expert-Level" Missing Details List**: Identify at least 5-8 highly technical parameters missing from the notes that an expert must know before executing (e.g., soil load-bearing capacity, water table level, local municipal permissions, right-of-way issues, electricity/water source coordinates, local labor unions/wage dynamics, material storage space availability). Formulate these as precise, sharp questions the user can copy-paste to ask the other party.
            3. **Hidden Project Risks**: Identify potential execution bottlenecks or legal pitfalls based on the inputs.
            4. **Visionary Strategy Pitch**: Provide a paragraph of professional, high-level vocabulary that the user can say to the client to make them sound incredibly competent and forward-thinking.

            Raw Notes:
            {raw_notes}
            """
            
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                
                st.success("✅ Audit Complete!")
                st.markdown("---")
                st.markdown(response.text)
                
                # Allow download of the report
                st.download_button(
                    label="📥 Download Audit Report as Text",
                    data=response.text,
                    file_name=f"{project_name.replace(' ', '_')}_Scope_Audit.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error generating content from Gemini API: {e}")

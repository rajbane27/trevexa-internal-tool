import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Project Tracking Dashboard")
st.caption("Real-time visual command console for Trevexa's concurrent projects, workforce deployment, and liquid capital metrics.")

# Mock Datasets representing underlying operational records
@st.cache_data
def load_project_financials():
    data = {
        "Project Name": ["Sector 62 Piling", "NH-24 Earthwork", "Okhla Warehouse Rehab", "Metro Depot Framing"],
        "Budget Allocated (₹)": [1200000, 4500000, 2200000, 8500000],
        "Actual Expenses (₹)": [950000, 4100000, 2400000, 6200000],
        "Revenue Realized (₹)": [1500000, 3800000, 2000000, 7000000],
        "Completion %": [85, 90, 45, 70]
    }
    return pd.DataFrame(data)

@st.cache_data
def load_manpower_data():
    data = {
        "Metric Descriptions": ["Skilled Operatives Present", "General Labor Count", "Site Management Staff", "Unexcused/Absenteeism Rate %"],
        "Sector 62 Site": [12, 35, 3, 4.2],
        "NH-24 Site": [8, 55, 4, 8.5],
        "Okhla Site": [5, 18, 2, 2.0],
        "Metro Site": [24, 80, 8, 5.1]
    }
    return pd.DataFrame(data)

df_fin = load_project_financials()
df_man = load_manpower_data()

# Global Executive Summary Tiles
st.subheader("📈 Trevexa Macro Performance Indicators")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Active Portfolios", "4 Major Sites", "+1 Pending")
m2.metric("Total Committed Capital", "₹1.64 Cr")
m3.metric("Total Expenditure to Date", "₹1.36 Cr")
m4.metric("Avg Workforce Attainment", "94.5%", "+1.2% Var")

st.markdown("---")

# Layout: Split Analysis Blocks
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("💰 Financial Health Index")
    # Multi-bar comparisons for budgets vs actuals
    fig_cost = px.bar(
        df_fin, 
        x="Project Name", 
        y=["Budget Allocated (₹)", "Actual Expenses (₹)", "Revenue Realized (₹)"],
        barmode="group",
        title="Cost vs Budget vs Realized Revenue Inflows"
    )
    st.plotly_chart(fig_cost, use_container_width=True)

with right_col:
    st.subheader("🏗️ Work Completion Tracks")
    # Linear completion meters
    fig_comp = px.bar(
        df_fin,
        y="Project Name",
        x="Completion %",
        orientation="h",
        color="Completion %",
        color_continuous_scale="Blugrn",
        title="Physical Milestone Execution Targets Completed (%)"
    )
    st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("---")

# Manpower Matrix Table
st.subheader("👷 Manpower Attendance & Deployment Audit")
st.dataframe(df_man, use_container_width=True, hide_index=True)

# Smart Warnings Generator
st.subheader("⚠️ Automated Operational Red-Flags")
over_budget_projects = df_fin[df_fin["Actual Expenses (₹)"] > df_fin["Budget Allocated (₹)"]]
if not over_budget_projects.empty:
    for _, row in over_budget_projects.iterrows():
        st.error(f"🚨 **Margin Erosion Alert:** Project **{row['Project Name']}** has exceeded its structural budget by **₹{row['Actual Expenses (₹)'] - row['Budget Allocated (₹)']:,}**.")
else:
    st.success("💪 Financial Guardrails Intact: No current active projects are trending over assigned structural budget buffers.")

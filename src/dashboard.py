import streamlit as st
import json
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Skelar AI Support Dashboard", layout="wide")

def load_audit_data():
    try:
        with open("detailed_operational_audit.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

st.title("📊 Skelar AI Operations Dashboard")

data = load_audit_data()

if not data:
    st.error("detailed_operational_audit.json not found. Run your audit script first.")
else:
    # Flatten data for the main table
    rows = []
    for item in data:
        rows.append({
            "ID": item["chat_id"],
            "Customer": item["customer_name"],
            "Intent": item["copilot_analysis"]["intent"],
            "Conf": item["copilot_analysis"]["confidence"],
            "Risk": item["copilot_analysis"]["risk_level"],
            "Priority": item["prioritization"]["level"],
            "Score": item["prioritization"]["score"],
            "Status": item["system_execution"]["status"],
            "Action": item["system_execution"]["action_taken"],
            "Input": item["last_customer_input"]
        })
    
    df = pd.DataFrame(rows)

    # Top Level Metrics
    c1, c2, c3, c4 = st.columns(4)
    total = len(df)
    auto = len(df[df["Status"] == "Executed Automatically"])
    high_risk = len(df[df["Risk"] == "high"])
    
    c1.metric("Total Audited", total)
    c2.metric("Automation Rate", f"{(auto/total)*100:.1f}%" if total > 0 else "0%")
    c3.metric("Critical Risks", high_risk)
    c4.metric("Avg Priority Score", f"{df['Score'].mean():.1f}/100")

    st.divider()

    # Visualizations
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Intent Distribution")
        fig_pie = px.pie(df, names="Intent", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_r:
        st.subheader("Execution Status")
        fig_bar = px.histogram(df, x="Status", color="Status", color_discrete_map={
            "Executed Automatically": "#2ecc71",
            "Pending/Manual": "#e67e22"
        })
        st.plotly_chart(fig_bar, use_container_width=True)

    # Detailed Search and Table
    st.subheader("🔍 Detailed Processed Chats Explorer")
    
    search_term = st.text_input("Search by Customer Name or Intent Content:")
    selected_risks = st.multiselect("Filter by Risk Level:", options=df["Risk"].unique(), default=df["Risk"].unique())
    
    mask = (df["Risk"].isin(selected_risks))
    if search_term:
        mask &= (df["Customer"].str.contains(search_term, case=False) | df["Intent"].str.contains(search_term, case=False))
    
    st.dataframe(df[mask], use_container_width=True)

    # High Risk Focus
    if high_risk > 0:
        st.subheader("🚨 High Risk Alerts (Action Required)")
        st.table(df[df["Risk"] == "high"][["ID", "Customer", "Intent", "Priority", "Status"]])
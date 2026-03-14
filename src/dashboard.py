import streamlit as st
import json
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Skelar AI Support Dashboard", layout="wide")

def load_data(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

st.title("📊 Skelar AI Operations Dashboard")

audit_data = load_data("detailed_operational_audit.json")
metrics_data = load_data("learning_metrics.json")
kb_data = load_data("potential_kb_articles.json")

if not audit_data:
    st.error("detailed_operational_audit.json not found. Run your audit and KB scripts first.")
else:
    rows = []
    for item in audit_data:
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

    c1, c2, c3, c4 = st.columns(4)
    total = len(df)
    auto = len(df[df["Status"] == "Executed Automatically"])
    high_risk = len(df[df["Risk"] == "high"])
    
    c1.metric("Total Audited", total)
    c2.metric("Automation Rate", f"{(auto/total)*100:.1f}%")
    c3.metric("Critical Risks", high_risk)
    c4.metric("Avg Priority Score", f"{df['Score'].mean():.1f}/100")

    st.divider()

    if metrics_data:
        st.subheader("📈 AI Evolution & Automation Growth")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Current Rate", f"{metrics_data['initial_rate']:.1f}%")
        m_col2.metric("Next-Gen Potential", f"{metrics_data['new_rate']:.1f}%", f"+{metrics_data['improvement']:.1f}%")
        m_col3.metric("New Skills Learned", metrics_data['total_learned'])

        chart_df = pd.DataFrame({
            "Stage": ["Baseline", "After Human Demo"],
            "Automation %": [metrics_data['initial_rate'], metrics_data['new_rate']]
        })
        fig_growth = px.bar(chart_df, x="Stage", y="Automation %", color="Stage", 
                            color_discrete_sequence=["#f39c12", "#2ecc71"], text_auto='.1f')
        st.plotly_chart(fig_growth, use_container_width=True)
        st.divider()

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

    if kb_data:
        st.subheader("📚 Knowledge Base Inventory")
        kb_df = pd.DataFrame(kb_data)
        st.dataframe(kb_df, use_container_width=True)

    st.subheader("🔍 Detailed Processed Chats Explorer")
    search_term = st.text_input("Search by Customer Name or Intent Content:")
    selected_risks = st.multiselect("Filter by Risk Level:", options=df["Risk"].unique(), default=df["Risk"].unique())
    
    mask = (df["Risk"].isin(selected_risks))
    if search_term:
        mask &= (df["Customer"].str.contains(search_term, case=False) | df["Intent"].str.contains(search_term, case=False))
    st.dataframe(df[mask], use_container_width=True)

    if high_risk > 0:
        st.subheader("🚨 High Risk Alerts (Action Required)")
        st.table(df[df["Risk"] == "high"][["ID", "Customer", "Intent", "Priority", "Status"]])
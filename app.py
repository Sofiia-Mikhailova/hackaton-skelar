import streamlit as st
import json
import os
from datetime import datetime
from src.copilot2 import AICopilot
from src.customer_simulator import CustomerSimulator
from src.action_executor import ActionExecutor
from src.dashboard import render_dashboard
from src.proactive_engine import run_proactive_monitoring
from src.analyze import analyze_single, LLMClient
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Skelar Live Operations", layout="wide")

# --- INITIALIZATION ---
if 'copilot' not in st.session_state:
    st.session_state.copilot = AICopilot()
if 'simulator' not in st.session_state:
    st.session_state.simulator = CustomerSimulator()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'audit_logs' not in st.session_state:
    st.session_state.audit_logs = []
if 'draft_buffer' not in st.session_state:
    st.session_state.draft_buffer = ""
if 'last_analysis' not in st.session_state:
    st.session_state.last_analysis = None

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

dataset = load_json("data/dataset_clean.json")

# Helper to log system actions
def log_system_event(event_type, description, chat_id):
    entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "chat_id": chat_id,
        "event": event_type,
        "description": description
    }
    st.session_state.audit_logs.append(entry)

# --- SIDEBAR ---
st.sidebar.title("SKELAR AI")
page = st.sidebar.radio("Navigate:", ["Agent Workspace", "Supervisor Dashboard","Proactive Intelligence", "System Audit Log", "Automatic Chat Analysis"])

if page == "Agent Workspace":
    st.title("Interactive Agent Workspace")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Live Chat")
        
        # Scenario Selection
        chat_ids = [c['id'] for c in dataset]
        selected_id = st.selectbox("Select Scenario:", chat_ids)
        current_scenario = next((c for c in dataset if c['id'] == selected_id), {"customer_name": "Unknown", "messages": []})
        chat_id = current_scenario['id']

        # BUTTON TO GENERATE NEXT MESSAGE FROM DATASET
        if st.button("Next Message from Dataset ➡️"):
            dataset_msgs = current_scenario['messages']
            current_len = len(st.session_state.chat_history)
            if current_len < len(dataset_msgs):
                next_msg = dataset_msgs[current_len]
                st.session_state.chat_history.append(next_msg)
                log_system_event("Dataset Import", f"Imported {next_msg['role']} message from original chat.", chat_id)
                st.rerun()
            else:
                st.info("End of original chat reached.")

        # CHAT DISPLAY
        chat_container = st.container(height=400, border=True)
        with chat_container:
            for msg in st.session_state.chat_history:
                st.markdown(f"**{msg['role'].upper()}:** {msg['text']}")

        # AGENT INPUT
        agent_input = st.text_area("Your Response:", value=st.session_state.draft_buffer, height=100)
        
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        
        if btn_col1.button("Send Message", type="primary"):
            if agent_input:
                st.session_state.chat_history.append({"role": "agent", "text": agent_input})
                log_system_event("Manual Reply", f"Agent sent: {agent_input[:30]}...", chat_id)
                st.session_state.draft_buffer = "" # Clear buffer
                
                with st.spinner("Customer is typing..."):
                    history_str = "\n".join([f"{m['role']}: {m['text']}" for m in st.session_state.chat_history])
                    reply = st.session_state.simulator.get_customer_response(history_str)
                    st.session_state.chat_history.append({"role": "customer", "text": reply})
                st.rerun()

        if btn_col2.button("Close Chat & Run Executor"):
            log_system_event("Terminal State", "Agent closed chat. Triggering Executor...", chat_id)
            
            # Prepare final data for executor
            executor = ActionExecutor()
            executor.run_and_save()
            
            st.success("Chat closed and final workflows executed.")
            st.session_state.chat_history = []
            st.rerun()

        if btn_col3.button("Clear History"):
            st.session_state.chat_history = []
            st.rerun()

    with col2:
        st.subheader("AI Copilot")
        if st.session_state.chat_history:
            history_str = "\n".join([f"{m['role']}: {m['text']}" for m in st.session_state.chat_history])
            
            with st.spinner("Analyzing..."):
                res = st.session_state.copilot.get_ai_advice(history_str, customer_name=current_scenario.get('customer_name'))

            if res:
                # TIER-1 AUTOMATION LOGIC
                if res.get('confidence', 0) >= 90:
                    st.warning(f"AI Auto-Action: {res.get('suggested_action')}")
                    log_system_event("Tier-1 Auto-Action", f"Confident ({res.get('confidence')}%) execution of {res.get('suggested_action')}", chat_id)
                
                with st.container(border=True):
                    st.write(f"**Intent:** {res.get('intent')}")
                    
                    risk = str(res.get('churn_risk', 'low')).lower()
                    st.markdown(f"**Risk:** {risk.upper()}")
                    
                    st.write(f"**Action:** {res.get('suggested_action')}")
                    st.divider()
                    st.info(res.get('suggested_reply'))
                    
                    if st.button("Apply Suggested Reply"):
                        st.session_state.draft_buffer = res.get('suggested_reply')
                        st.rerun()

elif page == "Supervisor Dashboard":
    render_dashboard()

elif page == "Proactive Intelligence":
    st.title("🛡️ Proactive Intelligence Scanner")
    st.markdown("""
    This module shifts our support from **Reactive** to **Proactive**. The AI autonomously monitors 
    user behavior and system errors to initiate contact before a complaint is even filed.
    """)

    col1, col2 = st.columns([1, 3])
    
    if col1.button("Run System-Wide Intelligence Scan", type="primary"):
        with st.spinner("AI is scanning system logs for friction points..."):
            # Trigger the proactive engine logic
            run_proactive_monitoring()
            st.success("Scan Complete! New intelligence alerts generated.")
            log_system_event("Intelligence Scan", "Manual system-wide proactive scan triggered.", "SYSTEM")

    # Load the results generated by proactive_engine.py
    proactive_data = load_json("proactive_actions.json")

    if proactive_data:
        # Displaying key metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Alerts", len(proactive_data))
        c2.metric("Target: Agents", len([x for x in proactive_data if x['recipient'] == 'Agent']))
        c3.metric("Target: Customers", len([x for x in proactive_data if x['recipient'] == 'Customer']))

        # Detailed Alert Table
        st.subheader("Live Intelligence Feed")
        st.table(proactive_data)
    else:
        st.info("No proactive alerts found. Run a scan to find friction points.")

elif page == "System Audit Log":
    st.title("Raw Operational Audit Log")
    st.table(st.session_state.audit_logs)

elif page == "Automatic Chat Analysis":
    st.title("🔍 Automatic Chat Analysis & Scoring")
    st.markdown("This module uses **Llama 3.3 70B** to audit service quality.")

    # SECTION 1: LATEST SESSION RESULT
    if st.session_state.last_analysis:
        st.subheader("⚡ Result of Last Session")
        analysis = st.session_state.last_analysis['analysis']
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Quality Score", f"{analysis['quality_score']}/5")
        c2.metric("Intent", analysis['intent'])
        c3.metric("Satisfaction", analysis['satisfaction'])
        c4.metric("Scenario", analysis['scenario'])
        
        if analysis['agent_mistakes']:
            st.error(f"⚠️ Mistakes Detected: {', '.join(analysis['agent_mistakes'])}")
        else:
            st.success("✅ No mistakes detected. Great job!")
    
    st.divider()

    # SECTION 2: HISTORICAL AUDIT (From analysis_results.json)
    st.subheader("📊 Global Audit Results")
    analysis_data = load_json("data/analysis_results.json")

    if analysis_data:
        rows = []
        for item in analysis_data:
            rows.append({
                "ID": item["id"],
                "Customer": item["customer_name"],
                "Score": item["analysis"]["quality_score"],
                "Intent": item["analysis"]["intent"],
                "Satisfaction": item["analysis"]["satisfaction"],
                "Mistakes": ", ".join(item["analysis"]["agent_mistakes"])
            })
        
        df = pd.DataFrame(rows)

        # Charts
        v1, v2 = st.columns(2)
        with v1:
            fig_score = px.histogram(df, x="Score", title="Quality Score Distribution", color_discrete_sequence=['#2ecc71'])
            st.plotly_chart(fig_score, use_container_width=True)
        with v2:
            fig_pie = px.pie(df, names="Satisfaction", title="Customer Satisfaction Levels", hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)

        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No historical analysis found in data/analysis_results.json")
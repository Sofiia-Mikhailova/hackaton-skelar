import streamlit as st
import json
import os
import time
from datetime import datetime
import pandas as pd
import plotly.express as px

# Internal Skelar imports
from src.copilot2 import AICopilot
from src.customer_simulator import CustomerSimulator
from src.action_executor import ActionExecutor
from src.dashboard import render_dashboard
from src.proactive_engine import run_proactive_monitoring
from src.analyze import analyze_single
from src.follow_up import run_post_resolution_follow_up

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

def log_system_event(event_type, description, chat_id):
    entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "chat_id": chat_id,
        "event": event_type,
        "description": description
    }
    st.session_state.audit_logs.append(entry)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("SKELAR AI")
page = st.sidebar.radio("Navigate:", ["Agent Workspace", "Supervisor Dashboard", "Proactive Intelligence", "System Audit Log", "Automatic Chat Analysis"])

if page == "Agent Workspace":
    st.title("Interactive Agent Workspace")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Live Chat")
        
        chat_ids = [c['id'] for c in dataset]
        selected_id = st.selectbox("Select Scenario:", chat_ids)
        current_scenario = next((c for c in dataset if c['id'] == selected_id), {"customer_name": "Unknown", "messages": []})
        chat_id = current_scenario['id']

        if st.button("Next Message from Dataset ➡️"):
            dataset_msgs = current_scenario['messages']
            current_len = len(st.session_state.chat_history)
            if current_len < len(dataset_msgs):
                next_msg = dataset_msgs[current_len]
                st.session_state.chat_history.append(next_msg)
                log_system_event("Dataset Import", f"Imported {next_msg['role']} message.", chat_id)
                st.rerun()

        chat_container = st.container(height=400, border=True)
        with chat_container:
            for msg in st.session_state.chat_history:
                st.markdown(f"**{msg['role'].upper()}:** {msg['text']}")

        agent_input = st.text_area("Your Response:", value=st.session_state.draft_buffer, height=100)
        
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        
        if btn_col1.button("Send Message", type="primary"):
            if agent_input:
                st.session_state.chat_history.append({"role": "agent", "text": agent_input})
                st.session_state.draft_buffer = "" 
                with st.spinner("Customer is typing..."):
                    history_str = "\n".join([f"{m['role']}: {m['text']}" for m in st.session_state.chat_history])
                    reply = st.session_state.simulator.get_customer_response(history_str)
                    st.session_state.chat_history.append({"role": "customer", "text": reply})
                st.rerun()

        # WORKFLOW TRIGGER: Close Chat, Analyze, Wait, and Follow-up
        if btn_col2.button("Close Chat & Run Executor"):
            if not st.session_state.chat_history:
                st.warning("Chat history is empty.")
            else:
                log_system_event("Terminal State", "Closing chat and triggering audit.", chat_id)
                
                # 1. Action Executor
                executor = ActionExecutor()
                executor.run_and_save()

                # 2. Automatic Analysis (LLM Scoring)
                with st.spinner("Llama 3.3 auditing service quality..."):
                    history_str = "\n".join([f"{m['role']}: {m['text']}" for m in st.session_state.chat_history])
                    new_analysis = analyze_single(chat_id, current_scenario.get('customer_name'), history_str)
                    st.session_state.last_analysis = new_analysis
                    
                    # Persist analysis to the global log
                    analysis_file = "data/analysis_results.json"
                    hist_data = load_json(analysis_file)
                    hist_data = [item for item in hist_data if item.get('id') != chat_id] # Avoid duplicates
                    hist_data.append(new_analysis)
                    with open(analysis_file, 'w', encoding='utf-8') as f:
                        json.dump(hist_data, f, indent=4, ensure_ascii=False)

                # 3. Demo Delay
                with st.spinner("Waiting 3 seconds for automated follow-up..."):
                    time.sleep(3) 
                    run_post_resolution_follow_up()
                    log_system_event("Post-Resolution", "Follow-up message logged.", chat_id)
                
                st.success("Session audited and follow-up triggered!")
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
                with st.container(border=True):
                    st.write(f"**Intent:** {res.get('intent')}")
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
    if st.button("Run System-Wide Intelligence Scan", type="primary"):
        with st.spinner("Scanning system logs..."):
            run_proactive_monitoring()
            st.success("Scan Complete!")
    
    proactive_data = load_json("proactive_actions.json")
    if proactive_data:
        st.table(proactive_data)

elif page == "System Audit Log":
    st.title("Operational Audit Log")
    st.table(st.session_state.audit_logs)
    st.divider()
    st.subheader("📬 Post-Resolution Follow-up Log")
    st.dataframe(load_json("follow_up_log.json"), use_container_width=True)

elif page == "Automatic Chat Analysis":
    st.title("🔍 Automatic Chat Analysis & Scoring")
    if st.session_state.last_analysis:
        st.subheader("⚡ Result of Last Session")
        analysis = st.session_state.last_analysis['analysis']
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Quality Score", f"{analysis['quality_score']}/5")
        c2.metric("Intent", analysis['intent'])
        c3.metric("Satisfaction", analysis['satisfaction'])
        c4.metric("Scenario", analysis['scenario'])
    
    st.divider()
    st.subheader("📊 Global Audit Results")
    analysis_data = load_json("data/analysis_results.json")
    if analysis_data:
        df = pd.DataFrame([{
            "ID": i["id"], "Customer": i["customer_name"], 
            "Score": i["analysis"]["quality_score"], 
            "Intent": i["analysis"]["intent"], 
            "Satisfaction": i["analysis"]["satisfaction"]
        } for i in analysis_data])
        
        v1, v2 = st.columns(2)
        with v1:
            st.plotly_chart(px.histogram(df, x="Score", title="Score Distribution", color_discrete_sequence=['#2ecc71']), use_container_width=True)
        with v2:
            st.plotly_chart(px.pie(df, names="Satisfaction", title="Satisfaction Levels", hole=0.4), use_container_width=True)
        st.dataframe(df, use_container_width=True)
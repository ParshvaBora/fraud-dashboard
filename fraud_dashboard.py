import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# 1. THE MOCK DATA & AI SIMULATOR
# ==========================================
def load_mock_data():
    data = [
        {"tx_id": "TXN-1001", "amount": 45.50, "type": "Domestic", "device": "Known", "acc_age_days": 400, "ai_anomaly_score": 12},
        {"tx_id": "TXN-1002", "amount": 8500.00, "type": "Domestic", "device": "Known", "acc_age_days": 15, "ai_anomaly_score": 85},
        {"tx_id": "TXN-1003", "amount": 120.00, "type": "International", "device": "New", "acc_age_days": 300, "ai_anomaly_score": 65},
        {"tx_id": "TXN-1004", "amount": 9500.00, "type": "International", "device": "New", "acc_age_days": 800, "ai_anomaly_score": 92},
        {"tx_id": "TXN-1005", "amount": 15.00, "type": "Domestic", "device": "Known", "acc_age_days": 1200, "ai_anomaly_score": 5},
    ]
    return pd.DataFrame(data)

def simulate_ai_score(amount, location, device, acc_age):
    # This simulates our "Black Box" Machine Learning model
    score = 5
    if amount > 1000: score += 15
    if amount > 5000: score += 25
    if location == "International": score += 25
    if device == "New": score += 30
    if acc_age < 30: score += 15
    return min(max(int(score), 0), 100) # Keep score between 0 and 100

# ==========================================
# 2. THE EXPERT SYSTEM (Knowledge Base)
# ==========================================
def evaluate_rules(amount, location, device, acc_age):
    rules_failed = []
    if amount > 5000 and acc_age < 30:
        rules_failed.append("Rule 1: Large transaction on new account (< 30 days).")
    if location == "International" and device == "New":
        rules_failed.append("Rule 2: International transaction from an unrecognized device.")
    if amount > 9000:
        rules_failed.append("Rule 3: Transaction exceeds single-swipe sanity limit ($9,000).")
    return rules_failed

# ==========================================
# 3. THE HYBRID INFERENCE ENGINE
# ==========================================
def get_final_verdict(ai_score, rules_failed):
    if ai_score > 80 or len(rules_failed) >= 2:
        return "BLOCKED", "🚨"
    elif ai_score > 50 or len(rules_failed) == 1:
        return "REVIEW", "⚠️"
    else:
        return "APPROVED", "✅"

# ==========================================
# 4. THE UI DASHBOARD
# ==========================================
st.set_page_config(page_title="AI Fraud Investigator", layout="wide")

# --- SIDEBAR: CUSTOM INPUT FORM ---
st.sidebar.header("🛠️ Custom Simulator")
st.sidebar.markdown("Test the hybrid system by entering custom transaction details below.")

with st.sidebar.form("custom_tx_form"):
    custom_amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=250.00, step=50.0)
    custom_location = st.selectbox("Location", ["Domestic", "International"])
    custom_device = st.selectbox("Device Status", ["Known", "New"])
    custom_age = st.number_input("Account Age (Days)", min_value=0, value=365, step=30)
    
    submitted = st.form_submit_button("Run Analysis")

# --- MAIN LAYOUT ---
st.title("🛡️ Hybrid AI & Expert System: Fraud Investigator")
st.markdown("Monitoring live transaction feeds using Machine Learning Anomaly Detection and Rule-Based Logic.")
st.divider()

left_col, right_col = st.columns([1.5, 1])

# If the user submitted a custom transaction, show that. Otherwise, show the feed.
if submitted:
    with left_col:
        st.subheader("📡 Live Intercept: Custom Transaction")
        st.info("The system has intercepted the manual transaction you just submitted. Analyzing routing data...")
        
        # Display the custom inputs cleanly
        st.markdown(f"**Amount:** ${custom_amount:,.2f}")
        st.markdown(f"**Location:** {custom_location}")
        st.markdown(f"**Device:** {custom_device}")
        st.markdown(f"**Account Age:** {custom_age} days")
        
        if st.button("← Back to Live Feed"):
            st.rerun()

    with right_col:
        st.subheader("Detailed Investigation")
        
        # Run the logic on custom inputs
        ai_score = simulate_ai_score(custom_amount, custom_location, custom_device, custom_age)
        rules = evaluate_rules(custom_amount, custom

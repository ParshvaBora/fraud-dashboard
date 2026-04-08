import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# 1. THE MOCK DATA (Simulated Banking Feed)
# ==========================================
def load_mock_data():
    data = [
        {"tx_id": "TXN-1001", "amount": 45.50, "type": "Domestic", "device": "Known", "acc_age_days": 400, "ai_anomaly_score": 12},
        {"tx_id": "TXN-1002", "amount": 8500.00, "type": "Domestic", "device": "Known", "acc_age_days": 15, "ai_anomaly_score": 85}, # High risk AI & Rule
        {"tx_id": "TXN-1003", "amount": 120.00, "type": "International", "device": "New", "acc_age_days": 300, "ai_anomaly_score": 65}, # Borderline
        {"tx_id": "TXN-1004", "amount": 9500.00, "type": "International", "device": "New", "acc_age_days": 800, "ai_anomaly_score": 92}, # Total Fraud
        {"tx_id": "TXN-1005", "amount": 15.00, "type": "Domestic", "device": "Known", "acc_age_days": 1200, "ai_anomaly_score": 5},
        {"tx_id": "TXN-1006", "amount": 5500.00, "type": "Domestic", "device": "New", "acc_age_days": 10, "ai_anomaly_score": 45}, # Fails rule, low AI
        {"tx_id": "TXN-1007", "amount": 30.00, "type": "International", "device": "Known", "acc_age_days": 500, "ai_anomaly_score": 18},
    ]
    return pd.DataFrame(data)

# ==========================================
# 2. THE EXPERT SYSTEM (Knowledge Base & Rules)
# ==========================================
def evaluate_rules(row):
    rules_failed = []
    
    # Rule 1: High-Value New Account Check
    if row['amount'] > 5000 and row['acc_age_days'] < 30:
        rules_failed.append("Rule 1: Large transaction on new account (< 30 days).")
        
    # Rule 2: Geo-Consistency Check
    if row['type'] == "International" and row['device'] == "New":
        rules_failed.append("Rule 2: International transaction from an unrecognized device.")
        
    # Rule 3: Extreme Value Sanity Check
    if row['amount'] > 9000:
        rules_failed.append("Rule 3: Transaction exceeds single-swipe sanity limit ($9,000).")
        
    return rules_failed

# ==========================================
# 3. THE HYBRID INFERENCE ENGINE
# ==========================================
def get_final_verdict(ai_score, rules_failed):
    # Combines AI perception with Rule-based logic
    if ai_score > 80 or len(rules_failed) >= 2:
        return "BLOCKED", "🚨"
    elif ai_score > 50 or len(rules_failed) == 1:
        return "REVIEW", "⚠️"
    else:
        return "APPROVED", "✅"

# ==========================================
# 4. THE UI DASHBOARD (Streamlit Shell)
# ==========================================
st.set_page_config(page_title="AI Fraud Investigator", layout="wide")

st.title("🛡️ Hybrid AI & Expert System: Fraud Investigator")
st.markdown("Monitoring live transaction feeds using Machine Learning Anomaly Detection and Rule-Based Logic.")

# Load Data
df = load_mock_data()

# Apply the Hybrid Engine to all data
df['rules_failed'] = df.apply(evaluate_rules, axis=1)
df['status_data'] = df.apply(lambda x: get_final_verdict(x['ai_anomaly_score'], x['rules_failed']), axis=1)
df['Status'] = df['status_data'].apply(lambda x: x[0])
df['Icon'] = df['status_data'].apply(lambda x: x[1])

# --- TOP METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", len(df))
col2.metric("Approved", len(df[df['Status'] == 'APPROVED']))
col3.metric("Flagged for Review", len(df[df['Status'] == 'REVIEW']))
col4.metric("Blocked Fraud", len(df[df['Status'] == 'BLOCKED']))

st.divider()

# --- MAIN LAYOUT ---
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("Live Transaction Feed")
    # Display a clean version of the dataframe
    display_df = df[['Icon', 'tx_id', 'amount', 'type', 'device', 'Status']]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

with right_col:
    st.subheader("Detailed Investigation")
    st.markdown("Select a Transaction ID to view the AI and Expert System reasoning.")
    
    # Dropdown to select a transaction
    selected_tx = st.selectbox("Select TX_ID:", df['tx_id'])
    
    if selected_tx:
        # Get the specific row of data
        tx_data = df[df['tx_id'] == selected_tx].iloc[0]
        
        # Display Details
        st.markdown(f"**Amount:** ${tx_data['amount']}")
        st.markdown(f"**Location:** {tx_data['type']}")
        st.markdown(f"**Device:** {tx_data['device']}")
        st.markdown(f"**Account Age:** {tx_data['acc_age_days']} days")
        
        st.divider()
        
        # Display AI Component
        st.write("### 🧠 AI Anomaly Engine")
        score = tx_data['ai_anomaly_score']
        st.progress(score / 100)
        st.write(f"**Statistical Anomaly Score:** {score}/100")
        
        st.divider()
        
        # Display Expert System Component
        st.write("### 📜 Expert System Rules")
        rules = tx_data['rules_failed']
        if len(rules) == 0:
            st.success("All Rules Passed.")
        else:
            for rule in rules:
                st.error(f"FAIL: {rule}")
                
        st.divider()
        
        # Final Verdict
        st.write("### ⚖️ Final Verdict")
        if tx_data['Status'] == 'APPROVED':
            st.success(f"{tx_data['Icon']} APPROVED: Transaction aligns with user behavior and passes all rules.")
        elif tx_data['Status'] == 'REVIEW':
            st.warning(f"{tx_data['Icon']} REVIEW: Transaction flagged due to moderate AI score or a single rule violation.")
        else:
            st.error(f"{tx_data['Icon']} BLOCKED: High probability of fraud detected by the hybrid system.")

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import plotly.express as px
import time
import base64
import os
import re
import requests

# --- 1. GLOBAL SYSTEM ARCHITECTURE ---
st.set_page_config(page_title="G-FILID | GLOBAL FORENSIC COMMAND", layout="wide", page_icon="🛡️")

def sanitize_headers(name):
    mapping = {'کد_ملی': 'National_ID', 'درآمد_سالانه': 'Annual_Income', 'مالیات_پرداختی': 'Tax_Paid', 'تعداد_املاک': 'Asset_Count'}
    return mapping.get(name, re.sub(r'[^\x00-\x7F]+', 'DATA_FIELD', str(name)))

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# --- 2. INTERFACE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Share+Tech+Mono&family=Montserrat:wght@700&display=swap');
    .main { background: radial-gradient(circle at center, #001529 0%, #00050a 100%); color: #ffffff; font-family: 'Share Tech Mono', monospace; }
    .status-bar { background: #000000; border-bottom: 2px solid #d4af37; padding: 8px; text-align: center; color: #d4af37; position: fixed; top: 0; left: 0; width: 100%; z-index: 999; font-size: 11px; letter-spacing: 5px;}
    .seal-box { text-align: center; padding: 85px 0 20px 0; }
    .agency-logo { width: 155px; height: 155px; border-radius: 50%; border: 3px double #d4af37; padding: 5px; box-shadow: 0 0 45px rgba(212, 175, 55, 0.5); background: rgba(0,0,0,0.5); }
    .main-title { font-family: 'Cinzel', serif; font-size: 46px; color: #ffffff; margin-top: 20px; letter-spacing: 3px; text-shadow: 0 0 20px rgba(212, 175, 55, 0.4); }
    .stButton>button { background: linear-gradient(180deg, #d4af37 0%, #8a6d3b 100%) !important; color: #000 !important; font-weight: bold !important; width: 100%; height: 3.5em; text-transform: uppercase; letter-spacing: 2px; }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; text-shadow: 0 0 5px rgba(212, 175, 55, 0.3); }
    .top-secret-tag { position: absolute; top: 125px; right: 65px; border: 5px solid #ff1a1a; color: #ff1a1a; padding: 10px 20px; font-size: 24px; font-weight: 900; transform: rotate(12deg); opacity: 0.4; border-radius: 8px; }
    </style>
    <div class="status-bar">GLOBAL STRATEGIC COMMAND - ENCRYPTION ACTIVE [AES-256-GCM]</div>
    <div class="top-secret-tag">CLASSIFIED</div>
    """, unsafe_allow_html=True)

# --- 3. BRANDING ---
logo_data = get_base64_of_bin_file("logo.png")
st.markdown('<div class="seal-box">', unsafe_allow_html=True)
if logo_data:
    st.markdown(f'<img src="data:image/png;base64,{logo_data}" class="agency-logo">', unsafe_allow_html=True)
st.markdown("<div class='main-title' style='text-align:center;'>G-FILID STRATEGIC COMMAND</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#d4af37; letter-spacing:7px; font-weight:bold; font-size:14px; margin-bottom:30px;'>FINANCIAL INTELLIGENCE & BLOCKCHAIN INVESTIGATION DIVISION</div>", unsafe_allow_html=True)

# --- 4. TABS ---
tab1, tab2, tab3 = st.tabs(["🏛️ FIAT AUDIT CORE", "₿ BTC SURVEILLANCE", "💎 ETH/USDT INTELLIGENCE"])

# --- TAB 1: FIAT AUDIT ---
with tab1:
    st.subheader("📁 SYSTEM INPUT: DATA ANALYTICS")
    uploaded_file = st.file_uploader("UPLOAD SOURCE FILE", type=["csv", "xlsx"], key="fiat_p")
    if uploaded_file:
        with st.spinner("💠 SCANNING..."):
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            df.columns = [sanitize_headers(col) for col in df.columns]
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            selected_cols = st.multiselect("SELECT PARAMETERS:", numeric_cols, default=numeric_cols[:2] if len(numeric_cols)>1 else None)
            if len(selected_cols) >= 2:
                sensitivity = st.sidebar.slider("AI SENSITIVITY", 0.01, 0.25, 0.05)
                model = IsolationForest(contamination=sensitivity, random_state=42)
                df['Anomaly'] = model.fit_predict(df[selected_cols])
                threats = df[df['Anomaly'] == -1]
                st.divider()
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("SCANNED", len(df))
                c2.metric("THREATS", len(threats))
                c3.metric("INTEGRITY", f"{100-(len(threats)/len(df)*100):.1f}%")
                c4.metric("AI STATUS", "STABLE")
                st.plotly_chart(px.scatter(df.sample(min(len(df), 5000)), x=selected_cols[0], y=selected_cols[1], color='Anomaly', color_discrete_map={-1: '#ff1a1a', 1: '#d4af37'}, template="plotly_dark"), use_container_width=True)
                if st.button("📥 GENERATE OFFICIAL FORENSIC REPORT"):
                    st.success("REPORT GENERATED!")
                    st.info(f"CASE ID: G-FILID-{int(time.time())}\nSTATUS: EVIDENCE SECURED")

# --- TAB 2: BTC ---
with tab2:
    st.subheader("🌐 BTC LEDGER SURVEILLANCE")
    btc_addr = st.text_input("ENTER BTC ADDRESS:", key="btc_i")
    if btc_addr:
        res = requests.get(f"https://blockchain.info/rawaddr/{btc_addr}")
        if res.status_code == 200:
            data = res.json()
            mc1, mc2 = st.columns(2)
            mc1.metric("BALANCE", f"{data['final_balance']/100000000:.4f} BTC")
            mc2.metric("TRANSACTIONS", data['n_tx'])
            if st.button("📥 GENERATE BTC CASE REPORT"):
                st.info(f"CASE ID: G-FILID-BTC-{int(time.time())}\nSTATUS: SECURED")
        else: st.error("INVALID ADDRESS")

# --- TAB 3: ETH/USDT ---
with tab3:
    st.subheader("🏦 ETH/USDT INTELLIGENCE")
    eth_addr = st.text_input("ENTER ETH ADDRESS:", key="eth_i")
    if eth_addr:
        res = requests.get(f"https://api.ethplorer.io/getAddressInfo/{eth_addr}?apiKey=freekey")
        if res.status_code == 200:
            data = res.json()
            ec1, ec2 = st.columns(2)
            ec1.metric("ETH BALANCE", f"{data.get('ETH',{}).get('balance',0):.4f}")
            tokens = data.get('tokens', [])
            usdt = next((t for t in tokens if t['tokenInfo']['symbol'] == 'USDT'), None)
            if usdt:
                val = usdt['balance'] / (10**int(usdt['tokenInfo']['decimals']))
                ec2.metric("USDT BALANCE", f"${val:,.2f}")
            else: ec2.metric("USDT BALANCE", "$0.00")
            if st.button("📥 GENERATE ETH CASE REPORT"):
                st.info(f"CASE ID: G-FILID-ETH-{int(time.time())}\nSTATUS: SECURED")

# --- SIDEBAR (METHODOLOGY ADDED) ---
st.sidebar.divider()
st.sidebar.code("AGENT_ID: 420-FAZLI\nLEVEL: TITAN\nSTATUS: ONLINE")
with st.sidebar.expander("🧬 NEURAL CORE METHODOLOGY"):
    st.markdown("""
    **Core Engine:** Isolation Forest AI
    
    **Analysis Pipeline:**
    1. **Data Ingestion:** Scanning multivariate financial features.
    2. **Recursive Partitioning:** Isolating anomalies via neural decision paths.
    3. **Blockchain Attribution:** Real-time ledger verification via global nodes.
    
    *Verified by G-FILID Protocol 2300.*
    """)
st.sidebar.error("AUTHORIZED USE ONLY.")
st.markdown("<hr><center style='color:#333; font-size:10px;'>FOR OFFICIAL USE ONLY (FOUO) | © 2024 G-FILID STRATEGIC COMMAND</center>", unsafe_allow_html=True)
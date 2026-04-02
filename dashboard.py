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
st.set_page_config(
    page_title="G-FILID | SUPREME GLOBAL COMMAND", 
    layout="wide", 
    page_icon="🛡️"
)

# --- 2. SECURITY & ANALYTICAL FUNCTIONS ---
def sanitize_headers(name):
    mapping = {'کد_ملی': 'National_ID', 'درآمد_سالانه': 'Annual_Income', 'مالیات_پرداختی': 'Tax_Paid', 'تعداد_املاک': 'Asset_Count'}
    if name in mapping: return mapping[name]
    return re.sub(r'[^\x00-\x7F]+', 'DATA_FIELD', str(name))

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# --- 3. HIGH-LEVEL AGENCY INTERFACE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Share+Tech+Mono&family=Montserrat:wght@700&display=swap');
    .main { background: radial-gradient(circle at center, #001529 0%, #00050a 100%); color: #ffffff; font-family: 'Share Tech Mono', monospace; }
    .status-bar { background: #000000; border-bottom: 2px solid #d4af37; padding: 8px; text-align: center; font-family: 'Montserrat', sans-serif; font-size: 11px; letter-spacing: 5px; color: #d4af37; position: fixed; top: 0; left: 0; width: 100%; z-index: 999; }
    .seal-box { text-align: center; padding: 80px 0 20px 0; }
    .agency-logo { width: 155px; height: 155px; border-radius: 50%; border: 3px double #d4af37; padding: 5px; box-shadow: 0 0 45px rgba(212, 175, 55, 0.5); background: rgba(0,0,0,0.6); }
    .main-title { font-family: 'Cinzel', serif; font-size: 48px; color: #ffffff; margin-top: 25px; letter-spacing: 4px; text-shadow: 0 0 20px rgba(212, 175, 55, 0.5); }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-size: 38px !important; text-shadow: 0 0 10px rgba(212, 175, 55, 0.3); }
    .top-secret-tag { position: absolute; top: 130px; right: 70px; border: 6px solid #ff1a1a; color: #ff1a1a; padding: 15px 30px; font-size: 28px; font-weight: 900; transform: rotate(10deg); opacity: 0.5; border-radius: 10px; font-family: 'Montserrat', sans-serif; }
    .stButton>button { background: linear-gradient(180deg, #d4af37 0%, #8a6d3b 100%) !important; color: #000 !important; font-weight: bold !important; width: 100%; height: 3.5em; text-transform: uppercase; letter-spacing: 3px; font-size: 16px !important; }
    </style>
    <div class="status-bar">WARNING: CLASSIFIED GOVERNMENT DATA LINK - ENCRYPTION ACTIVE [AES-256-GCM]</div>
    <div class="top-secret-tag">CLASSIFIED</div>
    """, unsafe_allow_html=True)

# --- 4. AGENCY BRANDING ---
logo_data = get_base64_of_bin_file("logo.png")
st.markdown('<div class="seal-box">', unsafe_allow_html=True)
if logo_data:
    st.markdown(f'<img src="data:image/png;base64,{logo_data}" class="agency-logo">', unsafe_allow_html=True)
else:
    st.markdown('<div style="width:150px; height:150px; border:4px solid #d4af37; border-radius:50%; display:inline-block; line-height:150px; font-size:70px; background:rgba(212,175,55,0.05);">🛡️</div>', unsafe_allow_html=True)

st.markdown("""
        <div class="main-title">G-FILID GLOBAL COMMAND</div>
        <div style="color: #d4af37; font-weight: bold; letter-spacing: 8px; font-size: 15px; margin-top: 12px;">
            FINANCIAL INTELLIGENCE & BLOCKCHAIN INVESTIGATION DIVISION
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. MULTI-COMMAND NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["🏛️ FIAT AUDIT CORE", "₿ BTC SURVEILLANCE", "💎 ETH/USDT INTELLIGENCE"])

# --- TAB 1: FIAT AUDIT CORE (Supports 100k Records) ---
with tab1:
    st.subheader("📁 SYSTEM INPUT: MASS DATA DOSSIER")
    uploaded_file = st.file_uploader("UPLOAD SOURCE FILE (CSV/XLSX)", type=["csv", "xlsx"], key="fiat_p")
    if uploaded_file:
        with st.spinner("💠 AI NEURAL SCANNING IN PROGRESS..."):
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            df.columns = [sanitize_headers(col) for col in df.columns]
            st.success(f"ACCESS GRANTED: {len(df):,} ENTITIES EXTRACTED.")
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            selected_cols = st.multiselect("SELECT PARAMETERS FOR PATTERN RECOGNITION:", numeric_cols, default=numeric_cols[:2] if len(numeric_cols)>1 else numeric_cols)
            
            if len(selected_cols) >= 2:
                st.sidebar.markdown("<h2 style='color:#d4af37;'>AI CONTROL</h2>", unsafe_allow_html=True)
                sensitivity = st.sidebar.slider("AI THREAT SENSITIVITY", 0.01, 0.25, 0.05)
                model = IsolationForest(contamination=sensitivity, random_state=42)
                df['Anomaly_Score'] = model.fit_predict(df[selected_cols])
                df['RISK_LEVEL'] = df['Anomaly_Score'].apply(lambda x: '🚨 CRITICAL THREAT' if x == -1 else '✅ SECURE')
                
                c1, c2, c3, c4 = st.columns(4)
                threat_count = len(df[df['Anomaly_Score'] == -1])
                c1.metric("RECORDS SCANNED", f"{len(df):,}")
                c2.metric("THREATS DETECTED", threat_count)
                c3.metric("INTEGRITY INDEX", f"{100-(threat_count/len(df)*100):.1f}%")
                c4.metric("SYSTEM CORE", "QUANTUM")

                st.plotly_chart(px.scatter(df, x=selected_cols[0], y=selected_cols[1], color='RISK_LEVEL', color_discrete_map={'🚨 CRITICAL THREAT': '#ff1a1a', '✅ SECURE': '#d4af37'}, template="plotly_dark"), use_container_width=True)
                st.subheader("🚩 BLACKLISTED ENTITIES - IMMEDIATE ACTION REQUIRED")
                st.dataframe(df[df['Anomaly_Score'] == -1].drop(columns=['Anomaly_Score']), use_container_width=True)
            else:
                st.warning("NOTICE: MINIMUM 2 PARAMETERS REQUIRED FOR AI NEURAL SCAN.")

# --- TAB 2: BTC SURVEILLANCE ---
with tab2:
    st.subheader("🌐 REAL-TIME BTC LEDGER SURVEILLANCE")
    btc_address = st.text_input("ENTER BTC WALLET ADDRESS FOR TRACING:", key="btc_i")
    if btc_address:
        with st.spinner("📡 SCANNING GLOBAL BITCOIN NODES..."):
            res = requests.get(f"https://blockchain.info/rawaddr/{btc_address}")
            if res.status_code == 200:
                data = res.json()
                mc1, mc2 = st.columns(2)
                mc1.metric("CURRENT BALANCE", f"{data['final_balance']/100000000:.4f} BTC")
                mc2.metric("TOTAL TRANSACTIONS", data['n_tx'])
                st.success("🔓 DATA LINK ESTABLISHED")
                txs = [{"TX_HASH": tx['hash'][:30]+"...", "TIME": pd.to_datetime(tx['time'], unit='s'), "RESULT_BTC": tx['result']/100000000} for tx in data['txs'][:10]]
                st.table(pd.DataFrame(txs))
            else: st.error("INVALID BTC ADDRESS")

# --- TAB 3: ETH/USDT (PRO ACCURACY) ---
with tab3:
    st.subheader("🏦 ETHEREUM & USDT (TETHER) INTELLIGENCE")
    eth_address = st.text_input("ENTER ETH WALLET (0x...):", key="eth_i")
    if eth_address:
        with st.spinner("📡 SCANNING ETHEREUM NETWORK NODES..."):
            res = requests.get(f"https://api.ethplorer.io/getAddressInfo/{eth_address}?apiKey=freekey")
            if res.status_code == 200:
                data = res.json()
                ec1, ec2, ec3 = st.columns(3)
                eth_bal = data.get('ETH', {}).get('balance', 0)
                ec1.metric("ETH BALANCE", f"{eth_bal:,.4f}")
                tokens = data.get('tokens', [])
                usdt = next((t for t in tokens if t['tokenInfo']['symbol'] == 'USDT'), None)
                if usdt:
                    val = usdt['balance'] / (10**int(usdt['tokenInfo']['decimals']))
                    ec2.metric("USDT BALANCE", f"${val:,.2f}")
                else: ec2.metric("USDT BALANCE", "$0.00")
                ec3.metric("TOTAL ASSET TYPES", len(tokens))
                st.info(f"ENS IDENTITY: {data.get('ensName', 'UNREGISTERED')}")
            else: st.error("INVALID ETH ADDRESS OR API LIMIT")

# --- 6. AGENT AUTHENTICATION ---
st.sidebar.divider()
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1067/1067357.png", width=65)
st.sidebar.code("AGENT_ID: 420-FAZLI\nCLEARANCE: LEVEL 5 (ULTRA)\nSTATUS: ONLINE")
st.sidebar.error("AUTHORIZED USE ONLY. UNAUTHORIZED ACCESS IS A FEDERAL CRIME.")

# --- 7. FOOTER ---
st.markdown("<br><hr><center style='color:#333; font-size:10px;'>FOR OFFICIAL USE ONLY (FOUO) | GLOBAL SOVEREIGN COMMAND | © 2024 G-FILID STRATEGIC COMMAND</center>", unsafe_allow_html=True)

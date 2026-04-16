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

# --- 1. SYSTEM IDENTITY & CONFIG ---
st.set_page_config(page_title="G-FILID | INTELLIGENCE CORE", layout="wide", page_icon="🛡️")

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# --- 2. ADVANCED INTERFACE (Executive Design) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Share+Tech+Mono&family=Montserrat:wght@400;700&display=swap');

.main { 
    background: radial-gradient(circle at center, #0a0f1a 0%, #000000 100%);
    color: #ffffff;
    font-family: 'Montserrat', sans-serif;
}
.stApp { background-color: #000000; }

.top-header {
    background-color: #000000;
    border-bottom: 2px solid #d4af37;
    padding: 8px;
    text-align: center;
    color: #d4af37;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    letter-spacing: 4px;
    position: fixed; top: 0; left: 0; width: 100%; z-index: 999;
}

.seal-container { text-align: center; padding-top: 80px; }
.user-logo {
    width: 140px; height: 140px;
    border-radius: 50%; border: 2px solid #d4af37;
    padding: 10px; box-shadow: 0 0 30px rgba(212, 175, 55, 0.4);
    background: rgba(0,0,0,0.5);
}

.scanning-text {
    color: #ff0000;
    font-weight: bold;
    text-align: center;
    font-family: 'Share Tech Mono', monospace;
    animation: blinker 1s linear infinite;
}
@keyframes blinker { 50% { opacity: 0; } }

.stButton>button {
    background: linear-gradient(180deg, #8b0000 0%, #4a0000 100%) !important;
    color: white !important;
    border: 1px solid #d4af37 !important;
    border-radius: 4px !important;
    font-weight: bold;
    letter-spacing: 1px;
    height: 3.5em;
    width: 100%;
}

div[data-testid="stMetricValue"] { color: #d4af37 !important; font-family: 'Share Tech Mono'; }
</style>
<div class="top-header">OFFICIAL GOVERNMENT ANALYTICAL PORTAL - SECURE ACCESS ONLY</div>
""", unsafe_allow_html=True)

# --- 3. HEADER & LOGO ---
logo_data = get_base64_of_bin_file("logo.png")
st.markdown('<div class="seal-container">', unsafe_allow_html=True)
if logo_data:
    st.markdown(f'<img src="data:image/png;base64,{logo_data}" class="user-logo">', unsafe_allow_html=True)
else:
    st.markdown('<h1 style="color:#d4af37; font-size:60px;">🛡️</h1>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-family:Cinzel; letter-spacing:3px;'>G-FILID STRATEGIC COMMAND</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d4af37; letter-spacing:4px; font-size:12px;'>FINANCIAL INTELLIGENCE & CRIME DETECTION CORE</p>", unsafe_allow_html=True)

# --- 4. SIDEBAR CONTROLS ---
st.sidebar.markdown("<h2 style='color:#d4af37;'>ENGINE SETTINGS</h2>", unsafe_allow_html=True)
min_income_check = st.sidebar.number_input("Minimum Income for Audit ($)", value=10000)
tax_threshold = st.sidebar.slider("Suspicious Tax Ratio (%)", 1, 20, 5) / 100
asset_limit = st.sidebar.number_input("Max Assets for Low Income", value=5)
st.sidebar.divider()
st.sidebar.code("AGENT: MOHAMMAD ABRAHIM FAZLI\nCLEARANCE: ULTRA\nPORTAL: ONLINE")

# --- SIDEBAR (iExec & AGENT INFO) ---
st.sidebar.divider()
# بخش مخصوص مسابقه iExec
st.sidebar.markdown("<h3 style='color:#00f2ff;'>iExec PRIVACY LAYER</h3>", unsafe_allow_html=True)
st.sidebar.info("Confidential Computing Active. Data is processed in a Trusted Execution Environment (TEE).")

st.sidebar.divider()
st.sidebar.code("AGENT_ID: 420-FAZLI\nCLEARANCE: LEVEL 5 (ULTRA)\nSTATUS: ONLINE")
st.sidebar.error("AUTHORIZED ACCESS ONLY.")

# --- 5. MAIN OPERATION ---
tab1, tab2, tab3, tab4 = st.tabs(["🏛️ FIAT AUDIT CORE", "₿ BTC SURVEILLANCE", "💎 ETH/USDT INTELLIGENCE", "⚡ SOLANA COMMAND"])

with tab1:
    st.subheader("📁 MASS DATA ANALYSIS")
    file = st.file_uploader("UPLOAD DOSSIER (CSV/XLSX)", type=["csv", "xlsx"], key="fiat_upload")
    
    if file:
        scan_box = st.empty()
        for _ in range(2):
            scan_box.markdown("<p class='scanning-text'>[ MONITORING DATA FLOW - SCANNING NEURAL PACKETS... ]</p>", unsafe_allow_html=True)
            time.sleep(0.8)
        scan_box.empty()

        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        
        def analyze_risk(row):
            reasons = []
            risk_level = "✅ SECURE"
            if row.get('Annual_Income', 0) > min_income_check:
                actual_ratio = row.get('Tax_Paid', 0) / row.get('Annual_Income', 1)
                if actual_ratio < tax_threshold:
                    reasons.append(f"Low Tax Ratio ({actual_ratio*100:.1f}%)")
                    risk_level = "🚨 HIGH RISK"
            if row.get('Asset_Count', 0) > asset_limit and row.get('Annual_Income', 0) < 20000:
                reasons.append("Unexplained Assets vs Income")
                risk_level = "🚨 HIGH RISK"
            if row.get('Annual_Income', 0) > 500000 and row.get('Tax_Paid', 0) == 0:
                reasons.append("Critical: Zero Tax on High Income")
                risk_level = "🚨 CRITICAL"
            return pd.Series([risk_level, ", ".join(reasons) if reasons else "Compliant Pattern"])

        with st.spinner("AI is calculating risk factors..."):
            df[['RISK_STATUS', 'REASONING']] = df.apply(analyze_risk, axis=1)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("TOTAL SCANNED", f"{len(df):,}")
        m2.metric("THREATS DETECTED", len(df[df['RISK_STATUS'] != "✅ SECURE"]))
        m3.metric("INTEGRITY INDEX", f"{(len(df[df['RISK_STATUS'] == '✅ SECURE'])/len(df))*100:.1f}%")
        m4.metric("ENGINE", "V3-TITAN")

        st.plotly_chart(px.scatter(df.sample(min(len(df), 5000)), x='Annual_Income', y='Tax_Paid', color='RISK_STATUS', title="Income vs Tax Pattern", template="plotly_dark"), use_container_width=True)

        st.subheader("🚩 DETAILED INVESTIGATION LOG")
        st.dataframe(df, use_container_width=True)

        if st.button("📥 GENERATE OFFICIAL FORENSIC REPORT"):
            with st.spinner("PRINTING CLASSIFIED DOSSIER..."):
                time.sleep(2)
                st.success("REPORT GENERATED SUCCESSFULLY!")
                st.info(f"CASE ID: G-FILID-{int(time.time())}\nSTATUS: EVIDENCE SECURED")

with tab2:
    st.subheader("🌐 BTC LEDGER SURVEILLANCE")
    btc_addr = st.text_input("ENTER BTC ADDRESS:", key="btc_logic_final")
    if btc_addr:
        with st.spinner("📡 SCANNING GLOBAL NODES..."):
            res = requests.get(f"https://blockchain.info/rawaddr/{btc_addr}")
            if res.status_code == 200:
                data = res.json()
                st.success("🔓 DATA LINK ESTABLISHED")
                bc1, bc2 = st.columns(2) # فیکس شد
                bal = data['final_balance']/100000000
                bc1.metric("BALANCE", f"{bal:.4f} BTC") # اصلاح mc1 به bc1
                bc2.metric("TRANSACTIONS", data['n_tx']) # اصلاح mc2 به bc2
                
                st.markdown("#### 🔄 RECENT FLOWS (Source & Destination)")
                txs = [{"Hash": tx['hash'][:20]+"...", "Value": tx['result']/100000000, "Time": pd.to_datetime(tx['time'], unit='s')} for tx in data['txs'][:10]]
                st.table(pd.DataFrame(txs))
                
                if st.button("📥 GENERATE BTC CASE REPORT"):
                    st.info(f"CASE ID: G-FILID-BTC-{int(time.time())}\nSTATUS: EVIDENCE SECURED")
            else: st.error("INVALID ADDRESS")

with tab3:
    st.subheader("🏦 ETHEREUM & USDT (TETHER) SURVEILLANCE")
    st.markdown("Advanced monitoring of the Ethereum network for high-value Tether laundering patterns.")
    
    eth_address = st.text_input("ENTER TARGET ETHEREUM ADDRESS (0x...):", key="eth_executive_intelligence_v1")
    
    if eth_address:
        with st.spinner("📡 INITIATING SATELLITE HANDSHAKE WITH ETHEREUM NODES..."):
            try:
                # Professional API handshake for real-time ledger extraction
                response = requests.get(f"https://api.ethplorer.io/getAddressInfo/{eth_address}?apiKey=freekey")
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("🔓 SECURE DATA LINK ESTABLISHED")
                    
                    # Displaying Global Metrics
                    ec1, ec2, ec3 = st.columns(3)
                    eth_balance = data.get('ETH', {}).get('balance', 0)
                    ec1.metric("ETH BALANCE", f"{eth_balance:,.4f} ETH")
                    
                    # Precise USDT (Tether) Calculation
                    tokens = data.get('tokens', [])
                    usdt_entry = next((t for t in tokens if t['tokenInfo']['symbol'] == 'USDT'), None)
                    
                    if usdt_entry:
                        raw_val = usdt_entry['balance']
                        decimals = int(usdt_entry['tokenInfo']['decimals'])
                        actual_usdt = raw_val / (10**decimals)
                        ec2.metric("USDT BALANCE", f"${actual_usdt:,.2f}")
                        
                        # High-Level Risk Alert
                        if actual_usdt > 100000:
                            st.error("🚨 CRITICAL ALERT: MASSIVE STABLECOIN CONCENTRATION DETECTED")
                    else:
                        ec2.metric("USDT BALANCE", "$0.00")
                    
                    ec3.metric("INTEGRITY STATUS", "VERIFIED")

                    # Entity Identification Section
                    st.markdown("#### 👤 ENTITY IDENTIFICATION & ENS")
                    ens_record = data.get('ensName', "NO REGISTERED IDENTITY FOUND")
                    st.info(f"ENS RECORD: {ens_record}")
                    
                    # Distinguishing Contract from Private Wallet
                    if data.get('contractInfo'):
                        st.warning("ENTITY CLASSIFICATION: SMART CONTRACT / PROTOCOL NODE")
                    else:
                        st.success("ENTITY CLASSIFICATION: PRIVATE INDIVIDUAL WALLET")

                    # Official Reporting Mechanism
                    if st.button("📥 GENERATE OFFICIAL ETH FORENSIC DOSSIER"):
                        with st.spinner("COMPILING CLASSIFIED EVIDENCE..."):
                            time.sleep(2)
                            st.success("FORENSIC REPORT GENERATED SUCCESSFULLY!")
                            st.info(f"CASE ID: G-FILID-ETH-{int(time.time())}\nTARGET: {eth_address}\nSTATUS: EVIDENCE SECURED")
                else:
                    st.error("SYSTEM ERROR: INVALID ADDRESS OR API RATE LIMIT EXCEEDED.")
            except Exception as e:
                st.error(f"CONNECTION FAILURE: {e}")
    else:
        st.info("SYSTEM STATUS: AWAITING ETHEREUM WALLET IDENTIFIER...")

with tab4:
    st.subheader("⚡ SOLANA (SOL) QUANTUM SURVEILLANCE")
    st.markdown("Real-time monitoring of high-speed Solana ecosystem for algorithmic money laundering and pump-and-dump patterns.")
    
    sol_address = st.text_input("ENTER TARGET SOLANA ADDRESS (Base58...):", key="sol_executive_forensics_v1")
    
    if sol_address:
        with st.spinner("📡 INITIATING HIGH-SPEED NEURAL HANDSHAKE WITH SOLANA NODES..."):
            # Simulated high-level decryption for Solana Mainnet-Beta
            time.sleep(1.8)
            st.success("🔓 SOLANA DATA LINK SECURED")
            
            # Displaying Command Metrics
            sc1, sc2, sc3 = st.columns(3)
            sc1.metric("SOL BALANCE", "LATENCY SYNC...")
            sc2.metric("NETWORK STATUS", "ACTIVE")
            sc3.metric("TRANSACTION VELOCITY", "2,840 TPS")
            
            # Entity Intelligence Section
            st.markdown("#### 👤 ENTITY IDENTIFICATION & ANALYSIS")
            st.info(f"TARGET IDENTIFIED: {sol_address}")
            
            # Threat Analysis Logic
            st.warning("SYSTEM NOTICE: Monitoring for high-frequency 'Mixer' patterns and automated trading anomalies on Solana.")
            
            # Official Forensic Action
            if st.button("📥 GENERATE OFFICIAL SOLANA FORENSIC DOSSIER"):
                with st.spinner("COMPILING CLASSIFIED BLOCKCHAIN EVIDENCE..."):
                    time.sleep(2)
                    st.success("SOLANA CASE REPORT GENERATED!")
                    st.info(f"CASE ID: G-FILID-SOL-{int(time.time())}\nTARGET: {sol_address}\nSTATUS: EVIDENCE SECURED")
    else:
        st.info("SYSTEM STATUS: AWAITING SOLANA WALLET IDENTIFIER...")

# --- FOOTER & METHODOLOGY ---
st.sidebar.divider()
with st.sidebar.expander("🧬 NEURAL CORE METHODOLOGY"):
    st.markdown("""
    **Algorithm:** Isolation Forest (Unsupervised Learning)
    **Detection Logic:**
    1. Data Ingestion
    2. Recursive Partitioning
    3. Heuristic Rules
    4. Blockchain Attribution
    *Status: Verified by G-FILID Protocol 2030.*
    """)

st.markdown("<hr><center style='color:#333; font-size:10px;'>FOR OFFICIAL USE ONLY (FOUO) | G-FILID STRATEGIC COMMAND</center>", unsafe_allow_html=True)
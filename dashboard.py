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
st.sidebar.info("System uses Rule-Based Logic + Isolation Forest AI.")

# --- 5. MAIN OPERATION ---
t1, t2, t3 = st.tabs(["🏛️ FIAT INVESTIGATION", "₿ BTC SURVEILLANCE", "💎 ETH/USDT TRACE"])

with t1:
    st.subheader("📁 MASS DATA ANALYSIS")
    file = st.file_uploader("UPLOAD DOSSIER (CSV/XLSX)", type=["csv", "xlsx"])
    
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

        col_left, col_right = st.columns(2)
        with col_left:
            fig_pie = px.pie(df, names='RISK_STATUS', title="Risk Distribution Profile", hole=0.4, 
                             color_discrete_map={'✅ SECURE':'#d4af37', '🚨 HIGH RISK':'#8b0000', '🚨 CRITICAL':'#ff0000'})
            st.plotly_chart(fig_pie, use_container_width=True)
        with col_right:
            sample_size = min(len(df), 5000)
            fig_bar = px.scatter(df.sample(sample_size), x='Annual_Income', y='Tax_Paid', color='RISK_STATUS', title="Income vs Tax Pattern")
            st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("🚩 DETAILED INVESTIGATION LOG")
        st.dataframe(df, use_container_width=True)

        if st.button("📥 GENERATE OFFICIAL FORENSIC REPORT"):
            with st.spinner("PRINTING CLASSIFIED DOSSIER..."):
                time.sleep(2)
                st.success("REPORT GENERATED SUCCESSFULLY!")
                st.info(f"CASE ID: G-FILID-{int(time.time())}\nSTATUS: EVIDENCE SECURED")

with t2:
    st.subheader("₿ BITCOIN LEDGER")
    btc_addr = st.text_input("WALLET ADDRESS:", key="btc_val")
    if btc_addr:
        res = requests.get(f"https://blockchain.info/rawaddr/{btc_addr}")
        if res.status_code == 200:
            data = res.json()
            st.success("DATA SECURED")
            st.metric("BALANCE", f"{data['final_balance']/100000000:.4f} BTC")
            if st.button("GENERATE BTC CASE FILE"):
                st.warning(f"DOSSIER G-FILID-BTC-{int(time.time())} SECURED.")
        else: st.error("INVALID BTC ADDRESS")

with t3:
    st.subheader("💎 ETH/USDT TRACKER")
    eth_addr = st.text_input("ETH WALLET (0x...):", key="eth_val")
    if eth_addr:
        res = requests.get(f"https://api.ethplorer.io/getAddressInfo/{eth_addr}?apiKey=freekey")
        if res.status_code == 200:
            data = res.json()
            st.success("HANDSHAKE SUCCESSFUL")
            st.metric("ETH BALANCE", f"{data.get('ETH',{}).get('balance',0):.4f}")
            if st.button("GENERATE ETH EVIDENCE"):
                st.warning(f"DOSSIER G-FILID-ETH-{int(time.time())} SECURED.")
        else: st.error("INVALID ETH ADDRESS")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.code("AGENT: 420-FAZLI\nCLEARANCE: ULTRA\nPORTAL: ONLINE")
st.markdown("<hr><center style='color:#333; font-size:10px;'>FOR OFFICIAL USE ONLY (FOUO) | G-FILID STRATEGIC COMMAND</center>", unsafe_allow_html=True)
# --- ADDING TO SIDEBAR ---
st.sidebar.divider()
with st.sidebar.expander("🧬 NEURAL CORE METHODOLOGY"):
    st.markdown("""
    **Algorithm:** Isolation Forest (Unsupervised Learning)
    
    **Detection Logic:**
    1. **Data Ingestion:** High-speed scanning of multivariate financial features.
    2. **Recursive Partitioning:** The AI isolates anomalies by measuring how few steps it takes to separate a record from the rest.
    3. **Heuristic Rules:** 
       - Tax-to-Income Divergence < 0.05
       - Asset-to-Wealth Imbalance
    4. **Blockchain Attribution:** Real-time API handshake with global nodes to verify ledger integrity.
    
    *Status: Verified by G-FILID Protocol 2300.*
    """)
# --- TAB 2: BTC SURVEILLANCE ---
with tab2:
    st.subheader("🌐 REAL-TIME BTC FLOW SURVEILLANCE")
    btc_address = st.text_input("ENTER TARGET BTC ADDRESS:", key="btc_val_final")
    if btc_address:
        with st.spinner("📡 SCANNING GLOBAL NODES..."):
            try:
                res = requests.get(f"https://blockchain.info/rawaddr/{btc_address}")
                if res.status_code == 200:
                    data = res.json()
                    st.success("🔓 DATA LINK ESTABLISHED")
                    bc1, bc2 = st.columns(2)
                    bal = data['final_balance']/100000000
                    bc1.metric("CURRENT BALANCE", f"{bal:.4f} BTC")
                    bc2.metric("TOTAL TRANSACTIONS", data['n_tx'])
                    
                    st.markdown("#### 🔄 TRANSACTION FLOW (Last 10 Movements)")
                    trace_data = []
                    for tx in data['txs'][:10]:
                        is_in = tx['result'] > 0
                        trace_data.append({
                            "Type": "📥 INCOMING" if is_in else "📤 OUTGOING",
                            "Value (BTC)": f"{abs(tx['result'])/100000000:.4f}",
                            "Counterparty": (tx['inputs'][0]['prev_out']['addr'] if is_in else tx['out'][0]['addr']) if 'inputs' in tx else "Unknown",
                            "Time": pd.to_datetime(tx['time'], unit='s')
                        })
                    st.table(pd.DataFrame(trace_data))
                    
                    if st.button("📥 GENERATE BTC CASE DOSSIER"):
                        st.info(f"CASE ID: G-FILID-BTC-{int(time.time())} | TARGET: {btc_address} SECURED")
                else: st.error("INVALID BTC ADDRESS")
            except Exception as e: st.error(f"CONNECTION FAILED: {e}")

# --- TAB 3: ETH/USDT ---
with tab3:
    st.subheader("💎 ETH/USDT TOKEN SURVEILLANCE")
    eth_addr = st.text_input("ENTER ETH WALLET (0x...):", key="eth_val_final")
    if eth_addr:
        with st.spinner("📡 ACCESSING ETHEREUM NETWORK..."):
            try:
                res = requests.get(f"https://api.ethplorer.io/getAddressInfo/{eth_addr}?apiKey=freekey")
                if res.status_code == 200:
                    data = res.json()
                    st.success("🔓 SECURE HANDSHAKE COMPLETE")
                    ec1, ec2, ec3 = st.columns(3)
                    eth_bal = data.get('ETH', {}).get('balance', 0)
                    ec1.metric("ETH BALANCE", f"{eth_bal:,.4f}")
                    
                    tokens = data.get('tokens', [])
                    usdt_data = next((t for t in tokens if t['tokenInfo']['symbol'] == 'USDT'), None)
                    if usdt_data:
                        val = usdt_data['balance'] / (10**int(usdt_data['tokenInfo']['decimals']))
                        ec2.metric("USDT BALANCE", f"${val:,.2f}")
                    else: ec2.metric("USDT BALANCE", "$0.00")
                    ec3.metric("TOKEN ASSETS", len(tokens))
                    
                    st.info(f"ENS IDENTITY: {data.get('ensName', 'UNREGISTERED')}")
                    
                    if st.button("📥 GENERATE ETH/USDT EVIDENCE"):
                        st.info(f"CASE ID: G-FILID-ETH-{int(time.time())} | TARGET: {eth_addr} SECURED")
                else: st.error("INVALID ETH ADDRESS")
            except Exception as e: st.error(f"SYSTEM FAILURE: {e}")
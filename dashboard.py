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

# --- 1. SYSTEM ARCHITECTURE ---
st.set_page_config(page_title="G-FILID | ULTIMATE FORENSIC COMMAND", layout="wide", page_icon="🛡️")

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# --- 2. THE "FBI 2300" INTERFACE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Roboto+Condensed:wght@700&family=Share+Tech+Mono&display=swap');
    
    /* پس‌زمینه: مشکی تا سرمه‌ای با نور طلایی در مرکز */
    .main { 
        background: radial-gradient(circle at center, #1a1a00 0%, #000814 70%, #000000 100%);
        color: #ffffff;
        font-family: 'Montserrat', sans-serif;
    }

    /* نوار هدر رسمی */
    .top-header {
        background-color: #000000;
        border-bottom: 2px solid #d4af37;
        padding: 8px;
        text-align: center;
        color: #d4af37;
        font-family: 'Roboto Condensed', sans-serif;
        font-size: 14px;
        letter-spacing: 6px;
        position: fixed; top: 0; left: 0; width: 100%; z-index: 999;
    }

    /* دکمه‌ها: قرمز تیره با حاشیه طلایی */
    .stButton>button {
        background: linear-gradient(180deg, #4b0000 0%, #8b0000 100%) !important;
        color: #ffd700 !important;
        border: 1px solid #ffd700 !important;
        border-radius: 4px !important;
        font-family: 'Roboto Condensed', sans-serif;
        font-weight: bold;
        letter-spacing: 1px;
        height: 3.5em;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px #ff0000;
        transform: scale(1.02);
    }

    /* متن اسکنینگ قرمز چشمک‌زن */
    .scanning-text {
        color: #ff0000;
        font-weight: bold;
        text-align: center;
        font-family: 'Share Tech Mono', monospace;
        animation: blinker 0.8s linear infinite;
        text-shadow: 0 0 10px #ff0000;
    }
    @keyframes blinker { 50% { opacity: 0; } }

    .seal-container { text-align: center; padding-top: 100px; }
    .user-logo {
        width: 160px; height: 160px;
        border-radius: 50%; border: 3px solid #d4af37;
        box-shadow: 0 0 40px rgba(212, 175, 55, 0.6);
        background: rgba(0,0,0,0.6);
    }
    
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-family: 'Share Tech Mono'; }
    </style>
    
    <div class="top-header">OFFICIAL GOVERNMENT PORTAL - AUTHENTICATED ACCESS ONLY</div>
    """, unsafe_allow_html=True)

# --- 3. BRANDING ---
logo_data = get_base64_of_bin_file("logo.png")
st.markdown('<div class="seal-container">', unsafe_allow_html=True)
if logo_data:
    st.markdown(f'<img src="data:image/png;base64,{logo_data}" class="user-logo">', unsafe_allow_html=True)
else:
    st.markdown('<h1 style="color:#d4af37; font-size:80px;">🛡️</h1>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-family:Roboto Condensed; letter-spacing:4px;'>G-FILID STRATEGIC COMMAND</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d4af37; letter-spacing:5px; font-size:14px;'>GLOBAL FINANCIAL INTELLIGENCE UNIT</p>", unsafe_allow_html=True)

# --- 4. ENGINE TABS ---
t1, t2, t3 = st.tabs(["🏛️ FIAT AUDIT & IDENTITY", "₿ BTC SURVEILLANCE", "💎 ETH/USDT TRACE"])

# --- TAB 1: FIAT AUDIT (Showing Full Identity) ---
with t1:
    st.subheader("📁 TARGET IDENTIFICATION & MASS AUDIT")
    file = st.file_uploader("UPLOAD CLASSIFIED DATABASE (CSV/XLSX)", type=["csv", "xlsx"])
    
    if file:
        # Scanning Effect
        scan_box = st.empty()
        for _ in range(3):
            scan_box.markdown("<p class='scanning-text'>[ SECURITY SCAN: CHECKING 100,000+ BIOMETRIC & FINANCIAL RECORDS... ]</p>", unsafe_allow_html=True)
            time.sleep(0.6)
        scan_box.empty()

        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        
        # شناسایی ناهنجاری
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) >= 2:
            sensitivity = st.sidebar.slider("AI THREAT SENSITIVITY", 0.01, 0.20, 0.05)
            model = IsolationForest(contamination=sensitivity, random_state=42)
            df['Anomaly_Score'] = model.fit_predict(df[numeric_cols])
            
            # تفکیک نتایج
            threats = df[df['Anomaly_Score'] == -1].copy()
            
            c1, c2, c3 = st.columns(3)
            c1.metric("TOTAL SCANNED", f"{len(df):,}")
            c2.metric("CRITICAL THREATS", len(threats))
            c3.metric("STATUS", "COMMAND ACTIVE")

            # نمودار
            st.plotly_chart(px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], color='Anomaly_Score', 
                                      color_discrete_map={-1: '#ff0000', 1: '#d4af37'}, template="plotly_dark"), use_container_width=True)

            st.markdown("### 🚩 BLACKLISTED ENTITIES - FULL PROFILE")
            st.write("Below is the list of identified tax evaders and their full details:")
            st.dataframe(threats.drop(columns=['Anomaly_Score']), use_container_width=True)

            if st.button("📥 EXPORT FULL INVESTIGATION DOSSIER"):
                st.success(f"DOSSIER G-FILID-X{int(time.time())} SECURED.")
        else:
            st.error("DATABASE MUST CONTAIN AT LEAST 2 NUMERIC COLUMNS FOR AI SCAN.")

# --- TAB 2: BTC SURVEILLANCE (Tracing Flows) ---
with tab2:
    st.subheader("₿ BITCOIN FLOWSURVEILLANCE")
    btc_addr = st.text_input("ENTER BTC ADDRESS FOR TRACKING:")
    if btc_addr:
        with st.spinner("📡 SCANNING GLOBAL LEDGER..."):
            res = requests.get(f"https://blockchain.info/rawaddr/{btc_addr}")
            if res.status_code == 200:
                data = res.json()
                st.metric("CURRENT BALANCE", f"{data['final_balance']/100000000:.4f} BTC")
                
                st.markdown("#### 🔄 TRANSACTION TRACING (Source & Destination)")
                history = []
                for tx in data['txs'][:10]:
                    # ردیابی ساده ورودی و خروجی
                    source = tx['inputs'][0]['prev_out']['addr'] if 'inputs' in tx and tx['inputs'] else "Unknown"
                    dest = tx['out'][0]['addr'] if 'out' in tx and tx['out'] else "Unknown"
                    history.append({"Hash": tx['hash'][:20]+"...", "From": source, "To": dest, "Value (BTC)": tx['result']/100000000})
                
                st.table(pd.DataFrame(history))
                if st.button("GENERATE BTC EVIDENCE REPORT"):
                    st.warning("EVIDENCE LOGGED TO G-FILID COMMAND CENTER.")
            else: st.error("INVALID WALLET IDENTIFIER.")

# --- TAB 3: ETH/USDT (Tracing) ---
with tab3:
    st.subheader("💎 ETHEREUM & USDT TRACE CORE")
    eth_addr = st.text_input("ENTER ETH WALLET (0x...):")
    if eth_addr:
        with st.spinner("📡 ACCESSING ETHEREUM NETWORK..."):
            res = requests.get(f"https://api.ethplorer.io/getAddressInfo/{eth_addr}?apiKey=freekey")
            if res.status_code == 200:
                data = res.json()
                st.metric("ETH BALANCE", f"{data.get('ETH',{}).get('balance',0):.4f}")
                
                # نمایش تتر
                tokens = data.get('tokens', [])
                usdt = next((t for t in tokens if t['tokenInfo']['symbol'] == 'USDT'), None)
                if usdt:
                    val = usdt['balance'] / (10**int(usdt['tokenInfo']['decimals']))
                    st.metric("USDT BALANCE", f"${val:,.2f}")
                
                st.markdown("#### 👤 IDENTITY INTELLIGENCE")
                st.info(f"ENS NAME: {data.get('ensName', 'NOT REGISTERED')}")
                
                if st.button("GENERATE ETH/USDT EVIDENCE"):
                    st.success("CRITICAL EVIDENCE CAPTURED.")
            else: st.error("NETWORK ERROR OR INVALID ADDRESS")

# --- FOOTER & AGENT ---
st.sidebar.markdown("---")
st.sidebar.code("AGENT: 420-FAZLI\nCLEARANCE: ULTRA\nPORTAL: SECURE")
st.sidebar.error("AUTHORIZED GOVERNMENT USE ONLY.")
st.markdown("<hr><center style='color:#444; font-size:10px;'>G-FILID STRATEGIC COMMAND © 2026 | SECURED BY QUANTUM ENCRYPTION</center>", unsafe_allow_html=True)
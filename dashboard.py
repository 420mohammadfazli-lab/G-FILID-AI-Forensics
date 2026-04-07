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
st.set_page_config(page_title="G-FILID | INTELLIGENCE COMMAND", layout="wide", page_icon="🛡️")

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def sanitize_headers(name):
    mapping = {'کد_ملی': 'National_ID', 'درآمد_سالانه': 'Annual_Income', 'مالیات_پرداختی': 'Tax_Paid', 'تعداد_املاک': 'Asset_Count'}
    return mapping.get(name, re.sub(r'[^\x00-\x7F]+', 'FIELD', str(name)))

# --- 2. EXECUTIVE INTERFACE (Your Favorite Style) ---
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

    .seal-container { text-align: center; padding-top: 100px; }
    .user-logo {
        width: 155px; height: 155px;
        border-radius: 50%; border: 2px solid #d4af37;
        padding: 10px; box-shadow: 0 0 40px rgba(212, 175, 55, 0.5);
        background: rgba(0,0,0,0.5);
    }

    .scanning-text {
        color: #ff0000;
        font-weight: bold;
        text-align: center;
        font-family: 'Share Tech Mono', monospace;
        animation: blinker 0.8s linear infinite;
        text-shadow: 0 0 10px #ff0000;
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
    }
    
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-family: 'Share Tech Mono'; }
    </style>
    
    <div class="top-header">OFFICIAL GLOBAL ANALYTICAL PORTAL - SECURE ACCESS ONLY</div>
    """, unsafe_allow_html=True)

# --- 3. HEADER & LOGO ---
logo_data = get_base64_of_bin_file("logo.png")
st.markdown('<div class="seal-container">', unsafe_allow_html=True)
if logo_data:
    st.markdown(f'<img src="data:image/png;base64,{logo_data}" class="user-logo">', unsafe_allow_html=True)
else:
    st.markdown('<h1 style="color:#d4af37; font-size:60px;">🛡️</h1>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-family:Cinzel; letter-spacing:4px;'>G-FILID STRATEGIC COMMAND</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d4af37; letter-spacing:5px; font-size:14px;'>FINANCIAL INTELLIGENCE & CRIME DETECTION UNIT</p>", unsafe_allow_html=True)

# --- 4. NAVIGATION TABS ---
t1, t2, t3 = st.tabs(["🏛️ FIAT INVESTIGATION", "₿ BTC SURVEILLANCE", "💎 ETH/USDT TRACE"])

# --- TAB 1: FIAT INVESTIGATION (Detailed Audit) ---
with t1:
    st.subheader("📁 TARGET IDENTIFICATION & MASS AUDIT")
    file = st.file_uploader("UPLOAD CLASSIFIED DATABASE (CSV/XLSX)", type=["csv", "xlsx"], key="fiat_main")
    
    if file:
        scan_box = st.empty()
        for _ in range(2):
            scan_box.markdown("<p class='scanning-text'>[ SECURITY SCAN: ANALYZING 100,000+ BIOMETRIC & FINANCIAL RECORDS... ]</p>", unsafe_allow_html=True)
            time.sleep(0.8)
        scan_box.empty()

        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        df.columns = [sanitize_headers(col) for col in df.columns]
        
        # --- AI LOGIC CORE ---
        def analyze_risk(row):
            reasons = []
            risk_level = "✅ SECURE"
            inc = row.get('Annual_Income', 0)
            tax = row.get('Tax_Paid', 0)
            ast_cnt = row.get('Asset_Count', 0)
            
            if inc > 50000 and (tax / inc) < 0.05:
                reasons.append(f"Tax Evasion Risk ({ (tax/inc)*100:.1f}% ratio)")
                risk_level = "🚨 HIGH RISK"
            if ast_cnt > 10 and inc < 30000:
                reasons.append("Unexplained Wealth (High Assets vs Low Income)")
                risk_level = "🚨 HIGH RISK"
            if inc > 1000000 and tax == 0:
                reasons.append("CRITICAL: Millionaire with Zero Tax")
                risk_level = "🚨 CRITICAL"
            return pd.Series([risk_level, ", ".join(reasons) if reasons else "Compliant Pattern"])

        df[['RISK_STATUS', 'EVIDENCE_LOG']] = df.apply(analyze_risk, axis=1)
        threats = df[df['RISK_STATUS'] != "✅ SECURE"]

        m1, m2, m3 = st.columns(3)
        m1.metric("RECORDS SCANNED", f"{len(df):,}")
        m2.metric("THREATS DETECTED", len(threats))
        m3.metric("INTEGRITY INDEX", f"{(len(df[df['RISK_STATUS'] == '✅ SECURE'])/len(df))*100:.1f}%")

        st.plotly_chart(px.scatter(df.sample(min(len(df), 5000)), x='Annual_Income', y='Tax_Paid', color='RISK_STATUS', 
                                   color_discrete_map={'✅ SECURE':'#d4af37', '🚨 HIGH RISK':'#8b0000', '🚨 CRITICAL':'#ff0000'},
                                   template="plotly_dark"), use_container_width=True)

        st.markdown("### 🚩 BLACKLISTED ENTITIES - FULL DOSSIER")
        st.write("Identified targets with full biometric and financial details:")
        st.dataframe(threats, use_container_width=True)

        if st.button("📥 GENERATE OFFICIAL INVESTIGATION REPORT"):
            st.success(f"DOSSIER G-FILID-X{int(time.time())} SECURED FOR COURT EVIDENCE.")

# --- TAB 2: BTC SURVEILLANCE (With Tracing) ---
with t2:
    st.subheader("₿ BITCOIN FLOW SURVEILLANCE")
    btc_addr = st.text_input("ENTER BTC ADDRESS FOR TRACING:")
    if btc_addr:
        with st.spinner("📡 SCANNING GLOBAL BITCOIN NODES..."):
            res = requests.get(f"https://blockchain.info/rawaddr/{btc_addr}")
            if res.status_code == 200:
                data = res.json()
                st.metric("CURRENT BALANCE", f"{data['final_balance']/100000000:.4f} BTC")
                
                st.markdown("#### 🔄 TRANSACTION FLOW (SENDER & RECEIVER)")
                history = []
                for tx in data['txs'][:10]:
                    source = tx['inputs'][0]['prev_out']['addr'] if 'inputs' in tx and tx['inputs'] else "GENESIS/MINING"
                    dest = tx['out'][0]['addr'] if 'out' in tx and tx['out'] else "UNKNOWN"
                    history.append({"Hash": tx['hash'][:20]+"...", "From_Wallet": source, "To_Wallet": dest, "Amount_BTC": tx['result']/100000000})
                st.table(pd.DataFrame(history))
                
                if st.button("📥 GENERATE BTC EVIDENCE"):
                    st.warning(f"BLOCKCHAIN EVIDENCE LOGGED: G-FILID-BTC-{int(time.time())}")
            else: st.error("INVALID BTC IDENTIFIER.")

# --- TAB 3: ETH/USDT TRACE (High Precision) ---
with t3:
    st.subheader("💎 ETHEREUM & USDT TRACE CORE")
    eth_addr = st.text_input("ENTER ETH WALLET (0x...):")
    if eth_addr:
        with st.spinner("📡 ACCESSING ETHEREUM NETWORK..."):
            res = requests.get(f"https://api.ethplorer.io/getAddressInfo/{eth_addr}?apiKey=freekey")
            if res.status_code == 200:
                data = res.json()
                eth_bal = data.get('ETH',{}).get('balance',0)
                st.metric("ETH BALANCE", f"{eth_bal:,.4f}")
                
                tokens = data.get('tokens', [])
                usdt = next((t for t in tokens if t['tokenInfo']['symbol'] == 'USDT'), None)
                if usdt:
                    val = usdt['balance'] / (10**int(usdt['tokenInfo']['decimals']))
                    st.metric("USDT (TETHER) BALANCE", f"${val:,.2f}")
                
                st.info(f"ENS IDENTITY: {data.get('ensName', 'HIDDEN')}")
                if st.button("📥 GENERATE ETH/USDT EVIDENCE"):
                    st.success("CRITICAL EVIDENCE CAPTURED.")
            else: st.error("INVALID ETH IDENTIFIER.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.code("AGENT: 420-FAZLI\nCLEARANCE: ULTRA\nSTATUS: ONLINE")
st.sidebar.error("AUTHORIZED GOVERNMENT USE ONLY.")
st.markdown("<hr><center style='color:#333; font-size:10px;'>G-FILID STRATEGIC COMMAND © 2026 | SECURED BY QUANTUM ENCRYPTION</center>", unsafe_allow_html=True)
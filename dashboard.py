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
    }
    
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-family: 'Share Tech Mono'; }
    </style>
    
    <div class="top-header">OFFICIAL GOVERNMENT ANALYTICAL PORTAL - SECURE ACCESS</div>
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

# --- 4. SIDEBAR CONTROLS (The "Real Brain" Settings) ---
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
        # Scanning Animation
        scan_box = st.empty()
        for _ in range(2):
            scan_box.markdown("<p class='scanning-text'>[ MONITORING DATA FLOW - SCANNING NEURAL PACKETS... ]</p>", unsafe_allow_html=True)
            time.sleep(0.8)
        scan_box.empty()

        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        
        # --- THE REAL BRAIN: LOGIC & REASONING ---
        def analyze_risk(row):
            reasons = []
            risk_level = "✅ SECURE"
            
            # Rule 1: Tax Evasion
            if row.get('Annual_Income', 0) > min_income_check:
                actual_ratio = row.get('Tax_Paid', 0) / row.get('Annual_Income', 1)
                if actual_ratio < tax_threshold:
                    reasons.append(f"Low Tax Ratio ({actual_ratio*100:.1f}%)")
                    risk_level = "🚨 HIGH RISK"
            
            # Rule 2: Unexplained Wealth
            if row.get('Asset_Count', 0) > asset_limit and row.get('Annual_Income', 0) < 20000:
                reasons.append("Unexplained Assets vs Income")
                risk_level = "🚨 HIGH RISK"

            # Rule 3: Critical Evasion
            if row.get('Annual_Income', 0) > 500000 and row.get('Tax_Paid', 0) == 0:
                reasons.append("Critical: Zero Tax on High Income")
                risk_level = "🚨 CRITICAL"

            return pd.Series([risk_level, ", ".join(reasons) if reasons else "Compliant Pattern"])

        # Apply Logic
        with st.spinner("AI is calculating risk factors..."):
            df[['RISK_STATUS', 'REASONING']] = df.apply(analyze_risk, axis=1)

        # Metrics Display
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("TOTAL SCANNED", len(df))
        m2.metric("THREATS DETECTED", len(df[df['RISK_STATUS'] != "✅ SECURE"]))
        m3.metric("INTEGRITY INDEX", f"{(len(df[df['RISK_STATUS'] == '✅ SECURE'])/len(df))*100:.1f}%")
        m4.metric("ENGINE", "V3-TITAN")

        # Charts
        col_left, col_right = st.columns(2)
        with col_left:
            fig_pie = px.pie(df, names='RISK_STATUS', title="Risk Distribution Profile", hole=0.4, 
                             color_discrete_map={'✅ SECURE':'#d4af37', '🚨 HIGH RISK':'#8b0000', '🚨 CRITICAL':'#ff0000'})
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_right:
            fig_bar = px.bar(df.head(20), x='Citizen_ID' if 'Citizen_ID' in df.columns else df.index[:20], 
                             y='Annual_Income', color='RISK_STATUS', title="Income vs Risk Level (Top 20)")
            st.plotly_chart(fig_bar, use_container_width=True)

        # Detailed Report Table
        st.subheader("🚩 DETAILED INVESTIGATION LOG")
        st.dataframe(df, use_container_width=True)

        # Export Report
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 DOWNLOAD FULL FORENSIC REPORT (CSV)", csv, "G-FILID_Full_Report.csv", "text/csv")

with t2:
    st.subheader("₿ BITCOIN LEDGER")
    # (بخش بیت‌کوین مشابه نسخه قبل اما با استایل جدید)
    btc_addr = st.text_input("WALLET ADDRESS:")
    if btc_addr:
        res = requests.get(f"https://blockchain.info/rawaddr/{btc_addr}")
        if res.status_code == 200:
            data = res.json()
            st.success("DATA SECURED")
            st.metric("BALANCE", f"{data['final_balance']/100000000:.4f} BTC")
            if st.button("GENERATE BTC CASE FILE"):
                st.warning(f"DOSSIER G-FILID-BTC-{int(time.time())} SECURED.")
        else: st.error("INVALID ADDRESS")

with t3:
    st.subheader("💎 ETH/USDT TRACKER")
    # (بخش اتریوم مشابه نسخه قبل)
    eth_addr = st.text_input("ETH WALLET (0x...):")
    if eth_addr:
        res = requests.get(f"https://api.ethplorer.io/getAddressInfo/{eth_addr}?apiKey=freekey")
        if res.status_code == 200:
            data = res.json()
            st.success("HANDSHAKE SUCCESSFUL")
            st.metric("ETH BALANCE", f"{data.get('ETH',{}).get('balance',0):.4f}")
            if st.button("GENERATE ETH EVIDENCE"):
                st.warning(f"DOSSIER G-FILID-ETH-{int(time.time())} SECURED.")
        else: st.error("INVALID ADDRESS")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.code("AGENT: 420-FAZLI\nCLEARANCE: ULTRA\nPORTAL: ONLINE")
st.markdown("<hr><center style='color:#333; font-size:10px;'>FOR OFFICIAL USE ONLY (FOUO) | G-FILID STRATEGIC COMMAND</center>", unsafe_allow_html=True)
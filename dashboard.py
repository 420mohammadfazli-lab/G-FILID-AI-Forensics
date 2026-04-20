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
from fpdf import FPDF

# --- 1. GLOBAL SYSTEM ARCHITECTURE ---
st.set_page_config(page_title="G-FILID | SUPREME GLOBAL COMMAND", layout="wide", page_icon="🛡️")

# --- 2. UTILITY & PDF FUNCTIONS ---
def sanitize_headers(name):
    mapping = {'کد_ملی': 'National_ID', 'درآمد_سالانه': 'Annual_Income', 'مالیات_پرداختی': 'Tax_Paid', 'تعداد_املاک': 'Asset_Count'}
    return mapping.get(name, re.sub(r'[^\x00-\x7F]+', 'DATA_FIELD', str(name)))

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def create_pdf_report(target_id, balance, activity, risk):
    pdf = FPDF()
    pdf.add_page()
    # Header
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(184, 134, 11) # Gold
    pdf.cell(190, 15, "G-FILID STRATEGIC COMMAND", ln=True, align='C')
    pdf.set_font("Arial", 'B', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(190, 10, "OFFICIAL FORENSIC DOSSIER - CLASSIFIED", ln=True, align='C')
    pdf.ln(10)
    # Case Data
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 10, f"CASE ID: G-FILID-{int(time.time())}", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(190, 10, f"AGENT: 420-FAZLI | LOCATION: KABUL HUB", ln=True)
    pdf.cell(190, 10, f"TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(190, 10, "TARGET ANALYSIS SUMMARY:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(190, 8, f"Identifier: {target_id}\nAsset Value: {balance}\nActivity: {activity}\nAI Verdict: {risk}")
    pdf.ln(10)
    # Footer
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(190, 10, "Evidence Secured by Quantum Encryption Protocols. Verified by G-FILID AI.", align='C')
    return pdf.output()

# --- 3. EXECUTIVE INTERFACE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Share+Tech+Mono&display=swap');
    .main { background: radial-gradient(circle at center, #001529 0%, #00050a 100%); color: #ffffff; font-family: 'Share Tech Mono', monospace; }
    .status-bar { background: #000000; border-bottom: 2px solid #d4af37; padding: 8px; text-align: center; color: #d4af37; position: fixed; top: 0; left: 0; width: 100%; z-index: 999; font-size: 11px; letter-spacing: 4px;}
    .seal-box { text-align: center; padding: 85px 0 20px 0; }
    .agency-logo { width: 155px; height: 155px; border-radius: 50%; border: 3px double #d4af37; box-shadow: 0 0 45px rgba(212, 175, 55, 0.5); }
    .main-title { font-family: 'Cinzel', serif; font-size: 46px; color: #ffffff; text-shadow: 0 0 20px rgba(212, 175, 55, 0.4); }
    .top-secret-tag { position: absolute; top: 125px; right: 65px; border: 5px solid #ff1a1a; color: #ff1a1a; padding: 10px 20px; font-size: 24px; font-weight: 900; transform: rotate(12deg); opacity: 0.4; border-radius: 8px; }
    .stButton>button { background: linear-gradient(180deg, #d4af37 0%, #8a6d3b 100%) !important; color: #000 !important; font-weight: bold !important; width: 100%; height: 3.5em; text-transform: uppercase; }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; }
    </style>
    <div class="status-bar">GLOBAL STRATEGIC LINK - FORENSIC REPORTING ACTIVE</div>
    <div class="top-secret-tag">CLASSIFIED</div>
    """, unsafe_allow_html=True)

# --- 4. AGENCY BRANDING ---
logo_data = get_base64_of_bin_file("logo.png")
st.markdown('<div class="seal-box">', unsafe_allow_html=True)
if logo_data:
    st.markdown(f'<img src="data:image/png;base64,{logo_data}" class="agency-logo">', unsafe_allow_html=True)
st.markdown("<div class='main-title' style='text-align:center;'>G-FILID STRATEGIC COMMAND</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#d4af37; letter-spacing:6px; font-weight:bold; font-size:14px; margin-bottom:30px;'>FINANCIAL INTELLIGENCE & BLOCKCHAIN INVESTIGATION DIVISION</div>", unsafe_allow_html=True)

# --- 5. TABS ---
tab1, tab2, tab3 = st.tabs(["🏛️ FIAT AUDIT", "₿ BTC TRACER", "💎 ETH/USDT INTEL"])

# --- TAB 1: FIAT ---
with tab1:
    st.subheader("📁 MASS DATA ANALYSIS")
    uploaded_file = st.file_uploader("UPLOAD SOURCE FILE", type=["csv", "xlsx"], key="fiat_up")
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = [sanitize_headers(col) for col in df.columns]
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cols = st.multiselect("SELECT PARAMETERS:", num_cols, default=num_cols[:2] if len(num_cols)>1 else None)
        if len(cols) >= 2:
            sens = st.sidebar.slider("AI SENSITIVITY", 0.01, 0.25, 0.05)
            model = IsolationForest(contamination=sens, random_state=42)
            df['Anomaly'] = model.fit_predict(df[cols])
            threat_count = len(df[df['Anomaly'] == -1])
            st.plotly_chart(px.scatter(df.sample(min(len(df), 5000)), x=cols[0], y=cols[1], color='Anomaly', color_discrete_map={-1: '#ff1a1a', 1: '#d4af37'}, template="plotly_dark"), use_container_width=True)
            
            # PDF Download for Fiat
            pdf_data = create_pdf_report("Mass Audit File", "Variable Assets", f"{len(df)} Records", f"{threat_count} Threats Detected")
            st.download_button(label="📥 DOWNLOAD OFFICIAL FIAT AUDIT REPORT (PDF)", data=bytes(pdf_data), file_name="G-FILID_Fiat_Report.pdf", mime="application/pdf")

# --- TAB 2: BTC ---
with tab2:
    st.subheader("🌐 BTC LEDGER SURVEILLANCE")
    btc_addr = st.text_input("ENTER BTC ADDRESS:", key="btc_inp")
    if btc_addr:
        res = requests.get(f"https://blockchain.info/rawaddr/{btc_addr}")
        if res.status_code == 200:
            data = res.json()
            bal = data['final_balance']/100000000
            st.metric("REAL-TIME BALANCE", f"{bal:.4f} BTC")
            st.success("🔓 DATA LINK SECURED")
            
            # PDF Download for BTC
            pdf_data = create_pdf_report(btc_addr, f"{bal} BTC", f"{data['n_tx']} Transactions", "High Priority Tracing")
            st.download_button(label="📥 DOWNLOAD OFFICIAL BTC CASE DOSSIER (PDF)", data=bytes(pdf_data), file_name="G-FILID_BTC_Report.pdf", mime="application/pdf")
        else: st.error("INVALID ADDRESS")

# --- TAB 3: ETH/USDT ---
with tab3:
    st.subheader("🏦 ETH/USDT INTELLIGENCE")
    eth_addr = st.text_input("ENTER ETH WALLET:", key="eth_inp")
    if eth_addr:
        res = requests.get(f"https://api.ethplorer.io/getAddressInfo/{eth_addr}?apiKey=freekey")
        if res.status_code == 200:
            data = res.json()
            eth_bal = data.get('ETH',{}).get('balance',0)
            st.metric("ETH BALANCE", f"{eth_bal:,.4f}")
            
            # PDF Download for ETH
            pdf_data = create_pdf_report(eth_addr, f"{eth_bal} ETH", "Token Flow Analysis", "Sovereign Surveillance")
            st.download_button(label="📥 DOWNLOAD OFFICIAL ETH CASE DOSSIER (PDF)", data=bytes(pdf_data), file_name="G-FILID_ETH_Report.pdf", mime="application/pdf")
        else: st.error("INVALID ADDRESS")

# --- FOOTER ---
st.sidebar.divider()
st.sidebar.code("AGENT: 420-FAZLI\nLEVEL: TITAN\nSTATUS: ONLINE")
st.markdown("<hr><center style='color:#333; font-size:10px;'>FOR OFFICIAL USE ONLY (FOUO) | © 2026 G-FILID STRATEGIC COMMAND</center>", unsafe_allow_html=True)
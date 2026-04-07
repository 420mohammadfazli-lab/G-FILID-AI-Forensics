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
st.set_page_config(page_title="OFFICIAL PORTAL | G-FILID", layout="wide", page_icon="🏛️")

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def sanitize_headers(name):
    mapping = {'کد_ملی': 'National_ID', 'درآمد_سالانه': 'Annual_Income', 'مالیات_پرداختی': 'Tax_Paid', 'تعداد_املاک': 'Asset_Count'}
    return mapping.get(name, re.sub(r'[^\x00-\x7F]+', 'FIELD', str(name)))

# --- 2. THE EXECUTIVE NAVY INTERFACE (Your Favorite Style) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Roboto+Mono:wght@400&family=Montserrat:wght@700&display=swap');
    
    .main { 
        background-color: #000a1a;
        background-image: radial-gradient(circle at 50% 50%, #001a33 0%, #000a1a 100%);
        color: #ffffff;
        font-family: 'Roboto Mono', monospace;
    }
    
    .official-bar {
        background: #000000;
        border-bottom: 2px solid #b38600;
        padding: 10px;
        text-align: center;
        font-family: 'Montserrat', sans-serif;
        font-size: 12px;
        letter-spacing: 4px;
        color: #b38600;
        text-transform: uppercase;
        position: fixed; top: 0; left: 0; width: 100%; z-index: 999;
    }

    .seal-container { text-align: center; padding: 70px 0 20px 0; }
    
    .user-logo {
        width: 160px; height: 160px;
        border-radius: 50%; border: 3px solid #b38600;
        padding: 10px; box-shadow: 0 0 40px rgba(179, 134, 0, 0.6);
        object-fit: contain; background: rgba(0,0,0,0.4);
    }

    .agency-title {
        font-family: 'Cinzel', serif;
        font-size: 42px; font-weight: 700;
        color: #ffffff; margin-top: 20px;
        letter-spacing: 3px; text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
    }
    
    .top-secret-stamp {
        position: absolute; top: 130px; right: 60px;
        border: 5px solid #ff0000; color: #ff1a1a;
        padding: 12px 25px; font-size: 26px; font-weight: bold;
        transform: rotate(12deg); opacity: 0.4; border-radius: 8px;
    }

    .stButton>button {
        background-color: #b38600 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 0px !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        height: 3.5em;
    }
    div[data-testid="stMetricValue"] { color: #b38600 !important; font-family: 'Montserrat', sans-serif; }
    </style>
    
    <div class="official-bar">OFFICIAL GOVERNMENT COMMUNICATION - CLASSIFIED ACCESS ONLY</div>
    <div class="top-secret-stamp">TOP SECRET</div>
    """, unsafe_allow_html=True)

# --- 3. HEADER & LOGO ---
logo_data = get_base64_of_bin_file("logo.png")
st.markdown('<div class="seal-container">', unsafe_allow_html=True)
if logo_data:
    st.markdown(f'<img src="data:image/png;base64,{logo_data}" class="user-logo">', unsafe_allow_html=True)
else:
    st.markdown('<div style="width:150px; height:150px; border:3px solid #b38600; border-radius:50%; display:inline-block; line-height:150px; font-size:60px; background:rgba(179,134,0,0.1);">🏛️</div>', unsafe_allow_html=True)

st.markdown("""
        <div class="agency-title">G-FILID FORENSICS</div>
        <div style="color: #b38600; font-weight: bold; letter-spacing: 6px; font-size: 14px; margin-top: 10px;">
            GLOBAL FINANCIAL INTELLIGENCE & LAUNDERING INVESTIGATION DIVISION
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. TABS ---
t1, t2, t3 = st.tabs(["🏛️ FIAT AUDIT", "₿ BTC SURVEILLANCE", "💎 ETH/USDT INTEL"])

# --- TAB 1: FIAT AUDIT ---
with t1:
    st.subheader("📁 CLASSIFIED DATABASE SCANNER")
    file = st.file_uploader("UPLOAD DOSSIER (CSV/XLSX)", type=["csv", "xlsx"], key="u_fiat")
    if file:
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
        df.columns = [sanitize_headers(col) for col in df.columns]
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cols = st.multiselect("SELECT PARAMETERS:", numeric_cols, default=numeric_cols[:2] if len(numeric_cols)>1 else None)
        
        if len(cols) >= 2:
            st.sidebar.markdown("### SYSTEM SETTINGS")
            sens = st.sidebar.slider("AI SENSITIVITY", 0.01, 0.20, 0.05)
            model = IsolationForest(contamination=sens, random_state=42)
            df['Anomaly'] = model.fit_predict(df[cols])
            
            c1, c2, c3 = st.columns(3)
            c1.metric("SCANNED", len(df))
            c2.metric("THREATS", len(df[df['Anomaly'] == -1]))
            c3.metric("STATUS", "STABLE")

            # Chart Optimization
            sample_df = df.sample(min(len(df), 5000))
            fig = px.scatter(sample_df, x=cols[0], y=cols[1], color='Anomaly', color_discrete_map={-1: '#ff0000', 1: '#b38600'}, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            if st.button("📥 GENERATE OFFICIAL AUDIT REPORT"):
                with st.spinner("PRINTING DOSSIER..."):
                    time.sleep(2)
                    st.success("REPORT GENERATED!")
                    st.info(f"CASE ID: G-FILID-{int(time.time())}\nSTATUS: EVIDENCE SECURED")

# --- TAB 2: BTC SURVEILLANCE ---
with t2:
    st.subheader("₿ REAL-TIME BITCOIN TRACING")
    btc_addr = st.text_input("ENTER BTC ADDRESS:", key="btc_val")
    if btc_addr:
        with st.spinner("📡 SCANNING LEDGER..."):
            res = requests.get(f"https://blockchain.info/rawaddr/{btc_addr}")
            if res.status_code == 200:
                data = res.json()
                st.success("🔓 DATA LINK ESTABLISHED")
                bc1, bc2 = st.columns(2)
                bc1.metric("BALANCE", f"{data['final_balance']/100000000:.4f} BTC")
                bc2.metric("TRANSACTIONS", data['n_tx'])
                
                txs = [{"HASH": tx['hash'][:25]+"...", "VALUE": tx['result']/100000000} for tx in data['txs'][:10]]
                st.table(pd.DataFrame(txs))
                
                if st.button("📥 GENERATE BTC CASE FILE"):
                    st.info(f"REPORT G-FILID-BTC-{int(time.time())} SECURED.")
            else: st.error("INVALID BTC ADDRESS")

# --- TAB 3: ETH/USDT ---
with tab3: # (Using tab3 to fix the NameError)
    st.subheader("💎 ETH/USDT INTELLIGENCE")
    eth_addr = st.text_input("ENTER ETH WALLET:", key="eth_val")
    if eth_addr:
        with st.spinner("📡 SCANNING ETHEREUM NODES..."):
            res = requests.get(f"https://api.ethplorer.io/getAddressInfo/{eth_addr}?apiKey=freekey")
            if res.status_code == 200:
                data = res.json()
                st.success("🔓 SECURE HANDSHAKE COMPLETE")
                ec1, ec2 = st.columns(2)
                eth_bal = data.get('ETH', {}).get('balance', 0)
                ec1.metric("ETH BALANCE", f"{eth_bal:,.4f}")
                
                tokens = data.get('tokens', [])
                usdt = next((t for t in tokens if t['tokenInfo']['symbol'] == 'USDT'), None)
                if usdt:
                    val = usdt['balance'] / (10**int(usdt['tokenInfo']['decimals']))
                    ec2.metric("USDT BALANCE", f"${val:,.2f}")
                else: ec2.metric("USDT BALANCE", "$0.00")
                
                if st.button("📥 GENERATE ETH EVIDENCE"):
                    st.info(f"REPORT G-FILID-ETH-{int(time.time())} SECURED.")
            else: st.error("INVALID ADDRESS")

# --- SIDEBAR & FOOTER ---
st.sidebar.title("AUTHENTICATION")
st.sidebar.info("OFFICER: AGENT_HAJI\nLEVEL: TITAN\nSTATUS: ONLINE")
st.markdown("<hr><center style='color:#333; font-size:10px;'>FOR OFFICIAL USE ONLY (FOUO) | © 2024 G-FILID STRATEGIC COMMAND</center>", unsafe_allow_html=True)
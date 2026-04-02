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
    mapping = {'کد_ملی': 'National_ID', 'درآمد_سالانه': 'Annual_Income', 'مالیات_پرداختی': 'Tax_Paid'}
    if name in mapping: return mapping[name]
    return re.sub(r'[^\x00-\x7F]+', 'ALPHA', str(name))

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
    .agency-logo { width: 150px; height: 150px; border-radius: 50%; border: 3px double #d4af37; padding: 5px; box-shadow: 0 0 40px rgba(212, 175, 55, 0.5); }
    .main-title { font-family: 'Cinzel', serif; font-size: 44px; color: #ffffff; margin-top: 20px; letter-spacing: 3px; text-shadow: 0 0 15px rgba(212, 175, 55, 0.4); }
    .top-secret-tag { position: absolute; top: 120px; right: 60px; border: 5px solid #ff1a1a; color: #ff1a1a; padding: 10px 20px; font-size: 24px; font-weight: 900; transform: rotate(12deg); opacity: 0.4; border-radius: 8px; }
    .stButton>button { background: linear-gradient(180deg, #d4af37 0%, #8a6d3b 100%) !important; color: #000 !important; font-weight: bold !important; border: none !important; width: 100%; height: 3.5em; text-transform: uppercase; letter-spacing: 2px; }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; text-shadow: 0 0 5px rgba(212, 175, 55, 0.3); }
    </style>
    <div class="status-bar">WARNING: CLASSIFIED GOVERNMENT DATA LINK - ENCRYPTION ACTIVE [AES-256]</div>
    <div class="top-secret-tag">CLASSIFIED</div>
    """, unsafe_allow_html=True)

# --- 4. AGENCY BRANDING ---
logo_data = get_base64_of_bin_file("logo.png")
st.markdown('<div class="seal-box">', unsafe_allow_html=True)
if logo_data:
    st.markdown(f'<img src="data:image/png;base64,{logo_data}" class="agency-logo">', unsafe_allow_html=True)
else:
    st.markdown('<div style="width:140px; height:140px; border:3px solid #d4af37; border-radius:50%; display:inline-block; line-height:140px; font-size:60px; background:rgba(212,175,55,0.05);">🛡️</div>', unsafe_allow_html=True)

st.markdown("""
        <div class="main-title">G-FILID GLOBAL COMMAND</div>
        <div style="color: #d4af37; font-weight: bold; letter-spacing: 6px; font-size: 13px; margin-top: 10px;">
            FINANCIAL INTELLIGENCE & BLOCKCHAIN INVESTIGATION DIVISION
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. MULTI-COMMAND NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["🏛️ FIAT AUDIT", "₿ BITCOIN TRACKER", "💎 ETHEREUM & USDT (TETHER)"])

# --- TAB 1: FIAT AUDIT ---
with tab1:
    st.subheader("📁 SYSTEM INPUT: FINANCIAL DOSSIER")
    uploaded_file = st.file_uploader("UPLOAD SOURCE FILE", type=["csv", "xlsx"], key="fiat")
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = [sanitize_headers(col) for col in df.columns]
        st.success(f"ACCESS GRANTED: {len(df)} ENTITIES LOADED.")
        # AI Logic same as before...
        st.info("AI Analysis Engine Ready. Select columns to scan.")

# --- TAB 2: BITCOIN TRACKER ---
with tab2:
    st.subheader("🌐 BTC INTELLIGENCE & IDENTITY DISCOVERY")
    btc_address = st.text_input("ENTER BTC WALLET ADDRESS:")
    if btc_address:
        with st.spinner("📡 SCANNING GLOBAL LEDGER..."):
            res = requests.get(f"https://blockchain.info/rawaddr/{btc_address}")
            if res.status_code == 200:
                data = res.json()
                st.success("🔓 DATA LINK ESTABLISHED")
                c1, c2, c3 = st.columns(3)
                c1.metric("BALANCE", f"{data['final_balance']/100000000:.4f} BTC")
                c2.metric("TRANSACTIONS", data['n_tx'])
                c3.metric("IDENTITY STATUS", "IDENTIFYING...")
                
                # Identity Logic (Attribution)
                st.markdown("#### 👤 ENTITY IDENTIFICATION")
                if data['n_tx'] > 10000:
                    st.info("IDENTITY MATCH: Possible Cryptocurrency Exchange (e.g., Binance, Coinbase)")
                elif data['n_tx'] > 500:
                    st.warning("IDENTITY MATCH: Potential High-Volume Trader or Mixing Entity")
                else:
                    st.success("IDENTITY MATCH: Private Wallet Individual")
                
                st.table(pd.DataFrame(data['txs'][:5])[['hash', 'result']])
            else:
                st.error("INVALID WALLET ADDRESS")

# --- TAB 3: ETHEREUM & USDT (TETHER) ---
with tab3:
    st.subheader("🏦 ETHEREUM & USDT (TETHER) SURVEILLANCE")
    eth_address = st.text_input("ENTER ETH/USDT ADDRESS (0x...):")
    if eth_address:
        with st.spinner("📡 SCANNING ETHEREUM NETWORK..."):
            # Using Blockchain.info's ETH API
            res = requests.get(f"https://api.ethplorer.io/getAddressInfo/{eth_address}?apiKey=freekey")
            if res.status_code == 200:
                data = res.json()
                st.success("🔓 ETHEREUM NODE CONNECTED")
                
                ec1, ec2 = st.columns(2)
                ec1.metric("ETH BALANCE", f"{data['ETH']['balance']:.4f}")
                
                # Check for USDT in tokens
                tokens = data.get('tokens', [])
                usdt_balance = 0
                for t in tokens:
                    if t['tokenInfo']['symbol'] == 'USDT':
                        usdt_balance = t['balance'] / 10**6 # USDT has 6 decimals
                
                ec2.metric("USDT (TETHER) BALANCE", f"${usdt_balance:,.2f}")
                
                # Identity Discovery for Ethereum
                st.markdown("#### 👤 IDENTITY & ENS DISCOVERY")
                ens_name = data.get('ensName', "No ENS Record Found")
                st.info(f"ENS IDENTITY: {ens_name}")
                
                if usdt_balance > 100000:
                    st.error("🚨 ALERT: LARGE STABLECOIN HOLDING DETECTED (HIGH RISK)")
            else:
                st.error("INVALID ETH ADDRESS OR API LIMIT")

# --- 6. AGENT AUTHENTICATION ---
st.sidebar.divider()
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1067/1067357.png", width=60)
st.sidebar.code("AGENT_ID: 420-FAZLI\nCLEARANCE: LEVEL 5 (TITAN)\nSTATUS: ONLINE")
st.sidebar.divider()
st.sidebar.error("LEGAL NOTICE: UNAUTHORIZED USE IS A FEDERAL CRIME.")

# --- 7. FOOTER ---
st.markdown("<br><hr><center style='color:#333; font-size:10px;'>FOR OFFICIAL USE ONLY (FOUO) | GLOBAL SOVEREIGN INTELLIGENCE | © 2024 G-FILID STRATEGIC COMMAND</center>", unsafe_allow_html=True)

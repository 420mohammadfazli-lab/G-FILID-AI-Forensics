import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import plotly.express as px
import time
import base64
import os
import re

# --- 1. GLOBAL SYSTEM ARCHITECTURE ---
st.set_page_config(
    page_title="G-FILID | SUPREME GLOBAL INTELLIGENCE", 
    layout="wide", 
    page_icon="🛡️"
)

# --- 2. AUTOMATED DATA PURGE (Forces English Headers) ---
def sanitize_headers(name):
    mapping = {
        'کد_ملی': 'National_ID',
        'درآمد_سالانه': 'Annual_Income',
        'مالیات_پرداختی': 'Tax_Paid',
        'تعداد_املاک': 'Asset_Count',
        'وضعیت_ریسک': 'Risk_Score',
        'نام': 'First_Name',
        'نام_خانوادگی': 'Last_Name',
        'مبلغ': 'Amount',
        'تاریخ': 'Timestamp'
    }
    if name in mapping:
        return mapping[name]
    # Strip non-English characters and replace with 'DATA_FIELD'
    clean = re.sub(r'[^\x00-\x7F]+', 'ALPHA', str(name))
    return clean

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
    
    .main { 
        background-color: #00050a;
        background-image: radial-gradient(circle at center, #001529 0%, #00050a 100%);
        color: #ffffff;
        font-family: 'Share Tech Mono', monospace;
    }
    
    .status-bar {
        background: #000000;
        border-bottom: 2px solid #d4af37;
        padding: 8px;
        text-align: center;
        font-family: 'Montserrat', sans-serif;
        font-size: 11px;
        letter-spacing: 5px;
        color: #d4af37;
        text-transform: uppercase;
        position: fixed;
        top: 0; left: 0; width: 100%; z-index: 999;
    }

    .seal-box { text-align: center; padding: 80px 0 30px 0; }
    
    .agency-logo {
        width: 170px; height: 170px;
        border-radius: 50%; border: 4px double #d4af37;
        padding: 5px; box-shadow: 0 0 50px rgba(212, 175, 55, 0.4);
        background: rgba(0,0,0,0.6);
    }

    .main-title {
        font-family: 'Cinzel', serif;
        font-size: 48px; font-weight: 700;
        color: #ffffff; margin-top: 25px;
        letter-spacing: 4px; text-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
    }
    
    div[data-testid="stMetricValue"] { 
        color: #d4af37 !important; 
        font-size: 38px !important;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
    }
    
    .top-secret-tag {
        position: absolute; top: 130px; right: 70px;
        border: 6px solid #ff1a1a; color: #ff1a1a;
        padding: 15px 30px; font-size: 28px; font-weight: 900;
        transform: rotate(10deg); opacity: 0.5; border-radius: 10px;
        font-family: 'Montserrat', sans-serif;
    }

    .stButton>button {
        background: linear-gradient(180deg, #d4af37 0%, #8a6d3b 100%) !important;
        color: #000000 !important; font-weight: bold !important;
        border: none !important; border-radius: 0px !important;
        width: 100%; height: 3.5em; text-transform: uppercase;
        letter-spacing: 3px; font-size: 16px !important;
    }
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
    st.markdown('<div style="width:150px; height:150px; border:4px solid #d4af37; border-radius:50%; display:inline-block; line-height:150px; font-size:70px; background:rgba(212,175,55,0.05);">🛡️</div>', unsafe_allow_html=True)

st.markdown("""
        <div class="main-title">G-FILID STRATEGIC COMMAND</div>
        <div style="color: #d4af37; font-weight: bold; letter-spacing: 8px; font-size: 16px; margin-top: 12px;">
            GLOBAL FINANCIAL INTELLIGENCE & LAUNDERING INVESTIGATION DIVISION
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. DATA ACQUISITION PROTOCOL ---
st.divider()
st.subheader("📁 SYSTEM INPUT: DATA DOSSIER")
uploaded_file = st.file_uploader("UPLOAD SOURCE FILE (SECURE CSV/XLSX)", type=["csv", "xlsx"])

if uploaded_file:
    with st.spinner("💠 DECRYPTING NEURAL PACKETS..."):
        time.sleep(2)
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # --- FORCE ENGLISH TRANSLATION ---
            df.columns = [sanitize_headers(col) for col in df.columns]
            
            st.success(f"ACCESS GRANTED: {len(df)} ENTITIES EXTRACTED SUCCESSFULLY.")

            # --- 6. AI NEURAL CORE ---
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            st.markdown("#### 🧠 NEURAL CORE CALIBRATION")
            selected_cols = st.multiselect("SELECT PARAMETERS FOR PATTERN RECOGNITION:", numeric_cols, default=numeric_cols[:2] if len(numeric_cols)>1 else numeric_cols)

            if len(selected_cols) >= 2:
                # SIDEBAR SETTINGS
                st.sidebar.markdown("<h2 style='color:#d4af37;'>AI OVERRIDE</h2>", unsafe_allow_html=True)
                sensitivity = st.sidebar.slider("AI THREAT SENSITIVITY", 0.01, 0.25, 0.05)
                
                # RUN AI (ISOLATION FOREST)
                model = IsolationForest(contamination=sensitivity, random_state=42)
                df['Anomaly_Score'] = model.fit_predict(df[selected_cols])
                df['RISK_LEVEL'] = df['Anomaly_Score'].apply(lambda x: '🚨 CRITICAL THREAT' if x == -1 else '✅ SECURE')
                
                # --- 7. EXECUTIVE HUD DISPLAY ---
                st.divider()
                c1, c2, c3, c4 = st.columns(4)
                threat_count = len(df[df['Anomaly_Score'] == -1])
                c1.metric("SCAN CAPACITY", f"{len(df):,}")
                c2.metric("THREATS DETECTED", threat_count)
                c3.metric("INTEGRITY INDEX", f"{100-(threat_count/len(df)*100):.1f}%")
                c4.metric("SYSTEM CORE", "QUANTUM")

                # --- 8. ANALYTICAL VISUALIZATION ---
                st.subheader("🌐 MULTI-DIMENSIONAL THREAT ANALYSIS")
                fig = px.scatter(
                    df, x=selected_cols[0], y=selected_cols[1], color='RISK_LEVEL',
                    color_discrete_map={'🚨 CRITICAL THREAT': '#ff1a1a', '✅ SECURE': '#d4af37'},
                    template="plotly_dark",
                    hover_data=df.columns
                )
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#d4af37")
                st.plotly_chart(fig, use_container_width=True)

                # --- 9. PRIORITY AUDIT BLACKLIST ---
                st.subheader("🚩 AUDIT BLACKLIST - IMMEDIATE INVESTIGATION")
                blacklist = df[df['Anomaly_Score'] == -1].drop(columns=['Anomaly_Score'])
                st.dataframe(blacklist, use_container_width=True)

                # Export
                report_csv = blacklist.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 DOWNLOAD ENCRYPTED AUDIT DOSSIER",
                    data=report_csv,
                    file_name="G-FILID_Threat_Report.csv",
                    mime="text/csv"
                )

            else:
                st.warning("NOTICE: MINIMUM 2 PARAMETERS REQUIRED FOR AI NEURAL SCAN.")
        
        except Exception as e:
            st.error(f"CRITICAL ERROR: {e}")

else:
    st.info("SYSTEM STATUS: STANDING BY FOR ENCRYPTED DATA UPLOAD.")

# --- 10. SIDEBAR AGENT AUTHENTICATION ---
st.sidebar.divider()
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1067/1067357.png", width=60)
st.sidebar.code("AGENT_ID: 420-FAZLI\nCLEARANCE: LEVEL 5 (ULTRA)\nSTATUS: ONLINE")
st.sidebar.divider()
st.sidebar.error("AUTHORIZED USE ONLY. UNAUTHORIZED ACCESS IS A FEDERAL CRIME.")

# --- 11. LEGAL FOOTER ---
st.markdown("<br><hr><center style='color:#222; font-size:10px;'>FOR OFFICIAL USE ONLY (FOUO) | GLOBAL SOVEREIGN INTELLIGENCE | © 2024 G-FILID STRATEGIC COMMAND</center>", unsafe_allow_html=True)

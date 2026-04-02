import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import plotly.express as px
import time
import base64
import os

# --- 1. SYSTEM IDENTITY CONFIG ---
st.set_page_config(
    page_title="OFFICIAL PORTAL | G-FILID FORENSICS", 
    layout="wide", 
    page_icon="🏛️"
)

# Function to encode the logo image to Base64
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# --- 2. THE EXECUTIVE NAVY INTERFACE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Roboto+Mono:wght@400&family=Montserrat:wght@700&display=swap');
    
    /* Background: Deep Executive Navy Radial Gradient */
    .main { 
        background-color: #000a1a;
        background-image: radial-gradient(circle at 50% 50%, #001a33 0%, #000a1a 100%);
        color: #ffffff;
        font-family: 'Roboto Mono', monospace;
    }
    
    /* Top Official Communication Bar */
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
        position: fixed;
        top: 0; left: 0; width: 100%; z-index: 999;
    }

    /* Professional Seal Logo Styling */
    .seal-container { text-align: center; padding: 60px 0 20px 0; }
    
    .user-logo {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        border: 3px solid #b38600;
        padding: 10px;
        box-shadow: 0 0 40px rgba(179, 134, 0, 0.6);
        object-fit: contain;
        background: rgba(0,0,0,0.4);
    }

    .agency-title {
        font-family: 'Cinzel', serif;
        font-size: 42px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 20px;
        letter-spacing: 3px;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
    }
    
    /* Metric & Data Styling */
    div[data-testid="stMetricValue"] { 
        color: #b38600 !important; 
        font-family: 'Montserrat', sans-serif; 
        font-size: 32px !important;
    }
    
    .stDataFrame { border: 1px solid #b38600 !important; }

    /* "TOP SECRET" Red Stamp */
    .top-secret-stamp {
        position: absolute; top: 120px; right: 60px;
        border: 5px solid #ff0000; color: #ff0000;
        padding: 12px 25px; font-size: 26px; font-weight: bold;
        transform: rotate(12deg); opacity: 0.4; border-radius: 8px;
        font-family: 'Montserrat', sans-serif;
    }

    /* Executive Gold Button */
    .stButton>button {
        background-color: #b38600 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 0px !important;
        width: 100%;
        height: 3em;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background-color: #ffd700 !important;
        box-shadow: 0 0 20px #b38600;
    }
    </style>
    
    <div class="official-bar">OFFICIAL GOVERNMENT COMMUNICATION - CLASSIFIED ACCESS ONLY</div>
    <div class="top-secret-stamp">TOP SECRET</div>
    """, unsafe_allow_html=True)

# --- 3. AGENCY HEADER WITH DYNAMIC LOGO ---
logo_data = get_base64_of_bin_file("logo.png")

st.markdown('<div class="seal-container">', unsafe_allow_html=True)
if logo_data:
    st.markdown(f'<img src="data:image/png;base64,{logo_data}" class="user-logo">', unsafe_allow_html=True)
else:
    # Default emblem if logo.png is missing
    st.markdown('<div style="width:150px; height:150px; border:3px solid #b38600; border-radius:50%; display:inline-block; line-height:150px; font-size:60px; background:rgba(179,134,0,0.1);">🏛️</div>', unsafe_allow_html=True)

st.markdown("""
        <div class="agency-title">G-FILID FORENSICS</div>
        <div style="color: #b38600; font-weight: bold; letter-spacing: 6px; font-size: 14px; margin-top: 10px;">
            GLOBAL FINANCIAL INTELLIGENCE & LAUNDERING INVESTIGATION DIVISION
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. SECURE DATA ACQUISITION ---
st.divider()
st.subheader("📁 CASE FILE IMPORT")
uploaded_file = st.file_uploader("UPLOAD CLASSIFIED FINANCIAL DOSSIER (CSV OR XLSX FORMAT)", type=["csv", "xlsx"])

if uploaded_file:
    with st.spinner("⚡ DECRYPTING AND SCANNING FOR ANOMALIES..."):
        time.sleep(2) # Simulation of high-level processing
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"SUCCESS: {len(df)} ENTITIES LOADED INTO THE ANALYTICAL CORE.")

            # --- 5. AI NEURAL ANALYSIS ---
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            st.markdown("#### 🧠 AI PARAMETER CALIBRATION")
            selected_cols = st.multiselect("SELECT TARGET FEATURES FOR PATTERN MATCHING:", numeric_cols, default=numeric_cols[:2] if len(numeric_cols)>1 else numeric_cols)

            if len(selected_cols) >= 2:
                # Sidebar System Settings
                sensitivity = st.sidebar.slider("AI DETECTION SENSITIVITY", 0.01, 0.20, 0.05)
                
                # Running Isolation Forest AI
                model = IsolationForest(contamination=sensitivity, random_state=42)
                df['Anomaly_Score'] = model.fit_predict(df[selected_cols])
                df['RISK_STATUS'] = df['Anomaly_Score'].apply(lambda x: '🚨 AUDIT REQUIRED' if x == -1 else '✅ SECURE')
                
                # --- 6. EXECUTIVE HUD METRICS ---
                st.divider()
                c1, c2, c3, c4 = st.columns(4)
                risk_count = len(df[df['Anomaly_Score'] == -1])
                c1.metric("SCAN CAPACITY", f"{len(df):,}")
                c2.metric("THREATS DETECTED", risk_count)
                c3.metric("INTEGRITY SCORE", f"{100-(risk_count/len(df)*100):.1f}%")
                c4.metric("SYSTEM LOAD", "STABLE")

                # --- 7. ANALYTICAL VISUALIZATION ---
                st.subheader("🌐 MULTI-DIMENSIONAL RISK PROFILING")
                fig = px.scatter(
                    df, x=selected_cols[0], y=selected_cols[1], color='RISK_STATUS',
                    color_discrete_map={'🚨 AUDIT REQUIRED': '#ff0000', '✅ SECURE': '#b38600'},
                    template="plotly_dark",
                    hover_data=df.columns
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)', 
                    font_color="#b38600",
                    margin=dict(l=0, r=0, b=0, t=40)
                )
                st.plotly_chart(fig, use_container_width=True)

                # --- 8. PRIORITY AUDIT LIST (THE BLACKLIST) ---
                st.subheader("🚩 CLASSIFIED BLACKLIST (IMMEDIATE INVESTIGATION)")
                blacklist = df[df['Anomaly_Score'] == -1].drop(columns=['Anomaly_Score'])
                st.dataframe(blacklist.style.set_properties(**{'background-color': '#001a33', 'color': 'white', 'border-color': '#b38600'}), use_container_width=True)

                # Export Dossier
                csv_data = blacklist.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 DOWNLOAD OFFICIAL CASE DOSSIER",
                    data=csv_data,
                    file_name="G_FILID_Investigation_Report.csv",
                    mime="text/csv"
                )

            else:
                st.warning("SYSTEM NOTICE: PLEASE SELECT AT LEAST 2 FINANCIAL PARAMETERS TO INITIATE THE AI SCAN.")
        
        except Exception as e:
            st.error(f"SYSTEM ERROR: UNABLE TO PROCESS DATA. DETAILS: {e}")

else:
    st.info("SYSTEM STATUS: IDLE. STANDING BY FOR SECURE DATA UPLOAD.")
    # Placeholder for Authority
    st.markdown("<center><p style='color:#333; font-size:12px; margin-top:50px;'>AUTHENTICATED ACCESS ONLY - 256-BIT ENCRYPTION ACTIVE</p></center>", unsafe_allow_html=True)

# --- 9. SIDEBAR AGENT CREDENTIALS ---
st.sidebar.title("AGENT AUTHENTICATION")
st.sidebar.markdown("---")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1067/1067357.png", width=80)
st.sidebar.info("**OFFICER:** AGENT_HAJI_AFG\n\n**CLEARANCE:** LEVEL 5 (TS/SCI)\n\n**SECTOR:** GLOBAL HUB")
st.sidebar.divider()
st.sidebar.error("LEGAL NOTICE: Any unauthorized extraction of classified data is a federal crime.")

# --- 10. FOOTER ---
st.markdown("<br><hr><center style='color:#222; font-size:11px;'>FOR OFFICIAL USE ONLY (FOUO) | SECURED BY NATIONAL INTELLIGENCE PROTOCOLS | © 2024 G-FILID GLOBAL DIVISION</center>", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GMC Jalgaon MIS", layout="wide", page_icon="https://www.nyatigroup.com/Nyati-logo-seo.png")

DPR_ID = "1rC8g812mywE_5rmNVTkBcBzjEsgzRT_G2m6olrGht9I"
DLR_ID = "1nlWQjCqVvNJr7Syu701MVztEfYcGBH2K2r1NBsmE6tU"

DPR_LINK = f"https://docs.google.com/spreadsheets/d/{DPR_ID}/export?format=xlsx"
DLR_LINK = f"https://docs.google.com/spreadsheets/d/{DLR_ID}/export?format=xlsx"

def check_password():
    def password_entered():
        if st.session_state["password_input"] == "hscc@nyati2026":
            st.session_state["password_correct"] = True
            del st.session_state["password_input"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("🔐 Please enter key to view GMC Jalgaon MIS.")
            st.text_input(
                "Enter Access Key", 
                type="password", 
                on_change=password_entered, 
                key="password_input",
                help="Enter the project security key",
                autocomplete="new-password" 
            )
        return False
    
    elif not st.session_state["password_correct"]:
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.error("🚫 Incorrect Key. Please try again.")
            st.text_input(
                "Enter Access Key", 
                type="password", 
                on_change=password_entered, 
                key="password_input",
                autocomplete="new-password"
            )
        return False
    
    else:
        return True

if not check_password():
    st.stop()

if "password_correct" in st.session_state and st.session_state["password_correct"]:
    if "first_login" not in st.session_state:
        st.session_state["first_login"] = True
        st.rerun()

st.markdown("""
    <style>
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    .block-container {padding-top: 1rem !important;}
    
    /* Metrics ka size */
    [data-testid="stMetricValue"] { font-size: 24px !important; font-weight: 600 !important; }

    /* --- Main Title --- */
    h1 {
        font-size: 40px !important;
        font-weight: 800 !important;
        color: #000000 !important;
        text-align: center !important;
        margin-top: 10px !important;
        text-transform: uppercase !important;
    }

    /* Baki headers */
    h2, h3, [data-testid="stMarkdownContainer"] h3 {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #000000 !important;
        font-family: 'Arial', sans-serif !important;
        margin-bottom: 10px !important;
    }

    /* --- 🔴 RED HIGHLIGHT: Categories (Bold) --- */
    [data-testid="stExpander"] p {
        font-size: 20px !important;
        font-weight: 650 !important; 
        color: #000000 !important;
    }

    /* --- 🔵 BLUE HIGHLIGHT: PDF Buttons (Normal Weight & Full Width) --- */
    /* Left alignment wala sara code yahan se delete kar diya hai */
    div[data-testid="stLinkButton"] {
        width: 100% !important;
    }

    div[data-testid="stLinkButton"] p {
        font-weight: 400 !important; /* Text normal rahega */
    }

    /* Selectbox label size */
    [data-testid="stWidgetLabel"] p {
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #000000 !important;
    }
    
    hr { margin-top: 1rem !important; margin-bottom: 1.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

header_col1, header_col2, header_col3 = st.columns([1, 4, 1])
with header_col1:
    st.image("https://www.govtjobsblog.in/wp-content/uploads/2023/08/HSCC.png", width=120) 
with header_col2:
    st.markdown("<h1 style='text-align: center; margin-top: 10px;'>GOVERNMENT MEDICAL COLLEGE, JALGAON</h1>", unsafe_allow_html=True)
with header_col3:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_SCCFqzFBiku7nsc76ytomhXnvIZ6rrHBQQ&s", width=120)

try:
    df_labour_data = pd.read_excel(DLR_LINK, skiprows=7) 
    df_labour_data = df_labour_data.dropna(subset=[df_labour_data.columns[1]])
    total_pax = pd.to_numeric(df_labour_data.iloc[:, 12], errors='coerce').sum()

    st.markdown("### 🏗️ Project Overview")
    d1, d2, d3 = st.columns(3)
    d1.metric("Start Date", "16 Mar 2023", "Project Start")
    d2.metric("End Date", "01 Apr 2026", "Completion")
    d3.metric("Tender Cost", "625.20 Cr.", "Project Value")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Plot Area", "66.29 Acres", "Total Site")
    m2.metric("Overall Progress", "88%", "MSP Linked")
    m3.metric("Total Manpower", "432 Pax", "Live Updates")

    s1, s2 = st.columns(2)
    s1.metric("Client Name", "HSCC (India) Limited", "Project Management")
    s2.metric("Contractor Name", "Nyati Engineers & Consultants Pvt. Ltd. (NECPL)", "Project Execution")

    st.divider()
    st.markdown("### 📂 Contract Documents & Management")

    doc_data = {
        "Contract Documents": {
            "LOA - Jalgaon EPC - Nyati Engineer": "https://drive.google.com/file/d/12Bznwh-5rioNN08ImXhOKws0PvXVnE-b/view?usp=sharing",
            "Part - 1 of 3": "https://drive.google.com/file/d/1O8AOt85_nufdDHUCebOjBwKzg83I6MDD/view?usp=sharing",
            "Part - 2 of 3": "https://drive.google.com/file/d/1OUiLdnNEHztL7iJufTVa1OVhWiRWqZJZ/view?usp=sharing",
            "Part - 3 of 3": "https://drive.google.com/file/d/1BKO-xUVF0ejwYzRCJH2xNAShhESEMPDv/view?usp=sharing"
        },
        # "Extension Of Time": {
        #     "NECPL letter Jalgaon EOT": "https://drive.google.com/file/d/1K6OY5c8N0lSpgRZWitTJo_xvH3QapbuB/view?usp=sharing",
        #     "Submission of EOT - 02 for GMC Jalgaon": "https://drive.google.com/file/d/10fOjLmAXeMjvnh8Kq3OBHEMt_sxxs4xF/view?usp=sharing"
        # },
        # "Escalation": {
        #     "GMCH Jalgaon - Contract Amendment": "https://drive.google.com/file/d/1jBPBZkF7qeCZWsSfizAf-7G-tTlgGS_T/view?usp=sharing",
        #     "HSCC Escalation letter": "https://drive.google.com/file/d/14UgaSlAvMADSC1TSIdFTx9S5RfCiUuQT/view?usp=sharing",
        #     "GMCH Jalgaon - Escalation Request": "https://drive.google.com/file/d/1yOCh2ucWHWYQadceQxf7z-onz5HVjUUD/view?usp=sharing"
        # },
        # "Additional Claim": {
        #     "Extra Claim Recieveing": "https://drive.google.com/file/d/1Xk9l18lXqc6JlEsp-bewTDvUEDdqUlok/view?usp=sharing",
        #     "HSCC Reply on Various Claim": "https://drive.google.com/file/d/1D1mQs7g83EFEOKFx4pFh-ZpxBEUSb3Mg/view?usp=sharing",
        # },
        "Outstanding Payment": {
            "B0074 - Reminder of release of Hold": "https://drive.google.com/file/d/1EHlgQ2eh80RCcwIdY0XNlhvGMEsJzpUa/view?usp=sharing",
            "Hold 6.8075": "https://drive.google.com/file/d/1BqWknz297vdGt2m7g55OoGbmRwuNA46b/view?usp=sharing"
        },
        # "Other": {
           
        # }
    }

    for category, files in doc_data.items():
        with st.expander(f" {category}"): 
            for file_name, link in files.items():
                st.link_button(f"📄 {file_name}", link, use_container_width=True)

    st.divider()

    xls_dpr = pd.ExcelFile(DPR_LINK)
    show_sheets = ["MCB & HB", "Residential", "Ancillary", "Development"]
    
    available_sheets = [sheet for sheet in xls_dpr.sheet_names if sheet.strip() in show_sheets]
    
    if not available_sheets:
        available_sheets = [sheet for sheet in xls_dpr.sheet_names if sheet.strip() not in ["Priority", "Development DPR"]]

    selected_sheet = st.selectbox("📂 Select Building View", available_sheets)
    
    df_dpr = pd.read_excel(DPR_LINK, sheet_name=selected_sheet, skiprows=6)
    df_dpr = df_dpr.dropna(how='all', axis=1).dropna(how='all', axis=0)

    df_dpr = df_dpr.iloc[:, 1:] 
    df_dpr = df_dpr.reset_index(drop=True) 

    if selected_sheet in ["MCB & HB", "Residential", "Ancillary"]:
        target_val = "External Paint"
        mask = df_dpr.iloc[:, 0].astype(str).str.contains(target_val, case=False, na=False)
        if mask.any():
            stop_idx = mask.idxmax()
            df_dpr = df_dpr.iloc[:stop_idx + 1] 

    st.subheader(f"Detailed Progress: {selected_sheet}")
    
    def highlight_completed(val):
        v_str = str(val).strip().lower()
        if v_str in ['completed', '1', '100%']:
            return 'background-color: rgba(34, 139, 34, 0.2); color: #28a745; font-weight: bold;'
        return ''
    
    def format_value(val):
        if isinstance(val, (int, float)):
            if 0 < val <= 1: 
                return f"{int(val * 100)}%"
            elif val > 1: 
                return f"{int(val)}%"
        return val 

    if selected_sheet == "Development":
        for col in df_dpr.columns:
            if "commulative %" in str(col).lower():
                df_dpr[col] = df_dpr[col].apply(format_value)
            else:
                df_dpr[col] = df_dpr[col].apply(lambda x: int(x) if isinstance(x, (int, float)) and x == int(x) else x)
    else:
        df_dpr = df_dpr.applymap(format_value)
   
    st.dataframe(df_dpr.head(100).style.applymap(highlight_completed), use_container_width=True)

    st.divider()
    st.write("### 👷 Manpower Breakdown")
    
    chart_df = pd.DataFrame({
        "Category": df_labour_data.iloc[0:29, 2].astype(str).str.strip(), 
        "Pax": pd.to_numeric(df_labour_data.iloc[0:29, 13], errors='coerce').fillna(0)
    })
    chart_df = chart_df[~chart_df["Category"].str.lower().str.contains('manpower|nan|total')]
    chart_df = chart_df[chart_df["Pax"] > 0] 

    fig_man = px.bar(chart_df, x="Category", y="Pax", text="Pax", color_discrete_sequence=['#0C2C55'])
    fig_man.update_traces(textposition='outside', textfont=dict(color='black', weight='bold'))
    fig_man.update_layout(
        template='plotly_white', xaxis_tickangle=-45, height=600, 
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title=dict(text="Personnel Count", font=dict(color='black', size=14)),
        xaxis=dict(tickfont=dict(color='black', size=11, family='Arial', weight=600)),
        yaxis=dict(tickfont=dict(color='black', weight=600))
    )
    
    fig_man.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    st.plotly_chart(fig_man, use_container_width=True)

    st.sidebar.success("✅ Live Data Connected")

except Exception as e:
    st.error(f"⚠️ Syncing Error: {e}")
    st.info("Bhai, check kijiye ki dono Google Sheets 'Anyone with the link' par set hain.")


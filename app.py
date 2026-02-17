import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GMC Jalgaon MIS", layout="wide", page_icon="https://www.nyatigroup.com/Nyati-logo-seo.png")

DPR_ID = "1rC8g812mywE_5rmNVTkBcBzjEsgzRT_G2m6olrGht9I"
DLR_ID = "1nlWQjCqVvNJr7Syu701MVztEfYcGBH2K2r1NBsmE6tU"

DPR_LINK = f"https://docs.google.com/spreadsheets/d/{DPR_ID}/export?format=xlsx"
DLR_LINK = f"https://docs.google.com/spreadsheets/d/{DLR_ID}/export?format=xlsx"

st.markdown("""
    <style>
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    .block-container {padding-top: 1rem !important;}
    [data-testid="stMetricValue"] { font-size: 24px !important; font-weight: 600 !important; }
    </style>
    """, unsafe_allow_html=True)

header_col1, header_col2, header_col3 = st.columns([1, 4, 1])
with header_col1:
    st.image("https://www.govtjobsblog.in/wp-content/uploads/2023/08/HSCC.png", width=120) 
with header_col2:
    st.markdown("<h1 style='text-align: center; margin-top: -10px;'> Medical College Jalgaon</h1>", unsafe_allow_html=True)
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

    xls_dpr = pd.ExcelFile(DPR_LINK)
    show_sheets = ["MCB & HB", "Residential", "Ancillary", "Development"]
    available_sheets = [s for s in xls_dpr.sheet_names if s.strip() in show_sheets]
    
    if not available_sheets:
        available_sheets = [s for s in xls_dpr.sheet_names if s.strip() not in ["Priority", "Development DPR"]]

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


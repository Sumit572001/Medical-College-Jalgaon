import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="GMC Jalgaon MIS", layout="wide", page_icon="https://www.nyatigroup.com/Nyati-logo-seo.png")


# --- CSS FOR UI FIXES ---
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 24px !important; 
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricLabel"] p {
        font-size: 17px !important; 
        font-weight: 350 !important;
    }

    [data-testid="stHorizontalBlock"] {
        gap: 1.5rem !important;
    }

    /* Logo styling taaki wo corners mein fit rahein */
    .logo-container {
        display: flex;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER WITH LOGOS (HSCC on Left, Title in Middle, Nyati on Right) ---
header_col1, header_col2, header_col3 = st.columns([1, 4, 1])

with header_col1:
    # HSCC Logo (Left side) - Paste your link below
    st.image("https://www.govtjobsblog.in/wp-content/uploads/2023/08/HSCC.png", width=120) 
    # Agar link nahi hai toh: st.markdown("### HSCC")

with header_col2:
    st.markdown("<h1 style='text-align: center; margin-top: -10px;'> Medical College Jalgaon</h1>", unsafe_allow_html=True)

with header_col3:
    # Nyati Logo (Right side) - Paste your link below
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_SCCFqzFBiku7nsc76ytomhXnvIZ6rrHBQQ&s", width=120)
    # Agar link nahi hai toh: st.markdown("<h3 style='text-align: right;'>NYATI</h3>", unsafe_allow_html=True)

# --- REST OF YOUR CODE (NO CHANGES MADE BELOW) ---

# --- CUSTOM FUNCTION FOR HIGHLIGHTING ---
def highlight_completed(val):
    v_str = str(val).strip().lower()
    if v_str == 'completed' or v_str == '1' or v_str == '100%':
        return (
            'background-color: rgba(34, 139, 34, 0.2); ' 
            'color: #28a745; ' 
            'font-weight: bold; '
            'border: 1px solid rgba(40, 167, 69, 0.5) !important; ' 
            'border-radius: 4px;'
        )
    return 'border: 0.5px solid #444;' 

# 2. Sidebar
st.sidebar.title("📁 Upload Center")
dpr_file = st.sidebar.file_uploader("Upload DPR Excel", type=["xlsx"])
dlr_file = st.sidebar.file_uploader("Upload DLR (Labour) Excel", type=["xlsx"])

if dpr_file and dlr_file:
    try:
        # --- 1. DLR (LABOUR) PROCESSING ---
        df_dlr = pd.read_excel(dlr_file)
        total_pax = 0
        try:
            df_labour_data = pd.read_excel(dlr_file, skiprows=7) 
            df_labour_data = df_labour_data.dropna(subset=[df_labour_data.columns[1]])
            total_pax = pd.to_numeric(df_labour_data.iloc[:, 12], errors='coerce').sum()
        except:
            total_pax = 242 

        # --- TOP METRICS ---
        st.markdown("### 🏗️ Project Overview")
        
        d1, d2, d3 = st.columns(3)
        d1.metric("Start Date", "16 Mar 2023", "Project Start")
        d2.metric("End Date", "01 Apr 2026", "Completion")
        d3.metric("Tender Cost", "625 Cr.", "Project Value")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Plot Area", "65 Acres", "Total Site")
        m2.metric("Overall Progress", "88%", "MSP Linked")
        m3.metric("Total Manpower", f"{int(total_pax)} Pax", "Active")
        
        s1, s2 = st.columns(2)
        s1.metric("Client Name", "Hospital Services Consultancy Corporation (India) Limited (HSCC)", "Management")
        s2.metric("Contractor", "Nyati Engineers & Consultants Private Limited (NECPL)", "Execution")

        st.divider()

        # --- 2. DPR PROCESSING ---
        xls = pd.ExcelFile(dpr_file)
        available_sheets = [s for s in xls.sheet_names if s.strip() not in ["Priority", "Development DPR"]]
        selected_sheet = st.selectbox("Select Building View", available_sheets)

        search_query = st.text_input("🔍 Search Activity", "")
        
        df_dpr = pd.read_excel(dpr_file, sheet_name=selected_sheet, skiprows=6)
        df_dpr = df_dpr.dropna(how='all', axis=1).dropna(how='all', axis=0)

        if search_query:
            df_dpr = df_dpr[df_dpr.iloc[:, 1].astype(str).str.contains(search_query, case=False, na=False)]

        st.subheader(f"Detailed Progress: {selected_sheet}")
        
        styled_df = df_dpr.head(100).style.applymap(highlight_completed)
        st.dataframe(styled_df, use_container_width=True)

       # --- 3. CHARTS (Fixed Range B9:B37 & N9:N37) ---
        st.divider()
        st.write("### 👷 Manpower Breakdown")
        
        try:
            # 1. Data copy (Graph logic same rakha hai)
            df_plot = df_labour_data.copy()
            
            # 2. EXACT RANGE PICK KARNA (B9:B37 aur N9:N37)
            chart_df = pd.DataFrame({
                "Category": df_plot.iloc[0:29, 2].astype(str).str.strip(), 
                "Pax": pd.to_numeric(df_plot.iloc[0:29, 13], errors='coerce').fillna(0)
            })

            # 3. Safai (Filters same rakhe hain)
            chart_df = chart_df[~chart_df["Category"].str.lower().str.contains('manpower|nan|total')]
            chart_df = chart_df[chart_df["Pax"] > 0] 

            # 4. Bar Chart Create karna
            fig_man = px.bar(
                chart_df, 
                x="Category", 
                y="Pax",
                text="Pax",
                color_discrete_sequence=['#0C2C55'], 
                labels={"Pax": "Total Pax", "Category": "Work Category"}
            )

            # --- TEXT DARK & BOLD UPDATES START ---
            fig_man.update_traces(
                textposition='outside', 
                # Bars ke upar wale numbers ko dark bold kiya
                textfont=dict(color='Dark gray', size=12, weight='bold'), 
                
            )
            
            fig_man.update_layout(
                xaxis_tickangle=-45, 
                height=600, 
                # Neeche ke worker names (X-Axis) ko dark bold kiya
                xaxis=dict(
                    tickfont=dict(color='Dark gray', size=13, weight='bold'),
                    title=None
                ),
                # Side ka title aur numbers (Y-Axis) ko dark bold kiya
                yaxis=dict(
                    title=dict(
                        text="<b>Personnel Count</b>", 
                        font=dict(size=14, color='black')
                    ),
                    tickfont=dict(color='black', weight='bold')
                ),
                margin=dict(t=50, b=200), 
                plot_bgcolor='rgba(0,0,0,0)',
                bargap=0.05, 
            )
            # --- TEXT DARK & BOLD UPDATES END ---

            fig_man.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
            st.plotly_chart(fig_man, use_container_width=True)
            
        except Exception as chart_e:
            st.error(f"❌ Chart Error: {chart_e}")

    except Exception as main_e:
        st.error(f"⚠️ Global Error: {main_e}")

else:
    st.info("👈 Sidebar mein 'Browse Files' par click karke DPR aur DLR Excel upload karein.")



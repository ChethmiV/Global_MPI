import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration ---
st.set_page_config(page_title="Global MPI Dashboard", page_icon="🌍", layout="wide")

# --- Title and Introduction ---
st.markdown("<h1 style='text-align: center;'>Global Multidimensional Poverty Index (MPI)</h1>", unsafe_allow_html=True)
st.image("2.png", use_container_width=True)
st.markdown("""
<p font-size: 18px;'>
<strong>Understanding global poverty patterns and identifying high-risk regions and drivers.</strong><br>
Designed for the Global Conference on Sustainability to provide policymakers and finance professionals with actionable insights.<br>
<em>Aligns with UN Sustainable Development Goal (SDG) 1: End poverty in all its forms everywhere.</em>
</p>
""", unsafe_allow_html=True)

# --- Data Loading & Preprocessing ---
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_global_mpi.csv')
    df['Poverty Risk Level'] = df['MPI'].apply(
        lambda x: 'Extreme' if x > 0.4 else ('High' if x > 0.2 else 'Moderate')
    )
    return df

df = load_data()

# ==========================================
# SIDEBAR: THE ULTIMATE CONTROL PANEL
# ==========================================

# --- View Mode Selector ---
st.sidebar.subheader(" Dashboard View")
view_mode = st.sidebar.radio("Select View Mode", ["Executive View", "Detailed Analysis"])

st.sidebar.subheader("🔻 Filters")

# 1. Country Filter
country_list = ['All'] + sorted(df['Country'].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", country_list, key="country_select")

# 2. Dynamic Region Filter
if selected_country != 'All':
    region_options = ['All'] + sorted(df[df['Country'] == selected_country]['Admin 1 Name'].dropna().unique().tolist())
else:
    region_options = ['All'] + sorted(df['Admin 1 Name'].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", region_options, key="region_select")

# 3. Poverty Category Multiselect
category = st.sidebar.multiselect(
    "Poverty Risk Level",
    ["Extreme", "High", "Moderate"],
    default=["Extreme", "High", "Moderate"],
    help="Filter by the severity classification of the MPI.",
    key="risk_category"
)

# --- Analysis Settings ---
st.sidebar.subheader("📊 Analysis Settings")

# 4. Core Metric Selector
selected_metric = st.sidebar.selectbox(
    "Select Key Metric",
    ["MPI", "Headcount Ratio", "Intensity of Deprivation", "Vulnerable to Poverty", "In Severe Poverty"],
    key="core_metric"
)

# 5. Top N Selector
top_n = st.sidebar.slider("Top N Regions to Display", 5, 50, 10, 5, key="top_n_slider")

# --- Advanced Thresholds ---
st.sidebar.subheader("⚙️ Advanced")

# 6. Minimum MPI Threshold
min_mpi = float(df['MPI'].min())
max_mpi = float(df['MPI'].max())
mpi_threshold = st.sidebar.slider("Minimum MPI Threshold", min_value=min_mpi, max_value=max_mpi, value=min_mpi, key="mpi_slider")

# 7. Intensity Threshold
min_intensity = float(df['Intensity of Deprivation'].min())
max_intensity = float(df['Intensity of Deprivation'].max())
selected_intensity = st.sidebar.slider("Minimum Intensity (%)", min_value=min_intensity, max_value=max_intensity, value=min_intensity, key="intensity_slider")

# --- Reset Button ---
def reset_filters():
    st.session_state["country_select"] = "All"
    st.session_state["region_select"] = "All"
    st.session_state["risk_category"] = ["Extreme", "High", "Moderate"]
    st.session_state["core_metric"] = "MPI"
    st.session_state["top_n_slider"] = 10
    st.session_state["mpi_slider"] = float(df['MPI'].min())
    st.session_state["intensity_slider"] = float(df['Intensity of Deprivation'].min())

st.sidebar.button("🔄 Reset All Filters", on_click=reset_filters, use_container_width=True, type="primary")
st.sidebar.divider()
st.sidebar.info("Developed for the 5DATA004C Data Science Project Lifecycle coursework.")

# =========================================
# APPLY ALL SIDEBAR FILTERS LOGIC
# =========================================
filtered_df = df.copy()

if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Admin 1 Name'] == selected_region]

filtered_df = filtered_df[filtered_df['Poverty Risk Level'].isin(category)]
filtered_df = filtered_df[filtered_df['MPI'] >= mpi_threshold]
filtered_df = filtered_df[filtered_df['Intensity of Deprivation'] >= selected_intensity]



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

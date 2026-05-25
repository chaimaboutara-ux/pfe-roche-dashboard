import streamlit as st
import pandas as pd
import plotly.express as px
import random

# 1. Page Configuration
st.set_page_config(page_title="Roche Tunisia Field Insights Dashboard", layout="wide")

# 2. Machine Learning Simulation Logic (Task Force Ingestion Gateway)
def simulate_ai_classification(text_content):
    text_lower = text_content.lower()
    categories = {
        'Is_Actionable': 0, 'Cat_Access_And_Policy': 0, 'Cat_Competitor_Intelligence': 0,
        'Cat_Medical_Education_&_Practice': 0, 'Cat_Operations_And_Diagnostics': 0,
        'Cat_Stakeholder_Mapping': 0, 'Cat_Strategic_Partnership': 0, 'Cat_Promotional_Activity': 0
    }
    if "cnam" in text_lower or "remboursement" in text_lower or "dpm" in text_lower or "dossier" in text_lower:
        categories['Cat_Access_And_Policy'] = 1
        categories['Is_Actionable'] = 1
    if "bayer" in text_lower or "novartis" in text_lower or "concurrent" in text_lower or "part de marche" in text_lower:
        categories['Cat_Competitor_Intelligence'] = 1
    if "congres" in text_lower or "symposium" in text_lower or "formation" in text_lower or "kol" in text_lower:
        categories['Cat_Medical_Education_&_Practice'] = 1
    if "blocage" in text_lower or "attente" in text_lower or "depistage" in text_lower or "capacite" in text_lower:
        categories['Cat_Operations_And_Diagnostics'] = 1
        categories['Is_Actionable'] = 1
    if "comite" in text_lower or "commission" in text_lower or "conseil" in text_lower:
        categories['Cat_Stakeholder_Mapping'] = 1
    if "partenariat" in text_lower or "mou" in text_lower or "convention" in text_lower:
        categories['Cat_Strategic_Partnership'] = 1
        categories['Is_Actionable'] = 1
        
    if sum(categories.values()) == 0:
        chosen = random.choice(['Cat_Medical_Education_&_Practice', 'Cat_Promotional_Activity'])
        categories[chosen] = 1
    return categories

# 3. Robust Data Ingestion Layer
@st.cache_data
def load_data():
    df = pd.read_csv('Insights_Master_Augmented.csv')
    # Standardize and parse dates safely, handling anomalies via coercion
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    return df

df = load_data()

# =====================================================================
# 4. STRATEGIC SIDEBAR CONTROL PANEL
# =====================================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/f/f5/Roche_Logo.svg", width=140)
st.sidebar.title("Navigation & Filtres")
st.sidebar.markdown("---")

st.sidebar.subheader("Controles Data Dynamiques")

# Filter 1: Temporal Range Selection
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()

start_date, end_date = st.sidebar.date_input(
    "Periode Temporelle:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filter 2: Therapeutic Area / Regional Territory Ingestion
disease_areas = df['Territory'].dropna().unique()
selected_disease_areas = st.sidebar.multiselect(
    "Aire Therapeutique / Territoire:",
    options=disease_areas,
    default=disease_areas
)

# Filter 3: Product Portfolio Ingestion
products = df['Product_Clean'].dropna().unique()
selected_products = st.sidebar.multiselect(
    "Produit Roche:",
    options=products,
    default=products
)

# =====================================================================
# 5. DATA RENDERING & FILTER APPLICATION
# =====================================================================
filtered_df = df[
    (df['Date'].dt.date >= start_date) & 
    (df['Date'].dt.date <= end_date) & 
    (df

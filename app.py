import streamlit as st
import pandas as pd
import plotly.express as px
import random

# 1. Configuration de la page
st.set_page_config(page_title="Roche Tunisia Field Insights Dashboard", layout="wide")

# 2. Simulation de l'Intelligence Artificielle (Pour l'onglet Ingestion Task Force)
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

# 3. Chargement de la Base de Données
@st.cache_data
def load_data():
    df = pd.read_csv('Insights_Master_Augmented.csv')
    # Conversion de la colonne Date pour le bon fonctionnement du filtre temporel
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# =====================================================================
# 4. BARRE LATÉRALE DE NAVIGATION (LOGO & FILTRES STRATÉGIQUES)
# =====================================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/f/f5/Roche_Logo.svg", width=150)
st.sidebar.title("Insights Task Force")
st.sidebar.markdown("---")

st.sidebar.subheader("🎛️ Dynamic Master Controls")

# --- FILTRE 1 : SÉLECTEUR DE PLAGE DE DATES ---
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()

start_date, end_date = st.sidebar.date_input(
    "📅 Date Range Period:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# --- FILTRE 2 : SÉLECTEUR D'AIRE THÉRAPEUTIQUE (DISEASE AREA) ---
# Se base sur la colonne 'Territory' de ta base de données
disease_areas = df['Territory'].dropna().unique()
selected_disease_areas = st.sidebar.multiselect(
    "🏥 Disease Area / Territory:",
    options=disease_areas,
    default=disease_areas
)

# --- FILTRE 3 : SÉLECTEUR DE PRODUITS ---
products = df['Product_Clean'].dropna().unique()
selected_products = st.sidebar.multiselect(
    "📦 Roche Products Filter:",
    options=products,
    default=products
)

# =====================================================================
# 5. APPLICATION DES FILTRES SUR LE DATAFRAME GLOBAL
# =====================================================================
filtered_df = df[
    (df['Date'].dt.date >= start_date) & 
    (df['Date'].dt.date <= end_date) & 
    (df['Territory'].isin(selected_disease_areas)) & 
    (df['Product_Clean'].isin(selected_products))
]

# 6. Structure des Onglets Principaux
tab1, tab2 = st.tabs(["📊 Executive KPI Dashboard", "📥 Task Force Ingestion Engine"])

# =====================================================================
# TAB 1: EXECUTIVE KPI DASHBOARD
# =====================================================================
with tab1:
    st.title("🇹🇳 Strategic Field Intelligence Platform")
    st.subheader("Roche Tunisia Affiliate — Cross-Functional Performance")
    st.markdown("Transforming qualitative healthcare ecosystem data into automated operational actions.")
    st.markdown("---")
    
    # Cartes d'indicateurs clés (KPIs)
    total_insights = len(filtered_df)
    actionable_count = filtered_df['Is_Actionable'].sum()
    actionable_rate = (actionable_count / total_insights * 100) if total_insights > 0 else 0

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(label="Total Filtered Insights", value=f"{total_insights} rows")
    with kpi2:
        st.metric(label="Actionable Red Flags Identified", value=f"{actionable_count} insights")
    with kpi3:
        st.metric(label="Field Actionability Rate", value=f"{actionable_rate:.1f}%")

    st.markdown("---")

    # Rangée des graphiques analytiques
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Volume Share of Strategic Pillars")
        target_cols = [
            'Cat_Access_And_Policy', 'Cat_Competitor_Intelligence', 
            'Cat_Medical_Education_&_Practice', 'Cat_Operations_And_Diagnostics', 
            'Cat_Stakeholder_Mapping', 'Cat_Strategic_Partnership', 'Cat_Promotional_Activity'
        ]
        category_counts = filtered_df[target_cols].sum().reset_index()
        category_counts.columns = ['Strategic Pillar', 'Insight Count']
        category_counts['Strategic Pillar'] = category_counts['Strategic Pillar'].str.replace('Cat_', '').str.replace('_', ' ')
        
        fig_pillar = px.bar(
            category_counts.sort_values(by='Insight Count', ascending=True), 
            x='Insight Count', 
            y='Strategic Pillar', 
            orientation='h', 
            color='Insight Count', 
            color_continuous_scale='Blugrn', 
            text_auto=True
        )
        fig_pillar.update_layout(showlegend=False, height=320)
        st.plotly_chart(fig_pillar, use_container_width=True)

    with col2:
        st.subheader("🏥 Top Account Hotspots (HCOs)")
        hco_counts = filtered_df['hco'].value_counts().head(6).reset_index()
        hco_counts.columns = ['Hospital / HCO', 'Total Insights']
        
        fig_hco = px.bar(
            hco_counts, 
            x='Hospital / HCO', 
            y='Total Insights', 
            color='Total Insights', 
            color_continuous_scale='Blues', 
            text_auto=True
        )
        fig_hco.update_layout(xaxis_tickangle=-25, showlegend=False, height=320)
        st.plotly_chart(fig_hco, use_container_width=True)

    st.markdown("---")
    st.subheader("🔍 Real-time Insight Audit Stream")
    
    display_df = filtered_df.copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    st.dataframe(
        display_df[['Date', 'Territory', 'Product_Clean', 'insight title', 'insight description', 'Category_ML']], 
        height=250, 
        use_container_width=True
    )

# =====================================================================
# TAB 2: OMNI-CHANNEL INGESTION (Task Force Gateway)
# =====================================================================
with tab2:
    st.title("📥 Omni-Channel Centralization Hub")
    st.subheader("Insights Automation Task Force Gateway")
    st.markdown("Use this staging gateway to manually log text snippets intercepted from fragmented communication vectors.")
    st.markdown("---")
    
    ingest_col1, ingest_col2 = st.columns([2, 3])
    
    with ingest_col1:
        st.markdown("### 📝 Core Data Entry")
        source_channel = st.selectbox("Captured From Source Channel:", ["Outlook Corporate Email", "Microsoft Teams Chat Group", "WhatsApp Cross-Functional Group", "Leadership Direct Memo", "Manual Google Sheet Tracker"])
        entered_product = st.selectbox("Target Product Context:", ["Hemlibra", "Vabysmo", "Phesgo", "Ocrevus", "Tecentriq", "General/Other"])
        entered_territory = st.selectbox("Therapeutic Franchise Area (Disease Area):", ["Hematology", "Ophthalmology", "Oncology", "Neurology", "Cross-TA"])
        insight_title = st.text_input("Insight Title Headline:", placeholder="e.g., Competitor Symposium Notification")
        raw_text = st.text_area("Paste Raw Intercepted Text / Description:", height=150, placeholder="Paste text here...")
        
        analyze_button = st.button("⚡ Process & Inject into Master Platform")
        
    with ingest_col2:
        st.markdown("### 🤖 Real-Time Machine Learning Diagnostic Engine")
        
        if analyze_button and raw_text:
            st.success(f"Successfully processed unstructured insight from: **{source_channel}**")
            predictions = simulate_ai_classification(raw_text)
            
            st.markdown("#### **AI Multi-Label Target Allocations:**")
            for key, val in predictions.items():
                if val == 1:
                    st.markdown(f"🟢 **`{key.replace('Cat_', '').replace('_', ' ')}`** allocated successfully.")
            
            st.markdown("#### 💡 **Automated Tactical Actions Matrix:**")
            if predictions['Cat_Access_And_Policy'] == 1:
                st.info("🔹 **[MARKET ACCESS ACTION]:** Route immediately to the Access Team lead. Cross-verify dossier validation bottlenecks.")
            if predictions['Cat_Competitor_Intelligence'] == 1:
                st.warning("🔹 **[COMMERCIAL INTEL ACTION]:** Dispatch alert payload to the dedicated Brand Manager.")
            if predictions['Cat_Medical_Education_&_Practice'] == 1:
                st.info("🔹 **[MEDICAL AFFAIRS ACTION]:** Coordinate with the Medical Science Liaison (MSL).")
            if predictions['Cat_Operations_And_Diagnostics'] == 1:
                st.success("🔹 **[HEALTHCARE ECOSYSTEM ACTION]:** Notify Patient Journey Partners (PJP).")
                
            if predictions['Is_Actionable'] == 1:
                st.error("⚠️ **[CRITICAL ESCALATION PROTOCOL]:** This insight has been flagged as highly operational. Action required within 48h.")
        else:
            st.info("Awaiting task force text payload... Input parameters and text on the left, then click 'Process & Inject'.")

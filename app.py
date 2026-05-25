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
# 5. DATA RENDERING & FILTER APPLICATION (Fixed Parentheses Syntax)
# =====================================================================
date_condition = (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)
territory_condition = df['Territory'].isin(selected_disease_areas)
product_condition = df['Product_Clean'].isin(selected_products)

filtered_df = df[date_condition & territory_condition & product_condition]

# Primary Architecture Tabs
tab1, tab2 = st.tabs(["Tableau de Bord Executif (KPI)", "Portail d'Ingestion Omnicanal"])

# =====================================================================
# TAB 1: EXECUTIVE KPI DASHBOARD
# =====================================================================
with tab1:
    st.title("Plateforme de Veille Strategique Locale")
    st.subheader("Roche Tunisia Affiliee — Dashboard d'Analyse Finie")
    st.markdown("Transformation automatique des donnees qualitatives fragmentees de l'ecosysteme en indicateurs decisionnels.")
    st.markdown("---")
    
    # Mathematical aggregation for key performance indicators
    total_insights = len(filtered_df)
    actionable_count = filtered_df['Is_Actionable'].sum()
    actionable_rate = (actionable_count / total_insights * 100) if total_insights > 0 else 0

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(label="Total des Insights Traites", value=f"{total_insights} lignes")
    with kpi2:
        st.metric(label="Alertes Actionnables Identifiees", value=f"{actionable_count} insights")
    with kpi3:
        st.metric(label="Taux d'Actionnabilite", value=f"{actionable_rate:.1f}%")

    st.markdown("---")

    # Analytical Data Visualization Row
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Volume Partage par Piliers Strategiques")
        target_cols = [
            'Cat_Access_And_Policy', 'Cat_Competitor_Intelligence', 
            'Cat_Medical_Education_&_Practice', 'Cat_Operations_And_Diagnostics', 
            'Cat_Stakeholder_Mapping', 'Cat_Strategic_Partnership', 'Cat_Promotional_Activity'
        ]
        category_counts = filtered_df[target_cols].sum().reset_index()
        category_counts.columns = ['Pilier Strategique', 'Nombre d\'Insights']
        category_counts['Pilier Strategique'] = category_counts['Pilier Strategique'].str.replace('Cat_', '').str.replace('_', ' ')
        
        fig_pillar = px.bar(
            category_counts.sort_values(by='Nombre d\'Insights', ascending=True), 
            x='Nombre d\'Insights', 
            y='Pilier Strategique', 
            orientation='h', 
            color='Nombre d\'Insights', 
            color_continuous_scale='Blues', 
            text_auto=True
        )
        fig_pillar.update_layout(showlegend=False, height=320)
        st.plotly_chart(fig_pillar, use_container_width=True)

    with col2:
        st.subheader("Distribution des Comptes Institutionnels Principaux (HCOs)")
        hco_counts = filtered_df['hco'].value_counts().head(6).reset_index()
        hco_counts.columns = ['Etablissement / HCO', 'Total Insights']
        
        fig_hco = px.bar(
            hco_counts, 
            x='Etablissement / HCO', 
            y='Total Insights', 
            color='Total Insights', 
            color_continuous_scale='Blues',
            text_auto=True
        )
        fig_hco.update_layout(xaxis_tickangle=-25, showlegend=False, height=320)
        st.plotly_chart(fig_hco, use_container_width=True)

    st.markdown("---")
    st.subheader("Flux d'Audit des Insights en Temps Reel")
    
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
    st.title("Module de Centralisation Omnicanal")
    st.subheader("Staging Ingestion Gateway — Insights Automation Task Force")
    st.markdown("Interface reservee a la Task Force locale pour indexer les flux informels captures hors-plateforme.")
    st.markdown("---")
    
    ingest_col1, ingest_col2 = st.columns([2, 3])
    
    with ingest_col1:
        st.markdown("### Saisie des Donnees Brutes")
        source_channel = st.selectbox("Canal de Capture Initial:", ["Outlook Corporate Email", "Microsoft Teams Chat Group", "WhatsApp Cross-Functional Group", "Leadership Direct Memo", "Manual Google Sheet Tracker"])
        entered_product = st.selectbox("Produit Concerne:", ["Hemlibra", "Vabysmo", "Phesgo", "Ocrevus", "Tecentriq", "General/Other"])
        entered_territory = st.selectbox("Aire Therapeutique (Franchise Area):", ["Hematology", "Ophthalmology", "Oncology", "Neurology", "Cross-TA"])
        insight_title = st.text_input("Titre Distinctif de l'Insight:", placeholder="Ex: Retard Dossier de Remboursement CNAM")
        raw_text = st.text_area("Contenu Unidimensionnel / Texte Brut Intercepte:", height=150, placeholder="Collez le texte brut ou l'e-mail ici...")
        
        analyze_button = st.button("Executer l'Analyse Algorithmique")
        
    with ingest_col2:
        st.markdown("### Diagnostic Multi-Label Applique (Machine Learning)")
        
        if analyze_button and raw_text:
            st.success(f"Traitement finalise pour le canal source : {source_channel}")
            predictions = simulate_ai_classification(raw_text)
            
            st.markdown("#### **Allocations Cibles Algorithmiques :**")
            for key, val in predictions.items():
                if val == 1:
                    st.info(f"Classification active : **`{key.replace('Cat_', '').replace('_', ' ')}`**")
            
            st.markdown("#### **Matrice Directrice d'Actions Tactiques (Decision-Support) :**")
            if predictions['Cat_Access_And_Policy'] == 1:
                st.warning("Directive : Transmission immediate au responsable Market Access. Analyse requise des goulots d'etranglement administratifs.")
            if predictions['Cat_Competitor_Intelligence'] == 1:
                st.warning("Directive : Alerte strategique transmise au Brand Manager. Surveillance requise des dynamiques de parts de marche concurrentielles.")
            if predictions['Cat_Medical_Education_&_Practice'] == 1:
                st.warning("Directive : Notification envoyee aux Medical Science Liaisons (MSL) pour contextualisation scientifique lors du prochain atelier.")
            if predictions['Cat_Operations_And_Diagnostics'] == 1:
                st.warning("Directive : Liaison Patient Journey Partner (PJP). Optimisation necessaire des parcours de soins et des capacites hospitalieres.")
                
            if predictions['Is_Actionable'] == 1:
                st.error("Protocole d'Escalade Strategique Urgent : Entree qualifiee de hautement operationnelle. Alignement requis sous 48 heures.")
        else:
            st.info("En attente de flux textuel brut. Veuillez renseigner le formulaire de gauche et executer l'analyse.")

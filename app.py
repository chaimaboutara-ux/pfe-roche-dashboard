import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration (The tab title and layout)
st.set_page_config(page_title="Roche Tunisia Field Insights Dashboard", layout="wide")

# 2. Load the augmented dataset
@st.cache_data # This keeps the dashboard running incredibly fast
def load_data():
    df = pd.read_csv('Insights_Master_Augmented.csv')
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/f/f5/Roche_Logo.svg", width=150)
st.sidebar.title("Strategic Navigation")
st.sidebar.markdown("Filter insights dynamically to analyze specific local performance indicators.")

selected_product = st.sidebar.multiselect(
    "Filter by Roche Product:",
    options=df['Product_Clean'].unique(),
    default=df['Product_Clean'].unique()
)

selected_territory = st.sidebar.multiselect(
    "Filter by Therapeutic Area:",
    options=df['Territory'].unique(),
    default=df['Territory'].unique()
)

# Apply filters to the dataframe
filtered_df = df[
    (df['Product_Clean'].isin(selected_product)) & 
    (df['Territory'].isin(selected_territory))
]

# 4. Dashboard Main Header
st.title("🇹🇳 Strategic Field Intelligence Platform")
st.subheader("Roche Tunisia Affiliate — Cross-Functional KPI Dashboard")
st.markdown("Transforming qualitative healthcare ecosystem data into automated operational actions.")

st.markdown("---")

# 5. KPI Highlight Cards (Top Row)
total_insights = len(filtered_df)
actionable_count = filtered_df['Is_Actionable'].sum()
actionable_rate = (actionable_count / total_insights * 100) if total_insights > 0 else 0

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="Total Processed Insights", value=f"{total_insights} rows")
with kpi2:
    st.metric(label="Actionable Red Flags Identified", value=f"{actionable_count} insights")
with kpi3:
    st.metric(label="Field Actionability Rate", value=f"{actionable_rate:.1f}%")

st.markdown("---")

# 6. Graphs Grid Layout (Middle Row)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Volume Share of Strategic Pillars")
    # Sum up all the binary column counts
    target_cols = [
        'Cat_Access_And_Policy', 'Cat_Competitor_Intelligence', 
        'Cat_Medical_Education_&_Practice', 'Cat_Operations_And_Diagnostics', 
        'Cat_Stakeholder_Mapping', 'Cat_Strategic_Partnership', 'Cat_Promotional_Activity'
    ]
    
    category_counts = filtered_df[target_cols].sum().reset_index()
    category_counts.columns = ['Strategic Pillar', 'Insight Count']
    # Format labels for cleaner layout
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
    fig_pillar.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig_pillar, use_container_width=True)

with col2:
    st.subheader("🏥 Top Institutional Account Hotspots (HCOs)")
    # Get top 8 hospitals generating strategic data
    hco_counts = filtered_df['hco'].value_counts().head(8).reset_index()
    hco_counts.columns = ['Hospital / HCO', 'Total Insights']
    
    fig_hco = px.bar(
        hco_counts,
        x='Hospital / HCO',
        y='Total Insights',
        color='Total Insights',
        color_continuous_scale='Blues',
        text_auto=True
    )
    fig_hco.update_layout(xaxis_tickangle=-35, showlegend=False, height=350)
    st.plotly_chart(fig_hco, use_container_width=True)

st.markdown("---")

# 7. Lower Section: Product Matrix & Deep Dive Table
col3, col4 = st.columns([2, 3])

with col3:
    st.subheader("📦 Actionable Priority Matrix by Product")
    product_matrix = filtered_df.groupby('Product_Clean')['Is_Actionable'].sum().reset_index()
    product_matrix.columns = ['Product', 'Actionable Flares']
    
    fig_prod = px.pie(
        product_matrix, 
        values='Actionable Flares', 
        names='Product', 
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Plotly3
    )
    fig_prod.update_layout(height=350)
    st.plotly_chart(fig_prod, use_container_width=True)

with col4:
    st.subheader("🔍 Real-time Insight Audit Stream")
    # Display raw details of selected records directly on screen
    display_df = filtered_df[['Date', 'Product_Clean', 'insight title', 'insight description', 'Category_ML']]
    st.dataframe(display_df, height=330, use_container_width=True)

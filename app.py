import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# ── CONFIGURATION ──────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Ventes",
    page_icon="",
    layout="wide"
)

# ── CHARGEMENT DES DONNÉES ──────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    return df

df = load_data()

# ── SIDEBAR FILTRES ─────────────────────────────────────────────
st.sidebar.title(" Filtres")

years = sorted(df["Year"].unique())
selected_years = st.sidebar.multiselect("Année", years, default=years)

regions = sorted(df["Region"].unique())
selected_regions = st.sidebar.multiselect("Région", regions, default=regions)

categories = sorted(df["Category"].unique())
selected_categories = st.sidebar.multiselect("Catégorie", categories, default=categories)

# Filtrage
df_filtered = df[
    (df["Year"].isin(selected_years)) &
    (df["Region"].isin(selected_regions)) &
    (df["Category"].isin(selected_categories))
]

# ── TITRE ───────────────────────────────────────────────────────
st.title(" Dashboard Analyse des Ventes")
st.markdown("---")

# ── KPIs ────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(" Chiffre d'affaires", f"${df_filtered['Sales'].sum():,.0f}")
with col2:
    st.metric(" Commandes", f"{df_filtered['Order ID'].nunique():,}")
with col3:
    st.metric(" Profit total", f"${df_filtered['Profit'].sum():,.0f}")
with col4:
    st.metric(" Clients", f"{df_filtered['Customer ID'].nunique():,}")

st.markdown("---")

# ── GRAPHIQUES LIGNE 1 ──────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader(" Ventes par catégorie")
    cat_sales = df_filtered.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=cat_sales.values, y=cat_sales.index, palette="Blues_d", ax=ax)
    ax.set_xlabel("Ventes ($)")
    ax.set_ylabel("")
    st.pyplot(fig)

with col2:
    st.subheader(" Ventes par région")
    reg_sales = df_filtered.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = ["#003366", "#005599", "#0077cc", "#3399ff"]
    ax.pie(reg_sales.values, labels=reg_sales.index, autopct="%1.1f%%", colors=colors)
    st.pyplot(fig)

st.markdown("---")

# ── GRAPHIQUES LIGNE 2 ──────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader(" Évolution des ventes dans le temps")
    time_sales = df_filtered.groupby(df_filtered["Order Date"].dt.to_period("M"))["Sales"].sum()
    time_sales.index = time_sales.index.astype(str)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(time_sales.index, time_sales.values, color="#003366", linewidth=2)
    ax.set_xlabel("Mois")
    ax.set_ylabel("Ventes ($)")
    plt.xticks(rotation=45, fontsize=7)
    st.pyplot(fig)

with col2:
    st.subheader(" Top 10 sous-catégories")
    sub_sales = df_filtered.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=sub_sales.values, y=sub_sales.index, palette="Blues_d", ax=ax)
    ax.set_xlabel("Ventes ($)")
    ax.set_ylabel("")
    st.pyplot(fig)

st.markdown("---")

# ── TABLEAU ─────────────────────────────────────────────────────
st.subheader(" Données détaillées")
st.dataframe(
    df_filtered[["Order Date", "Customer Name", "Category", "Sub-Category", "Sales", "Profit", "Region"]]
    .sort_values("Order Date", ascending=False)
    .head(50),
    use_container_width=True
)
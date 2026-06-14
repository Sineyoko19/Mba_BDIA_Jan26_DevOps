import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Airbnb Market Intelligence",
    page_icon="🏠",
    layout="wide"
)

DB_PATH = Path(__file__).parent.parent / "airbnb_analytics_platform" / "dev.duckdb"

@st.cache_resource
def get_conn():
    return duckdb.connect(str(DB_PATH), read_only=True)

def run_query(sql: str) -> pd.DataFrame:
    conn = get_conn()
    return conn.execute(sql).fetchdf()


# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/6/69/Airbnb_Logo_Bélo.svg",
    width=130
)

st.sidebar.title("Filters")

room_types = run_query("SELECT DISTINCT room_type FROM gold_listings ORDER BY 1")["room_type"].tolist()
selected_rooms = st.sidebar.multiselect("Room type", room_types, default=room_types)

price_min, price_max = run_query("SELECT MIN(price), MAX(price) FROM gold_listings").values[0]
price_range = st.sidebar.slider(
    "Price range (€)",
    float(price_min),
    float(price_max),
    (float(price_min), float(price_max))
)

superhost_mode = st.sidebar.radio("Superhost filter", ["All", "Yes", "No"])
superhost_sql = ""
if superhost_mode == "Yes":
    superhost_sql = "AND is_superhost = TRUE"
elif superhost_mode == "No":
    superhost_sql = "AND is_superhost = FALSE"

rooms_sql = ",".join([f"'{r}'" for r in selected_rooms])


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("🏠 Airbnb Market Intelligence Dashboard")
st.caption("Data-driven view of Airbnb supply, hosts and customer satisfaction")

st.divider()


# ─────────────────────────────────────────────
# KPI SECTION (BUSINESS ORIENTED)
# ─────────────────────────────────────────────
kpi = run_query(f"""
SELECT
    COUNT(DISTINCT listing_id) AS listings,
    ROUND(AVG(price),2) AS avg_price,
    SUM(total_reviews) AS reviews,
    ROUND(AVG(positive_rate_pct),1) AS satisfaction,
    ROUND(AVG(price / NULLIF(total_reviews,0)),2) AS price_efficiency
FROM gold_listings
WHERE room_type IN ({rooms_sql})
AND price BETWEEN {price_range[0]} AND {price_range[1]}
{superhost_sql}
""")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Listings", int(kpi["listings"][0]))
c2.metric("Avg price (€)", f"{kpi['avg_price'][0]:.0f}")
c3.metric("Reviews", int(kpi["reviews"][0]))
c4.metric("Satisfaction (%)", f"{kpi['satisfaction'][0]:.1f}")
c5.metric("Price efficiency", f"{kpi['price_efficiency'][0]:.2f}")

st.divider()


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Market", "Hosts", "Customer", "External factors"
])


# ─────────────────────────────────────────────
# TAB 1 - MARKET STRUCTURE
# ─────────────────────────────────────────────
with tab1:
    st.subheader("Market structure & pricing behaviour")

    df_market = run_query(f"""
    SELECT
        room_type,
        COUNT(*) AS listings,
        ROUND(AVG(price),2) AS avg_price,
        ROUND(AVG(total_reviews),1) AS avg_reviews
    FROM gold_listings
    WHERE room_type IN ({rooms_sql})
    AND price BETWEEN {price_range[0]} AND {price_range[1]}
    {superhost_sql}
    GROUP BY room_type
    ORDER BY listings DESC
    """)

    col1, col2 = st.columns(2)

    fig1 = px.pie(df_market, names="room_type", values="listings")
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(df_market, x="room_type", y="avg_price")
    col2.plotly_chart(fig2, use_container_width=True)

    st.dataframe(df_market, use_container_width=True)


# ─────────────────────────────────────────────
# TAB 2 - HOST ANALYSIS
# ─────────────────────────────────────────────
with tab2:
    st.subheader("Host performance segmentation")

    df_hosts = run_query("""
    SELECT
        is_superhost,
        COUNT(DISTINCT host_id) AS hosts,
        ROUND(AVG(nb_listings),1) AS avg_portfolio_size,
        ROUND(AVG(positive_rate_pct),1) AS satisfaction,
        ROUND(AVG(avg_price),2) AS avg_price
    FROM gold_hosts
    GROUP BY is_superhost
    """)

    df_hosts["segment"] = df_hosts["is_superhost"].fillna(False).map(
    lambda x: "Superhost" if x else "Standard"
)

    col1, col2 = st.columns(2)

    fig3 = px.bar(df_hosts, x="segment", y="satisfaction")
    col1.plotly_chart(fig3, use_container_width=True)

    fig4 = px.bar(df_hosts, x="segment", y="avg_portfolio_size")
    col2.plotly_chart(fig4, use_container_width=True)

    st.dataframe(df_hosts, use_container_width=True)


# ─────────────────────────────────────────────
# TAB 3 - CUSTOMER EXPERIENCE
# ─────────────────────────────────────────────
with tab3:
    st.subheader("Customer experience analysis")

    df_sent = run_query("""
    SELECT
        sentiment,
        SUM(nb_reviews) AS reviews,
        ROUND(SUM(nb_reviews)*100.0 / SUM(SUM(nb_reviews)) OVER (),1) AS share
    FROM gold_reviews
    GROUP BY sentiment
    """)

    fig5 = px.pie(df_sent, names="sentiment", values="reviews")
    st.plotly_chart(fig5, use_container_width=True)

    st.dataframe(df_sent, use_container_width=True)


# ─────────────────────────────────────────────
# TAB 4 - EXTERNAL FACTORS
# ─────────────────────────────────────────────
with tab4:
    st.subheader("External signal analysis")

    st.info("Testing whether external cycles influence customer perception")

    df_moon = run_query("""
    SELECT
        CASE WHEN is_near_full_moon THEN 'Full moon' ELSE 'Normal' END AS period,
        sentiment,
        pct_within_period
    FROM gold_full_moon_dates
    """)

    fig6 = px.bar(
        df_moon,
        x="period",
        y="pct_within_period",
        color="sentiment",
        barmode="group"
    )

    st.plotly_chart(fig6, use_container_width=True)

    st.dataframe(df_moon, use_container_width=True)


st.divider()
st.caption("Airbnb Market Intelligence - MBA Data Project 2026")
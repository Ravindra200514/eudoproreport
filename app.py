"""
EduPro — Learner Demographics & Course Enrollment Analysis
Streamlit Dashboard  |  Enhanced Version
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import warnings
warnings.filterwarnings("ignore")

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduPro Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Dark gradient background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 18px 22px;
    backdrop-filter: blur(10px);
    transition: transform .2s;
}
[data-testid="stMetric"]:hover { transform: translateY(-3px); }

[data-testid="stMetricLabel"]  { color: #94a3b8 !important; font-size: 13px !important; }
[data-testid="stMetricValue"]  { color: #f8fafc !important; font-size: 28px !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"]  { color: #34d399 !important; }

/* Headers */
h1, h2, h3 { color: #f8fafc !important; }

/* Section dividers */
hr { border-color: rgba(255,255,255,0.1); }

/* Tabs */
[data-baseweb="tab-list"] { background: rgba(255,255,255,0.05); border-radius: 12px; }
[data-baseweb="tab"]      { color: #94a3b8 !important; }
[aria-selected="true"]    { color: #818cf8 !important; background: rgba(129,140,248,0.12) !important; border-radius: 8px; }

/* Selectbox / multiselect */
[data-baseweb="select"] > div { background: rgba(255,255,255,0.07) !important; border-color: rgba(255,255,255,0.12) !important; color: #f8fafc !important; }
</style>
""", unsafe_allow_html=True)

PLOTLY_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e2e8f0",
    margin=dict(l=20, r=20, t=40, b=20),
)
PALETTE = px.colors.qualitative.Vivid

# ─── Data Loading ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    data_dir = "data"
    if not os.path.exists(data_dir):
        st.error("⚠️  Data folder not found. Run `python generate_data.py` first.")
        st.stop()
    users  = pd.read_csv(f"{data_dir}/users.csv",        parse_dates=["join_date"])
    courses= pd.read_csv(f"{data_dir}/courses.csv",      parse_dates=["launch_date"])
    txns   = pd.read_csv(f"{data_dir}/transactions.csv", parse_dates=["enroll_date"])
    # Merge
    df = txns.merge(users, on="user_id").merge(courses, on="course_id")
    df["enroll_year"]  = df["enroll_date"].dt.year
    df["enroll_month"] = df["enroll_date"].dt.to_period("M").astype(str)
    df["age_group"]    = pd.cut(df["age"], bins=[17,24,34,44,54,65],
                                labels=["18-24","25-34","35-44","45-54","55-65"])
    return users, courses, txns, df

users, courses, txns, df = load_data()

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 EduPro Analytics")
    st.markdown("---")

    selected_countries = st.multiselect(
        "🌍 Countries",
        options=sorted(df["country"].unique()),
        default=sorted(df["country"].unique()),
    )
    selected_categories = st.multiselect(
        "📚 Categories",
        options=sorted(df["category"].unique()),
        default=sorted(df["category"].unique()),
    )
    selected_levels = st.multiselect(
        "📊 Course Level",
        options=["Beginner", "Intermediate", "Advanced"],
        default=["Beginner", "Intermediate", "Advanced"],
    )
    selected_subs = st.multiselect(
        "💎 Subscription",
        options=["Free", "Basic", "Premium"],
        default=["Free", "Basic", "Premium"],
    )
    st.markdown("---")
    st.caption("Data auto-refreshes on filter change.")

# ─── Apply Filters ────────────────────────────────────────────────────────────
mask = (
    df["country"].isin(selected_countries) &
    df["category"].isin(selected_categories) &
    df["level"].isin(selected_levels) &
    df["subscription"].isin(selected_subs)
)
fdf = df[mask].copy()

# ─── Hero Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 28px 0 10px;">
    <h1 style="font-size:2.6rem; background: linear-gradient(90deg,#818cf8,#34d399,#f472b6);
               -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        🎓 EduPro Learner Analytics
    </h1>
    <p style="color:#94a3b8; font-size:1rem; margin-top:-8px;">
        Learner Demographics · Course Enrollment · Revenue Intelligence
    </p>
</div>
""", unsafe_allow_html=True)

# ─── KPI Row ──────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("👤 Learners",       f"{fdf['user_id'].nunique():,}")
k2.metric("📚 Courses",        f"{fdf['course_id'].nunique():,}")
k3.metric("📋 Enrollments",    f"{len(fdf):,}")
k4.metric("💰 Revenue (USD)",  f"${fdf['price_paid_usd'].sum():,.0f}")
k5.metric("✅ Completion Rate", f"{(fdf['completion_status']=='Completed').mean()*100:.1f}%")

st.markdown("---")

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "👥 Demographics",
    "📈 Enrollment Trends",
    "📚 Course Insights",
    "💰 Revenue",
    "🌍 Geo Analysis",
    "🔍 Deep Dive",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DEMOGRAPHICS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Age Distribution")
        fig = px.histogram(fdf.drop_duplicates("user_id"), x="age", nbins=30,
                           color_discrete_sequence=["#818cf8"], **PLOTLY_THEME)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Gender Split")
        g = fdf.drop_duplicates("user_id")["gender"].value_counts().reset_index()
        g.columns = ["gender", "count"]
        fig = px.pie(g, names="gender", values="count",
                     color_discrete_sequence=PALETTE, hole=0.55, **PLOTLY_THEME)
        fig.update_traces(textfont_size=13)
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Subscription Type")
        s = fdf.drop_duplicates("user_id")["subscription"].value_counts().reset_index()
        s.columns = ["sub", "count"]
        fig = px.bar(s, x="sub", y="count", color="sub",
                     color_discrete_sequence=["#34d399","#818cf8","#f472b6"],
                     **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.subheader("Referral Source")
        r = fdf.drop_duplicates("user_id")["referral_source"].value_counts().reset_index()
        r.columns = ["source", "count"]
        fig = px.funnel(r, x="count", y="source",
                        color_discrete_sequence=["#f472b6"], **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Age Group × Subscription Heatmap")
    heat = fdf.drop_duplicates("user_id").groupby(["age_group","subscription"]).size().unstack(fill_value=0)
    fig = px.imshow(heat, color_continuous_scale="Viridis",
                    aspect="auto", **PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ENROLLMENT TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.subheader("Monthly Enrollment Trend")
    monthly = fdf.groupby("enroll_month").size().reset_index(name="enrollments")
    monthly = monthly.sort_values("enroll_month")
    fig = px.area(monthly, x="enroll_month", y="enrollments",
                  color_discrete_sequence=["#818cf8"], **PLOTLY_THEME)
    fig.update_traces(fill="tozeroy", line_width=2)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Enrollments by Category")
        cat = fdf["category"].value_counts().reset_index()
        cat.columns = ["category", "count"]
        fig = px.bar(cat, x="count", y="category", orientation="h",
                     color="count", color_continuous_scale="Viridis", **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Completion Status Breakdown")
        cs = fdf["completion_status"].value_counts().reset_index()
        cs.columns = ["status", "count"]
        fig = px.pie(cs, names="status", values="count", hole=0.5,
                     color_discrete_sequence=["#34d399","#818cf8","#f472b6","#fbbf24"],
                     **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Device Usage Over Time")
    dev = fdf.groupby(["enroll_month","device"]).size().reset_index(name="count")
    dev = dev.sort_values("enroll_month")
    fig = px.line(dev, x="enroll_month", y="count", color="device",
                  color_discrete_sequence=PALETTE, **PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — COURSE INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top 15 Courses by Enrollments")
        top = fdf.groupby("title").size().nlargest(15).reset_index(name="enrollments")
        fig = px.bar(top, x="enrollments", y="title", orientation="h",
                     color="enrollments", color_continuous_scale="Plasma", **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Rating Distribution by Level")
        fig = px.violin(fdf, x="level", y="rating", color="level",
                        color_discrete_sequence=["#34d399","#818cf8","#f472b6"],
                        box=True, points="outliers", **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Category × Level Enrollment Matrix")
    matrix = fdf.groupby(["category","level"]).size().unstack(fill_value=0)
    fig = px.imshow(matrix, color_continuous_scale="Plasma",
                    aspect="auto", **PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Course Price vs Rating (bubble = enrollments)")
    bubble = fdf.groupby("title").agg(
        price=("price_paid_usd","mean"),
        rating=("rating","mean"),
        enrollments=("transaction_id","count"),
        category=("category","first"),
    ).reset_index()
    fig = px.scatter(bubble, x="price", y="rating", size="enrollments",
                     color="category", hover_name="title",
                     color_discrete_sequence=PALETTE, **PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — REVENUE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.subheader("Monthly Revenue Trend")
    rev = fdf.groupby("enroll_month")["price_paid_usd"].sum().reset_index()
    rev = rev.sort_values("enroll_month")
    fig = px.bar(rev, x="enroll_month", y="price_paid_usd",
                 color_discrete_sequence=["#f472b6"], **PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Revenue by Category")
        rc = fdf.groupby("category")["price_paid_usd"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(rc, x="price_paid_usd", y="category", orientation="h",
                     color="price_paid_usd", color_continuous_scale="RdPu", **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Revenue by Subscription Tier")
        rs = fdf.groupby("subscription")["price_paid_usd"].sum().reset_index()
        fig = px.pie(rs, names="subscription", values="price_paid_usd", hole=0.5,
                     color_discrete_sequence=["#34d399","#818cf8","#f472b6"],
                     **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Payment Method Distribution")
    pm = fdf["payment_method"].value_counts().reset_index()
    pm.columns = ["method", "count"]
    fig = px.bar(pm, x="method", y="count", color="method",
                 color_discrete_sequence=PALETTE, **PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — GEO ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.subheader("Enrollment & Revenue by Country")
    geo = fdf.groupby("country").agg(
        enrollments=("transaction_id","count"),
        revenue=("price_paid_usd","sum"),
        completion=("completion_status", lambda x: (x=="Completed").mean()*100),
    ).reset_index()

    fig = px.choropleth(
        geo, locations="country", locationmode="country names",
        color="enrollments", hover_data=["revenue","completion"],
        color_continuous_scale="Viridis", **PLOTLY_THEME,
    )
    fig.update_geos(showframe=False, bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top Countries by Enrollments")
        fig = px.bar(geo.sort_values("enrollments", ascending=False),
                     x="enrollments", y="country", orientation="h",
                     color="enrollments", color_continuous_scale="Viridis", **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Completion Rate by Country")
        fig = px.bar(geo.sort_values("completion", ascending=False),
                     x="completion", y="country", orientation="h",
                     color="completion", color_continuous_scale="Teal", **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.subheader("Coupon Usage Impact on Completion")
    coup = fdf.groupby(["coupon_used","completion_status"]).size().reset_index(name="count")
    coup["coupon_used"] = coup["coupon_used"].map({True:"Coupon", False:"No Coupon"})
    fig = px.bar(coup, x="coupon_used", y="count", color="completion_status",
                 barmode="group", color_discrete_sequence=PALETTE, **PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Avg Hours Completed by Category")
        ch = fdf.groupby("category")["completed_hours"].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(ch, x="completed_hours", y="category", orientation="h",
                     color="completed_hours", color_continuous_scale="Turbo", **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Learner Rating Distribution")
        fig = px.histogram(fdf[fdf["rating_given"].notna()], x="rating_given", nbins=25,
                           color_discrete_sequence=["#fbbf24"], **PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Filtered Raw Data")
    cols = ["user_id","name","country","age","subscription","title","category",
            "level","completion_status","price_paid_usd","enroll_date","device"]
    st.dataframe(
        fdf[cols].sort_values("enroll_date", ascending=False).head(500),
        use_container_width=True, height=400,
    )

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#475569; font-size:12px;'>"
    "EduPro Analytics · Built with Streamlit & Plotly · 2024</p>",
    unsafe_allow_html=True,
)

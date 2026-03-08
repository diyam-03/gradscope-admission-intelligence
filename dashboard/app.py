import streamlit as st
from helpers import load_css, topnav

st.set_page_config(
    page_title="GradScope",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
load_css()
topnav("app")

st.sidebar.markdown("""
<div style="padding:1.75rem 0.75rem 1.25rem;">
  <div style="font-family:'Fraunces',serif;font-size:1.5rem;font-weight:900;
              color:#ffffff;letter-spacing:-0.02em;">GradScope</div>
  <div style="font-family:'Outfit',sans-serif;font-size:0.7rem;font-weight:700;
              letter-spacing:0.12em;text-transform:uppercase;
              color:rgba(255,255,255,0.45);margin-top:0.25rem;">
    Admission Intelligence
  </div>
</div>
<div style="height:1px;background:rgba(255,255,255,0.10);margin:0 0 0.75rem;"></div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="gs-hero">
  <div class="gs-hero-eyebrow">Powered by real admissions data</div>
  <div class="gs-hero-title">
    Your intelligent guide to<br>
    <span style="color:#c8006e;">university admissions</span>
  </div>
  <p class="gs-hero-sub">
    Analyse real admission trends, evaluate your academic profile,
    and discover where you are most competitive — all in one place.
  </p>
</div>
""", unsafe_allow_html=True)

kpis = [
    ("Universities Tracked", "2,000+", "world rankings dataset",   "linear-gradient(90deg,#c8006e,#f5a623)"),
    ("Admission Records",    "400+",   "graduate admissions data",  "linear-gradient(90deg,#4a90d9,#0d1b3e)"),
    ("Countries Covered",    "70+",    "global university data",    "linear-gradient(90deg,#10b981,#4a90d9)"),
    ("ML Accuracy",          "~82%",   "gradient boosting R2",      "linear-gradient(90deg,#f5a623,#c8006e)"),
]
for col, (lbl, val, sub, bar) in zip(st.columns(4), kpis):
    with col:
        st.markdown(f"""
        <div class="gs-metric">
          <div class="gs-metric-bar" style="background:{bar}"></div>
          <div class="gs-metric-label">{lbl}</div>
          <div class="gs-metric-value">{val}</div>
          <div class="gs-metric-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-bottom:1.5rem;">
  <div class="gs-label">Explore the Platform</div>
  <div style="font-family:'Fraunces',serif;font-size:2rem;font-weight:900;
              color:#0d1b3e;letter-spacing:-0.025em;margin:0.15rem 0 0.5rem;">
    Six tools. One platform.
  </div>
  <p style="font-family:'Outfit',sans-serif;font-size:0.95rem;color:#3d4f7a;
            max-width:440px;margin:0;line-height:1.65;">
    From raw analytics to predictions — everything a serious applicant needs.
  </p>
</div>
""", unsafe_allow_html=True)

features = [
    ("Admission Analytics",
     "Visualise score distributions, trend lines and what drives admission decisions."),
    ("University Explorer",
     "Browse and filter 2,000+ universities by country, rank, and research score."),
    ("Profile Analyzer",
     "See how your GRE, CGPA and TOEFL stack up with a radar chart and improvement tips."),
    ("University Recommendation",
     "Get a personalised Dream, Target and Safe university list based on your scores."),
    ("Admission Assistant",
     "Ask anything about GRE prep, SoPs, deadlines, funding and application strategy."),
    ("University Comparison",
     "Compare up to 5 universities side-by-side across every ranking dimension."),
]

row1 = st.columns(3)
for i in range(3):
    title, desc = features[i]
    with row1[i]:
        st.markdown(f"""
        <div class="gs-card">
          <div class="gs-card-title">{title}</div>
          <p>{desc}</p>
        </div>""", unsafe_allow_html=True)

st.markdown('<div style="height:0.75rem"></div>', unsafe_allow_html=True)

row2 = st.columns(3)
for i in range(3):
    title, desc = features[i + 3]
    with row2[i]:
        st.markdown(f"""
        <div class="gs-card">
          <div class="gs-card-title">{title}</div>
          <p>{desc}</p>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;
            flex-wrap:wrap;gap:0.75rem;padding:0.5rem 0 1.5rem;">
  <span style="font-family:'Outfit',sans-serif;font-size:0.78rem;color:#7b8cb0;">
    Built with Streamlit · Supabase · Scikit-learn · Plotly
  </span>
  <span style="font-family:'Outfit',sans-serif;font-size:0.78rem;color:#7b8cb0;">
    Data: World University Rankings · Graduate Admissions Dataset
  </span>
</div>
""", unsafe_allow_html=True)
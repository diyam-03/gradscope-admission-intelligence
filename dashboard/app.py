import streamlit as st
from helpers import load_css, topnav
from auth import show_auth_page, get_session

st.set_page_config(
    page_title="GradScope — Admission Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Auth gate — show login/signup if not logged in ─────────────────────────
if not show_auth_page():
    st.stop()

load_css()
topnav("app")

# ── Animated home page styles ─────────────────────────────────────────────────
st.markdown("""
<style>
@keyframes fadeUp {
  from { opacity:0; transform:translateY(24px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes float {
  0%,100% { transform:translateY(0px); }
  50%      { transform:translateY(-8px); }
}
@keyframes shimmer {
  0%   { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}
@keyframes pulse-ring {
  0%   { transform:scale(0.95); box-shadow:0 0 0 0 rgba(200,0,110,0.4); }
  70%  { transform:scale(1);    box-shadow:0 0 0 14px rgba(200,0,110,0); }
  100% { transform:scale(0.95); box-shadow:0 0 0 0 rgba(200,0,110,0); }
}

.gs-home-hero {
  background: linear-gradient(135deg, #0d1b3e 0%, #162248 55%, #1a2d6b 100%);
  border-radius: 20px;
  padding: 4rem 3.5rem 3.5rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
  animation: fadeUp 0.7s ease both;
}
.gs-home-hero::before {
  content:'';
  position:absolute;
  top:-80px; right:-80px;
  width:400px; height:400px;
  background: radial-gradient(circle, rgba(200,0,110,0.22) 0%, transparent 70%);
  pointer-events:none;
}
.gs-home-hero::after {
  content:'';
  position:absolute;
  bottom:0; left:0; right:0; height:4px;
  background: linear-gradient(90deg,#c8006e,#f5a623,#4a90d9,#10b981);
}
.gs-brand {
  display:inline-flex;
  align-items:center;
  gap:0.65rem;
  margin-bottom:1.75rem;
  animation: fadeUp 0.6s ease both;
}
.gs-brand-icon {
  width:48px; height:48px;
  background: linear-gradient(135deg,#c8006e,#f5a623);
  border-radius:12px;
  display:flex; align-items:center; justify-content:center;
  font-size:1.5rem;
  animation: float 3s ease-in-out infinite;
  box-shadow: 0 8px 24px rgba(200,0,110,0.35);
}
.gs-brand-name {
  font-family:'Fraunces',serif;
  font-size:2rem; font-weight:900;
  color:#ffffff;
  letter-spacing:-0.03em;
}
.gs-brand-tag {
  font-family:'Outfit',sans-serif;
  font-size:0.68rem; font-weight:700;
  letter-spacing:0.14em; text-transform:uppercase;
  color:rgba(255,255,255,0.45);
  margin-top:0.1rem;
}
.gs-hero-headline {
  font-family:'Fraunces',serif;
  font-size:3.2rem; font-weight:900;
  color:#ffffff;
  line-height:1.08;
  letter-spacing:-0.03em;
  margin-bottom:1.1rem;
  animation: fadeUp 0.7s 0.1s ease both;
}
.gs-hero-headline span {
  background: linear-gradient(90deg,#c8006e,#f5a623);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
}
.gs-hero-sub {
  font-family:'Outfit',sans-serif;
  font-size:1.05rem; color:rgba(255,255,255,0.72);
  max-width:520px; line-height:1.7;
  margin-bottom:2rem;
  animation: fadeUp 0.7s 0.2s ease both;
}
.gs-hero-pills {
  display:flex; flex-wrap:wrap; gap:0.6rem;
  animation: fadeUp 0.7s 0.3s ease both;
}
.gs-hero-pill {
  background:rgba(255,255,255,0.10);
  border:1px solid rgba(255,255,255,0.18);
  border-radius:100px;
  padding:0.4rem 1rem;
  font-family:'Outfit',sans-serif;
  font-size:0.78rem; font-weight:600;
  color:rgba(255,255,255,0.80);
  letter-spacing:0.02em;
}

.gs-stat-strip {
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:1rem;
  margin-bottom:2rem;
}
.gs-stat-card {
  background:#fff;
  border-radius:14px;
  padding:1.3rem 1.4rem;
  box-shadow:0 4px 18px rgba(13,27,62,0.08);
  border-top:4px solid transparent;
  animation: fadeUp 0.7s ease both;
  transition: transform 0.22s ease, box-shadow 0.22s ease;
  cursor:default;
}
.gs-stat-card:hover {
  transform:translateY(-4px);
  box-shadow:0 10px 32px rgba(13,27,62,0.14);
}
.gs-stat-val {
  font-family:'Fraunces',serif;
  font-size:2.1rem; font-weight:900;
  color:#0d1b3e;
  line-height:1;
  margin-bottom:0.3rem;
}
.gs-stat-lbl {
  font-size:0.78rem; font-weight:700;
  text-transform:uppercase; letter-spacing:0.07em;
  color:#7b8cb0;
  margin-bottom:0.15rem;
}
.gs-stat-sub { font-size:0.75rem; color:#7b8cb0; }

.gs-section-head {
  margin-bottom:1.4rem;
  animation: fadeUp 0.6s ease both;
}
.gs-section-label {
  font-size:0.72rem; font-weight:700;
  text-transform:uppercase; letter-spacing:0.12em;
  color:#c8006e; margin-bottom:0.35rem;
}
.gs-section-title {
  font-family:'Fraunces',serif;
  font-size:2rem; font-weight:900;
  color:#0d1b3e; letter-spacing:-0.025em;
  margin:0 0 0.4rem;
}
.gs-section-desc {
  font-family:'Outfit',sans-serif;
  font-size:0.92rem; color:#3d4f7a;
  max-width:460px; line-height:1.65;
}

.gs-feature-card {
  background:#fff;
  border-radius:16px;
  padding:1.5rem 1.6rem;
  box-shadow:0 4px 18px rgba(13,27,62,0.07);
  border:1.5px solid rgba(255,255,255,0.9);
  height:100%;
  transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
  cursor:default;
  position:relative;
  overflow:hidden;
  animation: fadeUp 0.6s ease both;
}
.gs-feature-card:hover {
  transform:translateY(-6px);
  box-shadow:0 16px 40px rgba(13,27,62,0.14);
  border-color:rgba(200,0,110,0.25);
}
.gs-feature-card::before {
  content:'';
  position:absolute;
  top:0; left:0; right:0; height:3px;
  background:var(--accent, linear-gradient(90deg,#c8006e,#f5a623));
  opacity:0;
  transition:opacity 0.22s ease;
}
.gs-feature-card:hover::before { opacity:1; }
.gs-feature-icon {
  width:44px; height:44px;
  border-radius:12px;
  display:flex; align-items:center; justify-content:center;
  font-size:1.25rem;
  margin-bottom:1rem;
}
.gs-feature-title {
  font-family:'Fraunces',serif;
  font-size:1rem; font-weight:900;
  color:#0d1b3e;
  margin-bottom:0.5rem;
}
.gs-feature-desc {
  font-family:'Outfit',sans-serif;
  font-size:0.83rem; color:#3d4f7a;
  line-height:1.65;
}
.gs-cta-strip {
  background:linear-gradient(135deg,#0d1b3e,#1a2d6b);
  border-radius:16px;
  padding:2rem 2.5rem;
  display:flex; align-items:center;
  justify-content:space-between;
  flex-wrap:wrap; gap:1rem;
  margin:2rem 0 1.5rem;
  animation: fadeUp 0.7s ease both;
  position:relative; overflow:hidden;
}
.gs-cta-strip::after {
  content:'';
  position:absolute;
  top:0; right:0;
  width:200px; height:100%;
  background:radial-gradient(circle at right,rgba(200,0,110,0.18),transparent 70%);
}
.gs-footer {
  display:flex; justify-content:space-between; align-items:center;
  flex-wrap:wrap; gap:0.75rem;
  padding:1rem 0 2rem;
  font-family:'Outfit',sans-serif;
  font-size:0.75rem; color:#7b8cb0;
  border-top:1px solid rgba(13,27,62,0.07);
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="gs-home-hero">
  <div class="gs-brand">
    <div class="gs-brand-icon">🎓</div>
    <div>
      <div class="gs-brand-name">GradScope</div>
      <div class="gs-brand-tag">Admission Intelligence</div>
    </div>
  </div>
  <div class="gs-hero-headline">
    Your smartest move<br>starts with <span>better data</span>
  </div>
  <div class="gs-hero-sub">
    Analyse real admission trends, predict your chances with ML,
    and discover universities where you are most competitive —
    all in one platform built for serious applicants.
  </div>
  <div class="gs-hero-pills">
    <span class="gs-hero-pill">Real QS 2025 Data</span>
    <span class="gs-hero-pill">55 Subject Rankings</span>
    <span class="gs-hero-pill">ML Admission Predictor</span>
    <span class="gs-hero-pill">1,422 Universities</span>
    <span class="gs-hero-pill">Free to Use</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Stats strip ───────────────────────────────────────────────────────────────
stats = [
    ("1,422+", "Universities",     "from QS 2025 rankings",    "#c8006e", "0.1s"),
    ("55",     "Subject Rankings", "across all disciplines",    "#0d1b3e", "0.2s"),
    ("400+",   "Admission Records","real graduate applicants",  "#10b981", "0.3s"),
    ("~82%",   "ML Accuracy",      "gradient boosting model",   "#f5a623", "0.4s"),
]
st.markdown('<div class="gs-stat-strip">', unsafe_allow_html=True)
for val, lbl, sub, color, delay in stats:
    st.markdown(f"""
    <div class="gs-stat-card" style="border-top-color:{color};animation-delay:{delay};">
      <div class="gs-stat-lbl">{lbl}</div>
      <div class="gs-stat-val" style="color:{color};">{val}</div>
      <div class="gs-stat-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)

# ── Features ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="gs-section-head">
  <div class="gs-section-label">What's Inside</div>
  <div class="gs-section-title">Six tools. One platform.</div>
  <div class="gs-section-desc">Everything a serious applicant needs — from raw analytics to AI-powered recommendations.</div>
</div>
""", unsafe_allow_html=True)

features = [
    ("📊", "Admission Analytics",      "Explore what really drives admission decisions — based on 400 real applicant records. Understand how GRE, CGPA and research each affect your odds.",      "linear-gradient(135deg,#0d1b3e,#1a2d6b)", "rgba(13,27,62,0.08)",  "0.1s"),
    ("🏛",  "University Explorer",      "Browse and filter 1,422 universities by country, world rank and QS scores. Find institutions that match your target profile.",                           "linear-gradient(135deg,#c8006e,#e0057c)", "rgba(200,0,110,0.08)", "0.2s"),
    ("🧠", "Profile Analyzer",         "Enter your GRE, CGPA and TOEFL scores to get an ML-powered admission prediction, a radar chart, and a personalised action plan.",                       "linear-gradient(135deg,#10b981,#047857)", "rgba(16,185,129,0.08)","0.3s"),
    ("🎯", "University Recommendation","Pick your field of study from 55 real QS subject rankings. Get a personalised Dream, Target and Safe university list based on your profile.",            "linear-gradient(135deg,#f5a623,#c8006e)", "rgba(245,166,35,0.08)","0.4s"),
    ("💬", "Admission Assistant",      "A real chatbot advisor covering GRE prep, SoPs, LoRs, funding, visa, MS vs PhD — ask anything and get instant guidance.",                                "linear-gradient(135deg,#4a90d9,#0d1b3e)", "rgba(74,144,217,0.08)","0.5s"),
    ("⚖️", "University Comparison",    "Compare up to 5 universities side-by-side across every QS dimension: academic reputation, employer reputation, faculty ratio, citations and more.",      "linear-gradient(135deg,#0d1b3e,#c8006e)", "rgba(13,27,62,0.08)",  "0.6s"),
]

row1_cols = st.columns(3)
row2_cols = st.columns(3)
all_cols  = list(row1_cols) + list(row2_cols)

for col, (icon, title, desc, grad, bg, delay) in zip(all_cols, features):
    with col:
        st.markdown(f"""
        <div class="gs-feature-card" style="animation-delay:{delay};--accent:{grad};">
          <div class="gs-feature-icon" style="background:{bg};">{icon}</div>
          <div class="gs-feature-title">{title}</div>
          <div class="gs-feature-desc">{desc}</div>
        </div>
        <div style="height:1rem;"></div>
        """, unsafe_allow_html=True)

# ── CTA strip ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="gs-cta-strip">
  <div>
    <div style="font-family:'Fraunces',serif;font-size:1.4rem;font-weight:900;
                color:#fff;margin-bottom:0.35rem;">Ready to find your best-fit universities?</div>
    <div style="font-family:'Outfit',sans-serif;font-size:0.88rem;
                color:rgba(255,255,255,0.65);">
      Start with the Profile Analyzer or jump straight to University Recommendation.
    </div>
  </div>
  <div style="display:flex;gap:0.75rem;flex-wrap:wrap;">
    <a href="/Profile_Analyzer" target="_self" style="background:linear-gradient(90deg,#c8006e,#f5a623);
                border-radius:10px;padding:0.7rem 1.5rem;
                font-family:'Outfit',sans-serif;font-size:0.88rem;
                font-weight:700;color:#fff;text-decoration:none;
                box-shadow:0 4px 14px rgba(200,0,110,0.35);display:inline-block;">
      Analyze My Profile
    </a>
    <a href="/University_Recommendation" target="_self" style="background:rgba(255,255,255,0.10);border:1.5px solid rgba(255,255,255,0.25);
                border-radius:10px;padding:0.7rem 1.5rem;
                font-family:'Outfit',sans-serif;font-size:0.88rem;
                font-weight:700;color:#fff;text-decoration:none;display:inline-block;">
      Get Recommendations
    </a>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="gs-footer">
  <span>GradScope · Built with Streamlit, Supabase, Scikit-learn, Plotly</span>
  <span>Data: QS World University Rankings 2025 · QS Rankings by Subject 2025 · Graduate Admissions Dataset</span>
</div>
""", unsafe_allow_html=True)
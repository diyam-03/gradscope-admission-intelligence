import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from helpers import page_header

st.set_page_config(page_title="Admission Analytics · GradScope", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
page_header("Analyze", "Admission Analytics",
            "What really drives graduate admissions — insights from 400 real applicant records.",
            active="Admission_Analytics")

@st.cache_data
def load():
    p = Path(__file__).parent.parent.parent / "data" / "admissions.csv"
    df = pd.read_csv(p)
    df.columns = df.columns.str.strip()
    rename = {}
    for c in df.columns:
        l = c.lower()
        if "gre" in l:        rename[c] = "GRE"
        elif "toefl" in l:    rename[c] = "TOEFL"
        elif "cgpa" in l:     rename[c] = "CGPA"
        elif "chance" in l:   rename[c] = "Admit"
        elif "research" in l: rename[c] = "Research"
        elif "rating" in l:   rename[c] = "UniRating"
        elif "sop" in l:      rename[c] = "SOP"
        elif "lor" in l:      rename[c] = "LOR"
    return df.rename(columns=rename)

df = load()
df["Admit%"] = (df["Admit"] * 100).round(1) if df["Admit"].max() <= 1 else df["Admit"].round(1)
df["ResearchLabel"] = df["Research"].map({0: "No Research", 1: "Has Research"})


avg_admit       = df["Admit%"].mean()
gre_high_admit  = df[df["GRE"] >= 325]["Admit%"].mean()
gre_low_admit   = df[df["GRE"] < 310]["Admit%"].mean()
res_admit       = df[df["Research"] == 1]["Admit%"].mean()
nores_admit     = df[df["Research"] == 0]["Admit%"].mean()
cgpa_high_admit = df[df["CGPA"] >= 9]["Admit%"].mean()
cgpa_low_admit  = df[df["CGPA"] < 7.5]["Admit%"].mean()
corr_gre        = df["GRE"].corr(df["Admit%"])
corr_cgpa       = df["CGPA"].corr(df["Admit%"])
corr_toefl      = df["TOEFL"].corr(df["Admit%"])
corr_research   = df["Research"].corr(df["Admit%"])
top_rating_avg  = df[df["UniRating"] == 5]["Admit%"].mean()
bot_rating_avg  = df[df["UniRating"] == 1]["Admit%"].mean()


k1, k2, k3, k4, k5 = st.columns(5)
for col, label, value, sub, bar in [
    (k1, "Total Applicants",   f"{len(df):,}",                   "in dataset",          "linear-gradient(90deg,#0d1b3e,#4a90d9)"),
    (k2, "Avg GRE Score",      f"{df['GRE'].mean():.0f}",        "out of 340",          "linear-gradient(90deg,#c8006e,#f5a623)"),
    (k3, "Avg CGPA",           f"{df['CGPA'].mean():.2f}",       "out of 10",           "linear-gradient(90deg,#f5a623,#c8006e)"),
    (k4, "Avg Admit Chance",   f"{avg_admit:.1f}%",              "across all applicants","linear-gradient(90deg,#10b981,#4a90d9)"),
    (k5, "Have Research",      f"{int(df['Research'].sum())}",   f"of {len(df)} applicants","linear-gradient(90deg,#4a90d9,#10b981)"),
]:
    with col:
        st.markdown(f"""
        <div class="gs-metric">
          <div class="gs-metric-bar" style="background:{bar}"></div>
          <div class="gs-metric-label">{label}</div>
          <div class="gs-metric-value">{value}</div>
          <div class="gs-metric-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)


st.markdown('<div class="gs-label">Key Insights from the Data</div>', unsafe_allow_html=True)

insights = [
    {
        "title": "CGPA is the strongest predictor",
        "stat":  f"{corr_cgpa:.2f}",
        "stat_label": "correlation with admit chance",
        "body": f"Students with a CGPA of 9 or above have an average admit chance of {cgpa_high_admit:.0f}%, compared to just {cgpa_low_admit:.0f}% for those below 7.5. Focus on your GPA before anything else.",
        "color": "#c8006e",
    },
    {
        "title": "Research doubles your odds",
        "stat":  f"+{res_admit - nores_admit:.0f}%",
        "stat_label": "higher admit chance with research",
        "body": f"Applicants with research experience have an average admit chance of {res_admit:.0f}%, versus {nores_admit:.0f}% without. This is the single biggest differentiator you can act on.",
        "color": "#10b981",
    },
    {
        "title": "GRE matters — but less than you think",
        "stat":  f"{corr_gre:.2f}",
        "stat_label": "correlation with admit chance",
        "body": f"A GRE of 325+ lifts your average admit chance to {gre_high_admit:.0f}%, but scoring below 310 only drops it to {gre_low_admit:.0f}%. GRE is a threshold — once you clear it, focus energy elsewhere.",
        "color": "#0d1b3e",
    },
    {
        "title": "University target tier matters a lot",
        "stat":  f"{top_rating_avg:.0f}% vs {bot_rating_avg:.0f}%",
        "stat_label": "Tier 5 vs Tier 1 admit rate",
        "body": f"Students targeting Tier 5 universities (most selective) average {top_rating_avg:.0f}% admission chance. Targeting Tier 1 schools averages {bot_rating_avg:.0f}%. Calibrate your list realistically.",
        "color": "#f5a623",
    },
    {
        "title": "TOEFL has the weakest impact",
        "stat":  f"{corr_toefl:.2f}",
        "stat_label": "correlation with admit chance",
        "body": f"TOEFL has the lowest correlation of all factors at {corr_toefl:.2f}. Once you hit a threshold score (~100+), additional TOEFL improvement has diminishing returns on your admission odds.",
        "color": "#4a90d9",
    },
]

row1 = st.columns(3)
row2 = st.columns(2)
all_cols = row1 + row2

for col, ins in zip(all_cols, insights):
    with col:
        st.markdown(f"""
        <div style="background:#fff;border-radius:14px;overflow:hidden;
                    box-shadow:0 4px 18px rgba(13,27,62,0.08);
                    border-top:4px solid {ins['color']};
                    padding:1.2rem 1.3rem;height:100%;margin-bottom:1rem;">
          <div style="font-family:Fraunces,serif;font-size:1rem;font-weight:900;
                      color:#0d1b3e;margin-bottom:0.75rem;line-height:1.3;">
            {ins['title']}
          </div>
          <div style="display:flex;align-items:baseline;gap:0.5rem;margin-bottom:0.7rem;">
            <div style="font-family:Fraunces,serif;font-size:2rem;font-weight:900;color:{ins['color']};">
              {ins['stat']}
            </div>
            <div style="font-size:0.72rem;color:#7b8cb0;font-weight:600;
                        text-transform:uppercase;letter-spacing:0.06em;line-height:1.3;">
              {ins['stat_label']}
            </div>
          </div>
          <div style="font-size:0.83rem;color:#3d4f7a;line-height:1.65;">
            {ins['body']}
          </div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)


st.markdown('<div class="gs-label">How Much Does Each Factor Influence Admission?</div>', unsafe_allow_html=True)

factors = pd.DataFrame({
    "Factor":      ["CGPA", "GRE Score", "Research", "LOR", "SOP", "TOEFL", "Uni Rating"],
    "Correlation": [
        round(df["CGPA"].corr(df["Admit%"]), 3),
        round(df["GRE"].corr(df["Admit%"]), 3),
        round(df["Research"].corr(df["Admit%"]), 3),
        round(df["LOR"].corr(df["Admit%"]), 3),
        round(df["SOP"].corr(df["Admit%"]), 3),
        round(df["TOEFL"].corr(df["Admit%"]), 3),
        round(df["UniRating"].corr(df["Admit%"]), 3),
    ]
}).sort_values("Correlation", ascending=True)

factors["Color"] = factors["Correlation"].apply(
    lambda x: "#10b981" if x >= 0.8 else "#4a90d9" if x >= 0.6 else "#f5a623")

fig = go.Figure()
fig.add_trace(go.Bar(
    x=factors["Correlation"],
    y=factors["Factor"],
    orientation="h",
    marker_color=factors["Color"],
    text=factors["Correlation"].apply(lambda x: f"{x:.2f}"),
    textposition="outside",
    textfont=dict(size=12, color="#0d1b3e", family="Outfit"),
))
fig.update_layout(
    paper_bgcolor="rgba(255,255,255,0.80)",
    plot_bgcolor="rgba(247,248,252,0.90)",
    font_family="Outfit", font_color="#3d4f7a",
    height=320,
    margin=dict(l=0, r=60, t=10, b=10),
    xaxis=dict(showgrid=True, gridcolor="rgba(13,27,62,0.06)",
               range=[0, 1], title="Correlation with Admit Chance"),
    yaxis=dict(showgrid=False),
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("""<div style="font-size:0.75rem;color:#7b8cb0;margin-top:-0.5rem;">
    Correlation ranges from 0 (no relationship) to 1 (perfect relationship).
    Higher = stronger influence on admission outcome.</div>""", unsafe_allow_html=True)

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)
st.download_button("Download admissions data as CSV",
                   data=df.to_csv(index=False),
                   file_name="gradscope_admissions.csv", mime="text/csv")

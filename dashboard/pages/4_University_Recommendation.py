import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from helpers import page_header

st.set_page_config(page_title="University Recommendation · GradScope", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")
page_header("Discover", "University Recommendation",
            "Pick your field of study and enter your profile to get a personalised Dream, Target and Safe university list.",
            active="University_Recommendation")

@st.cache_data
def load_subjects():
    p = Path(__file__).parent.parent.parent / "data" / "subject_rankings.csv"
    df = pd.read_csv(p)
    df["world_rank"] = pd.to_numeric(df["world_rank"], errors="coerce")
    df["overall_score"] = pd.to_numeric(df["overall_score"], errors="coerce")
    return df

df_sub = load_subjects()
SUBJECTS = sorted(df_sub["subject"].unique().tolist())

T = dict(paper_bgcolor="rgba(255,255,255,0.80)", plot_bgcolor="rgba(247,248,252,0.90)",
         font_family="Outfit", font_color="#3d4f7a", margin=dict(l=0,r=0,t=10,b=40))

# ── Step 1 — Field ─────────────────────────────────────────────────────────────
st.markdown('<div class="gs-label">Step 1 — Your Field of Study</div>', unsafe_allow_html=True)

field = st.selectbox("What do you want to study?", options=SUBJECTS,
                     index=SUBJECTS.index("Computer Science") if "Computer Science" in SUBJECTS else 0)

# Teaser — top 5 for selected field
top5 = df_sub[df_sub["subject"] == field].sort_values("subject_rank").head(5)
st.markdown(f"""
<div style="background:rgba(13,27,62,0.05);border:1px solid rgba(13,27,62,0.10);
            border-radius:10px;padding:0.75rem 1.1rem;margin:0.5rem 0 1rem;">
  <span style="font-family:'Outfit',sans-serif;font-size:0.72rem;font-weight:700;
               letter-spacing:0.1em;text-transform:uppercase;color:#7b8cb0;">
    Top 5 globally for {field}:
  </span>
  <span style="font-family:'Outfit',sans-serif;font-size:0.85rem;color:#0d1b3e;margin-left:0.5rem;">
    {" · ".join(top5["institution"].tolist())}
  </span>
</div>""", unsafe_allow_html=True)

# ── Step 2 — Profile ───────────────────────────────────────────────────────────
st.markdown('<div class="gs-label">Step 2 — Your Academic Profile</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    gre = st.number_input("GRE Score (260–340)", min_value=260, max_value=340,
                          value=None, placeholder="e.g. 320")
with c2:
    cgpa = st.number_input("CGPA (out of 10)", min_value=0.0, max_value=10.0,
                           value=None, placeholder="e.g. 8.5", step=0.1)
with c3:
    toefl = st.number_input("TOEFL Score (0–120)", min_value=0, max_value=120,
                            value=None, placeholder="e.g. 105")
with c4:
    research = st.selectbox("Research Experience", options=[None, "Yes", "No"],
                            format_func=lambda x: "Select..." if x is None else x)

st.markdown('<div style="height:0.75rem"></div>', unsafe_allow_html=True)

all_filled = all([gre is not None, cgpa is not None,
                  toefl is not None, research is not None])

recommend = st.button("Get My University List", type="primary", disabled=not all_filled)
if not all_filled:
    st.markdown("""<div style="font-size:0.82rem;color:#7b8cb0;margin-top:0.4rem;">
        Fill in all fields above to get recommendations.</div>""", unsafe_allow_html=True)

# ── Results ────────────────────────────────────────────────────────────────────
if recommend or st.session_state.get("rec_done"):
    if recommend:
        st.session_state["rec_done"] = True
        st.session_state["rec_inputs"] = {
            "gre": gre, "cgpa": cgpa, "toefl": toefl,
            "research": research, "field": field
        }

    inp     = st.session_state.get("rec_inputs", {})
    gre_v   = inp.get("gre", 310)
    cgpa_v  = inp.get("cgpa", 8.5)
    toefl_v = inp.get("toefl", 105)
    res_v   = 1 if inp.get("research") == "Yes" else 0
    field_v = inp.get("field", "Computer Science")

    # Profile score 0-100
    score = (gre_v/340)*0.5 + (cgpa_v/10)*0.4 + (toefl_v/120)*0.1
    if res_v: score = min(1.0, score + 0.05)
    s100 = round(score * 100, 1)

    # Get subject-ranked universities for selected field
    ranked = df_sub[df_sub["subject"] == field_v].sort_values("subject_rank").copy()

    # Dynamic cutoffs based on profile score
    if s100 >= 88:
        dream_max, target_max = 5,  12
    elif s100 >= 80:
        dream_max, target_max = 7,  15
    elif s100 >= 70:
        dream_max, target_max = 10, 20
    elif s100 >= 60:
        dream_max, target_max = 12, 25
    else:
        dream_max, target_max = 15, 30

    dream_df  = ranked[ranked["subject_rank"] <= dream_max].head(10)
    target_df = ranked[(ranked["subject_rank"] > dream_max) & (ranked["subject_rank"] <= target_max)].head(10)
    safe_df   = ranked[ranked["subject_rank"] > target_max].head(10)

    st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)

    # KPI strip
    kpis = [
        ("Profile Score",  f"{s100}",          "out of 100",                             "linear-gradient(90deg,#c8006e,#f5a623)"),
        ("Subject",        field_v.split()[0], "selected field",                          "linear-gradient(90deg,#0d1b3e,#4a90d9)"),
        ("Dream Schools",  str(len(dream_df)), f"subject rank 1–{dream_max}",             "linear-gradient(90deg,#f5a623,#c8006e)"),
        ("Target Schools", str(len(target_df)),f"subject rank {dream_max+1}–{target_max}","linear-gradient(90deg,#4a90d9,#10b981)"),
        ("Safe Schools",   str(len(safe_df)),  f"subject rank {target_max+1}+",           "linear-gradient(90deg,#10b981,#4a90d9)"),
    ]
    for col, (lbl, val, sub, bar) in zip(st.columns(5), kpis):
        with col:
            st.markdown(f"""
            <div class="gs-metric">
              <div class="gs-metric-bar" style="background:{bar}"></div>
              <div class="gs-metric-label">{lbl}</div>
              <div class="gs-metric-value" style="font-size:1.4rem;">{val}</div>
              <div class="gs-metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)

    # Profile context note
    if s100 >= 85:
        note = "Your profile is very strong. You are competitive at top-ranked programs in this field."
        nc = "#10b981"
    elif s100 >= 70:
        note = "Your profile is competitive for mid-top programs. Improving GRE or CGPA could unlock more dream schools."
        nc = "#f5a623"
    else:
        note = "Your profile needs strengthening for top programs. Focus on GRE improvement and research experience."
        nc = "#c8006e"

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.78);border-left:4px solid {nc};
                border-radius:10px;padding:0.9rem 1.1rem;margin-bottom:1.25rem;">
      <div style="font-size:0.88rem;color:#0d1b3e;line-height:1.6;">{note}</div>
    </div>""", unsafe_allow_html=True)

    def tier_rows_html(data):
        if len(data) == 0:
            return '<div style="padding:1.2rem;text-align:center;color:#7b8cb0;font-size:0.83rem;">No universities in this tier.</div>'
        rows = ""
        for i, (_, row) in enumerate(data.iterrows()):
            bg = "rgba(13,27,62,0.025)" if i % 2 == 0 else "rgba(255,255,255,0)"
            wr = f'#{int(row["world_rank"])}' if pd.notna(row.get("world_rank")) else "—"
            rows += f"""
            <div style="display:grid;grid-template-columns:60px 1fr 160px 80px;
                        align-items:center;padding:0.6rem 1.1rem;background:{bg};
                        border-bottom:1px solid rgba(13,27,62,0.05);">
              <div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;">#{int(row['subject_rank'])}</div>
              <div style="font-size:0.85rem;color:#0d1b3e;">{row['institution']}</div>
              <div style="font-size:0.80rem;color:#7b8cb0;">{row['country']}</div>
              <div style="font-size:0.80rem;color:#7b8cb0;text-align:right;">{wr}</div>
            </div>"""
        return rows

    def tier_card(data, title, admit, accent, badge_bg):
        header_row = f"""
        <div style="display:grid;grid-template-columns:60px 1fr 160px 80px;
                    padding:0.45rem 1.1rem;border-bottom:2px solid rgba(13,27,62,0.08);">
          <div style="font-size:0.70rem;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;color:#7b8cb0;">Rank</div>
          <div style="font-size:0.70rem;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;color:#7b8cb0;">University</div>
          <div style="font-size:0.70rem;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;color:#7b8cb0;">Country</div>
          <div style="font-size:0.70rem;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;color:#7b8cb0;text-align:right;">World Rank</div>
        </div>"""
        return f"""
        <div style="background:rgba(255,255,255,0.88);border-radius:14px;overflow:hidden;
                    box-shadow:0 4px 20px rgba(13,27,62,0.08);margin-bottom:1.1rem;
                    border-left:5px solid {accent};">
          <div style="background:{badge_bg};padding:0.85rem 1.1rem;
                      display:flex;align-items:center;justify-content:space-between;">
            <div>
              <div style="font-family:'Fraunces',serif;font-size:1.1rem;font-weight:900;color:#fff;">{title}</div>
              <div style="font-size:0.75rem;color:rgba(255,255,255,0.80);margin-top:0.1rem;">Est. admit chance: {admit}</div>
            </div>
            <div style="background:rgba(255,255,255,0.18);border-radius:8px;
                        padding:0.3rem 0.75rem;font-size:0.80rem;font-weight:700;color:#fff;">
              {len(data)} universities
            </div>
          </div>
          {header_row}
          {tier_rows_html(data)}
        </div>"""

    st.markdown(tier_card(dream_df,  "Dream Schools",  "< 30%",  "#0d1b3e", "linear-gradient(90deg,#0d1b3e,#1a2d6b)"), unsafe_allow_html=True)
    st.markdown(tier_card(target_df, "Target Schools", "30–65%", "#c8006e", "linear-gradient(90deg,#c8006e,#e0057c)"), unsafe_allow_html=True)
    st.markdown(tier_card(safe_df,   "Safe Schools",   "65–90%", "#065f46", "linear-gradient(90deg,#065f46,#047857)"), unsafe_allow_html=True)

    st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)

    # Scatter — subject rank vs world rank
    plot_data = ranked.dropna(subset=["world_rank", "overall_score"]).copy()
    if len(plot_data) >= 3:
        plot_data["Tier"] = "Safe"
        plot_data.loc[plot_data["subject_rank"] <= target_max, "Tier"] = "Target"
        plot_data.loc[plot_data["subject_rank"] <= dream_max,  "Tier"] = "Dream"
        st.markdown(f'<div class="gs-label">Subject Rank vs World Rank — {field_v}</div>',
                    unsafe_allow_html=True)
        fig = px.scatter(plot_data, x="world_rank", y="subject_rank",
                         color="Tier", hover_name="institution",
                         size="overall_score",
                         color_discrete_map={"Dream":"#0d1b3e","Target":"#c8006e","Safe":"#10b981"},
                         labels={"world_rank":"QS World Rank",
                                 "subject_rank": f"{field_v} Subject Rank",
                                 "overall_score": "QS Score"})
        fig.update_layout(**T, height=340,
                          xaxis=dict(showgrid=True, gridcolor="rgba(13,27,62,0.06)"),
                          yaxis=dict(showgrid=True, gridcolor="rgba(13,27,62,0.06)",
                                     autorange="reversed"),
                          legend=dict(orientation="h", x=0.5, xanchor="center",
                                      y=-0.18, font_size=11))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""<div style="font-size:0.75rem;color:#7b8cb0;margin-top:-0.5rem;">
            Bubble size = overall QS score. Y-axis = subject rank (lower is better).
            Source: QS World University Rankings by Subject 2025.</div>""",
            unsafe_allow_html=True)

    # Download
    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
    all_recs = pd.concat([
        dream_df.assign(Tier="Dream"),
        target_df.assign(Tier="Target"),
        safe_df.assign(Tier="Safe")
    ])
    st.download_button("Download my university list as CSV",
                       data=all_recs.to_csv(index=False),
                       file_name=f"gradscope_{field_v.replace(' ','_')}_universities.csv",
                       mime="text/csv")

    if st.button("Reset"):
        st.session_state["rec_done"] = False
        st.session_state["rec_inputs"] = {}
        st.rerun()
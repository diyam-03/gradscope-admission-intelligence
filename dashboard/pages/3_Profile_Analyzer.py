import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path
from helpers import page_header

st.set_page_config(page_title="Profile Analyzer · GradScope", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")
page_header("Evaluate", "Profile Analyzer",
            "Fill in your details honestly, click Analyze, and get a real ML-powered admission prediction.",
            active="Profile_Analyzer")

try:
    from pipeline.predictor import predict_chance
    USE_ML = True
except Exception:
    USE_ML = False

@st.cache_data
def load_admissions():
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
    df = df.rename(columns=rename)
    if df["Admit"].max() <= 1:
        df["Admit"] = (df["Admit"] * 100).round(1)
    return df

df_adm = load_admissions()
T = dict(paper_bgcolor="rgba(255,255,255,0.80)", plot_bgcolor="rgba(247,248,252,0.90)",
         font_family="Outfit", font_color="#3d4f7a", margin=dict(l=0,r=120,t=10,b=0))

SOP_OPTIONS = {
    1.0: "I have not started writing yet",
    2.0: "I have a rough draft with no specific research focus",
    3.0: "I have a decent draft mentioning my goals but no specific faculty",
    4.0: "My SoP clearly states goals, mentions specific professors and their work",
    5.0: "My SoP is polished, reviewed by mentors, and tailored per university",
}
LOR_OPTIONS = {
    1.0: "From a professor who barely knows me, likely a generic letter",
    2.0: "From a professor I attended class with but did not work closely with",
    3.0: "From a professor who knows my academic work reasonably well",
    4.0: "From a supervisor who directly oversaw my project or research",
    5.0: "From a senior professor who can compare me to top students they have taught",
}

st.markdown('<div class="gs-label">Step 1 — Enter Your Academic Scores</div>',
            unsafe_allow_html=True)

r1c1, r1c2, r1c3 = st.columns(3)
with r1c1:
    gre = st.number_input("GRE Score (260–340)", min_value=260, max_value=340,
                          value=None, placeholder="e.g. 315")
with r1c2:
    toefl = st.number_input("TOEFL Score (0–120)", min_value=0, max_value=120,
                            value=None, placeholder="e.g. 105")
with r1c3:
    cgpa = st.number_input("CGPA (0–10)", min_value=0.0, max_value=10.0,
                           value=None, placeholder="e.g. 8.5", step=0.1)

r2c1, r2c2 = st.columns(2)
with r2c1:
    uni_r = st.selectbox("Target University Tier",
                         options=[None, 1, 2, 3, 4, 5],
                         format_func=lambda x: "Select..." if x is None else {
                             1: "1 — Top 10 globally (MIT, Stanford, Harvard)",
                             2: "2 — Top 50 globally",
                             3: "3 — Top 100–200 globally",
                             4: "4 — Top 300–500 globally",
                             5: "5 — Any accredited university",
                         }[x])
with r2c2:
    research = st.selectbox("Do you have research experience?",
                            options=[None, "Yes", "No"],
                            format_func=lambda x: "Select..." if x is None else x)


st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
st.markdown('<div class="gs-label">Step 2 — Self-Assess Your Application Materials</div>',
            unsafe_allow_html=True)

sc1, sc2 = st.columns(2)
with sc1:
    st.markdown("""
    <div style="font-family:'Outfit',sans-serif;font-size:0.84rem;font-weight:600;
                color:#0d1b3e;margin-bottom:0.4rem;">
        Statement of Purpose — where are you right now?
    </div>""", unsafe_allow_html=True)
    sop = st.radio("sop_q", list(SOP_OPTIONS.keys()),
                   format_func=lambda x: SOP_OPTIONS[x],
                   label_visibility="collapsed", index=None)
with sc2:
    st.markdown("""
    <div style="font-family:'Outfit',sans-serif;font-size:0.84rem;font-weight:600;
                color:#0d1b3e;margin-bottom:0.4rem;">
        Letters of Recommendation — who is writing yours?
    </div>""", unsafe_allow_html=True)
    lor = st.radio("lor_q", list(LOR_OPTIONS.keys()),
                   format_func=lambda x: LOR_OPTIONS[x],
                   label_visibility="collapsed", index=None)

st.markdown('<div style="height:0.75rem"></div>', unsafe_allow_html=True)

all_filled = all([gre is not None, toefl is not None, cgpa is not None,
                  uni_r is not None, research is not None,
                  sop is not None, lor is not None])

analyze = st.button("Analyze My Profile", type="primary", disabled=not all_filled)

if not all_filled:
    st.markdown("""
    <div style="font-size:0.82rem;color:#7b8cb0;margin-top:0.4rem;">
        Fill in all fields above to enable the analyzer.
    </div>""", unsafe_allow_html=True)


if analyze or st.session_state.get("analyzed"):
    if analyze:
        st.session_state["analyzed"] = True
        st.session_state["inputs"] = {
            "gre": gre, "toefl": toefl, "cgpa": cgpa,
            "uni_r": uni_r, "research": research,
            "sop": sop, "lor": lor
        }

    inp   = st.session_state.get("inputs", {})
    gre_v   = inp.get("gre", 300)
    toefl_v = inp.get("toefl", 100)
    cgpa_v  = inp.get("cgpa", 8.0)
    uni_v   = inp.get("uni_r", 3)
    res_v   = 1 if inp.get("research") == "Yes" else 0
    sop_v   = inp.get("sop", 3.0)
    lor_v   = inp.get("lor", 3.0)

    if USE_ML:
        chance = predict_chance(gre_v, toefl_v, cgpa_v, sop_v, lor_v, uni_v, res_v)
    else:
        chance = round(((gre_v/340)*0.20+(toefl_v/120)*0.10+(cgpa_v/10)*0.25+
                        (sop_v/5)*0.15+(lor_v/5)*0.15+(uni_v/5)*0.10+res_v*0.05)*100, 1)

    if chance >= 75:   clr, lbl, pill = "#10b981", "Strong Admit Profile", "green"
    elif chance >= 55: clr, lbl, pill = "#f5a623", "Competitive Profile",  "gold"
    else:              clr, lbl, pill = "#c8006e", "Needs Strengthening",  "magenta"

    bar = ("linear-gradient(135deg,#10b981,#4a90d9)" if chance >= 75
           else "linear-gradient(135deg,#f5a623,#f25c54)" if chance >= 55
           else "linear-gradient(135deg,#c8006e,#f5a623)")

    st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="gs-label">Your Results</div>', unsafe_allow_html=True)

    res_col, radar_col = st.columns([1, 1.6])

    with res_col:
        st.markdown(f"""
        <div class="gs-result">
          <div class="gs-metric-bar" style="background:{bar};position:absolute;
               top:0;left:0;right:0;height:4px;border-radius:16px 16px 0 0;"></div>
          <div class="gs-label" style="margin-bottom:0.5rem;">Predicted Admission Chance</div>
          <div style="font-family:'Fraunces',serif;font-size:5rem;font-weight:900;
                      color:{clr} !important;-webkit-text-fill-color:{clr} !important;
                      line-height:1;margin-bottom:0.75rem;">{chance}%</div>
          <div class="gs-pill gs-pill-{pill}">{lbl}</div>
          <div style="font-size:0.72rem;color:#7b8cb0;margin-top:0.75rem;">
            {"Real ML model · Gradient Boosting" if USE_ML else "Formula estimate"}
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div style="height:0.75rem"></div>', unsafe_allow_html=True)
        if st.button("Save My Profile", use_container_width=True):
            try:
                from dashboard.db import supabase
                supabase.table("user_profiles").insert({
                    "gre": gre_v, "toefl": toefl_v, "cgpa": cgpa_v,
                    "sop": sop_v, "lor": lor_v, "uni_rating": uni_v,
                    "research": res_v, "predicted_chance": chance
                }).execute()
                st.success("Profile saved.")
            except Exception as e:
                st.error(f"Could not save: {e}")

    with radar_col:
        cats  = ["GRE", "TOEFL", "CGPA", "SoP", "LoR", "Uni Rating", "Research"]
        vals  = [gre_v/340, toefl_v/120, cgpa_v/10, sop_v/5, lor_v/5, uni_v/5, res_v]
        cats2 = cats + [cats[0]]
        vals2 = vals + [vals[0]]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=vals2, theta=cats2, fill="toself",
            fillcolor="rgba(200,0,110,0.10)",
            line=dict(color="#c8006e", width=2.5),
            marker=dict(size=5, color="#c8006e"), name="Your Profile"))
        fig.add_trace(go.Scatterpolar(
            r=[0.85]*len(cats2), theta=cats2, fill="toself",
            fillcolor="rgba(245,166,35,0.06)",
            line=dict(color="#f5a623", width=1.5, dash="dot"),
            name="Target (85th pct)"))
        fig.update_layout(
            polar=dict(bgcolor="rgba(255,255,255,0.60)",
                       radialaxis=dict(visible=True, range=[0,1],
                                       showticklabels=False,
                                       gridcolor="rgba(13,27,62,0.10)"),
                       angularaxis=dict(gridcolor="rgba(13,27,62,0.08)")),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.10,
                        font=dict(family="Outfit", size=11, color="#3d4f7a")),
            paper_bgcolor="rgba(255,255,255,0)", font_family="Outfit",
            margin=dict(l=50, r=50, t=30, b=50), height=320)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)


    st.markdown('<div class="gs-label">Similar Applicants from Our Dataset</div>',
                unsafe_allow_html=True)
    similar = df_adm[
        (df_adm["GRE"].between(gre_v - 10, gre_v + 10)) &
        (df_adm["CGPA"].between(cgpa_v - 0.5, cgpa_v + 0.5))
    ].copy().head(10)

    if len(similar) > 0:
        k1, k2, k3 = st.columns(3)
        for col, lbl, val, sub, b in [
            (k1, "Avg Admit Chance", f"{similar['Admit'].mean():.1f}%",
             "among similar profiles", "linear-gradient(90deg,#c8006e,#f5a623)"),
            (k2, "Highest Chance", f"{similar['Admit'].max():.1f}%",
             "in similar group", "linear-gradient(90deg,#10b981,#4a90d9)"),
            (k3, "Similar Profiles Found", str(len(similar)),
             "in our dataset", "linear-gradient(90deg,#0d1b3e,#4a90d9)"),
        ]:
            with col:
                st.markdown(f"""
                <div class="gs-metric">
                  <div class="gs-metric-bar" style="background:{b}"></div>
                  <div class="gs-metric-label">{lbl}</div>
                  <div class="gs-metric-value">{val}</div>
                  <div class="gs-metric-sub">{sub}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
        fig2 = px.scatter(similar, x="GRE", y="Admit", color="Research",
                          color_discrete_map={0: "#f5a623", 1: "#10b981"},
                          size="CGPA",
                          hover_data=["TOEFL", "CGPA", "SOP", "LOR"],
                          labels={"GRE": "GRE Score", "Admit": "Admit Chance (%)",
                                  "Research": "Has Research"},
                          title="Similar Applicants — GRE vs Admit Chance")
        fig2.add_hline(y=chance, line_dash="dot", line_color="#c8006e",
                       annotation_text=f"Your prediction: {chance}%",
                       annotation_position="top right")
        fig2.update_layout(paper_bgcolor="rgba(255,255,255,0.80)",
                           plot_bgcolor="rgba(247,248,252,0.90)",
                           font_family="Outfit", font_color="#3d4f7a",
                           margin=dict(l=0, r=160, t=40, b=0),
                           height=320,
                           xaxis=dict(showgrid=True, gridcolor="rgba(13,27,62,0.06)"),
                           yaxis=dict(showgrid=True, gridcolor="rgba(13,27,62,0.06)"),
                           title_font=dict(size=12, color="#0d1b3e", family="Fraunces"))
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.78);border-radius:12px;
                    padding:1.25rem;text-align:center;color:#7b8cb0;font-size:0.88rem;">
          No applicants with a closely matching profile found in the dataset.
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)

   
    st.markdown('<div class="gs-label">Your Action Plan</div>', unsafe_allow_html=True)
    actions = []
    if gre_v < 315:
        actions.append(("Improve Your GRE", "#c8006e",
                        "Your GRE is below 315. Aim for 320+. Each 5-point gain meaningfully increases your chances. Spend 2-3 months on ETS official materials and Magoosh."))
    if cgpa_v < 8.0:
        actions.append(("Address Your CGPA", "#0d1b3e",
                        "A CGPA below 8.0 will be scrutinised. Address this in your SoP by showing an upward grade trend and compensating with strong research or work experience."))
    if res_v == 0:
        actions.append(("Get Research Experience", "#f5a623",
                        "Research is the single biggest differentiator for top programs. Email 3-5 professors at your university this week asking to assist on an ongoing project."))
    if sop_v < 4.0:
        actions.append(("Strengthen Your SoP", "#4a90d9",
                        "A weak SoP costs admissions even with great scores. Name specific faculty you want to work with, tie your past experience to your future goals, and get it reviewed by a mentor."))
    if lor_v < 4.0:
        actions.append(("Secure Stronger LoRs", "#10b981",
                        "Ask people who directly supervised your work. Give them your CV and SoP draft so they can write specifically about your contributions rather than a generic letter."))
    if not actions:
        actions.append(("Apply Strategically", "#10b981",
                        "Your profile looks competitive. Build a balanced list — 2-3 dream schools, 3-4 targets, 2-3 safe options. Use the University Recommendation page to find the right fit."))

    cols = st.columns(min(len(actions), 3))
    for col, (title, c, text) in zip(cols, actions[:3]):
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.78);border:1px solid rgba(255,255,255,0.90);
                        border-top:3px solid {c};border-radius:12px;padding:1.1rem;
                        box-shadow:0 2px 8px rgba(13,27,62,0.07);">
              <div style="font-family:'Fraunces',serif;font-size:0.95rem;font-weight:900;
                          color:{c} !important;-webkit-text-fill-color:{c} !important;
                          margin-bottom:0.5rem;">{title}</div>
              <div style="font-size:0.83rem;color:#3d4f7a;line-height:1.65;">{text}</div>
            </div>""", unsafe_allow_html=True)

    if len(actions) > 3:
        st.markdown('<div style="height:0.75rem"></div>', unsafe_allow_html=True)
        cols2 = st.columns(min(len(actions) - 3, 3))
        for col, (title, c, text) in zip(cols2, actions[3:]):
            with col:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.78);border:1px solid rgba(255,255,255,0.90);
                            border-top:3px solid {c};border-radius:12px;padding:1.1rem;
                            box-shadow:0 2px 8px rgba(13,27,62,0.07);">
                  <div style="font-family:'Fraunces',serif;font-size:0.95rem;font-weight:900;
                              color:{c} !important;-webkit-text-fill-color:{c} !important;
                              margin-bottom:0.5rem;">{title}</div>
                  <div style="font-size:0.83rem;color:#3d4f7a;line-height:1.65;">{text}</div>
                </div>""", unsafe_allow_html=True)

    if st.button("Reset and Start Over"):
        st.session_state["analyzed"] = False
        st.session_state["inputs"] = {}
        st.rerun()

import streamlit as st
import plotly.graph_objects as go
from helpers import page_header

st.set_page_config(page_title="Profile Analyzer · GradScope", page_icon="🎓", layout="wide")
page_header("🎓 Evaluate", "Profile Analyzer",
            "Enter your scores to see how competitive your profile is — and exactly where to improve.")

left, _, right = st.columns([2, 0.15, 2.5])
with left:
    st.markdown('<div class="gs-label" style="margin-bottom:1rem;">Your Academic Profile</div>', unsafe_allow_html=True)
    gre   = st.slider("GRE Score", 260, 340, 310)
    toefl = st.slider("TOEFL Score", 80, 120, 105)
    cgpa  = st.slider("CGPA (out of 10)", 6.0, 10.0, 8.5, step=0.1)
    c1,c2 = st.columns(2)
    with c1: uni_r = st.selectbox("University Rating", [1,2,3,4,5], index=2)
    with c2: research = st.selectbox("Research Experience", ["No","Yes"])
    sop = st.slider("Statement of Purpose", 1.0, 5.0, 3.5, step=0.5)
    lor = st.slider("Letter of Recommendation", 1.0, 5.0, 3.5, step=0.5)
    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
    st.button("Analyze My Profile →", type="primary", use_container_width=True)

rv = 1 if research == "Yes" else 0
chance = round(((gre/340)*0.20+(toefl/120)*0.10+(cgpa/10)*0.25+
                (sop/5)*0.15+(lor/5)*0.15+(uni_r/5)*0.10+rv*0.05)*100, 1)

with right:
    if chance >= 75:   clr,lbl = "#10b981","Strong Admit Profile"
    elif chance >= 55: clr,lbl = "#f5a623","Competitive Profile"
    else:              clr,lbl = "#c8006e","Needs Strengthening"

    bar = (f"linear-gradient(135deg,#10b981,#4a90d9)" if chance>=75
           else "linear-gradient(135deg,#f5a623,#f25c54)" if chance>=55
           else "linear-gradient(135deg,#c8006e,#f5a623)")

    st.markdown(f"""
    <div class="gs-result">
      <div class="gs-metric-bar" style="background:{bar};position:absolute;
           top:0;left:0;right:0;height:4px;border-radius:16px 16px 0 0;"></div>
      <div class="gs-label" style="margin-bottom:0.5rem;">Predicted Admission Chance</div>
      <div style="font-family:'Fraunces',serif;font-size:5.5rem;font-weight:900;
                  color:{clr};line-height:1;margin-bottom:0.7rem;">{chance}%</div>
      <div class="gs-pill gs-pill-{'green' if chance>=75 else 'gold' if chance>=55 else 'magenta'}">{lbl}</div>
    </div>""", unsafe_allow_html=True)

    cats  = ["GRE","TOEFL","CGPA","SoP","LoR","Uni Rating","Research"]
    vals  = [gre/340,toefl/120,cgpa/10,sop/5,lor/5,uni_r/5,rv]
    cats2 = cats+[cats[0]]; vals2 = vals+[vals[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals2,theta=cats2,fill="toself",
        fillcolor="rgba(200,0,110,0.10)",
        line=dict(color="#c8006e",width=2.5),marker=dict(size=5,color="#c8006e"),name="Your Profile"))
    fig.add_trace(go.Scatterpolar(r=[0.85]*len(cats2),theta=cats2,fill="toself",
        fillcolor="rgba(245,166,35,0.06)",
        line=dict(color="#f5a623",width=1.5,dash="dot"),name="Target (85th pct)"))
    fig.update_layout(
        polar=dict(bgcolor="rgba(255,255,255,0.60)",
                   radialaxis=dict(visible=True,range=[0,1],showticklabels=False,
                                   gridcolor="rgba(13,27,62,0.10)"),
                   angularaxis=dict(gridcolor="rgba(13,27,62,0.08)")),
        legend=dict(orientation="h",x=0.5,xanchor="center",y=-0.12,
                    font=dict(family="Outfit",size=11,color="#3d4f7a")),
        paper_bgcolor="rgba(255,255,255,0)",
        font_family="Outfit", margin=dict(l=40,r=40,t=20,b=40), height=295)
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="gs-label">Score Breakdown — How Each Factor Contributes</div>', unsafe_allow_html=True)
components = {"GRE":((gre/340)*0.20*100,20),"CGPA":((cgpa/10)*0.25*100,25),
              "SoP":((sop/5)*0.15*100,15),"LoR":((lor/5)*0.15*100,15),
              "TOEFL":((toefl/120)*0.10*100,10),"Uni Rating":((uni_r/5)*0.10*100,10),
              "Research":(rv*0.05*100,5)}
for col,(name,(earned,mx)) in zip(st.columns(7),components.items()):
    pct = earned/mx*100
    c = "#10b981" if pct>=75 else "#f5a623" if pct>=50 else "#c8006e"
    with col:
        st.markdown(f"""
        <div style="text-align:center;padding:0.8rem 0.4rem;
                    background:rgba(255,255,255,0.78);border:1px solid rgba(255,255,255,0.90);
                    border-radius:12px;box-shadow:0 2px 8px rgba(13,27,62,0.07);">
          <div style="font-family:'Outfit',sans-serif;font-size:0.62rem;font-weight:700;
                      letter-spacing:0.08em;text-transform:uppercase;color:#7b8cb0;margin-bottom:0.3rem;">{name}</div>
          <div style="font-family:'Fraunces',serif;font-size:1.35rem;font-weight:900;
                      color:{c};line-height:1;">{earned:.1f}</div>
          <div style="font-size:0.65rem;color:#7b8cb0;margin-bottom:0.35rem;">of {mx}</div>
          <div style="background:rgba(13,27,62,0.08);border-radius:10px;height:4px;overflow:hidden;">
            <div style="height:4px;width:{pct:.0f}%;background:{c};border-radius:10px;"></div>
          </div>
        </div>""", unsafe_allow_html=True)

tips = []
if gre<315:  tips.append(("GRE Score","#c8006e","Aim for 320+. A 5–10 point improvement significantly boosts your profile."))
if cgpa<8.5: tips.append(("CGPA","#0d1b3e","A CGPA above 8.5 is ideal for top-50 universities."))
if rv==0:    tips.append(("Research","#f5a623","Students with research experience have ~15% higher admit rates."))
if sop<4.0:  tips.append(("SoP Quality","#4a90d9","Get your SoP reviewed by a mentor — quality writing sets you apart."))
if lor<4.0:  tips.append(("LoR Strength","#10b981","Ask professors who know your work well — specificity beats seniority."))
if tips:
    st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="gs-label">Personalised Improvement Tips</div>', unsafe_allow_html=True)
    for col,(area,c,tip) in zip(st.columns(min(len(tips),3)),tips):
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.78);border:1px solid rgba(255,255,255,0.90);
                        border-left:4px solid {c};border-radius:12px;padding:1rem 1.1rem;
                        box-shadow:0 2px 8px rgba(13,27,62,0.07);">
              <div style="font-family:'Outfit',sans-serif;font-size:0.72rem;font-weight:700;
                          letter-spacing:0.08em;text-transform:uppercase;color:{c};margin-bottom:0.4rem;">{area}</div>
              <div style="font-size:0.85rem;color:#3d4f7a;line-height:1.6;">{tip}</div>
            </div>""", unsafe_allow_html=True)
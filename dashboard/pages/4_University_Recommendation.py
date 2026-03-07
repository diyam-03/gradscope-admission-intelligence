import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from helpers import page_header, kpi_row

st.set_page_config(page_title="University Recommendation · GradScope", page_icon="🎯", layout="wide")
page_header("🎯 Discover", "University Recommendation",
            "Get your personalised Dream, Target and Safe university list based on your profile.")

@st.cache_data
def load():
    p = Path(__file__).parent.parent.parent / "data" / "universities.csv"
    df = pd.read_csv(p); df.columns = df.columns.str.strip()
    return df.drop_duplicates(subset=["institution"])

df = load()
T = dict(paper_bgcolor="rgba(255,255,255,0.80)", plot_bgcolor="rgba(247,248,252,0.90)",
         font_family="Outfit", font_color="#3d4f7a", margin=dict(l=0,r=0,t=10,b=40))

st.markdown('<div class="gs-filter"><div class="gs-label">Enter Your Profile</div>', unsafe_allow_html=True)
pc1,pc2,pc3,pc4 = st.columns(4)
with pc1: gre   = st.slider("GRE Score",260,340,310)
with pc2: cgpa  = st.slider("CGPA",6.0,10.0,8.5,step=0.1)
with pc3: toefl = st.slider("TOEFL Score",80,120,105)
with pc4: research = st.selectbox("Research Experience",["No","Yes"])
st.markdown('</div>', unsafe_allow_html=True)

rv = 1 if research=="Yes" else 0
score = (gre/340)*0.5+(cgpa/10)*0.4+(toefl/120)*0.1
s100  = score*100
dream_cut  = max(5,  int(20*(1-score*0.4)))
target_cut = max(25, int(60*(1-score*0.3)))
dream  = df[df["world_rank"]<=dream_cut].head(8)
target = df[(df["world_rank"]>dream_cut) & (df["world_rank"]<=target_cut)].head(10)
safe   = df[(df["world_rank"]>target_cut)& (df["world_rank"]<=200)].head(10)

kpi_row([("Profile Score",f"{s100:.1f}","out of 100"),
         ("Dream",str(len(dream)),f"rank ≤ {dream_cut}"),
         ("Target",str(len(target)),f"rank {dream_cut+1}–{target_cut}"),
         ("Safe",str(len(safe)),f"rank {target_cut+1}–200")])
st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)

dcols_base = ["world_rank","institution","country","score"]
def tier_col(col, data, icon, title, admit, hdr_css, txt_color):
    dcols = [c for c in dcols_base if c in data.columns]
    with col:
        st.markdown(f"""
        <div style="{hdr_css};border-radius:14px 14px 0 0;padding:0.9rem 1.1rem;">
          <div style="display:flex;align-items:center;gap:0.45rem;">
            <span style="font-size:1.2rem">{icon}</span>
            <span style="font-family:'Fraunces',serif;font-size:1.1rem;font-weight:900;
                         color:{txt_color};">{title}</span>
          </div>
          <div style="font-family:'Outfit',sans-serif;font-size:0.75rem;
                      color:{txt_color};opacity:0.75;margin-top:0.2rem;">
            Est. admit chance: {admit}
          </div>
        </div>""", unsafe_allow_html=True)
        if len(data)==0:
            st.markdown("""<div style="background:rgba(255,255,255,0.70);border:1px solid rgba(255,255,255,0.85);
                border-top:none;border-radius:0 0 14px 14px;padding:1.5rem;text-align:center;
                font-size:0.85rem;color:#7b8cb0;font-style:italic;">No universities in this tier.</div>""",
                unsafe_allow_html=True)
        else:
            st.dataframe(data[dcols].rename(columns={"world_rank":"Rank","institution":"University",
                                                      "country":"Country","score":"Score"}),
                         use_container_width=True,hide_index=True,height=min(len(data)*38+40,320))

c1,c2,c3 = st.columns(3)
tier_col(c1,dream, "⭐","Dream","< 30%",
         "background:linear-gradient(135deg,#0d1b3e,#1a2d6b)","#ffffff")
tier_col(c2,target,"🎯","Target","30–65%",
         "background:linear-gradient(135deg,#c8006e,#e0057c)","#ffffff")
tier_col(c3,safe,  "✅","Safe","65–90%",
         "background:linear-gradient(135deg,#065f46,#047857)","#ffffff")

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)
top100 = df[df["world_rank"]<=100].copy()
if "score" in top100.columns:
    top100["Tier"]="Safe"
    top100.loc[top100["world_rank"]<=target_cut,"Tier"]="Target"
    top100.loc[top100["world_rank"]<=dream_cut,"Tier"]="Dream"
    st.markdown('<div class="gs-label">Score vs World Rank — Top 100</div>', unsafe_allow_html=True)
    fig = px.scatter(top100,x="world_rank",y="score",color="Tier",hover_name="institution",
                     color_discrete_map={"Dream":"#0d1b3e","Target":"#c8006e","Safe":"#10b981"},
                     labels={"world_rank":"World Rank","score":"Overall Score"})
    fig.update_traces(marker=dict(size=9,opacity=0.82))
    fig.update_layout(**T,height=330,
                      xaxis=dict(showgrid=True,gridcolor="rgba(13,27,62,0.06)"),
                      yaxis=dict(showgrid=True,gridcolor="rgba(13,27,62,0.06)"),
                      legend=dict(orientation="h",x=0.5,xanchor="center",y=-0.18,font_size=11))
    st.plotly_chart(fig, use_container_width=True)

all_recs = pd.concat([dream.assign(Tier="Dream"),target.assign(Tier="Target"),safe.assign(Tier="Safe")])
st.download_button("⬇  Download my university list as CSV",data=all_recs.to_csv(index=False),
                   file_name="gradscope_my_universities.csv",mime="text/csv")
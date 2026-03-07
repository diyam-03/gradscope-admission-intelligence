import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from helpers import page_header

st.set_page_config(page_title="University Comparison · GradScope", page_icon="⚖️", layout="wide")
page_header("⚖️ Compare", "University Comparison",
            "Select up to 5 universities for a detailed side-by-side comparison across all ranking dimensions.")

@st.cache_data
def load():
    p = Path(__file__).parent.parent.parent / "data" / "universities.csv"
    df = pd.read_csv(p); df.columns = df.columns.str.strip()
    return df.drop_duplicates(subset=["institution"])

df = load()
SCORE_MAP = {"score":"Overall","research_score":"Research","teaching_score":"Teaching",
             "international_score":"International","industry_score":"Industry","citations_score":"Citations"}
PALETTE = ["#0d1b3e","#c8006e","#10b981","#f5a623","#4a90d9"]
T = dict(paper_bgcolor="rgba(255,255,255,0.80)", plot_bgcolor="rgba(247,248,252,0.90)",
         font_family="Outfit", font_color="#3d4f7a", margin=dict(l=0,r=0,t=20,b=0))

st.markdown('<div class="gs-filter"><div class="gs-label">Choose Universities to Compare (up to 5)</div>',
            unsafe_allow_html=True)
defaults = [n for n in ["Harvard University","Massachusetts Institute of Technology",
                         "Stanford University","University of Oxford"] if n in df["institution"].values][:2]
selected = st.multiselect("Universities", df["institution"].tolist(), default=defaults,
                          max_selections=5, label_visibility="collapsed", placeholder="Type to search…")
st.markdown('</div>', unsafe_allow_html=True)

if not selected:
    st.markdown("""
    <div style="text-align:center;padding:4rem 0;">
      <div style="font-size:2.5rem;margin-bottom:0.75rem;">⚖️</div>
      <div style="font-family:'Fraunces',serif;font-size:1.5rem;font-weight:900;
                  color:#0d1b3e;">Select universities above to start comparing</div>
      <div style="font-size:0.9rem;color:#7b8cb0;margin-top:0.4rem;">
        Try: Stanford, Oxford, MIT, Cambridge, Harvard</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

comp = df[df["institution"].isin(selected)].copy()
cmap = {u:PALETTE[i%len(PALETTE)] for i,u in enumerate(selected)}
rcols = [k for k in SCORE_MAP if k in comp.columns]
rlbls = [SCORE_MAP[k] for k in rcols]

for col,(_,row) in zip(st.columns(len(comp)),comp.iterrows()):
    c   = cmap[row["institution"]]
    ovr = f"{row['score']:.1f}" if "score" in comp.columns else "—"
    res = f"{row['research_score']:.1f}" if "research_score" in comp.columns else "—"
    rnk = f"#{int(row['world_rank'])}" if "world_rank" in comp.columns else "—"
    with col:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.82);border:1.5px solid rgba(255,255,255,0.92);
                    border-top:4px solid {c};border-radius:14px;padding:1.1rem;
                    box-shadow:0 4px 16px rgba(13,27,62,0.09);">
          <div style="font-family:'Outfit',sans-serif;font-size:0.7rem;font-weight:700;
                      color:{c};margin-bottom:0.3rem;">{rnk} · {row.get('country','—')}</div>
          <div style="font-family:'Fraunces',serif;font-size:0.95rem;font-weight:900;
                      color:#0d1b3e;line-height:1.25;margin-bottom:0.7rem;">{row['institution'][:40]}</div>
          <div style="display:flex;gap:1.2rem;">
            <div>
              <div style="font-size:0.62rem;text-transform:uppercase;letter-spacing:.08em;color:#7b8cb0;font-weight:700;">Overall</div>
              <div style="font-family:'Fraunces',serif;font-size:1.5rem;font-weight:900;color:{c};">{ovr}</div>
            </div>
            <div>
              <div style="font-size:0.62rem;text-transform:uppercase;letter-spacing:.08em;color:#7b8cb0;font-weight:700;">Research</div>
              <div style="font-family:'Fraunces',serif;font-size:1.5rem;font-weight:900;color:{c};">{res}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)

if len(rcols)>=3:
    st.markdown('<div class="gs-label">Radar — Multi-Dimensional View</div>', unsafe_allow_html=True)
    rl,rr = st.columns([3,2])
    with rl:
        rlbls_c = rlbls+[rlbls[0]]
        fig = go.Figure()
        for _,row in comp.iterrows():
            vals  = [row[k] for k in rcols]
            norm  = [v/df[k].max() if df[k].max()>0 else 0 for v,k in zip(vals,rcols)]
            nc    = norm+[norm[0]]; c = cmap[row["institution"]]
            fig.add_trace(go.Scatterpolar(r=nc,theta=rlbls_c,fill="toself",
                fillcolor=c+"22",line=dict(color=c,width=2.5),marker=dict(size=5,color=c),
                name=row["institution"].split(",")[0][:22]))
        fig.update_layout(
            polar=dict(bgcolor="rgba(255,255,255,0.65)",
                       radialaxis=dict(visible=True,range=[0,1],showticklabels=False,
                                       gridcolor="rgba(13,27,62,0.10)"),
                       angularaxis=dict(gridcolor="rgba(13,27,62,0.08)")),
            legend=dict(orientation="h",x=0.5,xanchor="center",y=-0.12,
                        font=dict(family="Outfit",size=11,color="#3d4f7a")),
            paper_bgcolor="rgba(255,255,255,0)",font_family="Outfit",
            margin=dict(l=40,r=40,t=10,b=60),height=360)
        st.plotly_chart(fig, use_container_width=True)
    with rr:
        if "score" in comp.columns:
            cs = comp.sort_values("score",ascending=True)
            fig2 = go.Figure()
            for _,row in cs.iterrows():
                fig2.add_trace(go.Bar(y=[row["institution"].split(",")[0][:28]],x=[row["score"]],
                    orientation="h",marker_color=cmap[row["institution"]],
                    text=f"{row['score']:.1f}",textposition="outside",showlegend=False))
            fig2.update_layout(**T,barmode="overlay",
                               xaxis=dict(showgrid=True,gridcolor="rgba(13,27,62,0.06)",range=[0,108]),
                               yaxis=dict(showgrid=False),height=360,
                               title=dict(text="Overall Score",font=dict(size=12,color="#0d1b3e",family="Fraunces"),x=0))
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="gs-label">Score Breakdown — All Dimensions</div>', unsafe_allow_html=True)
    melt = comp[["institution"]+rcols].melt(id_vars="institution",var_name="Dimension",value_name="Score")
    melt["Dimension"] = melt["Dimension"].map(SCORE_MAP)
    fig3 = px.bar(melt,x="Dimension",y="Score",color="institution",barmode="group",
                  color_discrete_map=cmap,text=melt["Score"].round(1))
    fig3.update_traces(textposition="outside",textfont_size=10)
    fig3.update_layout(**T,xaxis=dict(showgrid=False),
                       yaxis=dict(showgrid=True,gridcolor="rgba(13,27,62,0.06)"),
                       legend=dict(orientation="h",y=-0.22,x=0.5,xanchor="center",font_size=10),
                       margin=dict(l=0,r=0,t=10,b=60),height=340,bargap=0.18,bargroupgap=0.06)
    st.plotly_chart(fig3, use_container_width=True)

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="gs-label">Raw Data</div>', unsafe_allow_html=True)
dcols = [c for c in ["institution","country","world_rank","score","research_score",
                      "teaching_score","international_score"] if c in comp.columns]
st.dataframe(comp[dcols].rename(columns={"institution":"University","country":"Country",
    "world_rank":"Rank","score":"Overall","research_score":"Research",
    "teaching_score":"Teaching","international_score":"International"}),
    use_container_width=True,hide_index=True)
st.download_button("⬇  Download comparison as CSV",data=comp.to_csv(index=False),
                   file_name="gradscope_comparison.csv",mime="text/csv")
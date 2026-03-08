import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from helpers import page_header, kpi_row

st.set_page_config(page_title="University Explorer · GradScope", page_icon="🏫", layout="wide", initial_sidebar_state="expanded")
page_header("🏫 Explore", "University Explorer",
            "Browse and filter 2,000+ universities across 70+ countries.")

@st.cache_data
def load():
    p = Path(__file__).parent.parent.parent / "data" / "universities.csv"
    df = pd.read_csv(p); df.columns = df.columns.str.strip()
    return df.drop_duplicates(subset=["institution"])

df = load()
T = dict(paper_bgcolor="rgba(255,255,255,0.80)", plot_bgcolor="rgba(247,248,252,0.90)",
         font_family="Outfit", font_color="#3d4f7a", margin=dict(l=0,r=0,t=10,b=0))

st.markdown('<div class="gs-filter"><div class="gs-label">Filter Universities</div>', unsafe_allow_html=True)
fc1, fc2, fc3 = st.columns([2,2,1])
with fc1: country = st.selectbox("Country", ["All Countries"]+sorted(df["country"].dropna().unique().tolist()), label_visibility="collapsed")
with fc2: search  = st.text_input("Search", placeholder="e.g. MIT, Oxford, Stanford…", label_visibility="collapsed")
with fc3: top_n   = st.number_input("Top N", 10, 2000, 100, 10, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

filt = df.copy()
if country != "All Countries": filt = filt[filt["country"]==country]
if search: filt = filt[filt["institution"].str.contains(search,case=False,na=False)]
filt = filt[filt["world_rank"]<=top_n].sort_values("world_rank")

kpi_row([
    ("Showing",    f"{len(filt):,}",                                           "universities"),
    ("Countries",  str(filt["country"].nunique()),                             "represented"),
    ("Avg Score",  f"{filt['score'].mean():.1f}" if "score" in filt.columns else "—", "out of 100"),
    ("Top Ranked", f"#{int(filt['world_rank'].min())}" if len(filt) else "—", "in filter"),
])
st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)

left, right = st.columns([3,2])
with left:
    st.markdown('<div class="gs-label">Rankings Table</div>', unsafe_allow_html=True)
    dcols = [c for c in ["world_rank","institution","country","score","research_score","teaching_score"] if c in filt.columns]
    st.dataframe(filt[dcols].rename(columns={"world_rank":"Rank","institution":"University","country":"Country",
                                              "score":"Overall","research_score":"Research","teaching_score":"Teaching"}),
                 use_container_width=True, hide_index=True, height=450)
with right:
    if "score" in filt.columns and len(filt)>1:
        st.markdown('<div class="gs-label">Score Distribution</div>', unsafe_allow_html=True)
        fig = px.histogram(filt, x="score", nbins=20, color_discrete_sequence=["#0d1b3e"],
                           labels={"score":"Overall Score"})
        fig.update_layout(**T, bargap=0.07, height=210,
                          xaxis=dict(showgrid=False), yaxis=dict(showgrid=True,gridcolor="rgba(13,27,62,0.06)"))
        st.plotly_chart(fig, use_container_width=True)
    top_c = filt.groupby("country").size().reset_index(name="n").sort_values("n",ascending=False).head(8)
    st.markdown('<div class="gs-label">Top Countries</div>', unsafe_allow_html=True)
    fig2 = px.bar(top_c, x="n", y="country", orientation="h",
                  color_discrete_sequence=["#c8006e"], labels={"n":"Universities","country":""})
    fig2.update_layout(**T, height=215, xaxis=dict(showgrid=True,gridcolor="rgba(13,27,62,0.06)"),
                       yaxis=dict(showgrid=False))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)
st.download_button("⬇  Download filtered data as CSV", data=filt.to_csv(index=False),
                   file_name="gradscope_universities.csv", mime="text/csv")
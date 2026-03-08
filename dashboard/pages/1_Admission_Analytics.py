import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path
from helpers import page_header, kpi_row

st.set_page_config(page_title="Admission Analytics · GradScope", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
page_header("📊 Analyze", "Admission Analytics",
            "Explore what really drives admission decisions — based on 400+ real graduate applicant records.")

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
df["Admit %"] = (df["Admit"] * 100).round(1) if df["Admit"].max() <= 1 else df["Admit"].round(1)
df["Research Label"] = df["Research"].map({0: "No Research", 1: "Has Research"})

T = dict(paper_bgcolor="rgba(255,255,255,0.80)", plot_bgcolor="rgba(247,248,252,0.90)",
         font_family="Outfit", font_color="#3d4f7a", margin=dict(l=0,r=0,t=32,b=0))

kpi_row([
    ("Total Applicants",  f"{len(df):,}",              "in dataset"),
    ("Avg GRE",           f"{df['GRE'].mean():.0f}",   "out of 340"),
    ("Avg CGPA",          f"{df['CGPA'].mean():.2f}",  "out of 10"),
    ("Avg Admit Chance",  f"{df['Admit %'].mean():.1f}%", "mean"),
    ("With Research",     f"{int(df['Research'].sum())}", f"of {len(df)}"),
])
st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="gs-label">Score vs Admission Probability</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    fig = px.scatter(df, x="GRE", y="Admit %", color="Research Label",
                     color_discrete_map={"No Research":"#f5a623","Has Research":"#10b981"},
                     trendline="ols", trendline_scope="overall",
                     trendline_color_override="#c8006e", opacity=0.65,
                     title="GRE Score vs Admission Chance",
                     labels={"GRE":"GRE Score","Admit %":"Admit Chance (%)"})
    fig.update_traces(marker_size=6)
    fig.update_layout(**T, height=320,
                      xaxis=dict(showgrid=True, gridcolor="rgba(13,27,62,0.06)"),
                      yaxis=dict(showgrid=True, gridcolor="rgba(13,27,62,0.06)"),
                      legend=dict(orientation="h",y=-0.22,x=0.5,xanchor="center",font_size=11),
                      title_font=dict(size=13,color="#0d1b3e",family="Fraunces"))
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig2 = px.scatter(df, x="CGPA", y="Admit %", color="UniRating",
                      color_continuous_scale=["#eef1f9","#0d1b3e"],
                      trendline="ols", trendline_scope="overall",
                      trendline_color_override="#c8006e", opacity=0.65,
                      title="CGPA vs Admission Chance",
                      labels={"CGPA":"CGPA","Admit %":"Admit Chance (%)","UniRating":"Uni Rating"})
    fig2.update_traces(marker_size=6)
    fig2.update_layout(**T, height=320,
                       xaxis=dict(showgrid=True, gridcolor="rgba(13,27,62,0.06)"),
                       yaxis=dict(showgrid=True, gridcolor="rgba(13,27,62,0.06)"),
                       coloraxis_colorbar=dict(title="Rating",thickness=12,len=0.6),
                       title_font=dict(size=13,color="#0d1b3e",family="Fraunces"))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="gs-label">Score Distributions</div>', unsafe_allow_html=True)
d1, d2, d3 = st.columns(3)
for col, field, color, title in [
    (d1,"GRE",   "#0d1b3e","GRE Score Distribution"),
    (d2,"CGPA",  "#c8006e","CGPA Distribution"),
    (d3,"Admit %","#f5a623","Admit Chance Distribution"),
]:
    with col:
        fig = px.histogram(df, x=field, nbins=22, color_discrete_sequence=[color], title=title)
        fig.update_layout(**T, bargap=0.07, height=250,
                          xaxis=dict(showgrid=False),
                          yaxis=dict(showgrid=True,gridcolor="rgba(13,27,62,0.06)"),
                          title_font=dict(size=12,color="#0d1b3e",family="Fraunces"))
        st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="gs-label">What Factors Matter Most?</div>', unsafe_allow_html=True)
e1, e2 = st.columns(2)
with e1:
    fig = px.box(df, x="Research Label", y="Admit %", color="Research Label",
                 color_discrete_map={"No Research":"#f5a623","Has Research":"#10b981"},
                 title="Research Experience Impact", points="outliers",
                 labels={"Research Label":"","Admit %":"Admit Chance (%)"})
    fig.update_layout(**T, showlegend=False, height=290,
                      xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=True,gridcolor="rgba(13,27,62,0.06)"),
                      title_font=dict(size=12,color="#0d1b3e",family="Fraunces"))
    st.plotly_chart(fig, use_container_width=True)
with e2:
    ra = df.groupby("UniRating")["Admit %"].mean().reset_index().rename(columns={"Admit %":"Avg %"})
    fig = px.bar(ra, x="UniRating", y="Avg %", color="Avg %",
                 color_continuous_scale=["#eef1f9","#0d1b3e"],
                 title="Avg Admit Chance by University Rating",
                 text=ra["Avg %"].round(1).astype(str)+"%")
    fig.update_traces(textposition="outside")
    fig.update_layout(**T, showlegend=False, height=290, coloraxis_showscale=False,
                      xaxis=dict(showgrid=False,type="category"),
                      yaxis=dict(showgrid=True,gridcolor="rgba(13,27,62,0.06)"),
                      title_font=dict(size=12,color="#0d1b3e",family="Fraunces"))
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)
st.download_button("Download admissions CSV", data=df.to_csv(index=False),
                   file_name="gradscope_admissions.csv", mime="text/csv")
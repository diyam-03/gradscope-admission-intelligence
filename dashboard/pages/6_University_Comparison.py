import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from helpers import page_header

st.set_page_config(page_title="University Comparison · GradScope", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")
page_header("Compare", "University Comparison",
            "Select up to 5 universities for a detailed side-by-side comparison across all ranking dimensions.",
            active="University_Comparison")

@st.cache_data
def load():
    p = Path(__file__).parent.parent.parent / "data" / "universities.csv"
    df = pd.read_csv(p)
    df.columns = df.columns.str.strip()
    for c in ["world_rank","overall_score","academic_score","employer_score",
              "faculty_score","citations_score"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.drop_duplicates(subset=["institution"])

df = load()


SCORE_MAP = {
    "overall_score":   "Overall",
    "academic_score":  "Academic",
    "employer_score":  "Employer",
    "faculty_score":   "Faculty",
    "citations_score": "Citations",
}
PALETTE  = ["#0d1b3e","#c8006e","#10b981","#f5a623","#4a90d9"]
T = dict(paper_bgcolor="rgba(255,255,255,0.80)", plot_bgcolor="rgba(247,248,252,0.90)",
         font_family="Outfit", font_color="#3d4f7a", margin=dict(l=0,r=0,t=20,b=0))


st.markdown('<div class="gs-label">Choose Universities to Compare (up to 5)</div>', unsafe_allow_html=True)
defaults = [n for n in ["Harvard University","Massachusetts Institute of Technology (MIT)",
                         "Stanford University","University of Oxford"]
            if n in df["institution"].values][:2]
selected = st.multiselect("Universities", df["institution"].tolist(), default=defaults,
                          max_selections=5, label_visibility="collapsed",
                          placeholder="Type to search a university...")

if not selected:
    st.markdown("""
    <div style="text-align:center;padding:5rem 0;">
      <div style="font-family:'Fraunces',serif;font-size:1.6rem;font-weight:900;
                  color:#0d1b3e;">Select universities above to begin</div>
      <div style="font-size:0.9rem;color:#7b8cb0;margin-top:0.5rem;">
        Try: Harvard, MIT, Stanford, Oxford, Cambridge</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

comp  = df[df["institution"].isin(selected)].copy()
cmap  = {u: PALETTE[i % len(PALETTE)] for i, u in enumerate(selected)}
rcols = [k for k in SCORE_MAP if k in comp.columns]
rlbls = [SCORE_MAP[k] for k in rcols]

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)


cards_html = '<div style="display:grid;grid-template-columns:repeat(' + str(len(comp)) + ',1fr);gap:1rem;margin-bottom:1.5rem;">'

for _, row in comp.iterrows():
    c   = cmap[row["institution"]]
    rnk = f'#{int(row["world_rank"])}' if pd.notna(row.get("world_rank")) else "—"
    ovr = f'{row["overall_score"]:.1f}' if pd.notna(row.get("overall_score")) else "—"
    aca = f'{row["academic_score"]:.1f}' if pd.notna(row.get("academic_score")) else "—"
    emp = f'{row["employer_score"]:.1f}' if pd.notna(row.get("employer_score")) else "—"
    fac = f'{row["faculty_score"]:.1f}' if pd.notna(row.get("faculty_score")) else "—"
    cit = f'{row["citations_score"]:.1f}' if pd.notna(row.get("citations_score")) else "—"
    country = str(row.get("country", "—"))

    cards_html += (
        f'<div style="background:#fff;border-radius:16px;overflow:hidden;'
        f'box-shadow:0 4px 20px rgba(13,27,62,0.09);border-top:5px solid {c};">'

        # Header
        f'<div style="padding:1.1rem 1.2rem 0.8rem;">'
        f'<div style="font-size:0.72rem;font-weight:700;color:{c};letter-spacing:0.06em;'
        f'text-transform:uppercase;margin-bottom:0.35rem;">{rnk} · {country}</div>'
        f'<div style="font-family:Fraunces,serif;font-size:1.05rem;font-weight:900;'
        f'color:#0d1b3e;line-height:1.3;">{row["institution"]}</div>'
        f'</div>'

        # Big score
        f'<div style="background:linear-gradient(135deg,{c}12,{c}06);'
        f'padding:0.9rem 1.2rem;margin:0 0 0.5rem;">'
        f'<div style="font-size:0.68rem;font-weight:700;letter-spacing:0.08em;'
        f'text-transform:uppercase;color:#7b8cb0;margin-bottom:0.2rem;">QS Overall Score</div>'
        f'<div style="font-family:Fraunces,serif;font-size:2.2rem;font-weight:900;color:{c};">{ovr}</div>'
        f'</div>'

        # Score grid
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0;'
        f'border-top:1px solid rgba(13,27,62,0.06);">'

        f'<div style="padding:0.65rem 1.2rem;border-right:1px solid rgba(13,27,62,0.06);'
        f'border-bottom:1px solid rgba(13,27,62,0.06);">'
        f'<div style="font-size:0.65rem;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;color:#7b8cb0;">Academic</div>'
        f'<div style="font-size:1.1rem;font-weight:700;color:#0d1b3e;margin-top:0.1rem;">{aca}</div>'
        f'</div>'

        f'<div style="padding:0.65rem 1.2rem;border-bottom:1px solid rgba(13,27,62,0.06);">'
        f'<div style="font-size:0.65rem;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;color:#7b8cb0;">Employer</div>'
        f'<div style="font-size:1.1rem;font-weight:700;color:#0d1b3e;margin-top:0.1rem;">{emp}</div>'
        f'</div>'

        f'<div style="padding:0.65rem 1.2rem;border-right:1px solid rgba(13,27,62,0.06);">'
        f'<div style="font-size:0.65rem;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;color:#7b8cb0;">Faculty</div>'
        f'<div style="font-size:1.1rem;font-weight:700;color:#0d1b3e;margin-top:0.1rem;">{fac}</div>'
        f'</div>'

        f'<div style="padding:0.65rem 1.2rem;">'
        f'<div style="font-size:0.65rem;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;color:#7b8cb0;">Citations</div>'
        f'<div style="font-size:1.1rem;font-weight:700;color:#0d1b3e;margin-top:0.1rem;">{cit}</div>'
        f'</div>'

        f'</div>'  # score grid
        f'</div>'  # card
    )

cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)

if len(rcols) >= 3:
    cl, cr = st.columns([3, 2])

    with cl:
        st.markdown('<div class="gs-label">Radar — Multi-Dimensional View</div>', unsafe_allow_html=True)
        rlbls_c = rlbls + [rlbls[0]]
        fig = go.Figure()
        for _, row in comp.iterrows():
            vals = [row[k] for k in rcols]
            norm = [v / df[k].max() if pd.notna(v) and df[k].max() > 0 else 0
                    for v, k in zip(vals, rcols)]
            nc = norm + [norm[0]]
            c  = cmap[row["institution"]]
            fig.add_trace(go.Scatterpolar(
                r=nc, theta=rlbls_c, fill="toself",
                fillcolor=c, opacity=0.15,
                line=dict(color=c, width=2.5),
                marker=dict(size=5, color=c),
                name=row["institution"].split(",")[0][:28]))
        fig.update_layout(
            polar=dict(bgcolor="rgba(255,255,255,0.65)",
                       radialaxis=dict(visible=True, range=[0,1],
                                       showticklabels=False,
                                       gridcolor="rgba(13,27,62,0.10)"),
                       angularaxis=dict(gridcolor="rgba(13,27,62,0.08)")),
            legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.15,
                        font=dict(family="Outfit", size=11, color="#3d4f7a")),
            paper_bgcolor="rgba(255,255,255,0)", font_family="Outfit",
            margin=dict(l=40, r=40, t=10, b=70), height=380)
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        st.markdown('<div class="gs-label">Overall Score Ranking</div>', unsafe_allow_html=True)
        if "overall_score" in comp.columns:
            cs = comp.dropna(subset=["overall_score"]).sort_values("overall_score", ascending=True)
            fig2 = go.Figure()
            for _, row in cs.iterrows():
                fig2.add_trace(go.Bar(
                    y=[row["institution"].split(",")[0][:30]],
                    x=[row["overall_score"]],
                    orientation="h",
                    marker_color=cmap[row["institution"]],
                    text=f'{row["overall_score"]:.1f}',
                    textposition="outside",
                    showlegend=False))
            fig2.update_layout(
                paper_bgcolor="rgba(255,255,255,0.80)",
                plot_bgcolor="rgba(247,248,252,0.90)",
                font_family="Outfit", font_color="#3d4f7a",
                xaxis=dict(showgrid=True, gridcolor="rgba(13,27,62,0.06)", range=[0, 110]),
                yaxis=dict(showgrid=False),
                height=380, margin=dict(l=0,r=40,t=10,b=10))
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="gs-label">Score Breakdown — All Dimensions</div>', unsafe_allow_html=True)
    melt = comp[["institution"] + rcols].melt(id_vars="institution",
                                               var_name="Dimension", value_name="Score")
    melt["Dimension"] = melt["Dimension"].map(SCORE_MAP)
    melt = melt.dropna(subset=["Score"])
    fig3 = px.bar(melt, x="Dimension", y="Score", color="institution",
                  barmode="group", color_discrete_map=cmap,
                  text=melt["Score"].round(1))
    fig3.update_traces(textposition="outside", textfont_size=10)
    fig3.update_layout(
        paper_bgcolor="rgba(255,255,255,0.80)",
        plot_bgcolor="rgba(247,248,252,0.90)",
        font_family="Outfit", font_color="#3d4f7a",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(13,27,62,0.06)"),
        legend=dict(orientation="h", y=-0.22, x=0.5,
                    xanchor="center", font_size=10),
        margin=dict(l=0,r=0,t=10,b=70), height=360,
        bargap=0.18, bargroupgap=0.06)
    st.plotly_chart(fig3, use_container_width=True)


st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="gs-label">Full Data</div>', unsafe_allow_html=True)
show_cols = {
    "institution": "University", "country": "Country",
    "world_rank": "World Rank", "overall_score": "Overall",
    "academic_score": "Academic", "employer_score": "Employer",
    "faculty_score": "Faculty", "citations_score": "Citations"
}
dcols = [c for c in show_cols if c in comp.columns]
st.dataframe(comp[dcols].rename(columns=show_cols),
             use_container_width=True, hide_index=True)

st.download_button("Download comparison as CSV",
                   data=comp.to_csv(index=False),
                   file_name="gradscope_comparison.csv", mime="text/csv")

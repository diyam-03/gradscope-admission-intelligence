import streamlit as st
from pathlib import Path


def load_css():
    css_path = Path(__file__).parent / "styles" / "style.css"
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def topnav(active: str = ""):
    pages = [
        ("Home",                    "app"),
        ("Profile Analyzer",        "pages/3_Profile_Analyzer"),
        ("Explore Universities",    "pages/2_University_Explorer"),
        ("Universities Recommended","pages/4_University_Recommendation"),
        ("Compare Universities",    "pages/6_University_Comparison"),
        ("Admission Assistant",     "pages/5_Admission_Assistant"),
        ("Admission Analytics",     "pages/1_Admission_Analytics"),
    ]

    # GradScope brand + nav in one row
    all_cols = st.columns([0.9, 1.5, 1.5, 1.85, 1.85, 1.65, 1.85])

    with all_cols[0]:
        st.page_link("app.py", label="🎓 GradScope", use_container_width=True)

    for col, (label, path) in zip(all_cols[1:], pages[1:]):
        with col:
            st.page_link(f"{path}.py", label=label, use_container_width=True)

    st.markdown('<div style="margin-bottom:1rem;"></div>', unsafe_allow_html=True)


def page_header(eyebrow: str, title: str, subtitle: str = "", active: str = ""):
    load_css()
    topnav(active)
    sub_html = f'<div class="gs-page-header-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="gs-page-header">
        <div class="gs-page-header-eyebrow">{eyebrow}</div>
        <div class="gs-page-header-title">{title}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def kpi_row(items: list, bars: list = None):
    default_bars = [
        "linear-gradient(90deg,#c8006e,#f5a623)",
        "linear-gradient(90deg,#0d1b3e,#4a90d9)",
        "linear-gradient(90deg,#4a90d9,#10b981)",
        "linear-gradient(90deg,#f5a623,#c8006e)",
        "linear-gradient(90deg,#10b981,#4a90d9)",
    ]
    if bars is None:
        bars = default_bars
    for col, (lbl, val, sub), bar in zip(st.columns(len(items)), items,
                                          bars * (len(items) // len(bars) + 1)):
        with col:
            st.markdown(f"""
            <div class="gs-metric">
              <div class="gs-metric-bar" style="background:{bar}"></div>
              <div class="gs-metric-label">{lbl}</div>
              <div class="gs-metric-value">{val}</div>
              <div class="gs-metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)
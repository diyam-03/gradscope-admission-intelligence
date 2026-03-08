# dashboard/helpers.py
import streamlit as st
from pathlib import Path


def load_css():
    css_path = Path(__file__).parent / "styles" / "style.css"
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def sidebar_nav():
    st.sidebar.markdown("""
<div style="padding:1.75rem 0.75rem 1.25rem;">
  <div style="font-family:'Fraunces',serif;font-size:1.5rem;font-weight:900;
              color:#ffffff;letter-spacing:-0.02em;">GradScope</div>
  <div style="font-family:'Outfit',sans-serif;font-size:0.7rem;font-weight:700;
              letter-spacing:0.12em;text-transform:uppercase;
              color:rgba(255,255,255,0.45);margin-top:0.25rem;">
    Admission Intelligence
  </div>
</div>
<div style="height:1px;background:rgba(255,255,255,0.10);margin:0 0 0.75rem;"></div>
""", unsafe_allow_html=True)

    pages = [
        ("Home",                      "/"),
        ("Admission Analytics",       "/Admission_Analytics"),
        ("University Explorer",       "/University_Explorer"),
        ("Profile Analyzer",          "/Profile_Analyzer"),
        ("University Recommendation", "/University_Recommendation"),
        ("Admission Assistant",       "/Admission_Assistant"),
        ("University Comparison",     "/University_Comparison"),
    ]
    for label, _ in pages:
        st.sidebar.markdown(f"""
<div style="padding:0.4rem 0.85rem;font-family:'Outfit',sans-serif;
            font-size:0.87rem;font-weight:500;color:rgba(255,255,255,0.75);
            border-radius:8px;">
  {label}
</div>""", unsafe_allow_html=True)


def page_header(eyebrow: str, title: str, subtitle: str = ""):
    load_css()
    sidebar_nav()
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
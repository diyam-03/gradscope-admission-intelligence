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

    # Build nav as pure HTML — st.page_link truncates regardless of column width
    base = ""  # relative paths work in Streamlit multipage
    nav_items = [
        ("🎓 GradScope",              "app",                          True),
        ("Profile Analyzer",          "pages/3_Profile_Analyzer",     False),
        ("Explore Universities",      "pages/2_University_Explorer",  False),
        ("Universities Recommended",  "pages/4_University_Recommendation", False),
        ("Compare Universities",      "pages/6_University_Comparison",False),
        ("Admission Assistant",       "pages/5_Admission_Assistant",  False),
        ("Admission Analytics",       "pages/1_Admission_Analytics",  False),
    ]

    nav_html = """
    <style>
    .gs-nav {
      display:flex;align-items:center;gap:0.15rem;
      background:#0d1b3e;border-radius:12px;
      padding:0.4rem 0.75rem;margin-bottom:1.25rem;
      box-shadow:0 6px 24px rgba(13,27,62,0.18);
      flex-wrap:nowrap;overflow-x:auto;
    }
    .gs-nav a {
      font-family:'Outfit',sans-serif;font-size:0.78rem;font-weight:600;
      color:rgba(255,255,255,0.65);
      padding:0.4rem 0.7rem;border-radius:8px;
      white-space:nowrap;text-decoration:none;
      transition:background 0.18s,color 0.18s;
      flex-shrink:0;
    }
    .gs-nav a:hover { background:rgba(255,255,255,0.10);color:#fff; }
    .gs-nav a.gs-nav-brand {
      font-family:'Fraunces',serif;font-weight:900;font-size:0.95rem;
      color:#fff;margin-right:0.5rem;padding:0.4rem 0.85rem;
      background:rgba(255,255,255,0.08);border-radius:8px;
    }
    .gs-nav a.gs-nav-brand:hover { background:rgba(255,255,255,0.15); }
    </style>
    <nav class="gs-nav">
    """
    for label, path, is_brand in nav_items:
        cls = "gs-nav-brand" if is_brand else ""
        nav_html += f'<a href="{path}" class="{cls}" target="_self">{label}</a>'
    nav_html += "</nav>"

    st.markdown(nav_html, unsafe_allow_html=True)


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
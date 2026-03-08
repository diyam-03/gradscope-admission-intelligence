import streamlit as st
from pathlib import Path


def load_css():
    css_path = Path(__file__).parent / "styles" / "style.css"
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def topnav(active: str = ""):
    nav_items = [
        ("GradScope",                "/",                          True),
        ("Profile Analyzer",         "/Profile_Analyzer",          False),
        ("Explore Universities",     "/University_Explorer",       False),
        ("Universities Recommended", "/University_Recommendation", False),
        ("Compare Universities",     "/University_Comparison",     False),
        ("Admission Assistant",      "/Admission_Assistant",       False),
        ("Admission Analytics",      "/Admission_Analytics",       False),
    ]
    links = ""
    for label, path, is_brand in nav_items:
        cls = "gs-nav-brand" if is_brand else ""
        links += f'<a href="{path}" class="{cls}" target="_self">{label}</a>'

    st.markdown(f"""
    <style>
    /* Hide Streamlit's own page-link nav buttons */
    [data-testid="stPageLink"] {{ display: none !important; }}
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    [data-testid="collapsedControl"] {{ display: none !important; }}

    .gs-nav {{
      display: flex;
      align-items: center;
      gap: 0.15rem;
      background: #0d1b3e;
      border-radius: 12px;
      padding: 0.5rem 1rem;
      margin-bottom: 1.25rem;
      box-shadow: 0 6px 24px rgba(13,27,62,0.18);
      overflow-x: auto;
      scrollbar-width: none;
    }}
    .gs-nav::-webkit-scrollbar {{ display: none; }}
    .gs-nav a {{
      font-family: 'Outfit', sans-serif;
      font-size: 0.82rem;
      font-weight: 600;
      color: rgba(255,255,255,0.60);
      padding: 0.42rem 0.85rem;
      border-radius: 8px;
      white-space: nowrap;
      text-decoration: none;
      display: inline-block;
      transition: background 0.18s ease, color 0.18s ease;
      flex-shrink: 0;
    }}
    .gs-nav a:hover {{
      background: rgba(200,0,110,0.28);
      color: #ffffff;
    }}
    .gs-nav a.gs-nav-brand {{
      font-family: 'Fraunces', serif;
      font-weight: 900;
      font-size: 1.05rem;
      color: #ffffff;
      padding: 0.42rem 1.1rem;
      background: rgba(255,255,255,0.09);
      border-radius: 9px;
      letter-spacing: -0.02em;
      margin-right: 0.75rem;
    }}
    .gs-nav a.gs-nav-brand:hover {{
      background: rgba(200,0,110,0.35);
      color: #fff;
    }}
    /* Divider between brand and links */
    .gs-nav-divider {{
      width: 1px;
      height: 18px;
      background: rgba(255,255,255,0.15);
      margin: 0 0.5rem;
      flex-shrink: 0;
    }}
    </style>
    <nav class="gs-nav">
      {links}
    </nav>
    """, unsafe_allow_html=True)


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
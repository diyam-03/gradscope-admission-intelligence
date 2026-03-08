import streamlit as st
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_session():
    return st.session_state.get("user", None)


def require_auth():
    """Call at top of every page. Redirects to login if not authenticated."""
    if not get_session():
        st.switch_page("app.py")
        st.stop()


def logout():
    try:
        supabase.auth.sign_out()
    except:
        pass
    st.session_state.pop("user", None)
    st.session_state.pop("user_email", None)
    st.rerun()


def show_auth_page():
    """Full login/signup page. Returns True if authenticated."""

    # If already logged in, skip
    if get_session():
        return True

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@700;900&family=Outfit:wght@300;400;500;600;700&display=swap');

    .stApp {
      background:
        radial-gradient(ellipse at 0% 0%,    rgba(200,0,110,0.12) 0%, transparent 45%),
        radial-gradient(ellipse at 100% 0%,  rgba(74,144,217,0.14) 0%, transparent 45%),
        radial-gradient(ellipse at 100% 100%,rgba(245,166,35,0.09) 0%, transparent 40%),
        linear-gradient(160deg, #f7f8fc 0%, #eef1f9 50%, #f0f3fb 100%) !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stSidebar"]       { display: none !important; }
    [data-testid="collapsedControl"]{ display: none !important; }
    .block-container {
      max-width: 480px !important;
      padding-top: 4rem !important;
    }
    .gs-auth-card {
      background: #fff;
      border-radius: 20px;
      padding: 2.5rem 2.25rem;
      box-shadow: 0 20px 60px rgba(13,27,62,0.14);
      border: 1.5px solid rgba(255,255,255,0.9);
    }
    .gs-auth-brand {
      text-align: center;
      margin-bottom: 1.75rem;
    }
    .gs-auth-brand-icon {
      font-size: 2.5rem;
      margin-bottom: 0.5rem;
    }
    .gs-auth-brand-name {
      font-family: 'Fraunces', serif;
      font-size: 2rem;
      font-weight: 900;
      color: #0d1b3e;
      letter-spacing: -0.03em;
    }
    .gs-auth-brand-tag {
      font-family: 'Outfit', sans-serif;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #7b8cb0;
      margin-top: 0.2rem;
    }
    .gs-auth-title {
      font-family: 'Fraunces', serif;
      font-size: 1.35rem;
      font-weight: 900;
      color: #0d1b3e;
      margin-bottom: 0.25rem;
    }
    .gs-auth-sub {
      font-family: 'Outfit', sans-serif;
      font-size: 0.85rem;
      color: #7b8cb0;
      margin-bottom: 1.5rem;
    }
    /* Style inputs */
    .stTextInput input {
      border-radius: 10px !important;
      border: 1.5px solid rgba(13,27,62,0.15) !important;
      font-family: 'Outfit', sans-serif !important;
      font-size: 0.9rem !important;
      padding: 0.65rem 0.9rem !important;
      transition: border-color 0.18s !important;
    }
    .stTextInput input:focus {
      border-color: #c8006e !important;
      box-shadow: 0 0 0 3px rgba(200,0,110,0.10) !important;
    }
    /* Primary button */
    .stButton > button[kind="primary"] {
      background: linear-gradient(90deg, #c8006e, #f5a623) !important;
      border: none !important;
      border-radius: 10px !important;
      font-family: 'Outfit', sans-serif !important;
      font-weight: 700 !important;
      font-size: 0.92rem !important;
      color: #fff !important;
      padding: 0.65rem 1.5rem !important;
      width: 100% !important;
      box-shadow: 0 4px 14px rgba(200,0,110,0.30) !important;
      transition: opacity 0.18s !important;
    }
    .stButton > button[kind="primary"]:hover { opacity: 0.88 !important; }
    .stButton > button[kind="secondary"] {
      background: transparent !important;
      border: 1.5px solid rgba(13,27,62,0.18) !important;
      border-radius: 10px !important;
      font-family: 'Outfit', sans-serif !important;
      font-weight: 600 !important;
      font-size: 0.88rem !important;
      color: #3d4f7a !important;
      width: 100% !important;
    }
    .stTabs [data-baseweb="tab-list"] {
      background: rgba(13,27,62,0.04) !important;
      border-radius: 10px !important;
      padding: 0.25rem !important;
      gap: 0.25rem !important;
    }
    .stTabs [data-baseweb="tab"] {
      border-radius: 8px !important;
      font-family: 'Outfit', sans-serif !important;
      font-weight: 600 !important;
      font-size: 0.88rem !important;
    }
    .stTabs [aria-selected="true"] {
      background: #fff !important;
      color: #0d1b3e !important;
      box-shadow: 0 2px 8px rgba(13,27,62,0.10) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Brand
    st.markdown("""
    <div class="gs-auth-brand">
      <div class="gs-auth-brand-icon">🎓</div>
      <div class="gs-auth-brand-name">GradScope</div>
      <div class="gs-auth-brand-tag">Admission Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

    # ── LOGIN ──────────────────────────────────────────────────────────────────
    with tab_login:
        st.markdown('<div class="gs-auth-title">Welcome back</div>', unsafe_allow_html=True)
        st.markdown('<div class="gs-auth-sub">Sign in to your GradScope account</div>', unsafe_allow_html=True)

        login_email    = st.text_input("Email", key="login_email", placeholder="you@example.com")
        login_password = st.text_input("Password", key="login_password",
                                       type="password", placeholder="Your password")

        st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

        if st.button("Sign In", type="primary", key="btn_login"):
            if not login_email or not login_password:
                st.error("Please enter your email and password.")
            else:
                try:
                    res = supabase.auth.sign_in_with_password({
                        "email": login_email,
                        "password": login_password
                    })
                    st.session_state["user"]       = res.user
                    st.session_state["user_email"] = res.user.email
                    st.rerun()
                except Exception as e:
                    err = str(e).lower()
                    if "invalid" in err or "credentials" in err:
                        st.error("Incorrect email or password.")
                    elif "confirm" in err or "verified" in err:
                        st.warning("Please verify your email before signing in.")
                    else:
                        st.error(f"Sign in failed: {e}")

    # ── SIGNUP ─────────────────────────────────────────────────────────────────
    with tab_signup:
        st.markdown('<div class="gs-auth-title">Create your account</div>', unsafe_allow_html=True)
        st.markdown('<div class="gs-auth-sub">Free forever. No credit card needed.</div>', unsafe_allow_html=True)

        signup_name     = st.text_input("Full Name", key="signup_name", placeholder="Your name")
        signup_email    = st.text_input("Email", key="signup_email", placeholder="you@example.com")
        signup_password = st.text_input("Password", key="signup_password",
                                        type="password", placeholder="Min 6 characters")
        signup_confirm  = st.text_input("Confirm Password", key="signup_confirm",
                                        type="password", placeholder="Repeat your password")

        st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

        if st.button("Create Account", type="primary", key="btn_signup"):
            if not all([signup_name, signup_email, signup_password, signup_confirm]):
                st.error("Please fill in all fields.")
            elif len(signup_password) < 6:
                st.error("Password must be at least 6 characters.")
            elif signup_password != signup_confirm:
                st.error("Passwords do not match.")
            else:
                try:
                    res = supabase.auth.sign_up({
                        "email": signup_email,
                        "password": signup_password,
                        "options": {"data": {"full_name": signup_name}}
                    })
                    if res.user:
                        st.success("Account created! Check your email to verify, then sign in.")
                    else:
                        st.error("Signup failed. Please try again.")
                except Exception as e:
                    err = str(e).lower()
                    if "already" in err or "exists" in err:
                        st.error("An account with this email already exists. Please sign in.")
                    else:
                        st.error(f"Signup failed: {e}")

    return False
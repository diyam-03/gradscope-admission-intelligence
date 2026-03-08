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
    if get_session():
        return True

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@700;900&family=Outfit:wght@300;400;500;600;700&display=swap');
    .stApp {
      background:
        radial-gradient(ellipse at 0% 0%, rgba(200,0,110,0.12) 0%, transparent 45%),
        radial-gradient(ellipse at 100% 0%, rgba(74,144,217,0.14) 0%, transparent 45%),
        radial-gradient(ellipse at 100% 100%, rgba(245,166,35,0.09) 0%, transparent 40%),
        linear-gradient(160deg, #f7f8fc 0%, #eef1f9 50%, #f0f3fb 100%) !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stSidebar"]        { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    .block-container { max-width: 460px !important; padding-top: 3rem !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
      background: rgba(13,27,62,0.06) !important;
      border-radius: 12px !important; padding: 0.3rem !important; gap: 0.2rem !important;
      border: none !important;
    }
    .stTabs [data-baseweb="tab"] {
      border-radius: 9px !important;
      font-family: 'Outfit', sans-serif !important;
      font-weight: 600 !important; font-size: 0.9rem !important;
      color: #7b8cb0 !important; border: none !important;
      padding: 0.5rem 1.5rem !important;
    }
    .stTabs [aria-selected="true"] {
      background: #ffffff !important; color: #0d1b3e !important;
      box-shadow: 0 2px 10px rgba(13,27,62,0.12) !important;
    }
    /* Inputs */
    .stTextInput > div > div > input {
      border-radius: 10px !important;
      border: 1.5px solid rgba(13,27,62,0.14) !important;
      font-family: 'Outfit', sans-serif !important;
      font-size: 0.9rem !important; padding: 0.6rem 0.9rem !important;
      background: #fff !important;
      transition: border-color 0.18s, box-shadow 0.18s !important;
    }
    .stTextInput > div > div > input:focus {
      border-color: #c8006e !important;
      box-shadow: 0 0 0 3px rgba(200,0,110,0.10) !important;
      outline: none !important;
    }
    /* Primary button */
    .stButton > button {
      width: 100% !important; border-radius: 10px !important;
      font-family: 'Outfit', sans-serif !important;
      font-weight: 700 !important; font-size: 0.92rem !important;
      padding: 0.65rem 1rem !important; border: none !important;
      background: linear-gradient(90deg, #c8006e, #f5a623) !important;
      color: #fff !important;
      box-shadow: 0 4px 16px rgba(200,0,110,0.28) !important;
      transition: opacity 0.18s, transform 0.18s !important;
    }
    .stButton > button:hover {
      opacity: 0.88 !important; transform: translateY(-1px) !important;
    }
    /* Hide label for inputs */
    .stTextInput label { 
      font-family: 'Outfit', sans-serif !important;
      font-size: 0.82rem !important; font-weight: 600 !important;
      color: #3d4f7a !important; margin-bottom: 0.2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Brand
    st.markdown("""
    <div style="text-align:center;margin-bottom:1.5rem;">
      <div style="font-size:2.8rem;margin-bottom:0.4rem;">🎓</div>
      <div style="font-family:'Fraunces',serif;font-size:2.2rem;font-weight:900;
                  color:#0d1b3e;letter-spacing:-0.03em;">GradScope</div>
      <div style="font-family:'Outfit',sans-serif;font-size:0.72rem;font-weight:700;
                  letter-spacing:0.14em;text-transform:uppercase;color:#7b8cb0;
                  margin-top:0.2rem;">Admission Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

    # ── SIGN IN ───────────────────────────────────────────────────────────────
    with tab_login:
        st.markdown("""
        <div style="font-family:'Fraunces',serif;font-size:1.3rem;font-weight:900;
                    color:#0d1b3e;margin:1rem 0 0.2rem;">Welcome back</div>
        <div style="font-family:'Outfit',sans-serif;font-size:0.85rem;
                    color:#7b8cb0;margin-bottom:1.25rem;">Sign in to your GradScope account</div>
        """, unsafe_allow_html=True)

        login_email    = st.text_input("Email address", key="login_email",
                                       placeholder="you@example.com")
        login_password = st.text_input("Password", key="login_password",
                                       type="password", placeholder="Your password")
        st.markdown('<div style="height:0.4rem"></div>', unsafe_allow_html=True)

        if st.button("Sign In", key="btn_login"):
            if not login_email.strip() or not login_password:
                st.error("Please enter your email and password.")
            else:
                try:
                    res = supabase.auth.sign_in_with_password({
                        "email": login_email.strip(),
                        "password": login_password,
                    })
                    st.session_state["user"]       = res.user
                    st.session_state["user_email"] = res.user.email
                    st.rerun()
                except Exception as e:
                    err = str(e).lower()
                    if "invalid" in err or "credentials" in err or "wrong" in err:
                        st.error("Incorrect email or password. Please try again.")
                    elif "email not confirmed" in err or "not confirmed" in err:
                        st.warning("Please verify your email first, then sign in.")
                    elif "too many" in err:
                        st.error("Too many attempts. Please wait a moment and try again.")
                    else:
                        st.error(f"Sign in failed: {e}")

    # ── CREATE ACCOUNT ────────────────────────────────────────────────────────
    with tab_signup:
        st.markdown("""
        <div style="font-family:'Fraunces',serif;font-size:1.3rem;font-weight:900;
                    color:#0d1b3e;margin:1rem 0 0.2rem;">Create your account</div>
        <div style="font-family:'Outfit',sans-serif;font-size:0.85rem;
                    color:#7b8cb0;margin-bottom:1.25rem;">Free forever. No credit card needed.</div>
        """, unsafe_allow_html=True)

        signup_name     = st.text_input("Full Name", key="signup_name",
                                        placeholder="Your full name")
        signup_email    = st.text_input("Email address", key="signup_email",
                                        placeholder="you@example.com")
        signup_password = st.text_input("Password", key="signup_password",
                                        type="password", placeholder="Min 6 characters")
        signup_confirm  = st.text_input("Confirm Password", key="signup_confirm",
                                        type="password", placeholder="Repeat your password")
        st.markdown('<div style="height:0.4rem"></div>', unsafe_allow_html=True)

        if st.button("Create Account", key="btn_signup"):
            if not all([signup_name.strip(), signup_email.strip(),
                        signup_password, signup_confirm]):
                st.error("Please fill in all fields.")
            elif len(signup_password) < 6:
                st.error("Password must be at least 6 characters.")
            elif signup_password != signup_confirm:
                st.error("Passwords do not match.")
            elif "@" not in signup_email or "." not in signup_email:
                st.error("Please enter a valid email address.")
            else:
                try:
                    res = supabase.auth.sign_up({
                        "email": signup_email.strip(),
                        "password": signup_password,
                        "options": {"data": {"full_name": signup_name.strip()}}
                    })
                    if res.user:
                        # Save user profile to Supabase DB
                        try:
                            supabase.table("users").upsert({
                                "id": res.user.id,
                                "email": signup_email.strip(),
                                "full_name": signup_name.strip(),
                                "created_at": res.user.created_at.isoformat() if res.user.created_at else None,
                            }).execute()
                        except Exception:
                            pass  # Non-fatal — auth still works

                        if res.session:
                            st.session_state["user"]       = res.user
                            st.session_state["user_email"] = res.user.email
                            st.success(f"Welcome to GradScope, {signup_name.split()[0]}!")
                            st.rerun()
                        else:
                            st.success("Account created! Check your email to verify, then sign in.")
                    else:
                        st.error("Something went wrong. Please try again.")
                except Exception as e:
                    err = str(e).lower()
                    if "already registered" in err or "already exists" in err or "duplicate" in err:
                        st.error("An account with this email already exists. Please sign in.")
                    elif "password" in err and ("weak" in err or "short" in err):
                        st.error("Password is too weak. Use at least 6 characters.")
                    elif "rate" in err or "too many" in err:
                        st.error("Too many attempts. Please wait a moment and try again.")
                    else:
                        st.error(f"Signup failed. Please try again. ({e})")

    return False
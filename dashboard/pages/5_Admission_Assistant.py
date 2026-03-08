import streamlit as st
from helpers import page_header

st.set_page_config(page_title="Admission Assistant · GradScope", page_icon="💬", layout="wide", initial_sidebar_state="expanded")
page_header("Guidance", "Admission Assistant",
            "Ask anything about graduate admissions — GRE, SoPs, deadlines, funding and more.", active="Admission_Assistant")

KB = [
    {"keywords":["gre","gre score"],"topic":"GRE Score","color":"#0d1b3e",
     "answer":"A GRE score above **320** is strong for top-50 universities. Scores above **325** are competitive for top-10 programs. Aim for **Quant 165+** for STEM.",
     "tips":["Use ETS official practice tests","Magoosh or Manhattan Prep","Aim for 3–6 months of preparation"]},
    {"keywords":["cgpa","gpa","grades"],"topic":"CGPA / GPA","color":"#c8006e",
     "answer":"A CGPA of **8.5+ out of 10** is competitive for top universities. A slightly lower GPA can be offset by strong GRE and research experience.",
     "tips":["Highlight upward GPA trends in your SoP","Strong research compensates for GPA below 8.0","Explain anomalies in an addendum"]},
    {"keywords":["research","publications"],"topic":"Research Experience","color":"#10b981",
     "answer":"Research experience is one of the **most differentiating factors**. Students with research have significantly higher admit rates, especially for PhD programs.",
     "tips":["Reach out to professors for opportunities","Look for summer research programs","Document contributions clearly in your CV"]},
    {"keywords":["sop","statement of purpose","essay"],"topic":"Statement of Purpose","color":"#f5a623",
     "answer":"A great SoP tells a clear story: why this field, why now, why this program. Reference **specific professors** and their recent papers. Keep it to **1–2 pages**, tailored per school.",
     "tips":["Name specific faculty you want to work with","Connect past experience to future goals","Get reviewed by at least 2 people"]},
    {"keywords":["lor","recommendation"],"topic":"Letters of Recommendation","color":"#4a90d9",
     "answer":"Most programs require **3 letters**. A detailed letter from an assistant professor who worked closely with you beats a generic letter from a famous dean. Give recommenders **4–6 weeks** notice.",
     "tips":["Ask recommenders who supervised you directly","Provide your CV and SoP draft","Follow up politely 2 weeks before deadline"]},
    {"keywords":["toefl","ielts","english"],"topic":"English Proficiency","color":"#0d1b3e",
     "answer":"Most US universities require **TOEFL 100+** (iBT). Top programs expect **105–110+**. For IELTS, **7.0+** is generally accepted.",
     "tips":["TOEFL 100+ is the safe threshold","Reading and Writing sections are weighted most","Most programs accept your best score"]},
    {"keywords":["deadline","timeline","when","apply"],"topic":"Application Timeline","color":"#c8006e",
     "answer":"For **Fall intake**, US deadlines: Early Decision Nov 1–15, Regular Decision Dec–Jan 15. Start **12–14 months** before your intended start date.",
     "tips":["Create a spreadsheet tracking all requirements","Submit 1 week before deadline","Request transcripts 6 weeks in advance"]},
    {"keywords":["funding","scholarship","fellowship"],"topic":"Funding & Scholarships","color":"#f5a623",
     "answer":"PhD programs in the US often include full funding: tuition waiver + stipend ($18k–$35k/year). Look into **Fulbright, Commonwealth, DAAD, Chevening** fellowships.",
     "tips":["External fellowships strengthen PhD applications too","Email professors directly about RA positions","Ask about departmental fellowships during admission"]},
    {"keywords":["university","choose","ranking","best"],"topic":"Choosing Universities","color":"#10b981",
     "answer":"Build a **balanced list**: 2–3 dream schools, 3–4 target, 2–3 safe. Consider research fit, faculty, location, funding, and placement outcomes — not just rankings.",
     "tips":["Use the University Recommendation page","Read recent PhD theses from target programs","Email 1–2 faculty before applying"]},
]

# ── Topic pills as HTML — no column wrapping, no text truncation ──────────────
st.markdown('<div class="gs-label">Browse by Topic</div>', unsafe_allow_html=True)

pills_html = '<div style="display:flex;flex-wrap:wrap;gap:0.5rem;margin-bottom:0.5rem;">'
for item in KB:
    pills_html += f"""
    <form action="" method="get" style="margin:0;padding:0;">
      <button type="submit" name="topic_btn" value="{item['topic']}"
        style="background:rgba(255,255,255,0.82);
               border:1.5px solid rgba(13,27,62,0.15);
               border-radius:100px;
               padding:0.45rem 1.1rem;
               font-family:'Outfit',sans-serif;
               font-size:0.82rem;font-weight:600;
               color:{item['color']};
               cursor:pointer;
               white-space:nowrap;
               box-shadow:0 2px 8px rgba(13,27,62,0.07);
               transition:all 0.18s ease;">
        {item['topic']}
      </button>
    </form>"""
pills_html += '</div>'
st.markdown(pills_html, unsafe_allow_html=True)

# Use actual Streamlit buttons in a 3-col layout so clicks register
st.markdown('<div style="height:0.25rem"></div>', unsafe_allow_html=True)
btn_rows = [KB[:3], KB[3:6], KB[6:]]
for row in btn_rows:
    cols = st.columns(len(row))
    for col, item in zip(cols, row):
        with col:
            if st.button(item["topic"], key=f"btn_{item['topic']}", use_container_width=True):
                st.session_state["topic"] = item["topic"]
                st.session_state["q"] = ""
                st.rerun()

st.markdown('<div class="gs-divider"></div>', unsafe_allow_html=True)

# ── Search ─────────────────────────────────────────────────────────────────────
sc1, sc2 = st.columns([4, 1])
with sc1:
    q = st.text_input("Ask your question",
                      value=st.session_state.get("q", ""),
                      placeholder="e.g. What GRE score do I need? How important is research?",
                      label_visibility="collapsed")
with sc2:
    if st.button("Search", type="primary", use_container_width=True):
        pass

# ── Resolve topic ──────────────────────────────────────────────────────────────
matched = None
if q.strip():
    st.session_state["topic"] = None
    for item in KB:
        if any(kw in q.strip().lower() for kw in item["keywords"]):
            matched = item
            break
    if not matched:
        matched = "fallback"
elif st.session_state.get("topic"):
    for item in KB:
        if item["topic"] == st.session_state["topic"]:
            matched = item
            break

# ── Answer ─────────────────────────────────────────────────────────────────────
def bold(text):
    import re
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

if matched and matched != "fallback":
    c = matched["color"]
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.82);
                border:1px solid rgba(255,255,255,0.92);
                border-left:5px solid {c};
                border-radius:14px;
                padding:1.5rem 1.75rem;
                margin:1rem 0;
                box-shadow:0 4px 16px rgba(13,27,62,0.09);">
      <div style="font-family:'Fraunces',serif;font-size:1.2rem;font-weight:900;
                  color:#0d1b3e;margin-bottom:0.75rem;">{matched['topic']}</div>
      <div style="font-family:'Outfit',sans-serif;font-size:0.92rem;
                  color:#3d4f7a;line-height:1.72;">
        {bold(matched['answer'])}
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="gs-label" style="margin-top:1.25rem;">Quick Tips</div>',
                unsafe_allow_html=True)
    tip_cols = st.columns(len(matched["tips"]))
    for col, tip in zip(tip_cols, matched["tips"]):
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.80);
                        border:1px solid rgba(255,255,255,0.90);
                        border-top:3px solid {c};
                        border-radius:10px;padding:0.9rem 1rem;
                        box-shadow:0 2px 8px rgba(13,27,62,0.06);">
              <div style="font-size:0.84rem;color:#3d4f7a;line-height:1.6;">{tip}</div>
            </div>""", unsafe_allow_html=True)

elif matched == "fallback":
    st.markdown("""
    <div style="background:rgba(255,255,255,0.82);
                border:1px solid rgba(255,255,255,0.92);
                border-left:5px solid #f5a623;
                border-radius:14px;padding:1.5rem 1.75rem;margin:1rem 0;">
      <div style="font-family:'Fraunces',serif;font-size:1.1rem;font-weight:900;
                  color:#0d1b3e;margin-bottom:0.4rem;">No match found</div>
      <div style="font-size:0.9rem;color:#3d4f7a;line-height:1.65;">
        Try: <b>GRE scores</b>, <b>CGPA</b>, <b>research</b>, <b>SoP</b>,
        <b>LoR</b>, <b>TOEFL</b>, <b>deadlines</b>, <b>funding</b>, or
        <b>choosing universities</b>.
      </div>
    </div>""", unsafe_allow_html=True)

else:
    st.markdown('<div class="gs-label" style="margin-top:0.5rem;">All Topics</div>',
                unsafe_allow_html=True)
    for row_items in [KB[:3], KB[3:6], KB[6:]]:
        for col, item in zip(st.columns(3), row_items):
            with col:
                st.markdown(f"""
                <div class="gs-card" style="margin-bottom:0.75rem;">
                  <div class="gs-card-title" style="color:{item['color']} !important;
                       -webkit-text-fill-color:{item['color']} !important;">
                    {item['topic']}
                  </div>
                  <p>{item['answer'][:95].rstrip()}...</p>
                </div>""", unsafe_allow_html=True)
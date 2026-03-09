import streamlit as st
import re
from helpers import page_header

st.set_page_config(page_title="Admission Assistant · GradScope", page_icon="💬", layout="wide", initial_sidebar_state="expanded")
page_header("Guidance", "Admission Assistant",
            "Your personal grad school advisor. Ask anything about applications, GRE, SoP, funding and more.",
            active="Admission_Assistant")

KB = [
    {"keywords": ["gre", "gre score", "quant", "verbal"],
     "topic": "GRE Score",
     "answer": "A GRE score above **320** is strong for top-50 universities. Scores above **325** are competitive for top-10 programs. Aim for **Quant 165+** for STEM programs. For most programs, GRE is a threshold — once you clear it, extra points matter less than research and CGPA.",
     "tips": ["Use ETS official practice tests", "Magoosh or Manhattan Prep are popular resources", "Aim for 3–6 months of preparation", "Quant score matters more than verbal for STEM"]},

    {"keywords": ["cgpa", "gpa", "grades", "marks", "percentage"],
     "topic": "CGPA / GPA",
     "answer": "A CGPA of **8.5+ out of 10** is competitive for top universities. A slightly lower GPA can be offset by strong GRE and research experience. Admissions committees look at trends — a rising GPA in final years is viewed positively.",
     "tips": ["Highlight upward GPA trends in your SoP", "Strong research can compensate for a GPA below 8.0", "Explain any anomalies in your SoP or an addendum", "Convert to 4.0 scale: 8.5/10 ≈ 3.5/4.0"]},

    {"keywords": ["research", "publication", "paper", "lab", "intern"],
     "topic": "Research Experience",
     "answer": "Research experience is one of the **most differentiating factors** in graduate admissions. Students with research have significantly higher admit rates, especially for PhD programs. Even one strong research project with a professor at your undergrad institution makes a real difference.",
     "tips": ["Email professors at your own university asking to join their lab", "Look for summer research programs like DAAD WISE or Mitacs", "Document all contributions clearly in your CV", "Aim for at least one recommendation from a research supervisor"]},

    {"keywords": ["sop", "statement of purpose", "essay", "personal statement", "motivation letter"],
     "topic": "Statement of Purpose",
     "answer": "A great SoP tells a clear story: why this field, why now, why this program. Reference **specific professors** and their recent papers. Keep it to **1–2 pages**, tailored per school. Avoid generic statements — admissions readers can tell immediately when an SoP is copy-pasted.",
     "tips": ["Name 1–2 specific faculty you want to work with", "Connect your past experience directly to future goals", "Get reviewed by at least 2 people before submitting", "Start writing 3 months before deadlines"]},

    {"keywords": ["lor", "recommendation", "letter", "referee"],
     "topic": "Letters of Recommendation",
     "answer": "Most programs require **3 letters**. A detailed letter from an assistant professor who worked closely with you beats a generic letter from a famous dean who barely knows you. Give recommenders **4–6 weeks** notice and always provide your CV and SoP draft.",
     "tips": ["Choose recommenders who supervised you directly", "Provide your CV, SoP draft and deadline clearly", "Follow up politely 2 weeks before deadline", "At least one letter should be from a research supervisor"]},

    {"keywords": ["toefl", "ielts", "english", "language", "duolingo"],
     "topic": "English Proficiency",
     "answer": "Most US universities require **TOEFL 100+** (iBT). Top programs expect **105–110+**. For IELTS, **7.0+** is generally accepted. Some universities now accept Duolingo English Test (DET) with a score of 120+.",
     "tips": ["TOEFL 100+ is the safe threshold for most programs", "Reading and Writing sections are weighted most", "Most programs accept your best score across attempts", "Check each university's specific requirement — they vary"]},

    {"keywords": ["deadline", "timeline", "when", "apply", "schedule", "fall", "spring"],
     "topic": "Application Timeline",
     "answer": "For **Fall intake**, US deadlines run from November 1 (Early Decision) to January 15 (Regular Decision). Start **12–14 months** before your intended start date. Request transcripts 6 weeks in advance — institutions are often slow.",
     "tips": ["Create a spreadsheet tracking all requirements per school", "Submit 1 week before the deadline, not on the day", "Request official transcripts 6–8 weeks in advance", "GRE scores take 10–15 days to reach universities after the test"]},

    {"keywords": ["funding", "scholarship", "fellowship", "stipend", "financial", "money", "phd funding"],
     "topic": "Funding & Scholarships",
     "answer": "PhD programs in the US often include full funding: tuition waiver + stipend ($18k–$35k/year). Look into **Fulbright, Commonwealth, DAAD, Chevening** fellowships for masters. External fellowships also strengthen PhD applications.",
     "tips": ["Email professors directly about RA/TA positions", "Ask about departmental fellowships during admission", "External fellowships make you more attractive to programs", "Fulbright deadlines are typically in October, a year before enrollment"]},

    {"keywords": ["university", "choose", "ranking", "best", "list", "school", "shortlist"],
     "topic": "Choosing Universities",
     "answer": "Build a **balanced list**: 2–3 dream schools (reach), 3–4 target schools, 2–3 safe schools. Consider research fit with specific faculty, funding packages, placement outcomes and location — not just rankings. A Rank 30 program with the right advisor beats a Rank 5 program in the wrong lab.",
     "tips": ["Use the University Recommendation page on GradScope", "Read recent PhD theses from your target programs", "Email 1–2 faculty before applying to gauge interest", "Check placement data: where do graduates go after finishing?"]},

    {"keywords": ["visa", "f1", "student visa", "i20", "immigration"],
     "topic": "Student Visa (F-1)",
     "answer": "After receiving your I-20, apply for an **F-1 student visa** at the US Embassy. Apply at least 3 months before your program start date. Visa interview preparation is important — be clear about your study plans and ties to your home country.",
     "tips": ["Apply for your visa as soon as you get your I-20", "Have your financial documents ready for the interview", "Research common F-1 visa interview questions", "SEVIS fee must be paid before your visa interview"]},

    {"keywords": ["ms", "phd", "masters", "doctorate", "which degree", "ms vs phd"],
     "topic": "MS vs PhD",
     "answer": "**MS** is 1.5–2 years, usually self-funded or partially funded, focused on coursework with some research. **PhD** is 4–6 years, usually fully funded, research-intensive. If you are passionate about a specific research area and want an academic or research career, apply directly to PhD. If you are still exploring, MS first is a safer path.",
     "tips": ["PhDs are almost always fully funded in the US", "You can often transfer from MS to PhD within the same program", "Industry jobs often prefer MS; academia and research labs prefer PhD", "PhD applications require a much stronger research background"]},
]

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "Hi! I am your GradScope admission advisor. Ask me anything about GRE scores, SoPs, research experience, funding, visas, or choosing universities. You can also click a topic below to get started."}
    ]

st.markdown('<div class="gs-label">Quick Topics</div>', unsafe_allow_html=True)

topic_cols = st.columns(6)
topics_short = ["GRE Score", "CGPA / GPA", "Research", "SoP", "Funding", "MS vs PhD"]
topic_keys   = ["GRE Score", "CGPA / GPA", "Research Experience", "Statement of Purpose", "Funding & Scholarships", "MS vs PhD"]

for col, label, key in zip(topic_cols, topics_short, topic_keys):
    with col:
        if st.button(label, key=f"quick_{key}", use_container_width=True):
            st.session_state["chat_history"].append({"role": "user", "content": f"Tell me about {label}"})
            for item in KB:
                if item["topic"] == key:
                    tips_text = "\n\n**Quick tips:**\n" + "\n".join(f"- {t}" for t in item["tips"])
                    reply = re.sub(r'\*\*(.+?)\*\*', r'**\1**', item["answer"]) + tips_text
                    st.session_state["chat_history"].append({"role": "assistant", "content": reply})
                    break
            st.rerun()

st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "🧑‍💻"):
        st.markdown(msg["content"])


user_input = st.chat_input("Ask me anything about grad school applications...")

if user_input:
    st.session_state["chat_history"].append({"role": "user", "content": user_input})

    
    q_lower = user_input.lower()
    matched = None
    for item in KB:
        if any(kw in q_lower for kw in item["keywords"]):
            matched = item
            break

    if matched:
        tips_text = "\n\n**Quick tips:**\n" + "\n".join(f"- {t}" for t in matched["tips"])
        reply = matched["answer"] + tips_text
    else:
        reply = (
            "I am not sure I have a specific answer for that, but here are the topics I can help with:\n\n"
            + "\n".join(f"- **{item['topic']}**" for item in KB)
            + "\n\nTry rephrasing your question or click one of the quick topic buttons above."
        )

    st.session_state["chat_history"].append({"role": "assistant", "content": reply})
    st.rerun()


if len(st.session_state["chat_history"]) > 1:
    if st.button("Clear conversation", key="clear_chat"):
        st.session_state["chat_history"] = [
            {"role": "assistant", "content": "Hi! I am your GradScope admission advisor. Ask me anything about GRE scores, SoPs, research experience, funding, visas, or choosing universities."}
        ]
        st.rerun()

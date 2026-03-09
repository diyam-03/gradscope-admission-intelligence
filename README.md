# 🎓 GradScope - Admission Intelligence

A graduate admissions intelligence platform that helps students make smarter decisions about where to apply — powered by real QS 2025 data, machine learning, and a clean modern interface.

🔗 **Live:** https://gradscope-admission-intelligence-ttg37gftdrlyvapp27pudhs.streamlit.app

---

## Features

**Profile Analyzer**
Enter your GRE, CGPA, TOEFL and research experience to get an ML-powered admission chance prediction, a radar chart of your profile, and a personalised action plan.

**Universities Recommended**
Pick your field of study from 55 real QS 2025 subject rankings and get a personalised Dream, Target and Safe university list calibrated to your scores.

**Explore Universities**
Browse and filter 1,422 universities from QS 2025 by country, rank and score.

**Compare Universities**
Compare up to 5 universities side by side across every QS dimension — academic reputation, employer reputation, faculty ratio, citations and more.

**Admission Assistant**
A real chatbot advisor covering GRE prep, SoP writing, LoRs, funding, visa, MS vs PhD and more.

**Admission Analytics**
Insight cards and a factor importance chart showing what actually drives admission decisions — based on 400+ real applicant records.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Database | Supabase (PostgreSQL) |
| ML Model | Scikit-learn (Gradient Boosting) |
| Charts | Plotly |
| Auth | Supabase Auth |
| Deployment | Streamlit Cloud |
| Data | QS World University Rankings 2025, QS Rankings by Subject 2025, Graduate Admissions Dataset |

---

## ML Model

Trained on 400+ real graduate admissions records. Three models were evaluated:

| Model | R² | MAE |
|---|---|---|
| Gradient Boosting | 0.77 | 4.65 |
| Random Forest | 0.74 | 4.91 |
| Linear Regression | 0.68 | 5.43 |

Gradient Boosting was selected as the final model. Feature importances: CGPA (75%), GRE (15%), TOEFL (3%), SOP (3%), LOR (2%), Research (1%), University Rating (1%).

---

## Project Structure
```
gradscope-admission-intelligence/
├── dashboard/
│   ├── app.py
│   ├── auth.py
│   ├── helpers.py
│   ├── pages/
│   │   ├── 1_Admission_Analytics.py
│   │   ├── 2_University_Explorer.py
│   │   ├── 3_Profile_Analyzer.py
│   │   ├── 4_University_Recommendation.py
│   │   ├── 5_Admission_Assistant.py
│   │   └── 6_University_Comparison.py
│   └── styles/
│       └── style.css
├── data/
│   ├── admissions.csv
│   ├── universities.csv
│   └── subject_rankings.csv
├── pipeline/
│   ├── seed.py
│   ├── train.py
│   ├── predictor.py
│   └── model/
│       ├── model.joblib
│       └── scaler.joblib
└── requirements.txt
```

---

## Run Locally
```bash
git clone https://github.com/diyam-03/gradscope-admission-intelligence
cd gradscope-admission-intelligence
pip install -r requirements.txt
```

Create a `.env` file in the root:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

Run the app:
```bash
streamlit run dashboard/app.py
```

---

## Data Sources

- QS World University Rankings 2025
- QS Rankings by Subject 2025 (55 subjects)
- Graduate Admissions Dataset (Kaggle)

---

Built by [Diyam Mehta](https://github.com/diyam-03)

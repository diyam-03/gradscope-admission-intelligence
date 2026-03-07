import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dashboard.db import supabase

# Seed universities
print("Seeding universities...")
df_uni = pd.read_csv("data/universities.csv")
df_uni.columns = df_uni.columns.str.strip()

uni_rows = []
for _, row in df_uni.iterrows():
    uni_rows.append({
        "institution":        str(row.get("institution", "")),
        "world_rank":         int(row.get("world_rank", 0)),
        "country":            str(row.get("country", "")),
        "score":              float(row.get("score", 0)),
        "research_score":     float(row.get("research_score", 0)),
        "teaching_score":     float(row.get("teaching_score", 0)),
        "international_score":float(row.get("international_score", 0)),
        "citations_score":    float(row.get("citations_score", 0)),
        "industry_score":     float(row.get("industry_score", 0)),
    })

# Insert in batches of 100
for i in range(0, len(uni_rows), 100):
    supabase.table("universities").insert(uni_rows[i:i+100]).execute()
    print(f"  inserted universities {i} to {i+100}")

# Seed admissions
print("Seeding admissions...")
df_adm = pd.read_csv("data/admissions.csv")
df_adm.columns = df_adm.columns.str.strip()

adm_rows = []
for _, row in df_adm.iterrows():
    adm_rows.append({
        "gre":          int(row.get("GRE Score", row.get("gre", 0))),
        "toefl":        int(row.get("TOEFL Score", row.get("toefl", 0))),
        "uni_rating":   int(row.get("University Rating", row.get("uni_rating", 0))),
        "sop":          float(row.get("SOP", row.get("sop", 0))),
        "lor":          float(row.get("LOR", row.get("lor", 0))),
        "cgpa":         float(row.get("CGPA", row.get("cgpa", 0))),
        "research":     int(row.get("Research", row.get("research", 0))),
        "admit_chance": float(row.get("Chance of Admit", row.get("admit_chance", 0))),
    })

for i in range(0, len(adm_rows), 100):
    supabase.table("admissions").insert(adm_rows[i:i+100]).execute()
    print(f"  inserted admissions {i} to {i+100}")

print("Done. Database seeded successfully.")

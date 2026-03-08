import pandas as pd
import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dashboard.db import supabase

def clean_float(val, default=0.0):
    """Convert NaN/inf to safe JSON-serialisable float."""
    try:
        if val is None:
            return default
        f = float(val)
        if math.isnan(f) or math.isinf(f):
            return default
        return round(f, 4)
    except:
        return default

def clean_int(val, default=0):
    try:
        f = float(val)
        if math.isnan(f) or math.isinf(f):
            return default
        return int(f)
    except:
        return default

# ── Clear existing data ────────────────────────────────────────────────────────
print("Clearing existing universities...")
supabase.table("universities").delete().neq("id", 0).execute()

# ── Seed universities ──────────────────────────────────────────────────────────
print("Seeding universities...")
df_uni = pd.read_csv("data/universities.csv")
df_uni.columns = df_uni.columns.str.strip()
print("Columns:", df_uni.columns.tolist())
print(f"Total universities: {len(df_uni)}")

uni_rows = []
for _, row in df_uni.iterrows():
    uni_rows.append({
        "institution":         str(row.get("institution", "")),
        "world_rank":          clean_int(row.get("world_rank", 0)),
        "country":             str(row.get("country", "")),
        "score":               clean_float(row.get("overall_score", row.get("score", 0))),
        "research_score":      clean_float(row.get("academic_score", row.get("research_score", 0))),
        "teaching_score":      clean_float(row.get("faculty_score", row.get("teaching_score", 0))),
        "citations_score":     clean_float(row.get("citations_score", 0)),
        "industry_score":      clean_float(row.get("employer_score", row.get("industry_score", 0))),
        "international_score": clean_float(row.get("isr score", row.get("international_score", 0))),
    })

for i in range(0, len(uni_rows), 100):
    supabase.table("universities").insert(uni_rows[i:i+100]).execute()
    print(f"  inserted universities {i} to {min(i+100, len(uni_rows))}")

print(f"Universities done: {len(uni_rows)} rows")

# ── Seed admissions ────────────────────────────────────────────────────────────
print("\nClearing existing admissions...")
supabase.table("admissions").delete().neq("id", 0).execute()

print("Seeding admissions...")
df_adm = pd.read_csv("data/admissions.csv")
df_adm.columns = df_adm.columns.str.strip()
print(f"Total admissions: {len(df_adm)}")

adm_rows = []
for _, row in df_adm.iterrows():
    adm_rows.append({
        "gre":          clean_int(row.get("GRE Score",          row.get("gre",          0))),
        "toefl":        clean_int(row.get("TOEFL Score",        row.get("toefl",        0))),
        "uni_rating":   clean_int(row.get("University Rating",  row.get("uni_rating",   0))),
        "sop":          clean_float(row.get("SOP",              row.get("sop",          0))),
        "lor":          clean_float(row.get("LOR",              row.get("lor",          0))),
        "cgpa":         clean_float(row.get("CGPA",             row.get("cgpa",         0))),
        "research":     clean_int(row.get("Research",           row.get("research",     0))),
        "admit_chance": clean_float(row.get("Chance of Admit",  row.get("admit_chance", 0))),
    })

for i in range(0, len(adm_rows), 100):
    supabase.table("admissions").insert(adm_rows[i:i+100]).execute()
    print(f"  inserted admissions {i} to {min(i+100, len(adm_rows))}")

print(f"Admissions done: {len(adm_rows)} rows")
print("\nDatabase seeded successfully.")
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Load data
print("Loading data...")
df = pd.read_csv("data/admissions.csv")
df.columns = df.columns.str.strip()

# Rename columns
rename = {}
for c in df.columns:
    l = c.lower()
    if "gre" in l:        rename[c] = "GRE"
    elif "toefl" in l:    rename[c] = "TOEFL"
    elif "cgpa" in l:     rename[c] = "CGPA"
    elif "chance" in l:   rename[c] = "Admit"
    elif "research" in l: rename[c] = "Research"
    elif "rating" in l:   rename[c] = "UniRating"
    elif "sop" in l:      rename[c] = "SOP"
    elif "lor" in l:      rename[c] = "LOR"
df = df.rename(columns=rename)

# Features and target
features = ["GRE", "TOEFL", "CGPA", "SOP", "LOR", "UniRating", "Research"]
target = "Admit"

X = df[features]
y = df[target]

# If admit chance is 0-1 scale it to 0-100
if y.max() <= 1:
    y = y * 100

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# Train model
print("Training model...")
model = GradientBoostingRegressor(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    random_state=42
)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
y_pred = np.clip(y_pred, 0, 100)
r2  = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print(f"R2 Score : {r2:.4f}")
print(f"MAE      : {mae:.4f}")

# Feature importance
print("\nFeature Importances:")
for feat, imp in sorted(zip(features, model.feature_importances_), key=lambda x: -x[1]):
    print(f"  {feat:12s} {imp:.4f}")

# Save model and scaler
os.makedirs("pipeline/model", exist_ok=True)
joblib.dump(model,  "pipeline/model/model.joblib")
joblib.dump(scaler, "pipeline/model/scaler.joblib")
print("\nModel saved to pipeline/model/")

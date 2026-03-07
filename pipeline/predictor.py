import joblib
import numpy as np
import os

BASE = os.path.dirname(os.path.abspath(__file__))

model  = joblib.load(os.path.join(BASE, "model/model.joblib"))
scaler = joblib.load(os.path.join(BASE, "model/scaler.joblib"))

def predict_chance(gre, toefl, cgpa, sop, lor, uni_rating, research):
    features = np.array([[gre, toefl, cgpa, sop, lor, uni_rating, research]])
    scaled   = scaler.transform(features)
    chance   = model.predict(scaled)[0]
    return round(float(np.clip(chance, 0, 100)), 1)

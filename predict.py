import joblib
import os
import sys
from datetime import datetime
import pandas as pd

# Load AI Assets
MODEL_DIR = os.path.join(os.path.dirname(__file__), "model_files")
model = joblib.load(os.path.join(MODEL_DIR, "food_model.pkl"))
le_type = joblib.load(os.path.join(MODEL_DIR, "type_encoder.pkl"))
le_target = joblib.load(os.path.join(MODEL_DIR, "target_encoder.pkl"))

def match_ngo(category, city):
    csv_path = os.path.join(os.path.dirname(__file__), "../data/ngo_data.csv")
    if not os.path.exists(csv_path): return []
    df = pd.read_csv(csv_path)
    matches = df[(df['type'] == category) & (df['city'].str.lower() == city.lower())]
    return matches.to_dict(orient='records')

def process_donation(food_list):
    results = []
    dashboard = {"total": 0, "accepted": 0, "rejected": 0, "co2_saved": 0}

    for food in food_list:
        dashboard["total"] += 1
        
        # 1. Real-time Age Calculation
        prep_dt = datetime.strptime(food["prepared_date"], "%Y-%m-%d")
        hours_old = (datetime.now() - prep_dt).total_seconds() / 3600

        # 2. AI Decision
        try:
            type_enc = le_type.transform([food["food_type"]])[0]
            pred = model.predict([[type_enc, hours_old]])
            decision = le_target.inverse_transform(pred)[0]
        except:
            decision = "People"

        if decision == "Rejected":
            dashboard["rejected"] += 1
            results.append({
                "food_name": food["food_name"],
                "status": "Rejected",
                "reason": f"AI Spoilage Alert: {food['food_type']} is unsafe at {round(hours_old)} hrs."
            })
        else:
            dashboard["accepted"] += 1
            dashboard["co2_saved"] += (int(food["quantity"]) * 2.5)
            
            matches = match_ngo(decision, food["city"])
            results.append({
                "food_name": food["food_name"],
                "category": decision,
                "status": "Accepted",
                "hours_old": round(hours_old, 1),
                "city": food["city"],
                "matches": matches
            })

    return {"donations": results, "dashboard": dashboard}
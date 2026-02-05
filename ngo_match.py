import pandas as pd
import os

def match_ngo(category, city):
    # Path to your CSV
    csv_path = os.path.join(os.path.dirname(__file__), "../data/ngo_data.csv")
    
    if not os.path.exists(csv_path):
        return []

    df = pd.read_csv(csv_path)
    
    # 1. Filter by Category (People, Dog, Cow)
    # 2. Filter by City (Case-insensitive)
    matches = df[(df['type'] == category) & (df['city'].str.lower() == city.lower())]
    
    # Return as a list of dictionaries for the UI to read
    return matches.to_dict(orient='records')
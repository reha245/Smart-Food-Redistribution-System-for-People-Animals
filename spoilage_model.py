from datetime import datetime

def spoilage_probability(expiry_date):
    today = datetime.today().date()
    days_left = (expiry_date - today).days

    if days_left < 0:
        return 1.0  # Already Expired
    elif days_left == 0:
        return 0.8  # High Risk (Same day)
    elif days_left <= 2:
        return 0.5  # Moderate Risk
    else:
        return 0.2  # Safe
import pandas as pd
from datetime import datetime, timedelta

def get_streak():
    try:
        meal_log = pd.read_csv("meal_log.csv")
    except FileNotFoundError:
        return 0

    meal_log['timestamp'] = pd.to_datetime(meal_log['timestamp'])
    meal_log['date'] = meal_log['timestamp'].dt.date
    unique_dates = meal_log['date'].drop_duplicates().sort_values(ascending=False)

    streak = 0
    today = datetime.now().date()

    for date in unique_dates:
        if date == today - timedelta(days=streak):
            streak += 1
        else:
            break

    return streak
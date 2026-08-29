import pandas as pd
from datetime import datetime

meal_log = pd.read_csv("meal_log.csv") if pd.io.common.file_exists("meal_log.csv") else pd.DataFrame(columns=["timestamp", "dish", "user_portion", "calories", "protein", "carbs", "fat"])

def get_today_summary():
    today = datetime.now().strftime("%Y-%m-%d")
    today_log = meal_log[meal_log["timestamp"].str.startswith(today)]
    
    total_calories = today_log["calories"].sum()
    total_protein = today_log["protein"].sum()
    total_carbs = today_log["carbs"].sum()
    total_fat = today_log["fat"].sum()

    return {
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_fat": total_fat,
        "today_log": today_log
    }
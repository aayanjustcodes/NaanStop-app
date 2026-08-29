import pandas as pd
from datetime import datetime

def log_meal(dish, user_portion):
    food_data = pd.read_csv("food_data.csv")
    result = food_data[food_data["dish"] == dish]

    if len(result) == 0:
        return None
    else:
        serving_size = result['serving_size'].values[0]
        calories = (user_portion / serving_size) * result['calories'].values[0]
        protein = (user_portion / serving_size) * result['protein'].values[0]
        carbs = (user_portion / serving_size) * result['carbs'].values[0]
        fat = (user_portion / serving_size) * result['fat'].values[0]

        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dish": dish,
            "user_portion": user_portion,
            "calories": round(calories),
            "protein": round(protein),
            "carbs": round(carbs),
            "fat": round(fat)
        }

        try:
            meal_log = pd.read_csv("meal_log.csv")
            meal_log = pd.concat([meal_log, pd.DataFrame([log_entry])], ignore_index=True)
        except FileNotFoundError:
            meal_log = pd.DataFrame([log_entry])

        meal_log.to_csv("meal_log.csv", index=False)
        return log_entry
    
if __name__ == "__main__":
    dish = input("Enter the dish name: ").lower().replace(" ", "_")
    user_portion = float(input("Enter the portion size in grams: "))
    log_entry = log_meal(dish, user_portion)
    if log_entry is None:
        print("Sorry! We do not have nutrition information for that dish at this time.")
    else:
        print(f"Meal logged: {log_entry}")
import pandas as pd

food_data = pd.read_csv("food_data.csv")

def calculate_nutrients(nutrient, user_portion, serving_size):
    nutrition_value = (user_portion / serving_size) * nutrient
    return nutrition_value

def nutrition(dish, user_portion):
    result = food_data[food_data["dish"] == dish]

    if len(result) == 0:
        return None
    else: 
        if result["is_halal"].values[0] == 1:
            halal = "Yes"
        else:
            halal = "No"

        if result["is_vegan"].values[0] == 1:
            vegan = "Yes"
        else:
            vegan = "No"

        if result["is_vegetarian"].values[0] == 1:
            vegetarian = "Yes"
        else:
            vegetarian = "No"
        
        if result["is_sikh_friendly"].values[0] == 1:
            sikh_friendly = "Yes"
        else:
            sikh_friendly = "No"
        
        if result["is_fasting_friendly"].values[0] == 1:
            fasting_friendly = "Yes"
        else:
            fasting_friendly = "No"

        serving_size = result['serving_size'].values[0]

        calories = calculate_nutrients(result['calories'].values[0], user_portion, serving_size)
        protein = calculate_nutrients(result['protein'].values[0], user_portion, serving_size)
        carbs = calculate_nutrients(result['carbs'].values[0], user_portion, serving_size)
        fat = calculate_nutrients(result['fat'].values[0], user_portion, serving_size)

        return {
            "dish": dish,
            "user_portion": user_portion,
            "calories": round(calories),
            "protein": round(protein),
            "carbs": round(carbs),
            "fat": round(fat),
            "halal": halal,
            "vegan": vegan,
            "vegetarian": vegetarian,
            "sikh_friendly": sikh_friendly,
            "fasting_friendly": fasting_friendly
        }

if __name__ == "__main__":
    query = input("Enter a dish name: ").lower()
    portion = float(input(f"How many grams did you eat? "))
    result = nutrition(query, portion)
    if result is None:
        print("Sorry! We do not have nutrition information for that dish at this time.")
    else:
        print(f"\nNutrition information for {result['dish']} ({result['user_portion']}g):")
        print(f"Calories: {result['calories']}")
        print(f"Protein: {result['protein']}g")
        print(f"Carbohydrates: {result['carbs']}g")
        print(f"Fat: {result['fat']}g")
        print(f"Halal: {result['halal']}")
        print(f"Vegan: {result['vegan']}")
        print(f"Vegetarian: {result['vegetarian']}")
        print(f"Sikh Friendly: {result['sikh_friendly']}")
        print(f"Fasting Friendly: {result['fasting_friendly']}")
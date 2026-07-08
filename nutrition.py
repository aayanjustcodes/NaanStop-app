import pandas as pd

food_data = pd.read_csv("food_data.csv")

def calculate_nutrients(nutrient, user_portion, serving_size):
    nutrition_value = (user_portion / serving_size) * nutrient
    return nutrition_value

def nutrition(dish):
    result = food_data[food_data["dish"] == dish]

    if len(result) == 0:
        print("Sorry! We do not have nutrition information for that dish at this time.")
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

        user_portion = float(input(f"How many grams of {dish} did you eat? "))
        serving_size = result['serving_size'].values[0]

        calories = calculate_nutrients(result['calories'].values[0], user_portion, serving_size)
        protein = calculate_nutrients(result['protein'].values[0], user_portion, serving_size)
        carbs = calculate_nutrients(result['carbs'].values[0], user_portion, serving_size)
        fat = calculate_nutrients(result['fat'].values[0], user_portion, serving_size)

        print(f"\nNutrition information for {dish} ({user_portion}g):")
        print(f"Calories: {round(calories)}")
        print(f"Protein: {round(protein)}g")
        print(f"Carbohydrates: {round(carbs)}g")
        print(f"Fat: {round(fat)}g")
        print(f"Halal: {halal}")
        print(f"Vegan: {vegan}")
        print(f"Vegetarian: {vegetarian}")
        print(f"Sikh Friendly: {sikh_friendly}")
        print(f"Fasting Friendly: {fasting_friendly}")

query = input("Enter a dish name: ").to_lower()
nutrition(query)
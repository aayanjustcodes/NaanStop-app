import pandas as pd

food_data = pd.read_csv("food_data.csv")

def nutrition(dish):
    result = food_data[food_data["dish"] == dish]

    if len(result) == 0:
        print("Sorry! We do not have nutrition information for that dis at this time.")
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

        print(f"\nNutrition information for {dish}:")
        print(f"Calories: {result['calories'].values[0]}")
        print(f"Protein: {result['protein'].values[0]}g")
        print(f"Carbohydrates: {result['carbs'].values[0]}g")
        print(f"Fat: {result['fat'].values[0]}g")
        print(f"Halal: {halal}")
        print(f"Vegan: {vegan}")
        print(f"Vegetarian: {vegetarian}")
        print(f"Sikh Friendly: {sikh_friendly}")
        print(f"Fasting Friendly: {fasting_friendly}")
              

query = input("Enter a dish name: ")
nutrition(query) 
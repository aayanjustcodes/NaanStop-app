import pandas as pd

food_data = pd.read_csv("food_data.csv")

def diet_filter(preference):
    result = food_data[food_data["is_" + preference] == 1]
    
    if len(result) == 0:
        print("No dishes found for that dietary preference.")
    else:
        print(f"\nDishes compatible with {preference}:")
        print(result["dish"])

preference = input("Enter your dietary preference (halal/vegan/vegetarian/sikh_friendly/fasting_friendly): ").lower()
diet_filter(preference)
import pandas as pd

food_data = pd.read_csv("food_data.csv")

def diet_filter(preference):
    result = food_data[food_data["is_" + preference] == 1]
    
    if len(result) == 0:
        return None
    else:
        return result["dish"].tolist()

if __name__ == "__main__":
    preference = input("Enter your dietary preference (halal/vegan/vegetarian/sikh_friendly/fasting_friendly): ").lower()
    result = diet_filter(preference)
    if result is None:
        print("No dishes found for that dietary preference.")
    else:
        print(f"\nCompatible dishes:")
        for dish in result:
            print(f"- {dish}")
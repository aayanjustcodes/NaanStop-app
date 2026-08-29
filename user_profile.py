def calculate_calorie_target(weight, height, age, gender, activity_level):
    if gender == "male":
        BMR = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        BMR = (10 * weight) + (6.25 * height) - (5 * age) - 161

    if activity_level == "sedentary":
        calorie_target = BMR * 1.2
    elif activity_level == "light":
        calorie_target = BMR * 1.375
    elif activity_level == "moderate":
        calorie_target = BMR * 1.55
    elif activity_level == "active":
        calorie_target = BMR * 1.725
    elif activity_level == "very active":
        calorie_target = BMR * 1.9

    return round(calorie_target)

if __name__ == "__main__":
    weight = float(input("Enter your weight in kg: "))
    height = float(input("Enter your height in cm: "))
    age = int(input("Enter your age in years: "))
    gender = input("Enter your gender (male/female): ").lower()
    activity_level = input("Enter your activity level (sedentary/light/moderate/active/very active): ").lower()

    calorie_target = calculate_calorie_target(weight, height, age, gender, activity_level)
    print(f"Your daily calorie target is: {round(calorie_target)} calories.")
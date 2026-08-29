import streamlit as st
from nutrition import nutrition
from filter import diet_filter
from user_profile import calculate_calorie_target
from meal_log import log_meal

st.title("NaanStop 🍛")
st.write("Your desi nutrition tracker.")

page = st.sidebar.selectbox("What do you want to do?", [
    "Nutrition Lookup",
    "Diet Filter",
    "Calorie Target Calculator",
    "Log a Meal"
])

if page == "Nutrition Lookup":
    st.header("Nutrition Lookup")
    dish = st.text_input("Enter a dish name (e.g. biryani, dal, roti):")
    user_portion = st.number_input("How many grams did you eat?", min_value=1, value=100)
    if dish:
        result = nutrition(dish.lower().replace(" ", "_"), user_portion)
        if result is None:
            st.error("Sorry! We do not have nutrition information for that dish at this time.")
        else:
            st.subheader(f"Nutrition info for {result['dish'].replace('_', ' ')} ({result['user_portion']}g):")
            st.write(f"Calories: {result['calories']}")
            st.write(f"Protein: {result['protein']}g")
            st.write(f"Carbohydrates: {result['carbs']}g")
            st.write(f"Fat: {result['fat']}g")
            st.write(f"Halal: {result['halal']}")
            st.write(f"Vegan: {result['vegan']}")
            st.write(f"Vegetarian: {result['vegetarian']}")
            st.write(f"Sikh Friendly: {result['sikh_friendly']}")
            st.write(f"Fasting Friendly: {result['fasting_friendly']}")

elif page == "Diet Filter":
    st.header("Diet Filter")
    preference = st.selectbox("Select your dietary preference:", [
        "halal", "vegan", "vegetarian", "sikh_friendly", "fasting_friendly"
    ], format_func=lambda x: x.replace("_", " ").title())
    if st.button("Find compatible dishes"):
        result = diet_filter(preference)
        if result is None:
            st.error("No dishes found for that dietary preference.")
        else:
            st.subheader(f"Dishes compatible with {preference.replace('_', ' ').title()}:")
            for dish in result:
                st.write(f"- {dish.replace('_', ' ').title()}")

elif page == "Calorie Target Calculator":
    st.header("Calorie Target Calculator")
    weight = st.number_input("Enter your weight in kg:", min_value=1.0, value=70.0)
    height = st.number_input("Enter your height in cm:", min_value=1.0, value=170.0)
    age = st.number_input("Enter your age in years:", min_value=1, value=25)
    gender = st.selectbox("Select your gender:", ["male", "female"])
    activity_level = st.selectbox("Select your activity level:", [
        "sedentary", "light", "moderate", "active", "very active"
    ], format_func=lambda x: x.title())
    if st.button("Calculate Calorie Target"):
        calorie_target = calculate_calorie_target(weight, height, age, gender, activity_level)
        st.success(f"Your daily calorie target is: {calorie_target} calories.")

elif page == "Log a Meal":
    st.header("Log a Meal")
    dish = st.text_input("Enter the dish name (e.g. biryani, dal, roti):")
    user_portion = st.number_input("Enter the portion size in grams:", min_value=1, value=100)
    if st.button("Log Meal"):
        log_entry = log_meal(dish.lower().replace(" ", "_"), user_portion)
        if log_entry is None:
            st.error("Sorry! We do not have nutrition information for that dish at this time.")
        else:
            st.success(f"Logged {log_entry['user_portion']}g of {log_entry['dish'].replace('_', ' ')} — {log_entry['calories']} calories")

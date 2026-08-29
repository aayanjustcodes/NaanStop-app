import streamlit as st
from nutrition import nutrition
from filter import diet_filter

st.title("NaanStop 🍛")
st.write("Your desi nutrition tracker.")

page = st.sidebar.selectbox("What do you want to do?", [
    "Nutrition Lookup",
    "Diet Filter"
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
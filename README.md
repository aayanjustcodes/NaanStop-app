# NaanStop 🍛

**Your desi nutrition tracker.**

NaanStop is an AI-powered nutrition tracking app built specifically for South Asian cuisine — filling the gap that apps like MyFitnessPal leave for desi food. Most nutrition apps have poor or nonexistent databases for South Asian dishes. NaanStop is built from the ground up for this cuisine, with diet compatibility filtering for Halal, Vegetarian, Vegan, Sikh-friendly, and Ramadan fasting diets.

---

## Current Features (MVP — In Progress)

- **Nutrition Lookup** — search any desi dish, enter how many grams you ate, and get scaled calorie/macro information based on your actual portion
- **Diet Filter** — filter dishes by dietary preference (Halal, Vegan, Vegetarian, Sikh-friendly, Fasting-friendly)
- **Portion Scaling** — all nutrition data scales proportionally to your actual portion size, not just a fixed serving
- **15 starter dishes** — biryani, dal, roti, samosa, butter chicken, palak paneer, dosa, idli, chole, paratha, gulab jamun, chicken tikka, rice, chicken karahi, lassi (expanding over time)

---

## Tech Stack

- **Python 3.13**
- **Streamlit** — web app UI
- **Pandas** — data loading and filtering
- **TensorFlow/Keras** — (coming in Phase 2) photo recognition model
- **Deployed on** Streamlit Community Cloud (coming soon)

---

## Setup (Local)

```bash
# Clone the repo
git clone https://github.com/aayanjustcodes/NaanStop-app.git
cd NaanStop-app

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install streamlit tensorflow pandas numpy pillow scikit-learn

# Run the app
streamlit run app.py
```

---

## Phase 2 Roadmap

- **Photo recognition** — upload a photo of a desi dish, AI predicts what it is using a custom-trained TensorFlow model (transfer learning on MobileNetV2)
- **User profile + calorie targets** — age, weight, height, activity level → personalized daily calorie goal using BMR formula
- **Meal logging** — save what you ate each day, persists between sessions
- **Consistency streak** — gamified daily logging streak to build habits
- **Tracking dashboard** — charts showing calorie intake and weight trend over time
- **Expanded food database** — more dishes, more granularity (chicken biryani vs veg biryani, plain rice vs biryani rice, individual ingredients like palak, paneer separately)
- **Hormone cycle tracking** — cycle-aware nutrition and calorie adjustments
- **Medical conditions survey** — short onboarding survey, expands over time with follow-up questions

---

## Phase 3 Roadmap

- **CGM Integration (Dexcom API)** — connect to continuous glucose monitor data to track real-time blood sugar response to specific desi dishes; over time learns your personal glucose response to each food and gives personalized carb estimates based on YOUR data, not generic database numbers. Especially powerful for Type 1 and Type 2 diabetics managing diet around South Asian cuisine.
- **Halal/dietary certification API** — integrate with halal certification databases for verified dish tagging
- **Multi-user accounts + cloud database** — real authentication, data synced across devices
- **Mobile app** — React Native or Flutter wrapper around the core logic

---

## Why NaanStop?

South Asian cuisine is eaten by over 1.5 billion people globally, yet nutrition apps treat it as an afterthought. Desi home-cooked meals are mixed dishes with regional variation and no standard portion sizes — impossible to track accurately with existing tools. NaanStop is built specifically for this gap.

---

*Built by Aayan Ali*
*Original concept: Aayan Ali, Roshan Srivatsan*
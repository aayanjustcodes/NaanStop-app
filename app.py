
import html
import os
import tempfile

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from nutrition import nutrition
from filter import diet_filter
from user_profile import calculate_calorie_target
from meal_log import log_meal
from dashboard import get_today_summary
from streak_counter import get_streak
from predict import predict_dish


# ==================================================
# CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="NaanStop",
    page_icon="🍛",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ==================================================
# STYLING
# ==================================================

st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap');

html, body, [data-testid="stApp"] {
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            circle at 85% 0%,
            rgba(35, 74, 118, 0.12),
            transparent 40%
        ),
        #151c27;
    color: #edf2f7;
}

[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3 {
    font-family: 'Outfit', sans-serif !important;
    color: #f8fafc !important;
}

[data-testid="stMetric"] {
    background: #1c2532;
    border: 1px solid #34475c;
    border-radius: 15px;
    padding: 17px 18px;
}

[data-testid="stMetricLabel"] {
    color: #aab8c8;
}

[data-testid="stMetricValue"] {
    color: #ffffff;
    font-family: 'Outfit', sans-serif;
}


/* ==================================================
   BUTTONS
   ================================================== */

/* Orange by default, including secondary buttons */
div[data-testid="stButton"] button[data-testid^="stBaseButton"],
div[data-testid="stButton"] > button,
.stButton > button {
    background-color: #f4a340 !important;
    color: #151a20 !important;
    border: 1px solid #f4a340 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    transition:
        background-color 0.15s ease,
        border-color 0.15s ease,
        transform 0.15s ease !important;
}

/* Darker orange on hover */
div[data-testid="stButton"] button[data-testid^="stBaseButton"]:hover,
div[data-testid="stButton"] > button:hover,
.stButton > button:hover {
    background-color: #df8624 !important;
    border-color: #df8624 !important;
    color: #151a20 !important;
}

/* Darkest orange while pressing */
div[data-testid="stButton"] button[data-testid^="stBaseButton"]:active,
div[data-testid="stButton"] > button:active,
.stButton > button:active {
    background-color: #c8751e !important;
    border-color: #c8751e !important;
    color: #151a20 !important;
}

/* Don't leave buttons dark after clicking */
div[data-testid="stButton"] button[data-testid^="stBaseButton"]:focus:not(:hover):not(:active),
div[data-testid="stButton"] > button:focus:not(:hover):not(:active) {
    background-color: #f4a340 !important;
    border-color: #f4a340 !important;
}

/* Keep icons the same colour as button text */
div[data-testid="stButton"] button svg {
    color: currentColor !important;
    fill: none;
}


/* ==================================================
   TEXT AND NUMBER INPUTS
   ================================================== */

[data-testid="stTextInput"] [data-baseweb="input"],
[data-testid="stNumberInput"] [data-baseweb="input"] {
    background: #202b39 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: transparent !important;
    color: #ffffff !important;
    border-radius: 10px !important;
}

[data-testid="stTextInput"] [data-baseweb="input"] > div,
[data-testid="stNumberInput"] [data-baseweb="input"] > div {
    border-radius: inherit !important;
}

/* Hide +/- buttons */
[data-testid="stNumberInput"] button {
    display: none !important;
}

/* Hide browser number spinners */
[data-testid="stNumberInput"] input::-webkit-inner-spin-button,
[data-testid="stNumberInput"] input::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

[data-testid="stNumberInput"] input[type="number"] {
    appearance: textfield;
    -moz-appearance: textfield;
}


/* ==================================================
   DROPDOWNS
   ================================================== */

[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #202b39 !important;
    border-radius: 10px !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"]:focus-within > div {
    border-color: #f4a340 !important;
}

[data-baseweb="popover"] [role="option"]:hover {
    background: rgba(244, 163, 64, 0.18) !important;
}

[data-baseweb="popover"] [aria-selected="true"] {
    background: rgba(244, 163, 64, 0.25) !important;
}


/* ==================================================
   GENDER SELECTOR
   ================================================== */

[data-testid="stSegmentedControl"] button {
    border-radius: 10px !important;
    transition: background-color 0.15s ease !important;
}

[data-testid="stSegmentedControl"] button[aria-checked="true"],
[data-testid="stSegmentedControl"] button[aria-pressed="true"],
[data-testid="stSegmentedControl"] button[aria-selected="true"] {
    background: #f4a340 !important;
    color: #151a20 !important;
}

[data-testid="stSegmentedControl"] button:hover {
    background: #df8624 !important;
    color: #151a20 !important;
}


/* ==================================================
   OTHER INPUTS
   ================================================== */

[data-testid="stFileUploader"] section {
    border-radius: 10px;
    border-color: #435165;
}

[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}


/* ==================================================
   BRAND
   ================================================== */

.ns-brand {
    padding: 9px 0 18px;
    text-align: center;
}

.ns-brand-name {
    font: 800 34px/1.15 'Outfit', sans-serif;
    color: #ffffff;
    letter-spacing: -1.5px;
}

.ns-brand-name span {
    color: #f4a340;
}

.ns-brand-sub {
    color: #9caec0;
    font-size: 13px;
    margin-top: 7px;
}

.ns-page-title {
    font: 700 32px/1.2 'Outfit', sans-serif;
    color: #ffffff;
    text-align: center;
    margin: 8px 0 26px;
}

.ns-section {
    color: #f1f5f9;
    font: 700 21px 'Outfit', sans-serif;
    margin: 25px 0 13px;
}


/* ==================================================
   STREAK CARD
   ================================================== */

.ns-streak {
    background: linear-gradient(135deg, #282d38, #1c2a3b);
    border: 1px solid #b17c39;
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0 22px;
}

.ns-streak-label {
    color: #f4bc74;
    font-weight: 700;
    font-size: 12px;
    letter-spacing: 1.2px;
}

.ns-streak-number {
    color: #ffffff;
    font: 800 37px/1.4 'Outfit', sans-serif;
    margin-top: 5px;
}

.ns-streak-number span {
    color: #cbd5e1;
    font: 500 14px 'DM Sans', sans-serif;
}

.ns-streak-note {
    color: #b4bfcc;
    font-size: 12px;
    margin-top: 4px;
}


/* ==================================================
   FLOATING EXPLORE BUTTON
   ================================================== */

.st-key-naanring_launcher {
    position: fixed;
    right: 22px;
    bottom: 22px;
    z-index: 999;
}

.st-key-naanring_launcher button {
    border-radius: 10px !important;
    min-height: 52px;
    padding: 0 23px;
    box-shadow:
        0 10px 34px rgba(0, 0, 0, 0.35),
        0 0 0 2px rgba(244, 163, 64, 0.12);
}


/* ==================================================
   NAANRING DIALOG
   ================================================== */

[data-testid="stDialog"] [role="dialog"] {
    background: #171f2b;
    border: 1px solid #435165;
    border-radius: 20px;
}

/* Same orange button styling inside the dialog */
[data-testid="stDialog"] .stButton button {
    min-height: 55px;
    background-color: #f4a340 !important;
    color: #151a20 !important;
    border: 1px solid #f4a340 !important;
    border-radius: 10px !important;
    font-size: 0.85rem;
    font-weight: 700;
    white-space: normal;
}

[data-testid="stDialog"] .stButton button:hover {
    background-color: #df8624 !important;
    border-color: #df8624 !important;
    color: #151a20 !important;
}

[data-testid="stDialog"] .stButton button:active {
    background-color: #c8751e !important;
    border-color: #c8751e !important;
}

[data-testid="stDialog"] .stButton button:focus:not(:hover):not(:active) {
    background-color: #f4a340 !important;
    border-color: #f4a340 !important;
}

[data-testid="stDialog"] [data-testid="stHorizontalBlock"] {
    align-items: center;
    margin-bottom: 10px;
}


/* ==================================================
   CSS-ONLY ORANGE PLATE
   ================================================== */

.ns-plate-wrap {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px 0 14px;
}

.ns-plate {
    width: min(100%, 205px);
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;

    background:
        radial-gradient(
            circle at 38% 30%,
            #ffc66d 0%,
            #f5a13a 48%,
            #df8528 83%,
            #b9651c 100%
        );

    border: 4px solid #ffc879;

    box-shadow:
        0 12px 28px rgba(0, 0, 0, 0.35),
        inset 0 0 0 4px #c47a2c,
        inset 0 0 0 8px #ffd18b,
        inset 0 0 0 12px #d58a32,
        inset 0 0 0 14px rgba(255, 229, 174, 0.75);
}

.ns-plate::before {
    content: "";
    position: absolute;
    inset: 19%;
    border-radius: 50%;

    background:
        radial-gradient(
            circle at 35% 27%,
            #ffc36a 0%,
            #f5a13a 72%,
            #d87920 100%
        );

    border: 2px solid rgba(255, 224, 167, 0.85);

    box-shadow:
        inset 0 4px 10px rgba(130, 67, 16, 0.13),
        0 2px 5px rgba(255, 255, 255, 0.15);
}

.ns-plate-center {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    text-align: center;
}

.ns-plate-name {
    color: #5a3213;
    font: 800 13px 'Outfit', sans-serif;
    letter-spacing: 1px;
}

.ns-plate-subtitle {
    color: #70401b;
    font: 600 9px 'DM Sans', sans-serif;
}


/* ==================================================
   MOBILE RESPONSIVENESS
   ================================================== */

@media (max-width: 600px) {

    .ns-brand-name {
        font-size: 29px;
    }

    .ns-page-title {
        font-size: 27px;
    }

    .st-key-naanring_launcher {
        right: 12px;
        bottom: 12px;
    }

    .st-key-naanring_launcher button {
        min-height: 47px;
        padding: 0 17px;
        border-radius: 10px !important;
    }

    [data-testid="stDialog"] .stButton button {
        min-height: 48px;
        font-size: 0.7rem;
        padding: 5px;
        border-radius: 10px !important;
    }

    [data-testid="stTextInput"] [data-baseweb="input"],
    [data-testid="stNumberInput"] [data-baseweb="input"],
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        border-radius: 10px !important;
    }

    [data-testid="stSegmentedControl"] button {
        border-radius: 10px !important;
    }

    /* The plate is intentionally still circular */
    .ns-plate {
        width: min(100%, 160px);
        border-radius: 50%;
    }

    .ns-plate-name {
        font-size: 11px;
    }

    .ns-plate-subtitle {
        font-size: 8px;
    }
}
</style>
""")


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def section(label):
    st.html(
        f'<div class="ns-section">{html.escape(label)}</div>'
    )


def page_title(label):
    st.html(
        f'<div class="ns-page-title">{html.escape(label)}</div>'
    )


def show_nutrition_info(result):
    dish_name = result["dish"].replace("_", " ").title()
    portion = result["user_portion"]

    st.subheader(f"{dish_name} ({portion}g)")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Calories", str(result["calories"]))
        st.metric("Protein", f"{result['protein']}g")

    with col2:
        st.metric("Carbohydrates", f"{result['carbs']}g")
        st.metric("Fat", f"{result['fat']}g")

    section("Dietary Information")

    dietary_labels = [
        ("halal", "Halal"),
        ("vegan", "Vegan"),
        ("vegetarian", "Vegetarian"),
        ("sikh_friendly", "Sikh Friendly"),
        ("fasting_friendly", "Fasting Friendly"),
    ]

    for key, label in dietary_labels:
        st.write(f"{label}: {result[key]}")


# ==================================================
# BRAND
# ==================================================

st.html("""
<div class="ns-brand">
    <div class="ns-brand-name">
        Naan<span>Stop</span>
    </div>
    <div class="ns-brand-sub">
        Desi food. Real numbers.
    </div>
</div>
""")


# ==================================================
# NAVIGATION
# ==================================================

PAGES = [
    "Dashboard",
    "Nutrition Lookup",
    "Photo Recognition",
    "Log a Meal",
    "Diet Filter",
    "Calorie Target Calculator",
]

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"


def go_to(destination):
    if destination in PAGES:
        st.session_state.current_page = destination
        st.rerun()


# ==================================================
# NAANRING
# ==================================================

@st.dialog("Explore NaanStop", width="large")
def naanring():

    left, center, right = st.columns([1, 1.1, 1])

    with center:
        if st.button(
            "Dashboard",
            icon=":material/dashboard:",
            key="ring_dashboard",
            use_container_width=True,
        ):
            go_to("Dashboard")

    left, center, right = st.columns([1, 1.5, 1])

    with left:
        if st.button(
            "Lookup",
            icon=":material/search:",
            key="ring_lookup",
            use_container_width=True,
        ):
            go_to("Nutrition Lookup")

        if st.button(
            "Diet Filter",
            icon=":material/filter_alt:",
            key="ring_diet",
            use_container_width=True,
        ):
            go_to("Diet Filter")

    with center:
        st.html("""
<div class="ns-plate-wrap">
    <div class="ns-plate">
        <div class="ns-plate-center">
            <div class="ns-plate-name">NAANSTOP</div>
            <div class="ns-plate-subtitle">What's cooking?</div>
        </div>
    </div>
</div>
""")

    with right:
        if st.button(
            "Scan Food",
            icon=":material/photo_camera:",
            key="ring_scan",
            use_container_width=True,
        ):
            go_to("Photo Recognition")

        if st.button(
            "Targets",
            icon=":material/track_changes:",
            key="ring_targets",
            use_container_width=True,
        ):
            go_to("Calorie Target Calculator")

    left, center, right = st.columns([1, 1.1, 1])

    with center:
        if st.button(
            "Log a Meal",
            icon=":material/add_circle:",
            key="ring_log",
            use_container_width=True,
        ):
            go_to("Log a Meal")


# ==================================================
# FLOATING EXPLORE BUTTON
# ==================================================

if st.button(
    "Explore",
    icon=":material/blur_circular:",
    key="naanring_launcher",
    type="primary",
):
    naanring()


page = st.session_state.current_page
streak = get_streak()


# ==================================================
# DASHBOARD
# ==================================================

if page == "Dashboard":

    page_title("Dashboard")

    today_summary = get_today_summary()
    today_log = today_summary["today_log"]

    st.html(f"""
<div class="ns-streak">
    <div class="ns-streak-label">
        YOUR LOGGING STREAK
    </div>
    <div class="ns-streak-number">
        {streak}
        <span>{"day" if streak == 1 else "days"}</span>
    </div>
    <div class="ns-streak-note">
        Small steps. Consistent progress.
    </div>
</div>
""")

    if today_log.empty:
        st.info(
            "No meals logged today. Open Explore and "
            "select Log a Meal to start tracking."
        )

    section("Today's Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Calories",
            f"{today_summary['total_calories']:.0f}",
        )
        st.metric(
            "Protein",
            f"{today_summary['total_protein']:.0f}g",
        )

    with col2:
        st.metric(
            "Carbohydrates",
            f"{today_summary['total_carbs']:.0f}g",
        )
        st.metric(
            "Fat",
            f"{today_summary['total_fat']:.0f}g",
        )

    section("Today's Meals")

    if today_log.empty:
        st.write("No meals to display yet.")

    else:
        display_log = today_log[
            [
                "timestamp",
                "dish",
                "user_portion",
                "calories",
            ]
        ].copy()

        display_log["timestamp"] = (
            pd.to_datetime(display_log["timestamp"])
            .dt.strftime("%b %d | %I:%M %p")
            .str.replace("| 0", "| ", regex=False)
        )

        display_log["dish"] = (
            display_log["dish"]
            .astype(str)
            .str.replace("_", " ", regex=False)
            .str.title()
        )

        st.dataframe(
            display_log,
            use_container_width=True,
            hide_index=True,
            column_config={
                "timestamp": st.column_config.TextColumn(
                    "Date & Time"
                ),
                "dish": st.column_config.TextColumn(
                    "Dish"
                ),
                "user_portion": st.column_config.NumberColumn(
                    "Portion (g)",
                    format="%d",
                ),
                "calories": st.column_config.NumberColumn(
                    "Calories",
                    format="%d",
                ),
            },
        )

        section("Meal Timeline")

        timeline = today_log.copy()

        timeline["timestamp"] = pd.to_datetime(
            timeline["timestamp"]
        )

        timeline = timeline.sort_values("timestamp")

        timeline["dish_display"] = (
            timeline["dish"]
            .astype(str)
            .str.replace("_", " ", regex=False)
            .str.title()
        )

        timeline["time_display"] = (
            timeline["timestamp"]
            .dt.strftime("%I:%M %p")
            .str.lstrip("0")
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=timeline["timestamp"],
                y=timeline["calories"],
                mode="markers",
                marker=dict(
                    size=13,
                    color="#f4a340",
                    symbol="circle",
                    line=dict(
                        color="#fde68a",
                        width=2,
                    ),
                ),
                customdata=timeline[
                    [
                        "dish_display",
                        "time_display",
                        "user_portion",
                    ]
                ].to_numpy(),
                hovertemplate=(
                    "<b>%{customdata[0]}</b>"
                    "<br>Time: %{customdata[1]}"
                    "<br>Portion: %{customdata[2]}g"
                    "<br>Calories: %{y:.0f}"
                    "<extra></extra>"
                ),
                name="Meals",
            )
        )

        max_calories = max(
            200,
            float(timeline["calories"].max()) * 1.2,
        )

        fig.update_layout(
            height=360,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=20,
            ),
            showlegend=False,
            hovermode="closest",
            xaxis_title="Time of Meal",
            yaxis_title="Calories",
            xaxis=dict(
                tickformat="%I:%M %p",
                showgrid=False,
                fixedrange=True,
                linecolor="#465365",
                tickfont=dict(color="#aab4c3"),
            ),
            yaxis=dict(
                range=[0, max_calories],
                fixedrange=True,
                gridcolor="rgba(150,150,150,0.15)",
                zeroline=False,
                tickfont=dict(color="#aab4c3"),
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="DM Sans, sans-serif",
                color="#dbe4ee",
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )


# ==================================================
# NUTRITION LOOKUP
# ==================================================

elif page == "Nutrition Lookup":

    page_title("Nutrition Lookup")

    dish = st.text_input(
        "Enter a dish name (e.g. biryani, dal, roti):"
    )

    user_portion = st.number_input(
        "How many grams did you eat?",
        min_value=1,
        value=100,
    )

    if dish:
        dish_key = (
            dish.strip()
            .lower()
            .replace(" ", "_")
        )

        result = nutrition(
            dish_key,
            user_portion,
        )

        if result is None:
            st.error(
                "Sorry! We do not have nutrition "
                "information for that dish at this time."
            )
        else:
            show_nutrition_info(result)


# ==================================================
# PHOTO RECOGNITION
# ==================================================

elif page == "Photo Recognition":

    page_title("Photo Recognition")

    uploaded_file = st.file_uploader(
        "Upload a photo of your food:",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file is not None:

        st.image(
            uploaded_file,
            caption="Uploaded image",
            width=300,
        )

        temp_path = None

        try:
            suffix = os.path.splitext(
                uploaded_file.name
            )[1].lower()

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix or ".jpg",
            ) as temp_file:
                temp_file.write(uploaded_file.getbuffer())
                temp_path = temp_file.name

            dish = predict_dish(temp_path)

            st.success(
                "Detected dish: "
                f"{dish.replace('_', ' ').title()}"
            )

            st.caption(
                "Experimental prediction. "
                "Please verify the identified dish."
            )

            user_portion = st.number_input(
                "How many grams did you eat?",
                min_value=1,
                value=100,
            )

            if st.button(
                "Get Nutrition Info",
                type="primary",
            ):
                result = nutrition(
                    dish,
                    user_portion,
                )

                if result is None:
                    st.error(
                        "Sorry, we don't have nutrition "
                        "information for this dish yet."
                    )
                else:
                    show_nutrition_info(result)

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)


# ==================================================
# LOG A MEAL
# ==================================================

elif page == "Log a Meal":

    page_title("Log a Meal")

    dish = st.text_input(
        "Enter the dish name (e.g. biryani, dal, roti):"
    )

    user_portion = st.number_input(
        "Enter the portion size in grams:",
        min_value=1,
        value=100,
    )

    if st.button("Log Meal", type="primary"):

        dish_key = (
            dish.strip()
            .lower()
            .replace(" ", "_")
        )

        log_entry = log_meal(
            dish_key,
            user_portion,
        )

        if log_entry is None:
            st.error(
                "Sorry! We do not have nutrition "
                "information for that dish at this time."
            )
        else:
            dish_name = (
                log_entry["dish"]
                .replace("_", " ")
                .title()
            )

            st.success(
                f"Logged {log_entry['user_portion']}g "
                f"of {dish_name} — "
                f"{log_entry['calories']} calories"
            )

            st.info(
                "Open Explore and select Dashboard "
                "to view your updated totals."
            )


# ==================================================
# DIET FILTER
# ==================================================

elif page == "Diet Filter":

    page_title("Diet Filter")

    preference = st.selectbox(
        "Choose your dietary preference:",
        [
            "halal",
            "vegan",
            "vegetarian",
            "sikh_friendly",
            "fasting_friendly",
        ],
        format_func=lambda x: (
            x.replace("_", " ").title()
        ),
        accept_new_options=False,
    )

    if st.button(
        "Find compatible dishes",
        type="primary",
    ):
        result = diet_filter(preference)

        if result is None or len(result) == 0:
            st.error(
                "No dishes found for that dietary preference."
            )
        else:
            preference_name = (
                preference.replace("_", " ").title()
            )

            st.subheader(
                f"Dishes compatible with {preference_name}:"
            )

            for dish in result:
                st.write(
                    f"- {dish.replace('_', ' ').title()}"
                )


# ==================================================
# CALORIE TARGET CALCULATOR
# ==================================================

elif page == "Calorie Target Calculator":

    page_title("Calorie Target Calculator")

    weight = st.number_input(
        "Enter your weight in kg:",
        min_value=1.0,
        value=70.0,
    )

    height = st.number_input(
        "Enter your height in cm:",
        min_value=1.0,
        value=170.0,
    )

    age = st.number_input(
        "Enter your age in years:",
        min_value=1,
        value=25,
    )

    gender = st.segmented_control(
        "Select your gender:",
        options=["male", "female"],
        format_func=lambda x: x.title(),
        default="male",
        selection_mode="single",
    )

    activity_level = st.selectbox(
        "Select your activity level:",
        [
            "sedentary",
            "light",
            "moderate",
            "active",
            "very active",
        ],
        format_func=lambda x: x.title(),
        accept_new_options=False,
    )

    if st.button(
        "Calculate Calorie Target",
        type="primary",
    ):
        if gender is None:
            st.warning("Please select your gender.")
        else:
            calorie_target = calculate_calorie_target(
                weight,
                height,
                age,
                gender,
                activity_level,
            )

            st.success(
                "Your estimated daily calorie target is: "
                f"{calorie_target} calories."
            )

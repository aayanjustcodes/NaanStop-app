# NaanStop 🍛

**A South Asian nutrition tracker built with Python, Streamlit, and PyTorch.**

NaanStop is a web application designed to make nutrition tracking more accessible for South Asian cuisine. It combines a curated food database, portion-based nutritional calculations, dietary filtering, meal tracking, and machine-learning-powered food image classification.

**[Try the Live App](https://g3bw2p7fj6an6natmgbanb.streamlit.app/)**

## Features

### 🍽️ Nutrition Lookup
- Browse 16 South Asian food entries.
- Calculate estimated calories, protein, carbohydrates, and fat based on portion size in grams.
- View dietary compatibility information for supported dishes.

### 🥗 Dietary Filtering
Filter the food database by:
- Halal
- Vegetarian
- Vegan
- Sikh-friendly
- Fasting-friendly

Dietary labels are based on the application's dataset and are not independently certified.

### 📸 AI Food Recognition
- Upload an image of a South Asian dish.
- Classify the image using a PyTorch model based on MobileNetV2.
- Supports seven food categories: biryani, butter chicken, chapati, chicken tikka, gulab jamun, lassi, and palak paneer.

The classifier is experimental and predictions may be inaccurate.

### 🎯 Personalized Calorie Targets
- Estimate daily calorie requirements using age, weight, height, sex, and activity level.
- Calculate an estimated daily target using a basal metabolic rate formula and activity multipliers.

### 📊 Meal Logging and Dashboard
- Record meals and their estimated nutritional values.
- View daily calorie and macronutrient totals.
- Visualize nutritional intake through dashboard charts.
- Track consecutive days of meal logging.

Meal data currently uses local CSV storage and is not associated with individual user accounts.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| Pandas | Food data processing and meal logging |
| PyTorch | Model training and inference |
| torchvision / MobileNetV2 | Transfer learning for food image classification |
| CSV | Nutrition database and meal records |
| Streamlit Community Cloud | Application deployment |

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/aayanjustcodes/NaanStop-app.git
cd NaanStop-app
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

On macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Open the local Streamlit URL displayed in your terminal.

## Machine Learning

NaanStop uses a MobileNetV2-based image classifier implemented with PyTorch.

The model was developed using transfer learning, with a pretrained feature extractor and a classification layer adapted to seven supported food categories.

Training includes image resizing, data augmentation, and a training/validation split.

The trained model weights are stored in `model.pth`, and class labels are defined in `class_labels.json`.

**Current limitation:** The model recognizes only its supported classes, and its accuracy has not been independently established.

## Project Structure

```text
NaanStop-app/
├── app.py
├── nutrition.py
├── filter.py
├── user_profile.py
├── meal_log.py
├── dashboard.py
├── streak_counter.py
├── train_model.py
├── predict.py
├── food_data.csv
├── class_labels.json
├── model.pth
├── requirements.txt
└── README.md
```

## Known Limitations

- The food database currently contains 16 entries.
- Nutritional values are estimates and may vary with ingredients, recipes, and portion preparation.
- Image classification is limited to seven supported categories.
- CSV-based meal storage is not a persistent, multi-user database.
- The application does not currently support individual user accounts.

## Future Improvements

- Expand the food database with more regional dishes and recipe variations.
- Improve and evaluate image-classification performance.
- Introduce user accounts and persistent cloud-based storage.
- Add more advanced nutrition insights and personalized tracking.

## Motivation

South Asian meals can be difficult to track using general-purpose nutrition applications because ingredients, preparation methods, and serving sizes vary widely.

NaanStop explores how a cuisine-specific food database and machine learning can make everyday nutrition tracking more accessible.

## Credits

**Development:** Aayan Ali

**Original concept:** Aayan Ali and Roshan Srivatsan

Built as an independently developed portfolio project.

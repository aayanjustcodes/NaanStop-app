"""
test_setup.py

First script for testing the desi-fitness-app project.

Purpose: To confirm python, pandas, and food_data.csv are working together properly
         before building any real features on top of them.
"""

import pandas as pd

food_data = pd.read_csv("food_data.csv")

print("First 5 rows of food_data.csv:")
print(food_data.head())

print(f"\nTotal dishes loaded: {len(food_data)}")
print(f"Columns: {list(food_data.columns)}")
import pandas as pd
from pathlib import Path
import os

def analyze_dataset():
    csv_path = Path(".cache/zomato.csv")
    if not csv_path.exists():
        print(f"Error: {csv_path} not found.")
        return

    print(f"Loading dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    print("\n--- Column Names ---")
    print(df.columns.tolist())
    
    # Identify location column
    location_col = None
    possible_loc_cols = ["location", "locality", "city", "City", "Locality"]
    for col in possible_loc_cols:
        if col in df.columns:
            location_col = col
            break
    
    if not location_col:
        print("Error: Could not find location column.")
        return
    
    print(f"\nUsing location column: '{location_col}'")
    
    # 1. Unique locations
    unique_locations = df[location_col].unique()
    print(f"\nTotal unique locations: {len(unique_locations)}")
    
    # 2. Sample 20 rows
    print("\n--- Sample 20 Rows ---")
    cols_to_show = []
    # Find matching columns for the request
    mapping = {
        "name": ["name", "Restaurant_Name"],
        "location": [location_col],
        "cuisines": ["cuisines", "Cuisine"],
        "cost": ["approx_cost(for two people)", "Average Cost for two", "cost"],
        "rating": ["rate", "Aggregate rating", "rating"]
    }
    
    display_cols = []
    for key, options in mapping.items():
        for opt in options:
            if opt in df.columns:
                display_cols.append(opt)
                break
                
    print(df[display_cols].sample(20).to_string(index=False))
    
    # 4. Count unique locations (already done)
    
    # 5. Top 10 most frequent locations
    print("\n--- Top 10 Most Frequent Locations ---")
    print(df[location_col].value_counts().head(10))
    
    # Check format samples
    print("\n--- Location Format Samples ---")
    print(df[location_col].dropna().unique()[:20])

if __name__ == "__main__":
    analyze_dataset()

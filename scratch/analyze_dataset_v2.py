import pandas as pd
from pathlib import Path

csv_path = Path(".cache/zomato.csv")
df = pd.read_csv(csv_path)

print("Columns:", df.columns.tolist())
location_col = "location"

print("\n--- 20 Sample Rows ---")
mapping = {
    "name": "name",
    "location": "location",
    "cuisines": "cuisines",
    "cost": "approx_cost(for two people)",
    "rating": "rate"
}
display_df = df[list(mapping.values())].sample(20)
print(display_df.to_string(index=False))

print("\nUnique location count:", df[location_col].nunique())
print("\nTop 10 locations:")
print(df[location_col].value_counts().head(10))

print("\nUnique location values (first 50):")
print(df[location_col].unique()[:50])

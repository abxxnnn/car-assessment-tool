import pandas as pd

# Create headers for 155 checklist items
headers = [f"Item_{i+1}" for i in range(155)]

# Create an empty DataFrame with those headers
df_template = pd.DataFrame(columns=headers)

# Save as a CSV file
df_template.to_csv("car_inspection_template.csv", index=False)

print("✅ Template saved as car_inspection_template.csv")

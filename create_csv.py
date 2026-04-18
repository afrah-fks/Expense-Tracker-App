import os
from src.data_generator import generate_synthetic_data

# 1. Create the data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# 2. Generate the data
print("Generating synthetic financial records...")
df = generate_synthetic_data(n_rows=1000)

# 3. Save to CSV
file_path = 'data/expenses.csv'
df.to_csv(file_path, index=False)

print(f"✅ Success! File saved at: {file_path}")
print(df.head()) # Show first 5 rows in terminal
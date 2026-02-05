import pandas as pd

df = pd.read_csv("cisa_coding - cisa.csv")

print(f"Number of unique subthemes: {df['Subtheme'].nunique()}")
print(f"Unique subthemes: {df['Subtheme'].unique()}")
import pandas as pd
from sklearn.metrics import cohen_kappa_score, jaccard_score

# Load the CSV file
file_path = "llm_30_validation.csv"
df = pd.read_csv(file_path)

# --- ADD THIS LINE TO DEBUG ---
print("Available columns:", df.columns)
# -----------------------------

# Extract the annotation columns
abdullah = df["Abdullah"]
lm = df["NotebookLM"]

# ... rest of your code
# Calculate Cohen's Kappa score
kappa_score = cohen_kappa_score(abdullah, lm)

# Filter out (0,0) pairs for Jaccard similarity
non_zero_mask = ~((abdullah == 0) & (lm == 0))
jaccard = jaccard_score(abdullah[non_zero_mask], lm[non_zero_mask])

# Print the results
print(f"Cohen's Kappa Score: {kappa_score:.3f}")
print(f"Jaccard Similarity Score (excluding (0,0)): {jaccard:.3f}")

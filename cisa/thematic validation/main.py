import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score

def compute_agreement(df, col1, col2):
    """Compute agreement metrics between two columns"""
    
    # Remove rows where either column has missing values
    clean_df = df[[col1, col2]].dropna()
    
    if clean_df.empty:
        print("No valid data found after removing missing values.")
        return
    
    # Extract the two columns
    annotations1 = clean_df[col1].values
    annotations2 = clean_df[col2].values
    
    # Calculate metrics
    exact_matches = np.sum(annotations1 == annotations2)
    total_pairs = len(annotations1)
    percentage_agreement = (exact_matches / total_pairs) * 100
    kappa_score = cohen_kappa_score(annotations1, annotations2)
    
    # Interpret Kappa score
    if kappa_score < 0:
        interpretation = "Poor (worse than random)"
    elif kappa_score < 0.20:
        interpretation = "Slight"
    elif kappa_score < 0.40:
        interpretation = "Fair"
    elif kappa_score < 0.60:
        interpretation = "Moderate"
    elif kappa_score < 0.80:
        interpretation = "Substantial"
    else:
        interpretation = "Almost Perfect"
    
    # Print results
    print(f"\nAgreement Analysis: '{col1}' vs '{col2}'")
    print("=" * 50)
    print(f"Total valid pairs: {total_pairs}")
    print(f"Exact matches: {exact_matches}")
    print(f"Disagreements: {total_pairs - exact_matches}")
    print(f"Percentage Agreement: {percentage_agreement:.2f}%")
    print(f"Cohen's Kappa: {kappa_score:.4f}")
    print(f"Kappa Interpretation: {interpretation}")

def show_disagreements(df, col1, col2):
    """Show disagreement patterns"""
    
    clean_df = df[[col1, col2]].dropna()
    disagreements = clean_df[clean_df[col1] != clean_df[col2]]
    
    if len(disagreements) == 0:
        print("\nNo disagreements found!")
        return
    
    print(f"\nTop Disagreement Patterns:")
    print("-" * 30)
    patterns = disagreements.groupby([col1, col2]).size().sort_values(ascending=False)
    
    for (cat1, cat2), count in patterns.head(10).items():
        print(f"{cat1} → {cat2}: {count} cases")

def main():
    """Main function"""
    
    # Load data
    try:
        # df = pd.read_csv("cisa_validation.csv")
        df = pd.read_csv("cycloneDX_validate.csv")
        print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    except FileNotFoundError:
        print("Error: cisa_validation.csv not found")
        return
    
    # Compute agreement
    # compute_agreement(df, 'Subtheme', 'Huzaifa')
    
    # Show disagreement patterns
    # show_disagreements(df, 'Subtheme', 'Huzaifa')

    # Compute agreement
    compute_agreement(df, 'Abdullah-Subtheme', 'Punar-Subtheme')
    show_disagreements(df, 'Abdullah-Subtheme', 'Punar-Subtheme')

if __name__ == "__main__":
    main()
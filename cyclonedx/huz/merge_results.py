import pandas as pd

# Load the three CSV files
try:
    df_ancestors = pd.read_csv("cyclonedx_ancestors.csv")
    df_breadth = pd.read_csv("cyclonedx_breadth.csv")
    df_depth = pd.read_csv("cyclonedx_depth.csv")

    # Merge them on 'class_name'
    # 1. Merge Ancestors and Breadth
    merged_df = pd.merge(df_ancestors, df_breadth[['class_name', 'breadth']], on='class_name', how='outer')
    
    # 2. Merge with Depth
    merged_df = pd.merge(merged_df, df_depth[['class_name', 'max_depth']], on='class_name', how='outer')

    # Reorder columns to look nice
    final_df = merged_df[['class_name', 'breadth', 'ancestor_count', 'max_depth', 'ancestors']]
    
    # Sort by Breadth (Usually most interesting for analysis)
    final_df = final_df.sort_values(by='breadth', ascending=False)

    # Save to final CSV
    final_df.to_csv("FINAL_CYCLONEDX_TABLE.csv", index=False)

    print("Success! Created 'FINAL_CYCLONEDX_TABLE.csv'. Send this to your partner.")

except FileNotFoundError as e:
    print(f"Error: Missing one of the CSV files. Run the 3 scripts first! {e}")
except Exception as e:
    print(f"An error occurred: {e}. (Do you have 'pandas' installed? Try 'pip install pandas')")
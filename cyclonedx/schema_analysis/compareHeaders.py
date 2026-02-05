#!/usr/bin/env python3
import json
import sys
import os

def compare_schemas(schema1_path, schema2_path, output_path="headerComparison.txt"):
    # Load both schemas
    with open(schema1_path, "r") as f1:
        schema1 = json.load(f1)
    with open(schema2_path, "r") as f2:
        schema2 = json.load(f2)

    # Extract definitions (support both "$defs" and "definitions")
    defs1 = schema1.get("$defs", schema1.get("definitions", {}))
    defs2 = schema2.get("$defs", schema2.get("definitions", {}))

    # Prepare lists
    abstract_classes = []
    missing_classes = []

    # Iterate through definitions in schema1
    for header in defs1.keys():
        if header in defs2:
            continue
        elif f"{header}_derived" in defs2:
            abstract_classes.append(header)
        else:
            missing_classes.append(header)

    # Write results
    with open(output_path, "w") as out:
        out.write("===== Header Comparison Results =====\n\n")

        out.write("Abstract Classes (found as _derived):\n")
        if abstract_classes:
            for item in abstract_classes:
                out.write(f"- {item}\n")
        else:
            out.write("None\n")

        out.write("\nMissing Classes (not found in schema2):\n")
        if missing_classes:
            for item in missing_classes:
                out.write(f"- {item}\n")
        else:
            out.write("None\n")

    print(f"[✔] Comparison complete. Results saved to '{output_path}'")

def main():
    # Ensure proper arguments
    if len(sys.argv) != 3:
        print("Usage: python3 checkHeaders.py <schema1>.json <schema2>.json")
        sys.exit(1)

    schema1_path = sys.argv[1]
    schema2_path = sys.argv[2]

    # Check that files exist
    if not os.path.exists(schema1_path):
        print(f"Error: File not found: {schema1_path}")
        sys.exit(1)
    if not os.path.exists(schema2_path):
        print(f"Error: File not found: {schema2_path}")
        sys.exit(1)

    compare_schemas(schema1_path, schema2_path)

if __name__ == "__main__":
    main()

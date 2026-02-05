# file: compare_structures.py
import json

def load_schema(filepath):
    """Loads a JSON schema from a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_structures():
    """Compares the structural presence of objects and properties between two schemas."""
    print("--- Running Structural Comparison (Levels 1 & 2) ---")
    
    try:
        prescriptive_schema = load_schema('01_schema.json')
        official_schema = load_schema('schema.json')
    except FileNotFoundError as e:
        print(f"Error: Schema file not found. Make sure '{e.filename}' is in the same directory.")
        return

    # Gracefully handle the difference between '$defs' and 'definitions'
    prescriptive_defs = prescriptive_schema.get('$defs', {})
    official_defs = official_schema.get('definitions', {})

    prescriptive_objects = set(prescriptive_defs.keys())
    official_objects = set(official_defs.keys())

    # --- Level 1: Top-Level Object Presence Comparison ---
    print("\n[Level 1] Comparing Top-Level Object Definitions...")
    
    missing_in_official = prescriptive_objects - official_objects
    added_in_official = official_objects - prescriptive_objects

    if not missing_in_official and not added_in_official:
        print("  ✅ SUCCESS: All top-level object definitions match.")
    else:
        if missing_in_official:
            print(f"  ⚠️ WARNING: Objects in Prescriptive Schema but NOT in Official: {sorted(list(missing_in_official))}")
        if added_in_official:
            print(f"  ℹ️  INFO: Objects in Official Schema but NOT in Prescriptive: {sorted(list(added_in_official))}")
    
    # --- Level 2: Deep Object Property Presence Comparison ---
    print("\n[Level 2] Comparing Property Presence within Common Objects...")
    
    common_objects = prescriptive_objects.intersection(official_objects)
    mismatch_found = False

    for obj_name in sorted(list(common_objects)):
        prescriptive_props = set(prescriptive_defs.get(obj_name, {}).get('properties', {}).keys())
        official_props = set(official_defs.get(obj_name, {}).get('properties', {}).keys())

        missing_props = prescriptive_props - official_props
        added_props = official_props - prescriptive_props

        if missing_props or added_props:
            mismatch_found = True
            print(f"\n  Mismatch found in object '{obj_name}':")
            if missing_props:
                print(f"    - Properties in Prescriptive but NOT in Official: {sorted(list(missing_props))}")
            if added_props:
                print(f"    - Properties in Official but NOT in Prescriptive: {sorted(list(added_props))}")

    if not mismatch_found:
        print("  ✅ SUCCESS: All properties within all common objects match.")
    
    print("\n--- Structural Comparison Complete ---")

if __name__ == '__main__':
    compare_structures()
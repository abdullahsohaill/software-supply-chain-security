# file: compare_constraints.py
import json

def load_schema(filepath):
    """Loads a JSON schema from a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_constraints():
    """Compares the validation constraints of common properties."""
    print("--- Running Granular Constraint Comparison (Level 3) ---")
    
    try:
        prescriptive_schema = load_schema('01_schema.json')
        official_schema = load_schema('schema.json')
    except FileNotFoundError as e:
        print(f"Error: Schema file not found. Make sure '{e.filename}' is in the same directory.")
        return

    prescriptive_defs = prescriptive_schema.get('$defs', {})
    official_defs = official_schema.get('definitions', {})

    common_objects = set(prescriptive_defs.keys()).intersection(set(official_defs.keys()))
    discrepancies = []
    
    constraints_to_check = ['type', 'format', 'pattern', 'const', 'enum', 'minimum', 'uniqueItems']

    # Check top-level properties first
    for prop_name in prescriptive_schema.get('properties', {}):
        if prop_name in official_schema.get('properties', {}):
            p1_prop = prescriptive_schema['properties'][prop_name]
            p2_prop = official_schema['properties'][prop_name]
            for const in constraints_to_check:
                v1 = p1_prop.get(const)
                v2 = p2_prop.get(const)
                if v1 != v2:
                    discrepancies.append(f"  - BOM Root -> '{prop_name}': Mismatch in '{const}'\n"
                                        f"    - Prescriptive: {v1}\n"
                                        f"    - Official....: {v2}")

    # Check defined objects
    for obj_name in sorted(list(common_objects)):
        prescriptive_props = prescriptive_defs.get(obj_name, {}).get('properties', {})
        official_props = official_defs.get(obj_name, {}).get('properties', {})
        common_props = set(prescriptive_props.keys()).intersection(set(official_props.keys()))

        for prop_name in sorted(list(common_props)):
            p1_prop = prescriptive_props[prop_name]
            p2_prop = official_props[prop_name]

            for const in constraints_to_check:
                v1 = p1_prop.get(const)
                v2 = p2_prop.get(const)
                
                # Normalize enums for comparison (order doesn't matter)
                if const == 'enum' and v1 is not None and v2 is not None:
                    if set(v1) == set(v2):
                        continue # They are the same, just maybe in a different order

                if v1 != v2:
                    discrepancies.append(f"  - Object '{obj_name}' -> Property '{prop_name}': Mismatch in '{const}'\n"
                                        f"    - Prescriptive: {v1}\n"
                                        f"    - Official....: {v2}")

    if discrepancies:
        print("\n[Level 3] Found the following constraint discrepancies:")
        for d in discrepancies:
            print(d)
    else:
        print("\n[Level 3] ✅ SUCCESS: No constraint discrepancies found for common properties.")

    print("\n--- Granular Constraint Comparison Complete ---")

if __name__ == '__main__':
    compare_constraints()
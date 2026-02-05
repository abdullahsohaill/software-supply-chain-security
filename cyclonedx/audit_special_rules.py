# file: audit_special_rules.py
import json

def load_schema(filepath):
    """Loads a JSON schema from a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_additional_properties_recursively(obj, path=""):
    """Recursively checks for additionalProperties settings in a schema object."""
    findings = []
    if isinstance(obj, dict):
        current_path = path if path else "BOM Root"
        if obj.get('type') == 'object':
            if 'additionalProperties' in obj:
                findings.append(f"  - At '{current_path}': additionalProperties is set to '{obj['additionalProperties']}'")
            else:
                findings.append(f"  - At '{current_path}': additionalProperties is NOT DEFINED (defaults to open/true)")
        
        for key, value in obj.items():
            findings.extend(find_additional_properties_recursively(value, f"{path}.{key}" if path else key))
            
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            findings.extend(find_additional_properties_recursively(item, f"{path}[{i}]"))
            
    return findings

def audit_rules():
    """Audits specific high-impact rules and architectural choices."""
    print("--- Running Semantic Rule and Architectural Audit ---")
    
    try:
        prescriptive = load_schema('01_schema.json')
        official = load_schema('schema.json')
    except FileNotFoundError as e:
        print(f"Error: Schema file not found. Make sure '{e.filename}' is in the same directory.")
        return

    # 1. Check specVersion Enforcement
    print("\n[Finding 1] Auditing 'specVersion' Enforcement...")
    prescriptive_sv = prescriptive.get('properties', {}).get('specVersion', {})
    official_sv = official.get('properties', {}).get('specVersion', {})
    
    if prescriptive_sv.get('const') == '1.6':
        print("  - Prescriptive Schema correctly enforces 'const: \"1.6\"'.")
    else:
        print("  - WARNING: Prescriptive Schema is NOT enforcing 'const: \"1.6\"' as expected.")
        
    if 'const' not in official_sv and 'enum' not in official_sv:
        print("  - CRITICAL: Official Schema does NOT enforce the value of 'specVersion'. It only checks for type: string.")
    else:
        print("  - INFO: Official Schema appears to have some value enforcement for 'specVersion'.")

    # 2. Check licenseChoice Structure
    print("\n[Finding 2] Auditing 'licenseChoice' Structural Interpretation...")
    try:
        # Check prescriptive (literal) structure
        p_struct = prescriptive['$defs']['licenseChoice']['oneOf'][0]['items']['$ref'] == '#/$defs/license'
        if p_struct:
            print("  - Prescriptive Schema uses a literal interpretation: an array of 'license' objects.")
        
        # Check official (nested) structure
        o_struct = 'license' in official['definitions']['licenseChoice']['oneOf'][0]['items']['properties']
        if o_struct:
             print("  - Official Schema uses a nested interpretation: an array of objects, each containing a 'license' property.")

        if p_struct and o_struct:
            print("  - VERIFIED: The schemas use incompatible structures for license arrays, confirming the mismatch.")
        else:
            print("  - WARNING: Could not automatically verify the licenseChoice mismatch. Manual review needed.")
            
    except (KeyError, IndexError) as e:
        print(f"  - ERROR: Could not traverse schema to check licenseChoice structure. Path may have changed. Error: {e}")

    # 3. Check additionalProperties (Global Strictness)
    print("\n[Finding 3] Auditing Global Strictness Policy ('additionalProperties')...")
    
    # Check root level for a quick summary
    prescriptive_open = 'additionalProperties' not in prescriptive
    official_closed = official.get('additionalProperties') is False
    
    if prescriptive_open:
        print("  - Prescriptive Schema is 'open' at the root level (allows extra properties).")
    else:
        print(f"  - Prescriptive Schema is 'closed' at the root: additionalProperties is {prescriptive.get('additionalProperties')}.")
        
    if official_closed:
        print("  - Official Schema is 'closed' at the root level (forbids extra properties). This is a non-normative hardening choice.")
    else:
        print("  - WARNING: Official Schema is unexpectedly 'open' at the root.")

    print("\n--- Semantic Audit Complete ---")

if __name__ == '__main__':
    audit_rules()
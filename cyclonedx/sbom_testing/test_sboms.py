# code for testing

# SBOMs needed:

# Microsoft SBOM tool (done)
# Syft by Anchore* (done)
# Trivy by Aqua* (done)
# SPDX SBOM generator (done)
# OSS review toolkit
# (all tools with * will have SBOMs generated in SPDX 2.2 or 2.3, and converted to 3.0)

import json
import sys

def load_and_normalize(sbom_path):
    with open(sbom_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    elements = []
    relationships = []
    if '@graph' in data and isinstance(data['@graph'], list):
        for entry in data['@graph']:
            etype = entry.get('type')
            if str(etype).lower() == 'relationship':
                relationships.append(entry)
            else:
                elements.append(entry)
    else:
        elements = data.get('elements', [])
        relationships = data.get('relationships', [])

    # normalize relationship 'to' to be a list and ensure 'from' exists
    for rel in relationships:
        tov = rel.get('to', [])
        if isinstance(tov, str):
            rel['to'] = [tov]
        elif tov is None:
            rel['to'] = []
        else:
            # keep list as-is, but if it contains dicts try to normalize later when used
            rel['to'] = list(tov)

        if 'from' not in rel:
            rel['from'] = rel.get('spdxId')

    normalized = {
        'elements': elements,
        'relationships': relationships,
        'raw': data
    }
    return normalized

def find_elements_by_type(sbom_data, element_type):
    return [elem for elem in sbom_data.get('elements', []) if elem.get('type') == element_type]

def extract_profiles(sbom_data):
    # Look for SpdxDocument entries and return profileConformance or profile
    for e in sbom_data.get('elements', []):
        if e.get('type') == 'SpdxDocument':
            return e.get('profileConformance', []) or e.get('profile', [])
    # fallback to top-level creationInfo.profile if present
    top = sbom_data.get('raw', {})
    if isinstance(top, dict):
        ci = top.get('creationInfo', {})
        return ci.get('profile', []) if isinstance(ci, dict) else []
    return []

def test_none_element_exclusive(sbom_data):
    for rel in sbom_data.get('relationships', []):
        to_elements = rel.get('to', [])
        if "NoneElement" in to_elements and len(to_elements) > 1:
            print(f"FAIL: Relationship from '{rel.get('from')}' contains NoneElement along with other elements in 'to'.")
            return 0
    print("PASS: No relationship violates the NoneElement exclusivity rule.")
    return 1

def test_relationship_type_exists(sbom_data):
    for i, rel in enumerate(sbom_data.get('relationships', [])):
        if 'relationshipType' not in rel:
            print(f"FAIL: Relationship at index {i} (from: {rel.get('from', 'N/A')}) is missing the 'relationshipType' property.")
            return 0
    print("PASS: All relationships have a 'relationshipType' property.")
    return 1

def test_licensing_profile_concluded_license(sbom_data):
    profiles = extract_profiles(sbom_data)
    if 'Licensing' not in profiles:
        print("SKIP: Licensing profile not declared. Test is not applicable.")
        return -1

    software_artifacts = find_elements_by_type(sbom_data, 'SoftwareArtifact')
    if not software_artifacts:
        print("PASS: Licensing profile is declared, but no SoftwareArtifacts are present.")
        return 1

    sources_with_license = {
        rel.get('from') for rel in sbom_data.get('relationships', [])
        if rel.get('relationshipType') == 'hasConcludedLicense'
    }

    all_pass = 1
    for artifact in software_artifacts:
        spdx_id = artifact.get('spdxId')
        if spdx_id not in sources_with_license:
            print(f"FAIL: [Licensing Profile] SoftwareArtifact '{spdx_id}' is missing a 'hasConcludedLicense' relationship.")
            all_pass = 0

    if all_pass == 1:
        print("PASS: All SoftwareArtifacts have a 'hasConcludedLicense' relationship as required by the Licensing profile.")
    return all_pass

def test_build_profile_relationships(sbom_data):
    profiles = extract_profiles(sbom_data)
    if 'Build' not in profiles:
        print("SKIP: Build profile not declared. Test is not applicable.")
        return -1

    build_elements = find_elements_by_type(sbom_data, 'Build')
    if not build_elements:
        print("PASS: Build profile is declared, but no Build elements are present.")
        return 1

    required_types = {"hasInput", "hasOutput", "invokedBy"}
    all_pass = 1

    for build_elem in build_elements:
        spdx_id = build_elem.get('spdxId')
        found_types = {
            rel.get('relationshipType') for rel in sbom_data.get('relationships', [])
            if rel.get('from') == spdx_id
        }

        if not required_types.issubset(found_types):
            missing = required_types - found_types
            print(f"FAIL: [Build Profile] Build element '{spdx_id}' is missing required relationship(s): {', '.join(missing)}.")
            all_pass = 0

    if all_pass == 1:
        print("PASS: All Build elements have the required relationships as per the Build profile.")
    return all_pass

def test_lite_profile(sbom_data): # Test [0][0]
    profiles = extract_profiles(sbom_data)
    if 'Lite' in profiles or 'lite' in profiles:
        return 1
    else:
        return 0

def check_minimum_elements(sbom_data): # Test [0][1]
    # [TODO] check which of the minimum elements are present
    return -2

def test_relationship_types(sbom_data): # Test [1][0]
    relationships = {}
    for rel in sbom_data.get('relationships', []):
        key = rel.get('relationshipType', 'UNKNOWN')

        if key in relationships:
            relationships[key] += 1
        else:
            relationships[key] = 1

    for rel in relationships:
        print(f"relationshipType -{rel}- count: {relationships[rel]}")

    return len(relationships)

def check_max_dependency_depth(sbom_data): # Test [1][1]
    max_depth = 100
    dependencies = {}
    for rel in sbom_data.get('relationships', []):
        if rel.get('relationshipType') == 'DEPENDS_ON' or rel.get('relationshipType') == 'dependsOn':
            from_id = rel.get('from')
            tos = rel.get('to', [])
            clean_tos = []
            for t in tos:
                if isinstance(t, dict):
                    clean_tos.append(t.get('@id') or t.get('spdxId') or str(t))
                else:
                    clean_tos.append(t)
            dependencies.setdefault(from_id, []).extend(clean_tos)

    if not dependencies:
        print("CHECK: No 'dependsOn' relationships found.")
        return 0

    memo = {}
    def get_depth(node_id, visited):
        if node_id in visited:
            print(f"FAIL: Cycle detected in dependency graph involving node '{node_id}'. Path: {' -> '.join(list(visited))} -> {node_id}")
            return float('inf')
        if node_id in memo:
            return memo[node_id]
        visited.add(node_id)
        max_child = 0
        for child in dependencies.get(node_id, []):
            d = get_depth(child, visited)
            if d == float('inf'):
                return float('inf')
            max_child = max(max_child, d)
        visited.remove(node_id)
        memo[node_id] = 1 + max_child
        return memo[node_id]

    all_spdx_ids = {e.get('spdxId') for e in sbom_data.get('elements', []) if 'spdxId' in e}
    max_overall = 1
    for sid in all_spdx_ids:
        d = get_depth(sid, set())
        if d == float('inf'):
            return -2
        max_overall = max(max_overall, d)

    if max_overall > max_depth:
        print(f"FAIL: Maximum dependency depth of {max_overall} exceeds the limit of {max_depth}.")
        return -2

    print(f"CHECK: Maximum dependency depth is {max_overall}")
    return max_overall

def test_methodologies(sbom_data): # Test [2][0]
    # Will remain empty
    return -2

def check_methodologies_result(sbom_data): # Test [2][1]
    # Needs extra inputs: directory path, command used to run
    return -2

def test_interoperability(sbom_data): # Test [3][0]
    # needs to be made more specific checking for cdxextension property
    profiles = extract_profiles(sbom_data)
    if 'Extension' in profiles or 'extension' in profiles:
        return 1
    else:
        return 0

def check_interoperability(sbom_data): # Test [3][1]
    # need access to sbom conversion tools to try converting
    return -2

def test_build_profile(sbom_data): # Test [4][0]
    profiles = extract_profiles(sbom_data)
    if 'Build' in profiles or 'build' in profiles:
        return 1
    else:
        return 0

def check_reproducibility(sbom_data): # Test [4][1]
    # [TODO] need to check how to check for reproducibility
    return -2

def test_profile_used(sbom_data): # Test [5][0]
    # Check if any profile used or not
    profiles = extract_profiles(sbom_data)
    if len(profiles) > 0:
        return 1
    else:
        return 0

def check_empty_fields(sbom_data): # Test [5][1]
    # [TODO] Need to check how many NOASSERTIONS there are as a % of total fields
    return -2

def test_purl(sbom_data): # Test [6][0]
    # [TODO] Need to check if purl format specified in specification is being followed
    return -2

def check_package_similarity(sbom_data): # Test [6][1]
    # [TODO] Check for package similarity across other SBOMs. Needs extra input: path to directory holding the other SBOMs
    return -2

def test_dependency_type(sbom_data): # Test [7][0]
    # [TODO] Check how to do it
    return -2

def check_dynamic_test(sbom_data): # Test [7][1]
    # [TODO] Check how to do it
    return -2

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 test_sboms.py <path_to_sbom.json> <test case number [0,7]> <type of test [0,1]>")
        return 0

    sbom_path = sys.argv[1]
    try:
        sbom_norm = load_and_normalize(sbom_path)
    except Exception as e:
        print("Error loading SBOM:", e)
        return 1

    tests = [
        [test_lite_profile, check_minimum_elements],
        [test_relationship_types, check_max_dependency_depth],
        [test_methodologies, check_methodologies_result],
        [test_interoperability, check_interoperability],
        [test_build_profile, check_reproducibility],
        [test_profile_used, check_empty_fields],
        [test_purl, check_package_similarity],
        [test_dependency_type, check_dynamic_test]
    ]

    testNo = int(sys.argv[2])
    typeNo = int(sys.argv[3])
    testToRun = tests[testNo][typeNo]
    print("Returns: ", testToRun(sbom_norm))
    return testToRun(sbom_norm)


if __name__ == '__main__':
    main()

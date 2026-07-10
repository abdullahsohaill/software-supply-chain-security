import sys
import json
import re
from urllib.parse import unquote

# ---------------------------------------------------------
# Test 1: Minimum Elements
# ---------------------------------------------------------
def check_minimum_elements(sbom_data): # Test [0][1]
    minElementsFound = 0
    TOTALMINELEMENTS = 8

    metadata = sbom_data.get('metadata', {})
    components = sbom_data.get('components', [])
    dependencies = sbom_data.get('dependencies', [])

    if metadata.get('authors'):
        print("SBOM author found")
        minElementsFound += 1
    else:
        print("SBOM author not found")

    if metadata.get('supplier'):
        print("Software producer (supplier) found")
        minElementsFound += 1
    else:
        print("Software producer (supplier) not found")

    if metadata.get('timestamp'):
        print("Timestamp found")
        minElementsFound += 1
    else:
        print("Timestamp not found")

    if metadata.get('tools'):
        print("Tool name found")
        minElementsFound += 1
    else:
        print("Tool name not found")

    all_names = True
    all_versions = True
    all_refs = True

    if not components:
        all_names = False
        all_versions = False
        all_refs = False

    for comp in components:
        if not comp.get('name'): all_names = False
        if not comp.get('version'): all_versions = False
        if not comp.get('bom-ref'): all_refs = False

    if all_names:
        print("Component names found")
        minElementsFound += 1
    else:
        print("Component names missing")

    if all_versions:
        print("Component versions found")
        minElementsFound += 1
    else:
        print("Component versions missing")

    if all_refs:
        print("Software identifiers (bom-ref) found")
        minElementsFound += 1
    else:
        print("Software identifiers missing")

    if dependencies:
        print("Dependency relationships found")
        minElementsFound += 1
    else:
        print("Dependency relationships not found")

    return minElementsFound / TOTALMINELEMENTS

# ---------------------------------------------------------
# Test 2: Maximum Dependency Depth
# ---------------------------------------------------------
def check_max_dependency_depth(sbom_data): # Test [1][1]
    dependencies = sbom_data.get('dependencies', [])
    if not dependencies:
        return 0

    adj_list = {}
    for dep in dependencies:
        ref = dep.get('ref')
        dependsOn = dep.get('dependsOn', [])
        adj_list[ref] = dependsOn

    memo = {}
    def get_depth(node_id, visited):
        if node_id in visited:
            return float('inf') # Cycle
        if node_id in memo:
            return memo[node_id]
        
        visited.add(node_id)
        max_child = 0
        for child in adj_list.get(node_id, []):
            d = get_depth(child, visited)
            if d == float('inf'): return float('inf')
            max_child = max(max_child, d)
        
        visited.remove(node_id)
        memo[node_id] = 1 + max_child
        return memo[node_id]

    max_overall = 0
    for node in adj_list.keys():
        d = get_depth(node, set())
        if d == float('inf'):
            return -2
        max_overall = max(max_overall, d)

    return max_overall

# ---------------------------------------------------------
# Test 3: Methodologies Result (Jaccard)
# ---------------------------------------------------------
def check_methodologies_result(sbom_data, other_sbom_data): # Test [2][1]
    pkgs1 = sbom_data.get('components', [])
    pkgs2 = other_sbom_data.get('components', [])

    names_1 = {pkg.get('name') for pkg in pkgs1 if pkg.get('name')}
    names_2 = {pkg.get('name') for pkg in pkgs2 if pkg.get('name')}

    if not names_1 and not names_2:
        return 0

    intersections = len(names_1.intersection(names_2))
    union = len(names_1.union(names_2))
    
    return intersections / union if union > 0 else 0

# ---------------------------------------------------------
# Test 4: Interoperability (Taxonomy)
# ---------------------------------------------------------
def check_interoperability(sbom_data): # Test [3][1]
    # In CDX, we look at properties. Check if they use 'cdx:' namespace.
    total_props = 0
    cdx_props = 0

    def scan_properties(obj):
        nonlocal total_props, cdx_props
        if isinstance(obj, dict):
            props = obj.get('properties', [])
            for p in props:
                total_props += 1
                name = p.get('name', '')
                if name.startswith('cdx:'):
                    cdx_props += 1
            for k, v in obj.items():
                scan_properties(v)
        elif isinstance(obj, list):
            for i in obj:
                scan_properties(i)

    scan_properties(sbom_data)
    
    if total_props == 0:
        return -2 # No properties to evaluate
    return cdx_props / total_props

# ---------------------------------------------------------
# Test 5: Reproducibility (Formulation)
# ---------------------------------------------------------
def check_reproducibility(sbom_data): # Test [4][1]
    # Check if formulation is present anywhere
    formulation = sbom_data.get('formulation', [])
    if formulation:
        return 1
    
    # Alternatively check components of type 'build' or 'operating-system'
    components = sbom_data.get('components', [])
    for comp in components:
        if comp.get('type') in ['build', 'operating-system']:
            return 1
            
    return 0

# ---------------------------------------------------------
# Test 6: Package Similarity (PURLs)
# ---------------------------------------------------------
def validate_purl(purl):
    if " " in purl or not purl.startswith("pkg:"):
        return False
    
    pattern = r"^pkg:(?P<type>[A-Za-z][A-Za-z0-9.\+\-]*)/(?P<namespace>.*[A-Za-z0-9_]*/)?(?P<name>[^@?#]+)(?:@(?P<version>[^?#]+))?(?:\?(?P<qualifiers>[^#]+))?(?:#(?P<subpath>.+))?$"
    match = re.match(pattern, purl)
    if not match:
        return False
    return True

def test_purl(sbom_data): # Test [6][0]
    components = sbom_data.get('components', [])
    if not components:
        return -2
    
    valid_count = 0
    total_purls = 0
    for comp in components:
        purl = comp.get('purl')
        if purl:
            total_purls += 1
            if validate_purl(purl):
                valid_count += 1
                
    if total_purls == 0:
        return 0
    return valid_count / total_purls

# Placeholder functions to match the index mapping
def placeholder(sbom_data): return -2
def placeholder_dual(sbom_data, other): return -2

def main():
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("Usage: python3 test_cdx_sboms.py <path_to_sbom.json> <test case number [0,5]> <type of test [0,1]>")
        return 0

    sbom_path = sys.argv[1]
    try:
        with open(sbom_path, 'r', encoding='utf-8') as f:
            sbom = json.load(f)
    except Exception as e:
        print("Error loading SBOM:", e)
        return 1

    tests = [
        [placeholder, check_minimum_elements],      # 0
        [placeholder, check_max_dependency_depth],  # 1
        [placeholder, check_methodologies_result],  # 2
        [placeholder, check_interoperability],      # 3
        [placeholder, check_reproducibility],       # 4
        [test_purl, placeholder]                    # 5
    ]

    testNo = int(sys.argv[2])
    typeNo = int(sys.argv[3])
    testToRun = tests[testNo][typeNo]
    
    if testNo == 2 and typeNo == 1:
        if len(sys.argv) != 5:
            print("Usage: python3 test_cdx_sboms.py <path_to_sbom> 2 1 <path_to_dynamic_sbom>")
            return 1
        try:
            with open(sys.argv[4], 'r', encoding='utf-8') as f:
                sbom_dynamic = json.load(f)
        except Exception:
            return 1
        returnVal = testToRun(sbom, sbom_dynamic)
    else:
        returnVal = testToRun(sbom)
        
    print("Returns: ", returnVal)
    return returnVal

if __name__ == '__main__':
    main()

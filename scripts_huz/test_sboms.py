import sys
import util
import json

def test_lite_profile(sbom_data): # Test [0][0]
    profiles = util.extract_profiles(sbom_data)
    if 'Lite' in profiles or 'lite' in profiles:
        return 1
    else:
        return 0

def check_minimum_elements(sbom_data): # Test [0][1]
    minElementsFound = 0
    TOTALMINELEMENTS = 11

    spdxDocuments = util.find_class(sbom_data, "SpdxDocument")
    
    if len(spdxDocuments) != 1:
        return -1
    
    spdxDocument = spdxDocuments[0]

    createdBy = util.find_nested_object(sbom_data, 'SpdxDocument', 'creationInfo/createdBy')

    if createdBy is not None:
        print("SBOM author found")
        minElementsFound += 1 # SBOM author
    else:
        print("SBOM author not found")

    packages = util.find_class(sbom_data, 'software_Package')

    flag = True
    for package in packages:
        if package.get('suppliedBy') is None:
            flag = False
            break
    if flag == True:
        minElementsFound += 1 # Software producer
        print("Software producer found")
    else:
        print("Software producer not found")

    flag = True
    for package in packages:
        if package.get('name') is None:
            flag = False
            break
    if flag == True:
        minElementsFound += 1 # Component name
        print("Component name found")
    else:
        print("Component name not found")

    flag = True
    creationInfos = util.find_class(sbom_data, 'CreationInfo')
    for creationInfo in creationInfos:
        if creationInfo.get('specVersion') is None:
            flag = False
            break
    if flag == True:
        minElementsFound += 1 # Component version
        print("Component version found")
    else:
        print("Component version not found")

    flag = True
    for package in packages:
        if package.get('spdxId') is None:
            flag = False
            break
    if flag == True:
        minElementsFound += 1 # Software identifiers
        print("Software identifiers found")
    else:
        print("Software identifiers not found")

    flag = False
    for package in packages:
        if package.get('verifiedUsing') is not None:
            flag = True
            break
    if spdxDocument.get('verifiedUsing') is not None:
        flag = True
    if flag == True:
        minElementsFound += 1 # Component hash
        print("Component hash found")
    else:
        print("Component hash not found")

    flag1 = False
    flag2 = False
    relationships = util.find_class(sbom_data, 'Relationship')
    for relationship in relationships:
        if relationship.get('relationshipType') == 'hasConcludedLicense':
            flag1 = True
        elif relationship.get('relationshipType') == 'hasDeclaredLicense':
            flag2= True
    if flag1 == True and flag2 == True:
        minElementsFound += 1 # License
        print("License found")
    else:
        print("License not found")

    flag = False
    for relationship in relationships:
        if relationship.get('relationshipType') == 'dependsOn' or relationship.get('relationshipType') == 'DEPENDS_ON':
            flag = True # Dependency relationship
            break
    if flag == True:
        minElementsFound += 1
        print("Dependency relationship found")
    else:
        print("Dependency relationship not found")

    createdUsing = util.find_nested_object(sbom_data, 'SpdxDocument', 'creationInfo/createdUsing')
    if createdUsing is not None:
        minElementsFound += 1 # Tool name
        print("Tool name found")
    else:
        print("Tool name not found")

    created = util.find_nested_object(sbom_data, 'SpdxDocument', 'creationInfo/created')
    if created is not None:
        minElementsFound += 1 # Timestamp
        print("Timestamp found")
    else:
        print("Timestamp not found")

    flag = False
    sboms = util.find_class(sbom_data, 'software_Sbom')
    for sbom in sboms:
        if sbom.get('sbomType') is not None:
            flag = True # Generation context
            break
    if flag == True:
        minElementsFound += 1
        print("Generation context found")
    else:
        print("Generation context not found")

    return minElementsFound/ TOTALMINELEMENTS


def test_relationship_types(sbom_data): # Test [1][0]
    relationships = {}
    rels = util.find_class(sbom_data, 'Relationship')

    for rel in rels:
        key = rel.get('relationshipType')

        if key is not None:
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
    rels = util.find_class(sbom_data, 'Relationship')
    for rel in rels:
        if rel.get('relationshipType') == 'DEPENDS_ON' or rel.get('relationshipType') == 'dependsOn' or rel.get('relationshipType') == 'contains':
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

def check_methodologies_result(sbom_data, other_sbom_data): # Test [2][1]
    packages_1 = util.find_class(sbom_data, 'software_Package')
    packages_2 = util.find_class(other_sbom_data, 'software_Package')

    # using the jaccard similarity

    names_1 = set()
    for pkg1 in packages_1:
        nm = pkg1.get('name')
        if nm is not None:
            names_1.add(nm)

    names_2 = set()
    for pkg2 in packages_2:
        nm = pkg2.get('name')
        if nm is not None:
            names_2.add(nm)

    intersections = 0

    for name in names_1:
        if name in names_2:
            intersections += 1

    return intersections/ (len(names_1) + len(names_2) - intersections)

def test_interoperability(sbom_data): # Test [3][0]
    profiles = util.extract_profiles(sbom_data)
    if 'Extension' in profiles or 'extension' in profiles:
        return 1

    if util.contains_class(sbom_data, "extension_CdxPropertiesExtension") == True or util.contains_class(sbom_data, "extension_CdxPropertyEntry") == True:
        return 1
        
    return 0

def check_interoperability(sbom_data): # Test [3][1]
    # need access to sbom conversion tools to try converting
    return -2

def test_build_profile(sbom_data): # Test [4][0]
    profiles = util.extract_profiles(sbom_data)
    if 'Build' in profiles or 'build' in profiles:
        return 1

    if util.contains_class(sbom_data, "build_Build") == True:
        return 1

    return 0

def check_reproducibility(sbom_data): # Test [4][1]
    # [TODO] need to check how to check for reproducibility
    return -2

def test_profile_used(sbom_data): # Test [5][0]
    # Check if any profile used or not
    profiles = util.extract_profiles(sbom_data)
    if len(profiles) > 0:
        return 1
    else:
        return 0

def check_empty_fields(sbom_data): # Test [5][1]
    total_count = 0
    noassertion_count = 0

    for item in sbom_data["@graph"]:
        n_count, t_count = helper_check_empty_fields(item)
        noassertion_count += n_count
        total_count += t_count

    return noassertion_count/ total_count

def helper_check_empty_fields(data):
    noassertion_count = 0
    total_count = 0

    for _, value in data.items():
        if type(value) == str:
            if value == "NOASSERTION":
                noassertion_count += 1
            total_count += 1
        elif type(value) == list:
            for v in value:
                if type(v) == str:
                    if value == "NOASSERTION":
                        noassertion_count += 1
                    total_count += 1
                else:
                    n_count, t_count = helper_check_empty_fields(v)
                    noassertion_count += n_count
                    total_count += t_count
        else:
            n_count, t_count = helper_check_empty_fields(value)
            noassertion_count += n_count
            total_count += t_count

    return noassertion_count, total_count



def test_purl(sbom_data): # Test [6][0]
    for item in sbom_data["@graph"]:
        if item.get("software_packageUrl") != None:
            packageUrl = item.get("software_packageUrl")
            if validate_purl(packageUrl) == False:
                return 0
            
    return 1

import re
from urllib.parse import unquote
def validate_purl(purl):
    if " " in purl or not purl.startswith("pkg:"):
        return False
    
    pattern = r"^pkg:(?P<type>[A-Za-z][A-Za-z0-9.\+\-]*)/(?P<namespace>.*[A-Za-z0-9_]*/)?(?P<name>[^@?#]+)(?:@(?P<version>[^?#]+))?(?:\?(?P<qualifiers>[^#]+))?(?:#(?P<subpath>.+))?$"
    match = re.match(pattern, purl)
    if not match:
        return False
        
    components = match.groupdict()
    
    if components["qualifiers"]:
        pairs = components["qualifiers"].split('&')
        keys = set()
        for pair in pairs:
            if '=' not in pair:
                return False
            k, v = pair.split('=', 1)
            if not k or not v:
                return False
            if k[0].isdigit():
                return False
            if not re.match(r"^[A-Za-z0-9.\-_]+$", k):
                return False
            if k in keys:
                return False
            keys.add(k)
            
    if components["subpath"]:
        segments = components["subpath"].split('/')
        for seg in segments:
            seg_decoded = unquote(seg)
            if seg_decoded in ('', '.', '..'):
                return False

    return True


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
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("Usage: python3 test_sboms.py <path_to_sbom.json> <test case number [0,7]> <type of test [0,1]>")
        return 0

    sbom_path = sys.argv[1]
    try:
        with open(sbom_path, 'r', encoding='utf-8') as f:
            sbom = json.load(f)
    except Exception as e:
        print("Error loading SBOM:", e)
        return 1
    
    if len(sys.argv) == 5:
        sbom_path = sys.argv[4]
        try:
            with open(sbom_path, 'r', encoding='utf-8') as f:
                sbom_dynamic = json.load(f)
        except Exception as e:
            print("Error loading SBOM: ", e)
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
    if testNo == 2 and typeNo == 1:
        if len(sys.argv) != 5:
            print("Usage: python3 test_sboms.py <path_to_sbom.json> <test case number [0,7]> <type of test [0,1]> <path_to_dynamic_sbom.json>")
            return 1
        
        returnVal = testToRun(sbom, sbom_dynamic)
    else:
        returnVal = testToRun(sbom)
    print("Returns: ", returnVal)
    return returnVal


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
testGap.py

Tests an SPDX 3.0 SBOM (JSON-LD) against the 15 requirements that are known
to be *structurally unenforceable* by official_schema.json, but which are
still MUST/SHOULD rules in the SPDX 3.0.1 specification text.

A schema-valid SBOM can still violate every one of these rules, because the
schema only checks presence/type of individual properties -- it has no
if/then, not, contains, maxItems, or uniqueItems keywords anywhere, so it
cannot check relationships *between* fields, uniqueness, exclusions, or
producer intent.

Usage:
    python3 testGap.py <path to sbom>
"""

import sys
import json
from collections import namedtuple, defaultdict

PASS = "PASS"
FAIL = "FAIL"
INFO = "INFO"     # not automatically verifiable (intent-based / advisory)
NA = "N/A"        # no applicable elements found in this document

TestResult = namedtuple("TestResult", ["gap", "section", "title", "status", "details"])

# --------------------------------------------------------------------------
# SBOM loading & indexing helpers
# --------------------------------------------------------------------------

def load_sbom(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def walk(obj, path="$"):
    """Yield (path, obj) for every dict/list node in the document, depth-first."""
    yield path, obj
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")


def build_id_index(data):
    """Map every spdxId / @id found anywhere in the doc to its node."""
    index = {}
    for _, node in walk(data):
        if isinstance(node, dict):
            for key in ("spdxId", "@id"):
                val = node.get(key)
                if isinstance(val, str):
                    index[val] = node
    return index


def resolve(ref, id_index):
    """Resolve a property value that may be an embedded object, a string
    reference (spdxId / blank node id), or a well-known individual IRI that
    doesn't appear as its own node in the graph."""
    if isinstance(ref, dict):
        return ref
    if isinstance(ref, str):
        node = id_index.get(ref)
        if node is not None:
            return node
        return {"type": None, "spdxId": ref, "_unresolved": True}
    return {"type": None, "spdxId": None}


def node_type_str(node):
    t = node.get("type") if isinstance(node, dict) else None
    return t or ""


def is_individual(node, keyword):
    """True if a (possibly unresolved) reference denotes the well-known
    NoneElement / NoAssertionElement individual."""
    t = node_type_str(node)
    sid = node.get("spdxId") or ""
    return keyword in t or keyword in str(sid)


def find_all(data, type_names):
    """Return every node anywhere in the document whose 'type' is in type_names."""
    if isinstance(type_names, str):
        type_names = {type_names}
    found = []
    for path, node in walk(data):
        if isinstance(node, dict) and node.get("type") in type_names:
            found.append((path, node))
    return found


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


# --------------------------------------------------------------------------
# Gap tests
# --------------------------------------------------------------------------

def test_gap17(data, idx):
    """DictionaryEntry keys must be unique within the collection that holds them."""
    gap, section, title = 17, "6.1.7", "DictionaryEntry keys must be unique within their collection"
    violations = []
    for path, node in walk(data):
        if isinstance(node, list) and node and all(
            isinstance(x, dict) and x.get("type") == "DictionaryEntry" for x in node
        ):
            keys = [x.get("key") for x in node]
            seen = set()
            dupes = set()
            for k in keys:
                if k in seen:
                    dupes.add(k)
                seen.add(k)
            if dupes:
                violations.append(f"{path}: duplicate key(s) {sorted(dupes)}")
    if not any(
        isinstance(n, dict) and n.get("type") == "DictionaryEntry" for _, n in walk(data)
    ):
        return TestResult(gap, section, title, NA, "No DictionaryEntry instances found in this SBOM.")
    if violations:
        return TestResult(gap, section, title, FAIL, "; ".join(violations))
    return TestResult(gap, section, title, PASS, "All DictionaryEntry collections have unique keys.")


def test_gap20(data, idx):
    """Every ElementCollection must satisfy Core requirements regardless of profileConformance."""
    gap, section, title = 20, "6.1.9", "ElementCollections must conform to Core profile implicitly"
    collections = find_all(data, {"Bom", "Bundle", "SpdxDocument", "software_Sbom"})
    if not collections:
        return TestResult(gap, section, title, NA, "No ElementCollection instances (Bom/Bundle/SpdxDocument/Sbom) found.")
    violations = []
    for path, node in collections:
        missing = [p for p in ("spdxId", "creationInfo") if not node.get(p)]
        conformance = node.get("profileConformance", [])
        if missing:
            violations.append(
                f"{path} (type={node.get('type')}): missing Core property/ies {missing} "
                f"(profileConformance={conformance})"
            )
    if violations:
        return TestResult(gap, section, title, FAIL, "; ".join(violations))
    return TestResult(
        gap, section, title, PASS,
        f"All {len(collections)} ElementCollection(s) satisfy Core requirements, "
        f"independent of their declared profileConformance."
    )


def test_gap21(data, idx):
    """If element has >= 1 entries, rootElement must also have >= 1 entries."""
    gap, section, title = 21, "6.1.9", "element >= 1 implies rootElement >= 1"
    collections = find_all(data, {"Bom", "Bundle", "SpdxDocument", "software_Sbom"})
    if not collections:
        return TestResult(gap, section, title, NA, "No ElementCollection instances found.")
    violations = []
    for path, node in collections:
        elements = as_list(node.get("element"))
        root_elements = as_list(node.get("rootElement"))
        if len(elements) >= 1 and len(root_elements) < 1:
            violations.append(f"{path} (type={node.get('type')}): has {len(elements)} element(s) but 0 rootElement(s)")
    if violations:
        return TestResult(gap, section, title, FAIL, "; ".join(violations))
    return TestResult(gap, section, title, PASS, f"Checked {len(collections)} collection(s); rule holds.")


def test_gap22(data, idx):
    """element must never resolve to a node of type SpdxDocument."""
    gap, section, title = 22, "6.1.9", "element must not be of type SpdxDocument"
    collections = find_all(data, {"Bom", "Bundle", "SpdxDocument", "software_Sbom"})
    if not collections:
        return TestResult(gap, section, title, NA, "No ElementCollection instances found.")
    violations = []
    for path, node in collections:
        for ref in as_list(node.get("element")):
            resolved = resolve(ref, idx)
            if resolved.get("type") == "SpdxDocument":
                violations.append(f"{path}: element references an SpdxDocument ({resolved.get('spdxId')})")
    if violations:
        return TestResult(gap, section, title, FAIL, "; ".join(violations))
    return TestResult(gap, section, title, PASS, "No 'element' entries resolve to an SpdxDocument.")


def test_gap23(data, idx):
    """rootElement must never resolve to a node of type SpdxDocument."""
    gap, section, title = 23, "6.1.9", "rootElement must not be of type SpdxDocument"
    collections = find_all(data, {"Bom", "Bundle", "SpdxDocument", "software_Sbom"})
    if not collections:
        return TestResult(gap, section, title, NA, "No ElementCollection instances found.")
    violations = []
    for path, node in collections:
        for ref in as_list(node.get("rootElement")):
            resolved = resolve(ref, idx)
            if resolved.get("type") == "SpdxDocument":
                violations.append(f"{path}: rootElement references an SpdxDocument ({resolved.get('spdxId')})")
    if violations:
        return TestResult(gap, section, title, FAIL, "; ".join(violations))
    return TestResult(gap, section, title, PASS, "No 'rootElement' entries resolve to an SpdxDocument.")


def test_gap39(data, idx):
    """beginIntegerRange must be <= endIntegerRange."""
    gap, section, title = 39, "6.1.21", "PositiveIntegerRange: begin <= end"
    ranges = find_all(data, "PositiveIntegerRange")
    if not ranges:
        return TestResult(gap, section, title, NA, "No PositiveIntegerRange instances found.")
    violations = []
    for path, node in ranges:
        begin, end = node.get("beginIntegerRange"), node.get("endIntegerRange")
        if isinstance(begin, (int, float)) and isinstance(end, (int, float)) and begin > end:
            violations.append(f"{path}: beginIntegerRange={begin} > endIntegerRange={end}")
    if violations:
        return TestResult(gap, section, title, FAIL, "; ".join(violations))
    return TestResult(gap, section, title, PASS, f"Checked {len(ranges)} PositiveIntegerRange(s); all valid.")


def _relationship_to_analysis(data, idx):
    rels = find_all(data, {"Relationship", "LifecycleScopedRelationship"})
    results = []
    for path, node in rels:
        to_refs = as_list(node.get("to"))
        resolved = [resolve(r, idx) for r in to_refs]
        none_flags = [is_individual(r, "NoneElement") for r in resolved]
        assertion_flags = [is_individual(r, "NoAssertionElement") for r in resolved]
        results.append((path, node, to_refs, none_flags, assertion_flags))
    return rels, results


def test_gap45_46(data, idx):
    """NoneElement, when used in 'to', must be the *only* entry present."""
    gap, section = "45/46", "6.1.22"
    title = "'to' containing NoneElement must contain no other elements"
    rels, results = _relationship_to_analysis(data, idx)
    if not rels:
        return TestResult(gap, section, title, NA, "No Relationship / LifecycleScopedRelationship instances found.")
    violations = []
    checked = 0
    for path, node, to_refs, none_flags, _ in results:
        if any(none_flags):
            checked += 1
            if len(to_refs) != 1:
                violations.append(
                    f"{path}: 'to' contains NoneElement alongside {len(to_refs) - 1} other element(s)"
                )
    if checked == 0:
        return TestResult(gap, section, title, NA, "No relationship in this SBOM uses NoneElement in 'to'.")
    if violations:
        return TestResult(gap, section, title, FAIL, "; ".join(violations))
    return TestResult(gap, section, title, PASS, f"Checked {checked} NoneElement usage(s); all exclusive.")


def test_gap47(data, idx):
    """NoAssertionElement usage in 'to' -- advisory, flagged for review."""
    gap, section, title = 47, "6.1.22", "'to' should contain NoAssertionElement to assert 'no assertion made'"
    rels, results = _relationship_to_analysis(data, idx)
    if not rels:
        return TestResult(gap, section, title, NA, "No Relationship / LifecycleScopedRelationship instances found.")
    flagged = []
    for path, node, to_refs, _, assertion_flags in results:
        if any(assertion_flags):
            flagged.append(f"{path}: 'to' has {len(to_refs)} entrie(s), includes NoAssertionElement")
    if not flagged:
        return TestResult(gap, section, title, NA, "No relationship in this SBOM uses NoAssertionElement in 'to'.")
    return TestResult(
        gap, section, title, INFO,
        f"{len(flagged)} relationship(s) use NoAssertionElement in 'to' -- the spec text does not give this "
        f"the same exclusivity rule as NoneElement, so this is informational, not a failure: " + "; ".join(flagged)
    )


def _count_individual_usage(data, keyword):
    count = 0
    locations = []
    for path, node in walk(data):
        if isinstance(node, dict) and is_individual(node, keyword):
            count += 1
            locations.append(path)
        elif isinstance(node, str) and keyword in node:
            count += 1
            locations.append(path)
    return count, locations


def test_gap52_54(data, idx):
    """NoAssertionElement usage guidance -- requires producer intent, not automatically checkable."""
    gap, section = "52-54", "6.4.1"
    title = "NoAssertionElement usage matches one of 3 documented intents"
    count, locations = _count_individual_usage(data, "NoAssertionElement")
    if count == 0:
        return TestResult(gap, section, title, NA, "NoAssertionElement is not used anywhere in this SBOM.")
    return TestResult(
        gap, section, title, INFO,
        f"NoAssertionElement appears {count} time(s) at: {locations[:10]}"
        f"{' ...' if len(locations) > 10 else ''}. Whether each usage reflects 'attempted but "
        f"undeterminable', 'not attempted', or 'intentionally withheld' is a question of producer "
        f"intent that cannot be derived from the document alone -- flagged for manual review."
    )


def test_gap55(data, idx):
    """NoneElement usage guidance -- requires producer intent, not automatically checkable."""
    gap, section, title = 55, "6.4.2", "NoneElement used only to assert 'no elements exist'"
    count, locations = _count_individual_usage(data, "NoneElement")
    if count == 0:
        return TestResult(gap, section, title, NA, "NoneElement is not used anywhere in this SBOM.")
    return TestResult(
        gap, section, title, INFO,
        f"NoneElement appears {count} time(s) at: {locations[:10]}"
        f"{' ...' if len(locations) > 10 else ''}. Confirming this reflects a deliberate 'nothing "
        f"exists here' assertion (rather than an omission) requires producer intent -- flagged for manual review."
    )


def test_gap56(data, idx):
    """/Core/Element/name minCount 1 (Software profile 7.1.2 -- File)."""
    gap, section, title = 56, "7.1.2", "software_File.name must be present"
    files = find_all(data, "software_File")
    if not files:
        return TestResult(gap, section, title, NA, "No software_File instances found.")
    violations = [path for path, node in files if not node.get("name")]
    if violations:
        return TestResult(gap, section, title, FAIL, f"Missing 'name' on: {violations}")
    return TestResult(gap, section, title, PASS, f"All {len(files)} software_File instance(s) have a name.")


def test_gap59(data, idx):
    """/Core/Element/name minCount 1 (Software profile 7.1.3 -- Package)."""
    gap, section, title = 59, "7.1.3", "software_Package.name must be present"
    packages = find_all(data, "software_Package")
    if not packages:
        return TestResult(gap, section, title, NA, "No software_Package instances found.")
    violations = [path for path, node in packages if not node.get("name")]
    if violations:
        return TestResult(gap, section, title, FAIL, f"Missing 'name' on: {violations}")
    return TestResult(gap, section, title, PASS, f"All {len(packages)} software_Package instance(s) have a name.")


ALL_TESTS = [
    test_gap17,
    test_gap20,
    test_gap21,
    test_gap22,
    test_gap23,
    test_gap39,
    test_gap45_46,
    test_gap47,
    test_gap52_54,
    test_gap55,
    test_gap56,
    test_gap59,
]


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

STATUS_LABEL = {
    PASS: "\033[92mPASS\033[0m",
    FAIL: "\033[91mFAIL\033[0m",
    INFO: "\033[93mINFO\033[0m",
    NA: "\033[90mN/A \033[0m",
}


def print_report(results, sbom_path):
    line = "=" * 78
    print(line)
    print(f" SPDX Schema-Gap Test Report")
    print(f" Target SBOM : {sbom_path}")
    print(f" Total tests : {len(results)}")
    print(line)

    for r in results:
        print(f"\n[Gap #{r.gap}] Section {r.section} -- {r.title}")
        print(f"  Result : {STATUS_LABEL.get(r.status, r.status)}")
        print(f"  Detail : {r.details}")

    counts = defaultdict(int)
    for r in results:
        counts[r.status] += 1

    print("\n" + line)
    print(" SUMMARY")
    print(line)
    print(f"  PASS : {counts[PASS]}")
    print(f"  FAIL : {counts[FAIL]}")
    print(f"  INFO (manual review required) : {counts[INFO]}")
    print(f"  N/A  (no applicable elements)  : {counts[NA]}")
    print(line)

    if counts[FAIL] > 0:
        print(f"\n RESULT: {counts[FAIL]} gap-rule violation(s) found. This SBOM is schema-valid but "
              f"violates spec rules the schema cannot check.")
    else:
        print(f"\n RESULT: No structural violations of the 15 gap rules were detected in this SBOM.")
        if counts[INFO] > 0:
            print(f" NOTE: {counts[INFO]} item(s) require manual/producer-intent review "
                  f"(see INFO entries above) -- these can never be fully automated.")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 testGap.py <path to sbom>")
        sys.exit(1)

    sbom_path = sys.argv[1]
    try:
        data = load_sbom(sbom_path)
    except FileNotFoundError:
        print(f"Error: file not found: {sbom_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: {sbom_path} is not valid JSON ({e}).")
        sys.exit(1)

    idx = build_id_index(data)

    results = []
    for test_fn in ALL_TESTS:
        try:
            results.append(test_fn(data, idx))
        except Exception as e:
            results.append(
                TestResult(getattr(test_fn, "__name__", "?"), "?", test_fn.__doc__ or "", FAIL, f"Test crashed: {e}")
            )

    print_report(results, sbom_path)


if __name__ == "__main__":
    main()

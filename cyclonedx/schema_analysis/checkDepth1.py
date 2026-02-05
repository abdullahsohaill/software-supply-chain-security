#!/usr/bin/env python3
import json
import sys
import os
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------
# Basic helpers
# ---------------------------------------------------

def load_schema(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_defs(doc: Dict[str, Any]) -> Dict[str, Any]:
    return doc.get("$defs", doc.get("definitions", {})) or {}

def _json_pointer(doc: Any, pointer: str) -> Any:
    if not pointer.startswith("#"):
        raise ValueError("Only local refs supported")
    parts = pointer[2:].split("/") if pointer.startswith("#/") else []
    cur = doc
    for p in parts:
        p = p.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            raise KeyError(f"Pointer not found: {pointer}")
    return cur

def resolve_ref(doc: Dict[str, Any], node: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(node, dict):
        return node
    ref = node.get("$ref")
    if not ref:
        return node
    if ref.startswith("#"):
        target = _json_pointer(doc, ref)
    else:
        return node  # skip remote refs
    merged = dict(target)
    for k, v in node.items():
        if k != "$ref":
            merged[k] = v
    return merged

def resolve_one_level(doc: Dict[str, Any], node: Dict[str, Any]) -> Dict[str, Any]:
    node1 = resolve_ref(doc, node)
    for combiner in ("oneOf", "anyOf", "allOf"):
        if combiner in node1 and isinstance(node1[combiner], list) and node1[combiner]:
            candidate = resolve_ref(doc, node1[combiner][0])
            node1 = {**candidate, **{k: v for k, v in node1.items() if k not in ("$ref", combiner)}}
            break
    return node1

def infer_type_string(doc: Dict[str, Any], schema_node: Any) -> str:
    if not isinstance(schema_node, dict):
        return type(schema_node).__name__
    node = resolve_one_level(doc, schema_node)
    t = node.get("type")
    if isinstance(t, list):
        t = " | ".join(sorted(map(str, t)))
    if t == "array" and "items" in node:
        inner = infer_type_string(doc, node["items"])
        return f"array<{inner}>"
    if t:
        return str(t)
    if "enum" in node:
        return f"enum<{len(node['enum'])} values>"
    if "const" in node:
        return "const"
    for combiner in ("oneOf", "anyOf", "allOf"):
        if combiner in node and isinstance(node[combiner], list) and node[combiner]:
            parts = [infer_type_string(doc, it) for it in node[combiner]]
            joiner = " | " if combiner != "allOf" else " & "
            return f"{combiner}({joiner.join(parts)})"
    if "$ref" in schema_node:
        return f"ref({schema_node['$ref']})"
    if "properties" in node or "required" in node:
        return "object"
    return "unknown"

def collect_prop_names_depth1(doc: Dict[str, Any], def_schema: Dict[str, Any]) -> List[str]:
    resolved = resolve_one_level(doc, def_schema)
    props = resolved.get("properties", {})
    if not isinstance(props, dict):
        return []
    return list(props.keys())

def property_type_in_schema1(doc1: Dict[str, Any], def_schema: Dict[str, Any], prop_name: str) -> str:
    resolved = resolve_one_level(doc1, def_schema)
    props = resolved.get("properties", {})
    node = props.get(prop_name, {})
    return infer_type_string(doc1, node)

# ---------------------------------------------------
# Recursive property search in schema2
# ---------------------------------------------------

def find_property_schema_in_node(doc2: Dict[str, Any], node: Any, prop_name: str) -> Optional[Dict[str, Any]]:
    if isinstance(node, dict):
        node_res = resolve_one_level(doc2, node)
        if "properties" in node_res and isinstance(node_res["properties"], dict):
            if prop_name in node_res["properties"]:
                return node_res["properties"][prop_name]
        for key in ("properties", "patternProperties", "additionalProperties", "items",
                    "oneOf", "anyOf", "allOf", "prefixItems", "then", "else", "if", "not"):
            if key in node_res:
                val = node_res[key]
                if isinstance(val, dict):
                    for v in val.values():
                        found = find_property_schema_in_node(doc2, v, prop_name)
                        if found is not None:
                            return found
                elif isinstance(val, list):
                    for v in val:
                        found = find_property_schema_in_node(doc2, v, prop_name)
                        if found is not None:
                            return found
    elif isinstance(node, list):
        for v in node:
            found = find_property_schema_in_node(doc2, v, prop_name)
            if found is not None:
                return found
    return None

def find_property_type_in_schema2(doc2: Dict[str, Any], defs2: Dict[str, Any], prop_name: str) -> Optional[str]:
    for header_name, header_schema in defs2.items():
        found = find_property_schema_in_node(doc2, header_schema, prop_name)
        if found is not None:
            return infer_type_string(doc2, found)
    return None

# ---------------------------------------------------
# Iterate over ALL definitions
# ---------------------------------------------------

def compare_all_headers(schema1_path: str, schema2_path: str, out_path: str = "differencesDepth1.txt") -> None:
    doc1 = load_schema(schema1_path)
    doc2 = load_schema(schema2_path)
    defs1 = get_defs(doc1)
    defs2 = get_defs(doc2)

    if not defs1:
        raise SystemExit("No $defs or definitions found in schema1")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"=== Property Type Comparison ===\n")
        f.write(f"schema1: {os.path.basename(schema1_path)}\n")
        f.write(f"schema2: {os.path.basename(schema2_path)}\n\n")

        for header_name, header_schema in defs1.items():
            prop_names = collect_prop_names_depth1(doc1, header_schema)
            if not prop_names:
                continue

            rows: List[Tuple[str, str, str]] = []
            for prop in prop_names:
                t1 = property_type_in_schema1(doc1, header_schema, prop)
                t2 = find_property_type_in_schema2(doc2, defs2, prop)
                rows.append((prop, t1, t2 if t2 is not None else "NOT FOUND"))

            f.write(f"--- Header: {header_name} ---\n")
            colw = {
                "prop": max(len("Property"), *(len(p) for p, _, _ in rows)),
                "s1":   max(len("Type in schema1"), *(len(s1) for _, s1, _ in rows)),
                "s2":   max(len("Type in schema2"), *(len(s2) for _, _, s2 in rows)),
            }
            header_line = f"{'Property'.ljust(colw['prop'])} | {'Type in schema1'.ljust(colw['s1'])} | {'Type in schema2'.ljust(colw['s2'])}\n"
            f.write(header_line)
            f.write("-" * (len(header_line) - 1) + "\n")
            for p, s1, s2 in rows:
                f.write(f"{p.ljust(colw['prop'])} | {s1.ljust(colw['s1'])} | {s2.ljust(colw['s2'])}\n")
            f.write("\n")

    print(f"[✔] Compared {len(defs1)} headers; results saved to {out_path}")

# ---------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 compare_all_schema_props.py <schema1>.json <schema2>.json")
        sys.exit(1)

    schema1_path = sys.argv[1]
    schema2_path = sys.argv[2]

    if not os.path.exists(schema1_path):
        print(f"Error: File not found: {schema1_path}")
        sys.exit(1)
    if not os.path.exists(schema2_path):
        print(f"Error: File not found: {schema2_path}")
        sys.exit(1)

    compare_all_headers(schema1_path, schema2_path, out_path="differencesDepth1.txt")

if __name__ == "__main__":
    main()

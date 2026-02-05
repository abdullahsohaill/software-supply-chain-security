import json
import csv
import sys

# Increase recursion limit just in case CycloneDX is very deep
sys.setrecursionlimit(2000)

SCHEMA_FILE = 'cyclonedx_schema.json'
OUTPUT_FILE = "cyclonedx_depth.csv"

### 1. Loading schema
with open(SCHEMA_FILE, 'r') as f:
    schema = json.load(f)

classes = list(schema["definitions"].keys())
print(f"{len(classes)} classes loaded.\n")

### 2. Building Graph
ancestor_graph = {}
all_nodes = set(schema["definitions"].keys())

for parent_name, definition in schema["definitions"].items():
    def find_refs_in_definition(obj):
        refs = set()
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "$ref" and isinstance(value, str):
                    child_name = value.split('/')[-1]
                    if child_name in all_nodes:
                        refs.add(child_name)
                else:
                    refs.update(find_refs_in_definition(value))
        elif isinstance(obj, list):
            for item in obj:
                refs.update(find_refs_in_definition(item))
        return refs

    children = find_refs_in_definition(definition)
    for child in children:
        if child not in ancestor_graph:
            ancestor_graph[child] = set()
        ancestor_graph[child].add(parent_name)

final_results = {}

### 3. Calculating Depth
for target_class in classes:
    all_paths = []

    def find_paths_recursive(current_node, current_path):
        # Stop cycles
        if current_node in current_path:
            all_paths.append(current_path) 
            return

        new_path = [current_node] + current_path

        # If this node has no parents, it is a root. End of path.
        if current_node not in ancestor_graph:
            all_paths.append(new_path)
            return

        for parent in ancestor_graph[current_node]:
            find_paths_recursive(parent, new_path)

    find_paths_recursive(target_class, [])

    if not all_paths:
        longest_path = [target_class]
    else:
        longest_path = max(all_paths, key=len)

    final_results[target_class] = {
        'path': longest_path,
        'length': len(longest_path)
    }

### 4. Saving results
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['class_name', 'max_depth', 'path'])

    for class_name, result in final_results.items():
        path_string = " -> ".join(result['path'])
        writer.writerow([class_name, result['length'], path_string])

print(f"Depth analysis saved to {OUTPUT_FILE}")
import json
import csv

SCHEMA_FILE = 'cyclonedx_schema.json'
OUTPUT_FILE = "cyclonedx_ancestors.csv"

### 1. Loading schema
with open(SCHEMA_FILE, 'r') as f:
    schema = json.load(f)

# Auto-extract classes from the schema definitions
if "definitions" not in schema:
    raise ValueError("Schema file does not contain a 'definitions' key.")
    
classes = list(schema["definitions"].keys())
print(f"{len(classes)} classes loaded from schema definitions.\n")

### 2. Finding all conditional classes
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
for target_class in classes:
    # Set to store all unique ancestors found during traversal.
    all_ancestors = set()
    # Set to keep track of visited nodes to prevent infinite loops
    visited_nodes = set()

    def find_all_ancestors_recursive(current_node):
        if current_node in visited_nodes:
            return
        visited_nodes.add(current_node)

        if current_node in ancestor_graph:
            direct_parents = ancestor_graph[current_node]
            all_ancestors.update(direct_parents)
            for parent in direct_parents:
                find_all_ancestors_recursive(parent)

    find_all_ancestors_recursive(target_class)

    final_results[target_class] = {
        'ancestors': all_ancestors,
        'count': len(all_ancestors)
    }

### 3. Saving results
with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['class_name', 'ancestor_count', 'ancestors'])

    for class_name, result in final_results.items():
        count = result['count']
        ancestors_set = result['ancestors']
        ancestors_string = ", ".join(sorted(list(ancestors_set)))
        writer.writerow([class_name, count, ancestors_string])

print(f"Ancestor analysis results have been saved to {OUTPUT_FILE}")
import json
import csv

SCHEMA_FILE = 'cyclonedx_schema.json'
OUTPUT_FILE = "cyclonedx_breadth.csv"

### 1. Loading schema
with open(SCHEMA_FILE, 'r') as f:
    schema = json.load(f)

# Auto-extract classes
classes = set(schema["definitions"].keys())
print(f"{len(classes)} classes loaded.\n")

### 2. Finding parents (Breadth)
class_parents = {class_name: set() for class_name in classes}

for parent_name, definition in schema["definitions"].items():
    def search_for_ref(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "$ref" and isinstance(value, str):
                    referenced_class = value.split('/')[-1]
                    if referenced_class in classes:
                        class_parents[referenced_class].add(parent_name)
                else:
                    search_for_ref(value)
        elif isinstance(obj, list):
            for item in obj:
                search_for_ref(item)

    search_for_ref(definition)

### 3. Printing and Saving results
with open(OUTPUT_FILE, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["class_name", "breadth", "parents"])
    for c, p in class_parents.items():
        # print(f"Breadth for class '{c}': {len(p)}")
        w.writerow([c, len(p), "-".join(sorted(list(p)))])

print(f"Saved breadth info to {OUTPUT_FILE}")
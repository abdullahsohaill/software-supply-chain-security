import os
import json
import pandas as pd
import requests
from jsonschema import validate, ValidationError



INPUT_DIR = "tool_experiment"
RESULTS_FILE = "cyclonedx_1.6_rigorous_results.csv"
SCHEMA_URL = "https://cyclonedx.org/schema/bom-1.6.schema.json"


print("[*] Fetching Official CycloneDX 1.6 Schema...")
try:
    schema_response = requests.get(SCHEMA_URL)
    schema_response.raise_for_status()
    CDX_SCHEMA = schema_response.json()
    print("[+] Schema fetched successfully.")
except Exception as e:
    print(f"[-] Failed to download schema: {e}")
    exit(1)

def analyze_sbom_rigorous(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return {
            "File": os.path.basename(file_path), 
            "Status": "Invalid JSON",
            "CISA_Supplier": False, "CISA_Timestamp": False, "CISA_Tool_Author": False,
            "Feature_Formulation": False, "Feature_ML_BOM": False,
            "Graph_Present": False, "Graph_Integrity": "N/A"
        }

    
    
    try:
        validate(instance=data, schema=CDX_SCHEMA)
        is_schema_valid = True
        validation_error = None
    except ValidationError as e:
        is_schema_valid = False
        
        validation_error = e.message.split("\n")[0][:100] 

    
    metadata = data.get("metadata", {})
    component = metadata.get("component", {})
    
    
    has_supplier = False
    
    if isinstance(component, dict) and "supplier" in component and isinstance(component["supplier"], dict):
        if "name" in component["supplier"] and component["supplier"]["name"]:
            has_supplier = True
    
    elif "supplier" in metadata and isinstance(metadata["supplier"], dict):
        if "name" in metadata["supplier"] and metadata["supplier"]["name"]:
            has_supplier = True

    has_timestamp = "timestamp" in metadata and bool(metadata["timestamp"])
    
    has_tool_author = False
    if "authors" in metadata and isinstance(metadata["authors"], list) and len(metadata["authors"]) > 0:
        has_tool_author = True
    elif "tools" in metadata:
        has_tool_author = True

    
    has_formulation = "formulation" in data and isinstance(data["formulation"], list) and len(data["formulation"]) > 0
    has_modelcard = "modelCard" in data
    
    if not has_modelcard:
        for c in data.get("components", []):
            if isinstance(c, dict) and c.get("type") == "machine-learning-model":
                has_modelcard = True
                break
    
    
    dependencies = data.get("dependencies", [])
    has_dep_graph = isinstance(dependencies, list) and len(dependencies) > 0
    
    graph_integrity = "N/A"
    
    if has_dep_graph:
        defined_refs = set()
        
        if isinstance(component, dict) and "bom-ref" in component:
            defined_refs.add(component["bom-ref"])
            
        
        if isinstance(data.get("components"), list):
            for c in data["components"]:
                if isinstance(c, dict) and "bom-ref" in c:
                    defined_refs.add(c["bom-ref"])
            
        dangling_count = 0
        malformed_count = 0
        
        for d in dependencies:
            if not isinstance(d, dict):
                malformed_count += 1
                continue
                
            ref = d.get("ref")
            if ref and ref not in defined_refs:
                dangling_count += 1
        
        if malformed_count > 0:
            graph_integrity = "Malformed (Non-Object in Array)"
        elif dangling_count == 0:
            graph_integrity = "Valid"
        else:
            graph_integrity = f"Failed ({dangling_count} dangling)"

    return {
        "File": os.path.basename(file_path),
        "Status": "Valid SBOM" if is_schema_valid else "Schema Violation",
        "Schema_Error": validation_error,
        "CISA_Supplier": has_supplier,
        "CISA_Timestamp": has_timestamp,
        "CISA_Tool_Author": has_tool_author,
        "Feature_Formulation": has_formulation,
        "Feature_ML_BOM": has_modelcard,
        "Graph_Present": has_dep_graph,
        "Graph_Integrity": graph_integrity
    }



















    


    


    












    







    






    




    









            





        


















def main():
    if not os.path.exists(INPUT_DIR):
        print(f"Directory {INPUT_DIR} not found.")
        return

    results = []
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".json")]
    
    print(f"[*] Rigorously Analyzing {len(files)} files against Official Schema...")

    for i, filename in enumerate(files):
        if i % 100 == 0: print(f"Processing {i}...")
        res = analyze_sbom_rigorous(os.path.join(INPUT_DIR, filename))
        results.append(res)

    df = pd.DataFrame(results)
    df.to_csv(RESULTS_FILE, index=False)
    
    print("\n=== CCS-GRADE ANALYSIS RESULTS ===")
    print(f"Total Files: {len(df)}")
    
    valid_sboms = df[df['Status'] == "Valid SBOM"]
    print(f"Schema Valid: {len(valid_sboms)} ({len(valid_sboms)/len(df)*100:.1f}%)")
    
    if len(valid_sboms) > 0:
        print("\n--- CISA Compliance (On Valid SBOMs Only) ---")
        print(f"Has Supplier: {valid_sboms['CISA_Supplier'].sum()} ({valid_sboms['CISA_Supplier'].mean()*100:.1f}%)")
        print(f"Has Timestamp: {valid_sboms['CISA_Timestamp'].sum()} ({valid_sboms['CISA_Timestamp'].mean()*100:.1f}%)")
        
        print("\n--- Advanced Feature Usage (Specification Bloat) ---")
        print(f"Uses Formulation: {valid_sboms['Feature_Formulation'].sum()}")
        print(f"Uses ML-BOM: {valid_sboms['Feature_ML_BOM'].sum()}")
        
        print("\n--- Graph Integrity ---")
        print(valid_sboms['Graph_Integrity'].value_counts())

if __name__ == "__main__":
    main()
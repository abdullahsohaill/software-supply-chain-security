import subprocess
import csv
import os

TOOLS = ["syft", "trivy", "cdxgen"]
SBOM_RANGE = range(1, 19)
TEST_RANGE = range(0, 6) # Tests 0 to 5 mapped to methodology cases

output_file = "tests_result_cdx.csv"

# Map to Huzaifa's array format: [0][1], [1][1], [2][1], [3][1], [4][1], [5][0]
TEST_MAPPINGS = [
    (0, 1), # Minimum elements
    (1, 1), # Max dependency depth
    (2, 1), # Methodologies (requires second SBOM, using syft as baseline)
    (3, 1), # Interoperability
    (4, 1), # Reproducibility
    (5, 0)  # PURLs
]

header = [""] + [f"Test {i+1}" for i in TEST_RANGE]
rows = []

for tool in TOOLS:
    print(f"Running tests for: {tool}")

    for sbom_num in SBOM_RANGE:
        row_name = f"{tool}_{sbom_num}"
        row = [row_name]
        
        sbom_path = f"sboms_cdx/{sbom_num}_{tool}.json"
        if not os.path.exists(sbom_path):
            row.extend(["-3"] * len(TEST_MAPPINGS))
            rows.append(row)
            continue

        for test_idx, (t_no, t_type) in enumerate(TEST_MAPPINGS):
            args = ["python3", "test_cdx_sboms.py", sbom_path, str(t_no), str(t_type)]
            
            # Test 2 (Methodologies) needs a second SBOM to compare
            # Using Syft output as the "other" baseline for Trivy and cdxgen
            if t_no == 2 and t_type == 1:
                baseline_path = f"sboms_cdx/{sbom_num}_syft.json"
                if os.path.exists(baseline_path):
                    args.append(baseline_path)
                else:
                    args.append(sbom_path) # Fallback to itself if baseline missing

            try:
                result = subprocess.run(args, capture_output=True, text=True)
                value = "-3"
                for line in result.stdout.splitlines():
                    if line.startswith("Returns: "):
                        value = line.replace("Returns: ", "").strip()
            except Exception:
                value = "-3"

            row.append(value)

        rows.append(row)

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"[+] Done. Results saved in {output_file}")

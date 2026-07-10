import subprocess
import csv

TOOLS = ["microsoft", "spdx_generator", "trivy", "syft"]
SBOM_RANGE = range(1, 19)
TEST_RANGE = range(1, 7)

output_file = "tests_result.csv"

header = [""] + [str(i) for i in TEST_RANGE]
rows = []

for tool in TOOLS:
    print("Running tests for:", tool)

    for sbom_num in SBOM_RANGE:
        row_name = f"{tool}_{sbom_num}"
        row = [row_name]

        for test_case in TEST_RANGE:
            sbom_path = f"sboms/{sbom_num}_{tool}.json"

            try:
                result = subprocess.run(
                    ["python3", "test_sboms.py", sbom_path, str(test_case), str(0)],
                    capture_output=True,
                    text=True
                )

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

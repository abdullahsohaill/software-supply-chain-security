import subprocess
import csv
import os

REPOS = ["fastify", "flask", "guava", "cobra", "express"]
TOOLS = ["syft", "trivy", "cdxgen", "microsoft"]

# Output CSV for the large scale experiment
output_file = "cyclonedx/measurement/large_scale_experiment_results.csv"

# Header will be handled by the called script (3_test_sboms.py) if we run it in --dir mode
# But here we want to run specific tests or just collect all? 
# The best way is to use the --dir mode of 3_test_sboms.py on the 'sboms' folder
# So this script essentially just becomes a wrapper to call the main measurement script

def main():
    print("Running measurement on generated SBOMs...")
    
    # Use absolute paths to avoid issues with CWD
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    measurement_script = os.path.join(base_dir, "measurement", "3_test_sboms.py")
    measurement_dir = os.path.join(base_dir, "measurement")
    sbom_dir = os.path.join(base_dir, "sbom_testing", "sboms")
    output_file = os.path.join(base_dir, "sbom_testing", "sboms_test_results.csv")
    
    if not os.path.exists(sbom_dir):
        print(f"Error: SBOM directory {sbom_dir} not found.")
        return

    try:
        subprocess.run(
            ["python3", measurement_script, "--dir", sbom_dir, "--output", output_file],
            check=True,
            cwd=measurement_dir # Ensure imports in 3_test_sboms.py work
        )
        print(f"[+] Done. Results saved in {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[-] Measurement failed: {e}")

if __name__ == "__main__":
    main()

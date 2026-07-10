import subprocess
import os

os.makedirs("sboms_spdx", exist_ok=True)

for i in range(1, 19):
    subprocess.run(
        ["syft", f"packages/{i}", "-o", "spdx-json"],
        check=True,
        stdout=open(f"sboms/{i}_syft.json", "w")
    )

for i in range(1, 19):
    subprocess.run(
        ["trivy", "fs", f"packages/{i}", "--format", "spdx-json"],
        check=True,
        stdout=open(f"sboms/{i}_trivy.json", "w")
    )

for i in range(1, 19):
    try:
        subprocess.run(
            [
                "spdx-sbom-generator", 
                "-p", f"packages/{i}",
                "-f", "json",
                "-o", "sboms/"
            ],
            check=True
        )    
        os.rename("sboms/bom-pyenv.json", f"sboms/{i}_spdx_generator.json")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to generate SBOM for packages/{i}")

import shutil

for i in range(1, 19):
    package_path = f"packages/{i}"
    temp_output_dir = f"sboms/temp_{i}"
    final_output_file = f"sboms/{i}_microsoft.json"

    # 1. Create the temp directory explicitly (Fixes "Directory not found" error)
    os.makedirs(temp_output_dir, exist_ok=True)
    
    print(f"Generating Microsoft SBOM for {package_path}...")

    try:
        # 2. Run the Microsoft SBOM Tool
        subprocess.run(
            [
                "sbom-tool", "generate",
                "-b", package_path,              # Build drop path
                "-bc", package_path,             # Build component path
                "-pn", f"package-{i}",           # Package Name
                "-pv", "1.0.0",                  # Package Version
                "-ps", "Organization",           # Supplier
                "-nsb", "https://example.com",   # Namespace Base URI
                "-mi", "SPDX:3.0",               # Manifest Info (See Note below regarding 3.0)
                "-m", temp_output_dir            # Output directory
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )

        # 3. Find the generated file within the temp directory structure
        # The tool creates deep structures like: temp_1/_manifest/spdx_2.2/manifest.spdx.json
        found_file = None
        for root, dirs, files in os.walk(temp_output_dir):
            for file in files:
                if file.endswith(".json") or file.endswith(".spdx"):
                    found_file = os.path.join(root, file)
                    break
            if found_file:
                break

        # 4. Move and Rename
        if found_file and os.path.exists(found_file):
            os.rename(found_file, final_output_file)
            print(f"Success: {final_output_file}")
        else:
            print(f"Error: SBOM file was not generated in {temp_output_dir}")

    except subprocess.CalledProcessError as e:
        print(f"Failed to generate SBOM for {i}")
        print("Error output:", e.stderr.decode())

    finally:
        # 5. Cleanup temporary folder
        if os.path.exists(temp_output_dir):
            shutil.rmtree(temp_output_dir)
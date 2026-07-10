import subprocess
import os
import shutil

# Ensure sboms directory exists
os.makedirs("sboms_cdx", exist_ok=True)

# Generate with Syft
for i in range(1, 19):
    print(f"Generating Syft CDX SBOM for package {i}...")
    try:
        subprocess.run(
            ["syft", f"packages/{i}", "-o", "cyclonedx-json"],
            check=True,
            stdout=open(f"sboms_cdx/{i}_syft.json", "w"),
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print(f"Error: Failed to generate Syft SBOM for package {i}")

# Generate with Trivy
for i in range(1, 19):
    print(f"Generating Trivy CDX SBOM for package {i}...")
    try:
        subprocess.run(
            ["trivy", "fs", f"packages/{i}", "--format", "cyclonedx"],
            check=True,
            stdout=open(f"sboms_cdx/{i}_trivy.json", "w"),
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print(f"Error: Failed to generate Trivy SBOM for package {i}")

# Generate with cdxgen
for i in range(1, 19):
    print(f"Generating cdxgen CDX SBOM for package {i}...")
    try:
        subprocess.run(
            ["npx", "cdxgen", "-o", f"sboms_cdx/{i}_cdxgen.json", f"packages/{i}"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print(f"Error: Failed to generate cdxgen SBOM for package {i}")

print("CycloneDX SBOM generation complete.")

import subprocess
import os
import shutil
TARGETS = {
    "fastify": "https://github.com/fastify/fastify.git",
    "flask": "https://github.com/pallets/flask.git",
    "guava": "https://github.com/google/guava.git", # Java
    "cobra": "https://github.com/spf13/cobra.git", # Go
    "express": "https://github.com/expressjs/express.git"
}

# Use paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGES_DIR = os.path.join(SCRIPT_DIR, "packages")
SBOM_DIR = os.path.join(SCRIPT_DIR, "sboms")
TEMP_DIR = os.path.join(SCRIPT_DIR, "tmp")

os.makedirs(PACKAGES_DIR, exist_ok=True)
os.makedirs(SBOM_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Fix for Trivy permission issues
os.environ["TMPDIR"] = TEMP_DIR
os.environ["TRIVY_CACHE_DIR"] = os.path.join(TEMP_DIR, "trivy_cache")

def clone_repos():
    for name, url in TARGETS.items():
        path = os.path.join(PACKAGES_DIR, name)
        if not os.path.exists(path):
            print(f"Cloning {name}...")
            subprocess.run(["git", "clone", "--depth", "1", url, path], check=True)
        else:
            print(f"{name} already exists.")

# 2. Define Tools
def run_syft(repo_path, output_file):
    subprocess.run(
        ["syft", repo_path, "-o", "cyclonedx-json", f"--file={output_file}"],
        check=True
    )

def run_trivy(repo_path, output_file):
    subprocess.run(
        ["trivy", "fs", repo_path, "--format", "cyclonedx", "--output", output_file],
        check=True
    )

def run_cdxgen(repo_path, output_file):
    # cdxgen requires running FROM the dir usually, or specifying specific args
    # We'll try running it on the directory
    subprocess.run(
        ["cdxgen", "-o", output_file, repo_path],
        check=True
    )

def run_microsoft(repo_path, output_file):
    # Uses npx @microsoft/sbom-tool
    # Needs a temp dir because it outputs a specific folder structure
    temp_dir = os.path.join(SBOM_DIR, "temp_ms")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    try:
        subprocess.run(
            [
                "npx", "-y", "@microsoft/sbom-tool", "generate",
                "-b", repo_path, "-bc", repo_path,
                "-pn", "test-package", "-pv", "1.0.0", "-ps", "test", "-nsb", "https://test.com",
                "-m", temp_dir
            ],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
        )
        
        # Find the file
        found = False
        for root, dirs, files in os.walk(temp_dir):
            for f in files:
                if f.endswith(".json"):
                    shutil.move(os.path.join(root, f), output_file)
                    found = True
                    break
            if found: break
            
    except subprocess.CalledProcessError as e:
        print(f"Microsoft Tool failed: {e}")
        if e.stderr:
            print(f"  Error message: {e.stderr.decode('utf-8', errors='ignore')}")
        raise # Re-raise to let the main loop catch it
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

# 3. Execution Loop
def main():
    clone_repos()
    
    tools = [
        ("syft", run_syft),
        ("trivy", run_trivy),
        ("cdxgen", run_cdxgen),
        # ("microsoft", run_microsoft) # Not on npm registry, disabling for now
    ]
    
    for repo_name in TARGETS.keys():
        repo_path = os.path.join(PACKAGES_DIR, repo_name)
        print(f"\nProcessing {repo_name}...")
        
        for tool_name, tool_func in tools:
            output_file = os.path.join(SBOM_DIR, f"{repo_name}_{tool_name}.json")
            print(f"  Running {tool_name}...")
            try:
                tool_func(repo_path, output_file)
                print(f"  [SUCCESS] {output_file}")
            except Exception as e:
                print(f"  [FAILED] {tool_name}: {e}")

if __name__ == "__main__":
    main()
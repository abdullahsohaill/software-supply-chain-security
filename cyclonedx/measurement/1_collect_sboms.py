import requests
import json
import time
import os

# --- CONFIGURATION ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "") 
OUTPUT_DIR = "wild_cyclonedx_1.6_sboms"
MAX_FILES = 1000

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def search_github_sboms():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    downloaded_repos = set()
    files_downloaded = 0
    
    # --- THE STRICT QUERY ---
    # This mirrors your partner's approach.
    # It looks for files ending in .json that contain the exact string: "specVersion": "1.6"
    # We add "CycloneDX" to ensure it's not some other random file with a specVersion key.
    query = 'extension:json "specVersion": "1.6" "CycloneDX"'
    
    url = f"https://api.github.com/search/code?q={query}&per_page=100"
    
    print(f"[*] Searching for CycloneDX 1.6 specific files...")

    page = 1
    # GitHub limits code search to 1000 results (10 pages)
    while page <= 10 and files_downloaded < MAX_FILES:
        try:
            print(f"[*] Fetching page {page}...")
            response = requests.get(f"{url}&page={page}", headers=headers)
            
            if response.status_code == 403:
                print("[-] Rate limited. Sleeping 60s...")
                time.sleep(60)
                continue
            
            if response.status_code != 200:
                print(f"[-] API Error: {response.status_code}")
                break

            items = response.json().get('items', [])
            
            if not items:
                print("[!] No more results found (1.6 might be rare!).")
                break

            for item in items:
                repo_name = item['repository']['full_name']
                
                # Filter: One SBOM per repository (same as partner)
                if repo_name in downloaded_repos:
                    continue

                raw_url = item['html_url'].replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
                
                try:
                    file_content = requests.get(raw_url).text
                    json_content = json.loads(file_content)
                    
                    # DOUBLE CHECK: Ensure it is actually 1.6
                    # (GitHub search is fuzzy, so we must verify manually)
                    if json_content.get("specVersion") == "1.6":
                        
                        safe_filename = repo_name.replace("/", "_") + ".json"
                        with open(f"{OUTPUT_DIR}/{safe_filename}", "w", encoding='utf-8') as f:
                            f.write(file_content)
                        
                        downloaded_repos.add(repo_name)
                        files_downloaded += 1
                        print(f"[+] ({files_downloaded}) Found 1.6: {safe_filename}")
                except:
                    pass

                if files_downloaded >= MAX_FILES:
                    break
            
            page += 1
            time.sleep(2) 

        except Exception as e:
            print(f"[-] Error: {e}")
            break

    print(f"[*] Done. Downloaded {files_downloaded} unique CycloneDX 1.6 SBOMs.")

if __name__ == "__main__":
    search_github_sboms()
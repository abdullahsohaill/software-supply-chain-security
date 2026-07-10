import os
import subprocess

# Replace with your 20 GitHub repo links
github_links = [
    "https://github.com/boto/boto3.git",
    "https://github.com/urllib3/urllib3.git",
    "https://github.com/psf/requests.git",
    "https://github.com/certifi/python-certifi.git",
    "https://github.com/jawah/charset_normalizer.git",
    "https://github.com/kjd/idna.git",
    "https://github.com/aio-libs/aiobotocore.git",
    "https://github.com/dateutil/dateutil.git",
    "https://github.com/pypa/setuptools.git",
    "https://github.com/benjaminp/six.git",
    "https://github.com/fsspec/s3fs.git",
    "https://github.com/boto/botocore.git",
    "https://github.com/python/typing_extensions.git",
    "https://github.com/pypa/packaging.git",
    "https://github.com/boto/s3transfer.git",
    "https://github.com/numpy/numpy.git",
    "https://github.com/pypa/pip.git",
    "https://github.com/yaml/pyyaml.git"
]

base_dir = os.getcwd()

for i, link in enumerate(github_links, start=1):
    folder_name = os.path.join(base_dir, str(i))
    os.makedirs(folder_name, exist_ok=True)

    print(f"Cloning {link} into folder {folder_name}...")
    
    try:
        subprocess.run(["git", "clone", link, folder_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone {link}: {e}")

print("All repositories have been cloned.")

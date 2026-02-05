import pandas as pd

# Load CSV
df = pd.read_csv("cyclone.csv")

# === Step 1: Normalization mapping (to RFC 2119 canonical keywords) ===
normalize_map = {
    "must": "MUST",
    "must not": "MUST NOT",
    "should": "SHOULD",
    "should not": "SHOULD NOT",
    "recommended": "RECOMMENDED",
    "recommends": "RECOMMENDED",
    "required": "REQUIRED",
    "optional": "OPTIONAL",
    "encouraged": "RECOMMENDED",
    "strongly encouraged": "RECOMMENDED",
    "allowed": "MAY",
    "minimum value": "REQUIRED",
}

def normalize_keyword(val: str) -> str | None:
    if not isinstance(val, str):
        return None
    v = val.strip().lower()
    # Drop rows for "default value" or "deprecated"
    if v in ["default value", "deprecated"]:
        return None
    return normalize_map.get(v, val.upper())

# Apply normalization
df["Normative Keyword"] = df["Normative Keyword"].apply(normalize_keyword)

# Drop rows removed during normalization
df = df.dropna(subset=["Normative Keyword"])

# === Step 2: Internal mapping (reduce to 3 categories) ===
internal_map = {
    "OPTIONAL": "MAY",
    "MAY": "MAY",
    "MUST": "REQUIRED",
    "MUST NOT": "REQUIRED",
    "REQUIRED": "REQUIRED",
    "SHOULD": "RECOMMENDED",
    "SHOULD NOT": "RECOMMENDED",
    "RECOMMENDED": "RECOMMENDED",
}

def internal_mapping(val: str) -> str:
    return internal_map.get(val, "NON-STANDARD")  # fallback

df["Internal Mapping"] = df["Normative Keyword"].apply(internal_mapping)

# === Step 3: Save cleaned dataset ===
df.to_csv("cyclone_clean_internal.csv", index=False)

# === Step 4: Diagnostics ===
print("✅ Unique RFC 2119 Normative Keywords:")
print(df["Normative Keyword"].unique())

print("\n✅ Unique Internal Mapping Categories:")
print(df["Internal Mapping"].unique())

print("\nSample preview:")
print(df.head())

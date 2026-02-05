import pandas as pd

# 1. Load Data
# Assuming you have the CSV file from your extraction phase
df = pd.read_csv('cyclonedx_thematic.csv')

# 2. Define your EXACT Mapping (7 Themes)
subtheme_to_theme_map = {
    'Specification Conformance': 'Foundational BOM Structure and Identity',
    'BOM Format and Versioning': 'Foundational BOM Structure and Identity',
    'BOM Identification': 'Foundational BOM Structure and Identity',
    'Root Object Model': 'Foundational BOM Structure and Identity',
    'Serialization and Schema': 'Foundational BOM Structure and Identity',
    'Internal Referencing (bom-ref)': 'Foundational BOM Structure and Identity',

    'BOM Metadata': 'Metadata and Provenance',
    'Organizational Entity Definition': 'Metadata and Provenance',
    'Contact Information': 'Metadata and Provenance',
    'Tooling Information': 'Metadata and Provenance',
    'Timestamping': 'Metadata and Provenance',
    'Lifecycle Information': 'Metadata and Provenance',

    'Component and Service Definition': 'Core Inventory and Component Attributes',
    'Component and Service Typing': 'Core Inventory and Component Attributes',
    'Component and Service Identification': 'Core Inventory and Component Attributes',
    'Standardized External Identifiers': 'Core Inventory and Component Attributes',
    'Descriptive Metadata': 'Core Inventory and Component Attributes',
    'Component Scope': 'Core Inventory and Component Attributes',

    'Dependency Graph Representation': 'Relationships and Composition',
    'Component Assemblies (Nesting)': 'Relationships and Composition',
    'Composition and Completeness': 'Relationships and Composition',
    'External References': 'Relationships and Composition',

    'Cryptographic Hashes': 'Trust, Integrity, and Security',
    'Digital Signatures': 'Trust, Integrity, and Security',
    'Vulnerability Information (Vulnerability Object)': 'Trust, Integrity, and Security',
    'Vulnerability Impact Analysis (VEX)': 'Trust, Integrity, and Security',
    'Component Pedigree and Provenance': 'Trust, Integrity, and Security',
    'Evidence and Substantiation': 'Trust, Integrity, and Security',

    'Licensing and Copyright': 'Advanced and Specialized Data Models',
    'Formulation and Reproducible Builds': 'Advanced and Specialized Data Models',
    'Cryptographic Asset Management (CBOM)': 'Advanced and Specialized Data Models',
    'AI/ML Model Cards (ML-BOM)': 'Advanced and Specialized Data Models',
    'Data Components and Governance': 'Advanced and Specialized Data Models',
    'Attestations and Declarations': 'Advanced and Specialized Data Models',
    'Annotations': 'Advanced and Specialized Data Models',

    'Extensibility via Properties': 'Extensibility and Customization',
    'Property Taxonomies': 'Extensibility and Customization'
}

# 3. Apply Mapping
df['Theme'] = df['Subtheme'].map(subtheme_to_theme_map)

# --- CALCULATIONS FOR MANUSCRIPT ---

print("=== DATA FOR TABLE: THEMATIC DISTRIBUTION ===")
total_reqs = len(df)
theme_counts = df['Theme'].value_counts()
theme_percents = (theme_counts / total_reqs * 100).round(1)

for theme, count in theme_counts.items():
    pct = theme_percents[theme]
    print(f"\\textbf{{{theme}}} & \\textbf{{{pct}}}\\% \\\\")
    
    # Get top 2 subthemes for this theme to list in table details
    sub_counts = df[df['Theme'] == theme]['Subtheme'].value_counts().head(2)
    for sub, sub_c in sub_counts.items():
        sub_pct = round((sub_c / total_reqs) * 100, 1)
        print(f"\\hspace{{1.5em}}{sub} & {sub_pct}\\% \\\\ [4pt]")
    print("")

print("\n=== DATA FOR CONDITIONALITY ANALYSIS ===")
# Count requirements specific to ML-BOM (Model Card)
ml_bom_count = len(df[df['Subtheme'] == 'AI/ML Model Cards (ML-BOM)'])
print(f"Total ML-BOM Requirements: {ml_bom_count}")

# Count requirements specific to Formulation
formulation_count = len(df[df['Subtheme'] == 'Formulation and Reproducible Builds'])
print(f"Total Formulation Requirements: {formulation_count}")

# Check CISA Gap (Supplier)
supplier_reqs = df[df['Subtheme'] == 'Organizational Entity Definition']
# Look for "supplier" in the text to see if it is optional
supplier_mandates = supplier_reqs[supplier_reqs['Recommendation / Requirement'].str.contains('supplier', case=False, na=False)]
print(f"\nCheck Supplier Requirements:")
print(supplier_mandates[['Recommendation / Requirement', 'Normative Keyword']].head())
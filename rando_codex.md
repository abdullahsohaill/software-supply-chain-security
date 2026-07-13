
read this entire chat:"Study SBOM inconsistencies



VS Code



shorten the response please, make it actionable instead of all the narrative stuff

also can say that i havent looked into sbom generator tool code myself btu I can look into them and trace how they populate:
dependency graphs,
supplier/timestamp/authors,
scope or completeness-related fields, or wtv

also mention sbom quality tool as to what he wants and i think only tool is sbomqs

and sure please rewrite 4.2.3 subsection as well, dont use em dashes or hyphens anywhere please otherwise it looks very AI:"\section{Results}
\label{sec:results}

\subsection{Finding list of known issues in SBOM generation}
\label{subsec:systematization}

Below is a list of the problems that need to be addressed:
\begin{enumerate}
\item Failure to meet the minimum elements specified by the CISA guidelines \cite{cmuplugfest}.
\item Transitive dependencies are missed \cite{differentialanalysisyu}.
\item Tools employ different methodologies for parsing metadata \cite{differentialanalysisyu}. Additionally, there is a lack of standardised meta-data formats in and across languages further preventing a single methodology to encompass every possibility. \cite{pythonsboms, javasboms}
\item Interoperability issues where one tool produces a better SBOM for one format over another \cite{bomsaway}.
\item Lack of reproducibility in the builds on which SBOMs are created. \cite{reproduciblebuildsforne}
\item View of SBOMs as unncessary and merely a compliance checkbox. \cite{maintainersvulnmgmtwermke}
\item Inconsistencies in the naming of packages. \cite{differentialanalysisyu}
\item Inability to capture whether a libary was actually loaded onto memory or not due to the static nature of an SBOM. \cite{nodeshieldcornelissen}
\end{enumerate}

We analyse each of the specifications according to each of the problems above and address them. We focus on what aspects of the specifications try to address these issues, and which of these issues do the specifications not address.


\subsection{Reproducible thematic analysis}

\subsubsection{SPDX}

The SPDX standard prescribes the structure, content, and conformance requirements for SBOM generation. Profiles in SPDX 3.0.1 are central to this architecture; they represent modular subsets of the full specification that allow SBOM authors to tailor the level of expressiveness and complexity to their specific use case. There are 8 profiles available, out of which only the core profile is mandatory and all the rest are optional: core, software, security, licensing, dataset, AI, build, lite, and extension profiles. % I need to explain profiles better but I am unsure how to

The document is organized into three major sections: (1) an introduction that provides guidance on how to interpret the overall structure alongside some overarching and legal rules; (2) a detailed description of the available profiles, including the classes, properties, definitions, and special requirements associated with each; and (3) an appendix that offers practical guidance such as a Lite-profile example SBOM and an extensive discussion of Package URL (purl) syntax.


Below is a description of each of the themes that was created. A distribution of the themes is shown in Table \ref{tab:spdx_theme_distribution}:
\begin{itemize}
    \item \textbf{Class-specific rules (57\%)}: Requirements defining the structure or content of what a class in SPDX may contain. It is further split into two categories, rules defining the properties a class may contain or the rules defining what the content inside these properties may be.
    \item \textbf{Overarching conformance (22\%)}: Requirements which are generalized and cannot be associated with any other theme. These are further split into three categories, requirements which apply to the core profile (thus every SBOM), requirements which apply only to the lite profile, and requirements which apply only to any other profile, excluding the core and lite profiles.
    \item \textbf{Serialization (6\%)}: Requirements about how to format an SBOM document. These are further divided into two, requirements which apply to only JSON-LD serialization and requirements which are more general.
    \item \textbf{Syntax (13\%)}: Syntactic requirements for writing SPDX license strings, creating old-style templates to match non-standard licenses, and requirements for correctly creating, reading, and handling Package URLs (purl).
    \item \textbf{Legal (2\%)}: Requirements relating to the legal side of using SBOMs, specifically how to use the SPDX name and reusing the specification document, and requirements for comparing license texts and interpreting approval flags.
\end{itemize}

\begin{table}[t]
\caption{Distribution of Thematic Categories in SPDX 3.0.1 Requirements}
\label{tab:spdx_theme_distribution}
\centering
\begin{tabular}{@{}ll@{}}
\toprule
\textbf{Theme} & \textbf{Percentage} \\ 
\midrule

\textbf{Class-Specific Rules} & \textbf{57}\% \\
\hspace{1.5em}Class Structure Rules & 49\% \\
\hspace{1.5em}Class Content Rules & 8\% \\[4pt]

\textbf{Overarching Conformance} & \textbf{22}\% \\
\hspace{1.5em}General Conformance & 2\% \\
\hspace{1.5em}Lite Profile Conformance & 17\% \\
\hspace{1.5em}Profile-Specific Conformance & 3\% \\[4pt]

\textbf{Serialization} & \textbf{6}\% \\
\hspace{1.5em}General Serialization & 5\% \\
\hspace{1.5em}JSON-LD Serialization & 1\% \\[4pt]

\textbf{Syntax} & \textbf{13}\% \\
\hspace{1.5em}Legacy Template Syntax & 1\% \\
\hspace{1.5em}License Expression Syntax & 1\% \\
\hspace{1.5em}Package URL (purl) Syntax & 11\% \\[4pt]

\textbf{Legal} & \textbf{2}\% \\
\hspace{1.5em}Legal Requirements & 1\% \\
\hspace{1.5em}License-Matching Requirements & 1\% \\

\bottomrule
\end{tabular}
\end{table}

We conclude that the focus of the SPDX 3.0.1 specifications is mainly on class-specific rules, which it defines and then these can be used to create objects which can be used to represent different aspects of an SBOM. However, the 6:1 ratio between class structure rules and class content rules shows SPDX 3.0.1's importance over maintaining the structure of the SBOM over its semantics. We also note notable focus into lite profile conformance to give a starting point for new developers to create a basic SBOM to fulfil the basic requirements. Moreover, the purl syntax is extensively discussed, which shows an effort to ensure that the packages are kept universally consistent once included in an SBOM.

\subsubsection{CycloneDX}

Our analysis of the 1,724 normative requirements from CycloneDX 1.6 reveals a specification distinct from SPDX in its emphasis on specialized security use cases. We categorized requirements into seven high-level themes (Table \ref{tab:cdx_theme_distribution}).

\begin{table}[t]
\caption{Distribution of Thematic Categories in CycloneDX 1.6 Requirements}
\label{tab:cdx_theme_distribution}
\centering
%\resizebox{\columnwidth}{!}{%
\begin{tabular}{@{}ll@{}}
\toprule
\textbf{Theme} & \textbf{Percentage} \\ 
\midrule

\textbf{Advanced \& Specialized Data Models} & \textbf{35.3}\% \\
\hspace{1.5em}Cryptographic Asset Mgmt (CBOM) & 12.8\% \\
\hspace{1.5em}Formulation \& Reproducibility & 8.8\% \\[4pt]

\textbf{Foundational BOM Structure} & \textbf{17.8}\% \\
\hspace{1.5em}Internal Referencing (bom-ref) & 15.1\% \\
\hspace{1.5em}BOM Identification & 1.1\% \\[4pt]

\textbf{Trust, Integrity, and Security} & \textbf{16.0}\% \\
\hspace{1.5em}Vulnerability Information & 6.2\% \\
\hspace{1.5em}Cryptographic Hashes & 4.4\% \\[4pt]

\textbf{Metadata \& Provenance} & \textbf{12.8}\% \\
\hspace{1.5em}Organizational Entity Definition & 6.3\% \\
\hspace{1.5em}Contact Information & 3.8\% \\[4pt]

\textbf{Extensibility and Customization} & \textbf{6.6}\% \\
\hspace{1.5em}Extensibility via Properties & 3.8\% \\
\hspace{1.5em}Property Taxonomies & 2.8\% \\[4pt]

\textbf{Core Inventory \& Attributes} & \textbf{6.4}\% \\
\hspace{1.5em}Descriptive Metadata & 2.1\% \\
\hspace{1.5em}Standardized Ext. Identifiers & 2.1\% \\[4pt]

\textbf{Relationships \& Composition} & \textbf{5.2}\% \\
\hspace{1.5em}External References & 2.7\% \\
\hspace{1.5em}Dependency Graph Representation & 1.3\% \\

\bottomrule
\end{tabular}
%}
\end{table}

The analysis highlights that CycloneDX allocates the largest portion of its normative text (35.3\%) to \textbf{Advanced and Specialized Data Models}, specifically for Cryptography (CBOM) and Build Formulation. In contrast, the \textbf{Core Inventory} theme—which covers basic component definitions—comprises only 6.4\% of the requirements. This structural imbalance suggests the standard is optimized for complex, high-maturity security use cases rather than basic inventory management.

\subsubsection{CycloneDX Revisited Through a Security Lens}
\label{subsec:cdx_security_lens}

The thematic distribution in Table~\ref{tab:cdx_theme_distribution} shows \emph{where} CycloneDX 1.6 allocates its normative attention, but it does not by itself explain whether those requirements function as meaningful security guardrails for SBOM generation. To address this limitation, we re-examined the extracted CycloneDX requirements through a security-oriented lens centered on the known failure modes in SBOM generation identified in Section~\ref{subsec:systematization}. Rather than asking only what the standard contains, this second pass asks three additional questions: (1) which known SBOM failure mode a requirement is relevant to, (2) whether that requirement acts as a \emph{strong}, \emph{weak}, or merely \emph{dormant} guardrail, and (3) whether compliance with that requirement can be verified from the SBOM artifact itself or only through external context.

This re-analysis yields a different picture of CycloneDX than the thematic distribution alone. The specification is not lacking in expressive power; rather, it is uneven in how that expressive power is converted into baseline security guarantees. CycloneDX is consistently strong at regulating the \emph{internal structure} of an object once that object is present, but much weaker at requiring the presence of the very objects that carry the security-relevant information needed by downstream consumers. In other words, the standard tightly constrains the \emph{shape} of chosen content, but only loosely constrains the \emph{existence} of that content.

We observed four recurring guardrail patterns.

\paragraph{(1) Strong local structural guardrails.}
CycloneDX imposes strict local constraints on syntax, typing, and referential integrity. For example, \texttt{bomFormat} and \texttt{specVersion} are required; \texttt{bom-ref} values must be unique within a BOM; dependency objects require a \texttt{ref}; external references require \texttt{type} and \texttt{url}; and identifier fields such as \texttt{purl}, \texttt{cpe}, \texttt{swhid}, and \texttt{omniborId}, when present, must conform to their respective external specifications. Similar local strictness appears throughout the standard in the form of uniqueness constraints, required child fields, and controlled enumerations for hashes, cryptographic assets, VEX states, and composition aggregates. These rules are valuable for parser reliability and structural interoperability, and they are generally artifact-verifiable.

\paragraph{(2) Weak baseline security guardrails.}
In contrast, many of the fields most directly tied to common supply-chain security tasks are optional. At the root level, \texttt{metadata}, \texttt{dependencies}, \texttt{compositions}, \texttt{vulnerabilities}, \texttt{annotations}, \texttt{formulation}, \texttt{declarations}, and \texttt{definitions} are all defined with \texttt{MAY}. Within \texttt{metadata}, the fields most relevant to provenance and accountability---such as \texttt{timestamp}, \texttt{supplier}, and \texttt{authors}---are likewise optional. At the component level, security-relevant fields such as \texttt{version}, \texttt{licenses}, \texttt{supplier}, and \texttt{scope} are not mandatory either. This means that a CycloneDX BOM can be structurally valid while omitting the basic evidence needed for minimum-elements compliance, provenance tracking, or vulnerability triage. The practical implication is that validity is decoupled from usefulness: a consumer may receive a conformant CycloneDX file that carries too little information to support actual security decisions.

\paragraph{(3) Dormant advanced guardrails.}
CycloneDX includes several sophisticated mechanisms aimed at higher-maturity security use cases, but these mechanisms are largely dormant because they are activated only when producers voluntarily choose to use the corresponding optional objects. The \texttt{formulation} object captures build and workflow provenance; \texttt{vulnerabilities} and \texttt{analysis} support VEX-style impact statements; \texttt{compositions} allow completeness assertions; \texttt{cryptoProperties} support cryptographic asset inventories; and \texttt{modelCard} and \texttt{data} extend the standard toward ML-BOM and data governance use cases. Yet none of these are part of the mandatory baseline. As a result, CycloneDX can represent many of the properties needed to mitigate known SBOM failures, but it rarely compels producers to provide them. This helps explain why optional advanced features remain under-adopted in practice despite being fully standardized.

\paragraph{(4) Aspirational guidance in place of enforceable protection.}
A number of the security-relevant statements in CycloneDX are formulated as recommendations rather than mandatory obligations. The standard states that SBOMs \emph{should ideally} contain all direct and transitive components and their dependency relationships; that serial numbers are recommended; that \texttt{compositions} are recommended to indicate unknown dependency graphs; that VEX justifications \emph{should} be provided for \texttt{not\_affected} cases; and that property names are encouraged to be registered in the CycloneDX Property Taxonomy. These recommendations are useful as best-practice guidance, but they do not function as enforceable guardrails. Their presence signals the standard's awareness of important quality goals, yet their non-mandatory status leaves tools free to ignore them without becoming non-conformant.

Taken together, these patterns suggest that CycloneDX 1.6 is better characterized as a flexible representation language for security-relevant software metadata than as a strong baseline control document for SBOM generation. The standard is highly expressive, but much of its security value is conditional on producer choice. This distinction is important because prior work has largely treated the standard as a stable oracle against which tool behavior can be judged. Our analysis suggests a more nuanced interpretation: some of the deficiencies observed in SBOM tools do not arise solely from poor implementation, but from a specification that makes many of its strongest safeguards optional, indirect, or difficult to operationalize.

Table~\ref{tab:cdx_security_guardrails} summarizes this security-lens analysis by mapping the major failure modes from prior SBOM literature to the corresponding CycloneDX guardrails, their strength, and their verifiability.

\begin{table*}[t]
\caption{CycloneDX 1.6 security-lens analysis of specification guardrails}
\label{tab:cdx_security_guardrails}
\centering
\small
\begin{tabular}{p{3.2cm} p{5.3cm} p{2.1cm} p{3.0cm}}
\toprule
\textbf{Failure mode} & \textbf{Relevant CycloneDX guardrail(s)} & \textbf{Guardrail strength} & \textbf{Verifiability} \\
\midrule
Failure to meet minimum elements &
\texttt{metadata.supplier}, \texttt{metadata.authors}, and \texttt{metadata.timestamp} exist in the model, but all are optional root metadata fields &
Weak &
Artifact-verifiable when present \\
\addlinespace[2pt]

Transitive dependency omission &
The specification states that SBOMs should ideally contain all direct and transitive dependencies; if a dependency graph is used, leaf nodes must be declared explicitly as empty dependency elements &
Weak to Moderate &
Partly artifact-verifiable; full verification requires external ground truth \\
\addlinespace[2pt]

Metadata parsing divergence &
The standard provides almost no normative guidance for \emph{how} metadata should be extracted from source files, environments, containers, or build systems &
None / Very Weak &
Not artifact-verifiable \\
\addlinespace[2pt]

Interoperability loss &
Strong local validation exists for typed fields, hashes, and external references; however, extensibility is largely delegated to optional \texttt{properties} and weak taxonomy guidance &
Mixed &
Partly artifact-verifiable \\
\addlinespace[2pt]

Reproducibility gap &
CycloneDX provides rich support through \texttt{formulation}, workflows, task dependencies, runtime topology, and associated references, but the entire object is optional &
Dormant &
Mostly artifact-verifiable when present \\
\addlinespace[2pt]

Checkbox compliance / ambiguity of completeness &
The \texttt{compositions} object can express whether a dependency or assembly view is complete, incomplete, or unknown, but it is optional and only recommended in some relevant cases &
Weak &
Artifact-verifiable when present \\
\addlinespace[2pt]

Package naming inconsistency &
CycloneDX supports normalized identifiers such as \texttt{purl}, \texttt{cpe}, \texttt{swhid}, \texttt{omniborId}, and \texttt{swid}; if present, they must conform to external standards &
Moderate &
Artifact-verifiable \\
\addlinespace[2pt]

Runtime / dynamic blind spot &
The standard can represent runtime topology and service/data relationships, but it does not impose a baseline obligation to distinguish statically listed components from actually used runtime components &
Weak &
Requires external runtime context \\
\bottomrule
\end{tabular}
\end{table*}

Several implications follow from this mapping.

First, CycloneDX's central weakness is not the absence of security-relevant constructs, but the absence of \emph{mandatory baseline security content}. This is most visible for the minimum-elements problem: the specification contains fields for provenance and authorship, yet does not require them even at the metadata level. As a result, a conformant BOM can remain unsuitable for the very policy and vulnerability-management workflows that motivated SBOM adoption.

Second, the standard is systematically stricter on object integrity than on evidence obligations. Once a producer elects to provide a hash, dependency object, external reference, or cryptographic asset description, the specification tightly constrains its format. By contrast, the producer is rarely obligated to provide evidence of supplier identity, dependency completeness, build reproducibility, or vulnerability impact in the first place. This asymmetry helps explain why real-world SBOMs can be formally valid yet semantically impoverished.

Third, dependency completeness in CycloneDX is only weakly governed. The standard clearly recognizes transitive completeness as an ideal goal, but it frames that goal using \texttt{RECOMMENDED} language and an optional root-level dependency graph. The only hard rule in this area---that dependency-free components should still appear as empty nodes---becomes active only after a producer has already opted into graph construction. Thus, the specification meaningfully constrains dependency graphs \emph{if they exist}, but does not force producers to provide one.

Fourth, CycloneDX contains a built-in tension between normalization and fragmentation. On the one hand, fields like \texttt{purl} and \texttt{cpe} provide strong normalization hooks that support interoperability. On the other hand, the pervasive use of optional \texttt{properties} fields, combined with only recommended taxonomy registration, creates a specification-sanctioned path toward semantic divergence. In this sense, CycloneDX solves extensibility by tolerating local customization, but does so at the cost of weakening cross-tool predictability.

Finally, this security-lens analysis clarifies the role of the specification in mediating between tools and downstream security workflows. CycloneDX 1.6 should not be interpreted as a complete operational guide for generating a security-sufficient SBOM. It is a representational standard that provides a broad vocabulary, but it leaves many crucial generation decisions underspecified: how to extract metadata, how to recover complete dependency depth, how to distinguish static presence from runtime use, and when to assert completeness. The practical burden of resolving these questions is therefore shifted to tool developers, which in turn creates space for divergent implementations. This observation helps explain why tool inconsistency persists even when tools are schema-valid and nominally standard-compliant.


\subsection{Practical applicability of the standards}

\subsubsection{Intra-specification consistency}

Our analysis revealed significant discrepancies in both specifications, indicating that the official schemas often diverge from the normative text.

\begin{itemize}
    \item \textbf{SPDX 3.0.1:} No differences were found in Definition Presence and Property Presence. However, a total of 30 differences were found in Property Type. In 14 cases, the official schema was more lax than the normative text, allowing a property to be a constant/ string as well as an object using the 'oneOf' condition. In 16 cases, the official schema was more strict than the normative text, where it applied 2 regexes instead of 1 using the 'allOf' condition in DateTime strings.
    
    \item \textbf{CycloneDX 1.6:} Our differential analysis between the prescriptive prose and the official JSON schema reveals a critical \textbf{CISA Compliance Gap}. 
        
    The CISA guidelines mark "Supplier Name", "Author Name", and "Timestamp" as \textbf{REQUIRED}. However, the official CycloneDX 1.6 JSON Schema defines \texttt{metadata.supplier}, \texttt{metadata.authors}, and \texttt{metadata.timestamp} as non-mandatory fields (no \texttt{required} constraint in JSON Schema). 
        
    Consequently, a JSON file can validate perfectly against the CycloneDX schema while failing to meet the federal minimum requirements. Additionally, our automated check found 38 granular constraint mismatches, including \texttt{specVersion} not enforcing the value '1.6' in the schema, despite the text mandating it.
    
\end{itemize}

\subsubsection{Conditionality analysis}

Our findings demonstrate that both specifications are overwhelmingly conditional, though they achieve this through different architectural patterns:
\begin{itemize}
    \item \textbf{SPDX 3.0.1:} Out of 429 extracted requirements, only \textbf{69 (16\%)} are applicable to the minimum template SBOM. The majority of requirements are conditional based on \textit{Class Instantiation} (242 cases) or \textit{Profile Conformance} (93 cases). This structural heavy-handedness allows for "valid but empty" SBOMs, where the topology is enforced, but data richness is optional.
    
    \item \textbf{CycloneDX 1.6:} Out of 1,724 requirements, only \textbf{6 (0.35\%)} are universally applicable to the minimum purposeful SBOM.

    The standard utilizes an architecture where requirements are conditional upon the presence of optional root-level objects. Our analysis identified exactly \textbf{56} normative requirements governing Machine Learning Model Cards (ML-BOM) and \textbf{151} requirements governing Formulation (build reproducibility). However, because the root \texttt{modelCard} and \texttt{formulation} objects are defined as \textbf{OPTIONAL} (MAY), these 207 combined requirements remain dormant unless a user voluntarily attempts to implement those specific features.
    
    This confirms that CycloneDX conformance is highly dynamic: a tool can be compliant while implementing less than 1\% of the specification, provided it does not attempt to use advanced features incorrectly.
    
\end{itemize}

To further investigate the structural mechanisms enabling this conditionality, we performed a topological analysis of the Prescriptive Schema. We calculated the Breadth (direct reuse count), Ancestor Count (complexity), and Max Depth for all CycloneDX classes. Table~\ref{tab:cdx_metrics} presents the metrics for the most structurally critical classes.

Three key architectural patterns emerge from this data:
\begin{itemize}
    \item \textbf{Graph Connectivity:} The \texttt{refType} class is the most reused definition (Breadth 25). This confirms the standard operates as a loosely connected graph of string references rather than a strict hierarchy.
    \item \textbf{Generic Extensions:} The \texttt{property} class is the second most reused structure (Breadth 17). This indicates a systemic reliance on generic key-value pairs over standardized schema fields.
    \item \textbf{Isolated Roots:} Major functional classes like \texttt{vulnerability} and \texttt{formula} exhibit zero Breadth, confirming they exist as isolated "silos" that do not enforce structural dependencies on the core component inventory.
\end{itemize}

\begin{table}[h]
\caption{Structural Metrics of Top 10 Critical CycloneDX 1.6 Classes.}
\label{tab:cdx_metrics}
\centering
\small
\begin{tabular}{@{}l c c l@{}}
\toprule
\textbf{Class Name} & \textbf{Breadth} & \textbf{Anc.} & \textbf{Structural Role} \\
\midrule
refType & 25 & 41 & Graph Connectivity \\
property & 17 & 25 & Generic Extension \\
signature & 12 & 18 & Integrity \\
organizationalEntity & 10 & 25 & Entity Definition \\
attachmentText & 10 & 31 & Inline Data \\
component & 6 & 8 & Core Inventory \\
vulnerability & 0 & 0 & Isolated Root \\
\bottomrule
\end{tabular}
\end{table}

\begin{table}[t]
\caption{Distribution of SPDX 3.0.1 Conditional Requirements by Dependency Type}
\label{tab:spdx_dependency_types}
\centering
\small
\begin{tabular}{@{}lcl@{}}
\toprule
\textbf{Type} & \textbf{Number of Cases} & \textbf{Description} \\
\midrule
Class & 242 & Instantiation of a class. \\
Profile & 93 & Conformance to a profile. \\
Property & 56 & Presence of a property. \\
DataType & 3 & Presence of a DataType. \\
Serialization & 5 & Specific serialization used. \\
\bottomrule
\end{tabular}
\end{table}

\subsubsection{Comparison with CISA minimum elements}

Our extraction of 133 normative requirements from the CISA "Framing" document reveals a distinct bifurcation in prescriptive intent. The thematic distribution is heavily skewed toward two categories: \textbf{Component \& SBOM Attributes} (36\%) and \textbf{SBOM Operations \& Lifecycle} (29\%).

Critically, we observe a divergence in the normative keywords used between these themes:
\begin{itemize}
    \item \textbf{Operations are Mandatory:} The \textit{Operations} theme is dominated by \textbf{REQUIRED} keywords (e.g., "An SBOM needs to be created when a Component is released"). This establishes a rigid policy baseline for \textit{when} and \textit{how} SBOMs are exchanged.
    \item \textbf{Data Quality is Aspirational:} The \textit{Component Attributes} theme frequently uses \textbf{SHOULD} or \textbf{RECOMMENDED} (e.g., "Supplier Name should be identified carefully" and "list as many globally unique identifiers as available"). 
\end{itemize}

This creates a regulatory concern where the process of generating an SBOM is strictly enforced, but the data quality within that SBOM is often relegated to "Recommended Practice" rather than "Minimum Expectation," allowing tools to produce operationally valid but semantically poor data.

\subsection{Dependency resolution mechanisms in action}

\subsubsection{Results - SPDX 3.0.1\\\\}
\textbf{Analysis of requirements} 

A dependency graph contains two parts in SPDX: the edges of the graph are expressed by using the 'Relationship' class in SPDX 3.0.1. The summary of relationship is as follows:

\begin{quote}
    "Describes a relationship between one or more elements."
\end{quote}

The nodes of the graph are represented by the abstract class ‘Element’. The description states the following:

\begin{quote}
	“Within SPDX-3.0 structure this is the base class acting as a consistent, unifying, and interoperable foundation for all explicit and inter-relatable content objects.”
\end{quote}

In order to investigate dependency resolution, we isolate all requirements which refer to the relationship class or the \textbf{resolution} of the Element class or any of its subclasses. A total of 17 requirements were selected which encompassed the relationship class, the requirements reveal that the relationship class have a mandatory field 'relationshipType' of type 'RelationshipType', an enumeration of 62 possible types. Out of the 62 types, we choose \textbf{'dependsOn'} as the type to signal a dependency, which is consistent with the report in \cite{cmuplugfest}. Additionally, we also choose \textbf{‘contains’} to signal a dependency.

Out of the 17 requirements, they can be classified as the following:
\begin{enumerate}
    \item \textbf{SHOULD: 3 cases}. E.g: "To explicitly assert that no such relationships exist, the to property SHOULD contain the NoneElement individual and no other elements."
    \item \textbf{MUST: 2 cases}. E.g: "relationshipType $|$ RelationshipType $|$ 1 $|$ 1 (relationship MUST have a relationshipType)."
    \item \textbf{Class based requirements: 8 cases}.
    \item \textbf{Dependent MUST: 3 cases}. E.g: "The Licensing profile only contains the additional requirement that any Software Artifact MUST have a Relationship of type hasConcludedLicense."
    \item \textbf{Redundancy: 1 case}.\\
\end{enumerate}

\textbf{Test cases}

5 test cases were constructed using a python script, based on the MUST requirements. The 6th test case was added to replicate the testing done in \cite{cmuplugfest}. The 7th test case was added to identify the breadth of use of the relationship class in SPDX. These were the following final test cases:
\begin{enumerate}
    \item A relationship MUST not contain any additional elements to NoneElement in the ‘to’ property
    \item Relationship MUST have a relationshipType
    \item IF Licensing Profile THEN Software Artifact MUST have a type “hasConcludedLicense”
    \item IF Build Profile THEN Build element MUST have relationship of types: “hasInput”, “hasOutput”, and “invokedBy“
    \item IF Lite Profile THEN Software Package MUST have relationship of types “hasConcludedLicense” and “hasDeclaredLicense”
    \item Maximum depth of the dependency graph (based on relationshipType: dependsOn).
    \item Number of different types of relationshipTypes present.
\end{enumerate}

The test cases were then used on a dataset of 4 SBOMs. 3 were extracted from a GitHub repository officially recognised by the Linux foundation. The 4th one was generated using microsoft/sbom-tool. The results of the test cases are present in Table 2.

\textbf{Limitations\\}
Given how none of the SBOMs in the dataset were using the Licensing, Build, and Lite profile, it resulted in none of the dependent tests being applicable. Moreover, in test 6 for generated 1, the relationshipClass was actually 'DEPENDS\_ON' instead of 'dependsOn' in the specifications which led to the test case failing at first, before this being rectified after manual analysis. The relationshipTypes for generated 1 were all listed differently than in the specifications.

\begin{table}[h!]
\centering
\begin{tabular}{lccccc|cc}
\toprule
\textbf{SBOM} & \textbf{T1} & \textbf{T2} & \textbf{T3} & \textbf{T4} & \textbf{T5} & \textbf{T6} & \textbf{T7} \\
\midrule
Example 1 & $\checkmark$ & $\checkmark$ & $\circ$ & $\circ$ & $\circ$ & $\circ$ & 1 \\
Example 2 & $\checkmark$ & $\checkmark$ & $\circ$ & $\circ$ & $\circ$ & 2 & 6 \\
Example 3 & $\checkmark$ & $\checkmark$ & $\circ$ & $\circ$ & $\circ$ & $\circ$ & 8 \\
Generated 1 & $\checkmark$ & $\checkmark$ & $\circ$ & $\circ$ & $\circ$ & 3 & 4 \\
\bottomrule
\end{tabular}
\caption{Results of test cases from 4.4.1}
\end{table}

\subsubsection{Results - CycloneDX 1.6\\}
\label{subsec:dep_res_cdx}

\textbf{Analysis of requirements\\}
In CycloneDX, dependency relationships are explicitly modeled within the root-level \texttt{dependencies} array. The specification states, "Each item of this array must be a Dependency object." Our extraction yielded 24 normative requirements related to the \texttt{dependencies} object and its properties.

The core of the dependency graph is the \texttt{dependency} object, which has one REQUIRED property, \texttt{ref}, and one key optional property, \texttt{dependsOn}. A critical rule from the specification (Section 11.1) states:
\begin{quote}
    "Components or services that do not have their own dependencies MUST be declared as empty elements within the graph."
\end{quote}
This implies that every component listed in the main \texttt{components} array should have a corresponding entry in the \texttt{dependencies} graph, even if its \texttt{dependsOn} array is empty. Furthermore, the specification includes a key recommendation (Section 5.2):
\begin{quote}
    "SBOMs SHOULD ideally contain all direct and transitive components and the dependency relationships between them."
\end{quote}
These rules, particularly the ambiguity between the strict \texttt{MUST} for leaf node declaration and the softer \texttt{SHOULD} for transitive completeness, form the basis for our test cases, which are designed to detect common failures in graph integrity.

\textbf{Test cases}
Based on the normative requirements and the failures observed in prior empirical work \cite{sei-harmonization-report, jbomaudit}, we designed three pilot test cases to probe the structural and semantic integrity of dependency graphs in CycloneDX SBOMs.
\begin{description}
    \item[Test Case 1: The "Dangling Component."] This test verifies the \texttt{MUST} requirement from Section 11.1. It checks for any component listed in the main \texttt{components} array that does not have a corresponding entry in the \texttt{dependencies} array. Such a component is "dangling" because its dependency status is not explicitly declared, making the graph incomplete and violating a mandatory rule.
    
    \item[Test Case 2: The "Implicitly Missing Transitive Dependency."] This test targets the \texttt{SHOULD ideally} clause. The test SBOM correctly lists a direct dependency (e.g., \texttt{requests}) but omits a known transitive dependency (e.g., \texttt{urllib3}) while incorrectly declaring the direct dependency as a leaf node (\texttt{"dependsOn": []}). This scenario represents a critical vulnerability blind spot and is the exact problem identified in related work as a primary cause of "dependency depth variance."
    
    \item[Test Case 3: The "Detached Dependency Graph."] This test verifies the implicit structural rule that the dependency graph must connect to the primary component described by the SBOM (often defined in \texttt{metadata.component}). The test SBOM defines a main component in the metadata, but its \texttt{dependencies} graph is internally consistent but has no link back to this main component, making it a "detached" and contextually meaningless graph.
\end{description}
These test cases form the foundation of our proposed automated conformance framework. They move beyond simple schema validation to test for the deeper structural and semantic integrity required for reliable security analysis.

\subsection{Empirical verification of the issues present}

\subsubsection{Design of test cases\\\\}

\textbf{SPDX 3.0.1}:

\paragraph{(1) Failure to meet the minimum elements specified by the CISA guidelines}: SPDX v3.0.1 directly addresses compliance failures through the introduction of the Lite Profile. Recognizing that the complexity of the full standard often leads to incomplete SBOMs, the Lite Profile captures the absolute minimum set of information required for license compliance, meeting the CISA minimum elements in the way: \texttt{copyrightText}, \texttt{creationInfo}, \texttt{name}, \texttt{packageVersion}, \texttt{spdxId}, and \texttt{suppliedBy}.

By explicitly mapping these mandatory fields to the minimum elements defined by CISA, the standard removes the ambiguity that previously allowed tools to generate "compliant" but empty SBOMs. Thus, as long as an SBOM is conformant to the Lite Profile it follows the CISA guidelines.

However, given that conformance to the Lite Profile is not mandatory and only the Core Profile is, it still remains the case that an SBOM can be created in the SPDX 3.0.1 format which is fully conformant to the standard but does not meet the CISA guidelines.

\paragraph{(2) Transitive dependencies are missed:}
While static analysis tools often miss transitive dependencies in dynamic languages (e.g., Python, JavaScript), SPDX v3.0.1 addresses this via the \textbf{Build Profile} (Section 14). Unlike previous versions that relied heavily on static file manifest parsing, the Build Profile models the actual build instance. This data model encourages tools to record dependencies observed during the build process rather than estimating them from static manifest files, significantly reducing missed transitive components.

Furthermore, explicit Relationship Types such as \texttt{hasPrerequisite}, \texttt{hasDynamicLink}, and \texttt{hasStaticLink}, allow tools to distinguish between direct source dependencies and transitive runtime dependencies.

However, this requires tooling which can capture this relationship. Since most SBOM tools only support estimating dependencies from static manifest files, most SBOM generation tools will still miss transitive dependencies \cite{sbomlandscape}.

\paragraph{(3) Tools employ different methodologies for parsing metadata:}

Although the standard provides ways of making sure that any components extracted can be represented and verified in a universal manner by using the Package URL (purl) or Hash algorithms, they do not contain any information on best ways to parse metadata. This provides a hole for SBOM generation tools to fill, which leads to inconsistencies since they can choose a variety of going about it.\\
Although SPDX 3.0.1 allows metadata to be mapped to a universal graph using the Resource Description Framework (RDF), it contains no fields where it can be noted what metadata should be preferred or used in component extraction. Considering how depending on whether an SBOM is created from a 'requirements.txt' file, a python environment, or a docker container, it can have a different output, this will lead to different SBOMs given that each SBOM generation tool will choose their own preferential option.

Additionally, given that there exists no property in SPDX which lists down which metadata option was chosen when creating the SBOM, it divorces the SBOM from the method of its creation, and creates an information gap between the SBOM generation tool itself and the created SBOM.

\paragraph{(4) Interoperability issues where one tool produces a better SBOM for one format over another:}
Interoperability issues, particularly between SPDX and CycloneDX, are explicitly addressed in the Extension Profile. The specification acknowledges that tools often specialize in one format, leading to data loss during conversion.

The \texttt{CdxPropertiesExtension} class is a standardized extension point which is intended to be compatible with CycloneDX properties, allowing an SPDX document to carry data generated by tools designed for the competing standard without loss. Additionally, the modular nature of the profiles allows tools to support specific subsets of the standard reliably, rather than failing to support the entire monolithic specification.

\paragraph{(5) Lack of reproducibility in the builds on which SBOMs are created:} The SPDX 3.0.1 specification directly addresses build reproducibility through two mechanisms. First, the \texttt{CreationInfo} class notes that the \texttt{created} timestamp should reflect the date of last change (e.g., a git commit date) rather than the date the SPDX data was generated, explicitly stating this supports reproducible builds.'' Second, the \texttt{Build} profile introduces a dedicated \texttt{Build} class that encapsulates all metadata related to a build process---its inputs, outputs, builders, and related identities---providing a structured, traceable record of the build from which the SBOM was generated. Crucially, \texttt{buildStartTime} and \texttt{buildEndTime} are described as optional and may be omitted to simplify creating reproducible builds,'' since timestamping the build process itself can introduce non-determinism.

\paragraph{(6) View of SBOMs as unnecessary and merely a compliance checkbox:}
The specification counters this perception architecturally through the \texttt{Lite Profile}, which is described as capturing the minimum information required for license compliance in the software supply chain, and through the modular profile system more broadly. By defining nine distinct compliance points, Core, Software, Security, Licensing, Dataset, AI, Build, Lite, and Extension, the specification frames SBOMs not as monolithic compliance documents but as targeted, functional artifacts serving real operational purposes. The \texttt{Security Profile}, for instance, enables interchange of vulnerability data between tools, making an SBOM an active security instrument rather than a passive document. The \texttt{Build Profile} similarly ties the SBOM to a verifiable build process, reinforcing its role as an auditable engineering artifact.

\paragraph{(7) Inconsistencies in the naming of packages:} The specification addresses package naming inconsistencies through two complementary mechanisms. The \texttt{packageUrl} property (part of the Software Profile) adopts the Package URL (\texttt{purl}) standard, described as an attempt to standardize package representations in order to reliably identify and locate software packages'' in a mostly universal and uniform way across programming languages, package managers, packaging conventions, tools, APIs and databases.'' The \texttt{purl} follows a structured schema that normalises identification across ecosystems. Complementarily, the \texttt{ExternalIdentifier} class supports referencing packages via established external naming schemes including \texttt{cpe22}, \texttt{cpe23}, \texttt{packageUrl}, \texttt{swid}, and \texttt{swhid}, providing a mapping from SPDX elements to authoritative, domain-specific identifiers and thereby reducing ambiguity from cross-ecosystem naming divergence.

\paragraph{(8) Inability to capture whether a library was actually loaded into memory or not due to the static nature of an SBOM:} The specification addresses this limitation through two related features. First, the \texttt{SBOMType} enumeration includes a \texttt{runtime} type, defined as an SBOM generated through instrumenting the system running the software, to capture only components present in the system, as well as external call-outs or dynamically loaded components''---also referred to as an Instrumented or Dynamic SBOM. This allows producers to explicitly distinguish a runtime-observed SBOM from a static analysis SBOM. Second, the \texttt{RelationshipType} enumeration provides \texttt{hasDynamicLink} (the from Element dynamically links in each to Element'') and \texttt{hasStaticLink} as distinct relationship types, scoped further by the \texttt{LifecycleScopeType}, which includes a \texttt{runtime} value defined as covering the execution phase of an element.'' Together, these allow an SBOM to express not merely what libraries are present in a package, but which were dynamically linked and active during execution, partially bridging the static/dynamic observability gap.

\textbf{CycloneDX}

\paragraph{(1) Failure to meet CISA Minimum Elements:}
Our intra-specification analysis reveals a direct conflict between the CISA guidelines and the CycloneDX normative requirements regarding the "Supplier" field. 

The CISA Minimum Elements explicitly list "Supplier Name" as \textbf{REQUIRED}. However, our extraction of the CycloneDX 1.6 specification confirms that the \texttt{supplier} property is defined as \textbf{OPTIONAL} (Normative Keyword: MAY) in lines 198, 242, and 264 of the specification data. Furthermore, the official JSON schema does not enforce the presence of metadata.supplier. 

This creates a systemic root cause for non-compliance. Our empirical analysis (Section 4.6) confirms this, showing that \textbf{96.1\%} of real-world SBOMs omit the supplier field because the schema permits it.

% \paragraph{(2) Transitive dependencies are missed:}
% CycloneDX utilizes a nested \texttt{components} array or a flattened \texttt{dependencies} graph. However, the specification relies heavily on the \texttt{metadata.tools} and \texttt{formulation} objects to describe the build environment. Our thematic analysis shows that while \textbf{Formulation} accounts for 9\% of the spec, it is almost entirely optional (\textbf{MAY}). Tools perform shallow scans (e.g., parsing \texttt{package.json}) because the specification does not mandate the complex formulation analysis required to capture transitive build-time dependencies.

\paragraph{(2) Lack of standardized metadata:}
CycloneDX addresses metadata via the \texttt{properties} object (a key-value store). Our thematic coding of the "Extensibility" theme reveals that while the standard "RECOMMENDS" registering properties in a taxonomy, it effectively allows ad-hoc strings. This results in the same fragmentation seen in the Python ecosystem \cite{pythonsboms}, where tools create arbitrary property names (e.g., \texttt{cdx:property:build\_host} vs \texttt{ex:build\_server}) that cannot be parsed universally. Our measurement study found that \textbf{21.7\%} of properties in the wild use ad-hoc, unregistered namespaces, confirming this fragmentation.

\paragraph{(3) Interoperability issues:}
The high degree of flexibility in CycloneDX (53\% \textbf{MAY}) creates interoperability friction. For example, the \texttt{licenseChoice} element allows an author to provide either an SPDX ID, a proprietary license name, or a license expression. A consumer tool expecting an SPDX ID (to automate policy checks) will fail when encountering a valid CycloneDX file that uses proprietary names. The specification prioritizes expressiveness over strict interoperability, requiring consumption tools to implement complex normalization logic \cite{bomsaway}. However, our empirical data suggests the ecosystem is self-correcting: \textbf{88.3\%} of analyzed SBOMs voluntarily use standard SPDX identifiers despite the specification allowing proprietary names.

\begin{table}[h]
\centering
\normalsize
\resizebox{0.5\textwidth}{!}{%
\begin{tabular}{|l|p{3.2cm}|p{3.2cm}|p{3.2cm}|}
\hline
 & \textbf{SPDX Guardrail} & \textbf{CycloneDX Guardrail} & \textbf{Test for issue} \\ \hline
1 & Lite profile presence 
  & Presence of \texttt{metadata.supplier}, \texttt{timestamp}, and \texttt{authors} 
  & Percentage of minimum elements included \\ \hline

2 & NULL 
  & NULL
  & Depth of dependency graph \\ \hline

3 & NULL 
  & NULL
  & Divergence between statically and dynamically created SBOM \\ \hline

4 & CycloneDX extension property presence 
  & Taxonomy usage (e.g., \texttt{cdx:} prefix) 
  & Degree of lossyness of conversion \\ \hline

5 & Build profile presence 
  & Presence of \texttt{formulation} or \texttt{annotations} 
  & NULL \\ \hline

6 & profileConformance presence 
  & Presence of \texttt{formulation.workflow} 
  & Percentage of noAssertion fields out of total fields \\ \hline

7 & PURL format correctly followed 
  & Presence of \texttt{compositions} 
  & Divergence between packages representing the same dependency but using different tools \\ \hline

8 & relationshipType presence 
  & Valid Package URL (purl) syntax 
  & Profileration of static injection of library not used in code \\ \hline
\end{tabular}
}
\caption{SPDX and CycloneDX mitigation checks and corresponding problem tests}
\label{tab:combined_sbom_checks}
\end{table}
% \begin{table}[h]
% \centering
% \begin{tabular}{|l|p{3.5cm}|p{3.5cm}|}
% \hline
%  & \textbf{Check for guardrails} & \textbf{Test for issue} \\ \hline
% 1 & Lite profile presence & Percentage of minimum elements included \\ \hline
% 2 & Set of 'relationshipType' present & Depth of relationship graph \\ \hline
% 3 & NULL & Divergence between statically and dynamically created SBOM \\ \hline
% 4 & CycloneDX extension property presence & Degree of lossyness of conversion \\ \hline
% 5 & Build profile presence & Measuring reproducibility of build \\ \hline
% 6 & profileConformance presence & Percentage of noAssertion fields out of total fields \\ \hline
% 7 & PURL format correctly followed & Divergence between packages representing the same dependency but using different tools \\ \hline
% 8 & relationshipType presence & Profileration of static injection of library not used in code \\ \hline
% \end{tabular}
% \caption{SPDX mitigation checks and corresponding problem tests}
% \end{table}

% \begin{table}[h]
% \centering
% \resizebox{\columnwidth}{!}{%
% \begin{tabular}{|l|p{3.8cm}|p{3.8cm}|}
% \hline
%  & \textbf{Check for guardrails} & \textbf{Test for issue} \\ \hline
% 1 & Presence of \texttt{metadata.supplier}, \texttt{timestamp}, and \texttt{authors} & Percentage of CISA required elements (7 fields) present \\ \hline
% 2 & Dependency graph depth $>1$ & Coverage of components appearing in the dependency graph \\ \hline
% 3 & N/A (No spec solution) & Standardization score (PURL + Hash presence) \\ \hline
% 4 & Taxonomy usage (e.g., \texttt{cdx:} prefix) & Fragmentation score (ad-hoc vs registered property names) \\ \hline
% 5 & Presence of \texttt{formulation} or \texttt{annotations} & Usage rate of advanced CycloneDX features \\ \hline
% 6 & Presence of \texttt{formulation.workflow} & Reproducibility score (hashes + environment data) \\ \hline
% 7 & Presence of \texttt{compositions} & Rate of missing completeness assertions \\ \hline
% 8 & Valid Package URL (purl) syntax & PURL coverage rate per SBOM \\ \hline
% \end{tabular}
% }
% \caption{CycloneDX Mitigation checks and corresponding problem measurements}
% \label{tab:cdx_test_cases}
% \end{table}

\newpage

\subsubsection{Use of test cases\\}

\textbf{\\SPDX\\}

The results of the test cases are present in table \ref{tab:spdx_test_results}.

\textbf{\\CycloneDX\\}

To validate the practical impact of the structural issues identified in Section 4.3.2, we developed a corresponding test suite for CycloneDX. We utilized the GitHub Code Search API to collect a dataset of 128 valid CycloneDX 1.6 SBOMs from public repositories.

We applied the test cases defined in Table \ref{tab:combined_sbom_checks} to our dataset of 128 CycloneDX 1.6 SBOMs. The analysis reveals a significant gap between specification capabilities and real-world adoption.

\paragraph{CISA Compliance Gap (TC1):}
Our measurement confirms the structural weakness identified in Section 4.3.2. Only \textbf{2.3\%} (3/128) of the analyzed SBOMs met the full CISA minimum requirements. The \texttt{supplier} field, which is optional in the CycloneDX schema, was missing in 96.1\% of the samples. This validates that optionality in the standard leads directly to non-compliance in practice.

\paragraph{Transitive Dependency Blindness (TC2):}
Despite the graph-based capabilities of CycloneDX, \textbf{57\%} of SBOMs either lacked a dependency graph entirely or only captured direct dependencies (Depth $\le 1$). This creates a "shallow visibility" problem where vulnerabilities in transitive dependencies (e.g., Log4j) remain undetectable.

\paragraph{The Reproducibility Void (TC6):}
While CycloneDX 1.6 introduced the \texttt{formulation} object to address build integrity \cite{reproduciblebuildsforne}, we found \textbf{0\%} adoption of this feature in the wild. This suggests that complex, optional security features in specifications are ignored by tool developers in favor of basic inventory generation.

\paragraph{Checkbox Compliance (TC7):}
We measured the usage of \texttt{compositions} to assert completeness. \textbf{98.4\%} of SBOMs made no assertion regarding their completeness (neither "complete" nor "incomplete"). This creates an ambiguity where consumers cannot distinguish between a thorough SBOM and a partial one, validating concerns regarding "checkbox compliance" \cite{maintainersvulnmgmtwermke}.

\paragraph{Standardization Success (TC8):}
Conversely, we found high adherence to Package URL (PURL) standards. \textbf{63.3\%} of SBOMs achieved high PURL coverage ($>80\%$), and cross-tool consistency was high ($>92\%$). This indicates that extensive specification guidance (as seen with PURL in the appendices) effectively drives standardization, whereas loose optional fields (like \texttt{properties}) lead to fragmentation.

\begin{table*}[ht]
\centering
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}|l|c c c c | c c c c|}
\hline
& \textbf{Guardrails} & & & & \textbf{Issues} & & & \\
\hline
& \textbf{microsoft tool} & \textbf{spdx-generator} & \textbf{syft} & \textbf{trivy} & \textbf{microsoft tool} & \textbf{spdx-generator} & \textbf{syft} & \textbf{trivy} \\
\hline
\textbf{Minimum elements} & 0\% & - & - & - & 91.7\% & 58.3\% & 41.7\% & 66.7\% \\
\textbf{Transitive dependencies} & 4 & 6 & 6 & 6 & 3 & 3 & 2 & 2 \\
\textbf{Metadata parsing} & - & - & - & - & 62\% & 39\% & 28\% & 27\% \\
\textbf{Interoperability} & 0\% & - & - & - & 19\% & 22\% & 27\% & 26\% \\
\textbf{Reproducibility} & 0\% & - & - & - & ? & ? & ? & ? \\
\textbf{Superficial compliance} & 100\% & - & - & - & 18\% & 28\% & 8\% & 5\% \\
\textbf{Package naming} & 12\% & 10\% & 16\% & 25\% & 0\% & 0\% & 0\% & 0\% \\
\textbf{Dynamic dependencies} & 100\% & 100\% & 100\% & 100\% & 100\% & 100\% & 100\% & 100\% \\
\hline
\end{tabular*}
\caption{Results of SPDX test cases}
\label{tab:spdx_test_results}
\end{table*}"



Show more
22 Apr, 11:52

Use this reply to your advisor:

Thank you, this is helpful.

I see the issue with the current subsection. It reads more like discussion than results, and I need to support each claim with clearer evidence from the specification, prior empirical work, and concrete examples.

I have not yet inspected SBOM generator implementations directly, but I can do that next. I can trace how selected generators populate:

dependency graphs
supplier, timestamp, and authors
scope and completeness related fields
I also take the point about SBOM quality tools. At the moment, the main one I have identified is sbomqs, so I can position our work against what sbomqs checks well and what it cannot check when the specification itself is underspecified.

I will revise Section 4.2.3 accordingly. In particular, I will make it result driven and evidence backed, including the concrete CycloneDX issues around production step and scope discussed in Balliu et al. I will also follow up with a smaller implementation focused comparison rather than a broad measurement study.

Replace your current \subsubsection{CycloneDX Revisited Through a Security Lens} with this:

\subsubsection{CycloneDX Security Relevant Guardrails}
\label{subsec:cdx_security_results}

The thematic distribution in Table~\ref{tab:cdx_theme_distribution} shows where CycloneDX 1.6 allocates normative attention, but it does not by itself show whether these requirements provide strong baseline protection against the failures identified in Section~\ref{subsec:systematization}. We therefore re examined the extracted requirements with a narrower question: which known SBOM failure modes are directly constrained by CycloneDX, how strong those constraints are, and whether they can be checked from the SBOM artifact itself.

This second pass shows a consistent pattern. CycloneDX is strict once a producer chooses to populate a field or object, but it is often permissive about whether the security relevant object must appear at all. The result is that local object integrity is usually well constrained, while baseline security sufficiency is not.

\paragraph{Minimum elements are weakly enforced.}
CycloneDX contains fields for provenance and authorship, but it does not require them at the metadata level. In particular, \texttt{metadata.supplier}, \texttt{metadata.authors}, and \texttt{metadata.timestamp} are optional. This is a concrete weakness for the first failure mode in Section~\ref{subsec:systematization}, since these fields are central to the CISA minimum elements. The implication is direct: a CycloneDX document may be valid while still omitting core provenance information needed for policy and vulnerability management workflows. This is not merely a theoretical concern. Our schema comparison in Section 4.3.1 shows that the official JSON schema also leaves these fields non mandatory, so this weakness is preserved in actual validation practice.

\paragraph{Dependency completeness is only partly constrained.}
CycloneDX contains an explicit dependency graph model through the root \texttt{dependencies} array. When this graph is present, the specification is locally strict. Each item must be a Dependency object, each dependency must contain a \texttt{ref}, and components or services without dependencies must still appear as empty elements in the graph. However, the root \texttt{dependencies} object itself remains optional, and the stronger statement about completeness is phrased only as guidance: SBOMs should ideally contain all direct and transitive components and the dependency relationships between them. This means the standard constrains dependency graphs if they are present, but does not require a producer to provide one. As a result, CycloneDX offers only partial protection against transitive dependency omission.

\paragraph{Population semantics remain underspecified.}
A key limitation is that CycloneDX often specifies representation without clearly specifying population. This point is supported by prior empirical work on Java SBOM production \cite{balliu2023sbomjava}. Balliu et al. show that producers generate CycloneDX SBOMs at different points in the software lifecycle, including source, build, and post packaging stages, and note that the standard does not clearly require producers to state or justify the production step they use. This matters because the set of observable dependencies can change substantially across these stages. The same study also shows disagreement in the use of the \texttt{scope} field. For the same dependency, some producers report \texttt{optional}, others report \texttt{required}, and others omit the field entirely. Because the specification does not clearly define how scope should be computed, these outputs cannot be reliably adjudicated against the standard. This is concrete evidence that CycloneDX can encode security relevant distinctions while still leaving the population process underspecified.

\paragraph{Advanced security objects exist, but they are dormant by default.}
CycloneDX 1.6 includes rich structures for vulnerability communication, build provenance, completeness assertions, and higher assurance use cases. Examples include \texttt{vulnerabilities}, \texttt{analysis}, \texttt{formulation}, and \texttt{compositions}. These objects are important because they relate directly to several of the failure modes in Section~\ref{subsec:systematization}, including reproducibility, checkbox compliance, and vulnerability context. However, these structures remain optional at the root level. This means the standard has the vocabulary needed to express important security properties, but it does not make those properties part of the baseline SBOM. In practical terms, these guardrails remain dormant unless the producer voluntarily opts into them.

\paragraph{Normalization is stronger than semantic consistency.}
CycloneDX provides useful normalization mechanisms for package identity. Fields such as \texttt{purl}, \texttt{cpe}, \texttt{swhid}, \texttt{omniborId}, and \texttt{swid} must conform to external specifications when present. This is a genuine strength for reducing package naming inconsistency. However, the same level of discipline is not applied to the \texttt{properties} mechanism. The specification recommends use of the CycloneDX Property Taxonomy, but formal registration remains optional. This gives producers a flexible extension mechanism, but also leaves room for semantic fragmentation across tools. Thus, CycloneDX is stronger at normalizing identifiers than at normalizing producer defined metadata.

These results suggest that CycloneDX is best understood as a strong representation standard with weak baseline guarantees for security sufficient SBOM generation. Its main limitation is not lack of expressiveness. Rather, the limitation is that many of its most security relevant controls are optional, conditional, or underspecified at the point where tools must actually populate them. This helps explain why tool inconsistency can persist even when tools produce schema valid and standard conformant output.

\begin{table*}[t]
\caption{CycloneDX guardrails against known SBOM failure modes}
\label{tab:cdx_security_guardrails}
\centering
\small
\begin{tabular}{p{3.4cm} p{5.1cm} p{2.2cm} p{3.0cm}}
\toprule
\textbf{Failure mode} & \textbf{Relevant CycloneDX mechanism} & \textbf{Strength} & \textbf{Verifiability} \\
\midrule
Failure to meet minimum elements &
\texttt{metadata.supplier}, \texttt{metadata.authors}, and \texttt{metadata.timestamp} exist, but all are optional &
Weak &
Artifact verifiable when present \\
\addlinespace[2pt]

Transitive dependency omission &
\texttt{dependencies} supports graph representation, but the object is optional and transitive completeness is only recommended &
Weak to Moderate &
Partly artifact verifiable \\
\addlinespace[2pt]

Metadata parsing divergence &
The standard provides little guidance on how metadata should be extracted from source, environment, or build context &
None to Very Weak &
Not artifact verifiable \\
\addlinespace[2pt]

Interoperability loss &
Typed identifiers and references are strongly constrained when present, but \texttt{properties} remain loosely governed &
Mixed &
Partly artifact verifiable \\
\addlinespace[2pt]

Reproducibility gap &
\texttt{formulation} can represent build provenance and workflow detail, but it is optional &
Dormant &
Artifact verifiable when present \\
\addlinespace[2pt]

Checkbox compliance &
\texttt{compositions} can express completeness claims, but it is optional &
Weak &
Artifact verifiable when present \\
\addlinespace[2pt]

Package naming inconsistency &
\texttt{purl}, \texttt{cpe}, \texttt{swhid}, \texttt{omniborId}, and \texttt{swid} support normalized identity &
Moderate &
Artifact verifiable \\
\addlinespace[2pt]

Runtime blind spot &
The model can represent runtime relevant information, but it does not require a baseline distinction between present and actually used components &
Weak &
Requires external context \\
\bottomrule
\end{tabular}
\end{table*}
This version is better because it:

reads as findings, not reflection
cites a concrete prior study for production step and scope
ties each claim to a specific failure mode
keeps the security angle, but makes it evidential
You can keep it in the same place, right after \subsubsection{CycloneDX} and before \subsection{Practical applicability of the standards}.





22 Apr, 11:53
do i need to add any new addition into references.bib or no?
22 Apr, 11:59

Yes, if you cite the Java paper as \cite{balliu2023sbomjava}, you need to add it to references.bib.

Use this BibTeX entry:

@article{balliu2023sbomjava,
  title = {Challenges of Producing Software Bill of Materials for Java},
  author = {Balliu, Musard and Baudry, Benoit and Bobadilla, Sofia and Ekstedt, Mathias and Monperrus, Martin and Ron, Javier and Sharma, Aman and Skoglund, Gabriel and Soto-Valero, C{\'e}sar and Wittlinger, Martin},
  journal = {arXiv preprint arXiv:2303.11102},
  year = {2023},
  url = {https://arxiv.org/abs/2303.11102}
}
If you do not use that citation in the rewritten subsection, then no new references.bib entry is needed.





22 Apr, 12:00
i have replaced the contents:"\section{Results}
\label{sec:results}

\subsection{Finding list of known issues in SBOM generation}
\label{subsec:systematization}

Below is a list of the problems that need to be addressed:
\begin{enumerate}
\item Failure to meet the minimum elements specified by the CISA guidelines \cite{cmuplugfest}.
\item Transitive dependencies are missed \cite{differentialanalysisyu}.
\item Tools employ different methodologies for parsing metadata \cite{differentialanalysisyu}. Additionally, there is a lack of standardised meta-data formats in and across languages further preventing a single methodology to encompass every possibility. \cite{pythonsboms, javasboms}
\item Interoperability issues where one tool produces a better SBOM for one format over another \cite{bomsaway}.
\item Lack of reproducibility in the builds on which SBOMs are created. \cite{reproduciblebuildsforne}
\item View of SBOMs as unncessary and merely a compliance checkbox. \cite{maintainersvulnmgmtwermke}
\item Inconsistencies in the naming of packages. \cite{differentialanalysisyu}
\item Inability to capture whether a libary was actually loaded onto memory or not due to the static nature of an SBOM. \cite{nodeshieldcornelissen}
\end{enumerate}

We analyse each of the specifications according to each of the problems above and address them. We focus on what aspects of the specifications try to address these issues, and which of these issues do the specifications not address.


\subsection{Reproducible thematic analysis}

\subsubsection{SPDX}

The SPDX standard prescribes the structure, content, and conformance requirements for SBOM generation. Profiles in SPDX 3.0.1 are central to this architecture; they represent modular subsets of the full specification that allow SBOM authors to tailor the level of expressiveness and complexity to their specific use case. There are 8 profiles available, out of which only the core profile is mandatory and all the rest are optional: core, software, security, licensing, dataset, AI, build, lite, and extension profiles. % I need to explain profiles better but I am unsure how to

The document is organized into three major sections: (1) an introduction that provides guidance on how to interpret the overall structure alongside some overarching and legal rules; (2) a detailed description of the available profiles, including the classes, properties, definitions, and special requirements associated with each; and (3) an appendix that offers practical guidance such as a Lite-profile example SBOM and an extensive discussion of Package URL (purl) syntax.


Below is a description of each of the themes that was created. A distribution of the themes is shown in Table \ref{tab:spdx_theme_distribution}:
\begin{itemize}
    \item \textbf{Class-specific rules (57\%)}: Requirements defining the structure or content of what a class in SPDX may contain. It is further split into two categories, rules defining the properties a class may contain or the rules defining what the content inside these properties may be.
    \item \textbf{Overarching conformance (22\%)}: Requirements which are generalized and cannot be associated with any other theme. These are further split into three categories, requirements which apply to the core profile (thus every SBOM), requirements which apply only to the lite profile, and requirements which apply only to any other profile, excluding the core and lite profiles.
    \item \textbf{Serialization (6\%)}: Requirements about how to format an SBOM document. These are further divided into two, requirements which apply to only JSON-LD serialization and requirements which are more general.
    \item \textbf{Syntax (13\%)}: Syntactic requirements for writing SPDX license strings, creating old-style templates to match non-standard licenses, and requirements for correctly creating, reading, and handling Package URLs (purl).
    \item \textbf{Legal (2\%)}: Requirements relating to the legal side of using SBOMs, specifically how to use the SPDX name and reusing the specification document, and requirements for comparing license texts and interpreting approval flags.
\end{itemize}

\begin{table}[t]
\caption{Distribution of Thematic Categories in SPDX 3.0.1 Requirements}
\label{tab:spdx_theme_distribution}
\centering
\begin{tabular}{@{}ll@{}}
\toprule
\textbf{Theme} & \textbf{Percentage} \\ 
\midrule

\textbf{Class-Specific Rules} & \textbf{57}\% \\
\hspace{1.5em}Class Structure Rules & 49\% \\
\hspace{1.5em}Class Content Rules & 8\% \\[4pt]

\textbf{Overarching Conformance} & \textbf{22}\% \\
\hspace{1.5em}General Conformance & 2\% \\
\hspace{1.5em}Lite Profile Conformance & 17\% \\
\hspace{1.5em}Profile-Specific Conformance & 3\% \\[4pt]

\textbf{Serialization} & \textbf{6}\% \\
\hspace{1.5em}General Serialization & 5\% \\
\hspace{1.5em}JSON-LD Serialization & 1\% \\[4pt]

\textbf{Syntax} & \textbf{13}\% \\
\hspace{1.5em}Legacy Template Syntax & 1\% \\
\hspace{1.5em}License Expression Syntax & 1\% \\
\hspace{1.5em}Package URL (purl) Syntax & 11\% \\[4pt]

\textbf{Legal} & \textbf{2}\% \\
\hspace{1.5em}Legal Requirements & 1\% \\
\hspace{1.5em}License-Matching Requirements & 1\% \\

\bottomrule
\end{tabular}
\end{table}

We conclude that the focus of the SPDX 3.0.1 specifications is mainly on class-specific rules, which it defines and then these can be used to create objects which can be used to represent different aspects of an SBOM. However, the 6:1 ratio between class structure rules and class content rules shows SPDX 3.0.1's importance over maintaining the structure of the SBOM over its semantics. We also note notable focus into lite profile conformance to give a starting point for new developers to create a basic SBOM to fulfil the basic requirements. Moreover, the purl syntax is extensively discussed, which shows an effort to ensure that the packages are kept universally consistent once included in an SBOM.

\subsubsection{CycloneDX}

Our analysis of the 1,724 normative requirements from CycloneDX 1.6 reveals a specification distinct from SPDX in its emphasis on specialized security use cases. We categorized requirements into seven high-level themes (Table \ref{tab:cdx_theme_distribution}).

\begin{table}[t]
\caption{Distribution of Thematic Categories in CycloneDX 1.6 Requirements}
\label{tab:cdx_theme_distribution}
\centering
%\resizebox{\columnwidth}{!}{%
\begin{tabular}{@{}ll@{}}
\toprule
\textbf{Theme} & \textbf{Percentage} \\ 
\midrule

\textbf{Advanced \& Specialized Data Models} & \textbf{35.3}\% \\
\hspace{1.5em}Cryptographic Asset Mgmt (CBOM) & 12.8\% \\
\hspace{1.5em}Formulation \& Reproducibility & 8.8\% \\[4pt]

\textbf{Foundational BOM Structure} & \textbf{17.8}\% \\
\hspace{1.5em}Internal Referencing (bom-ref) & 15.1\% \\
\hspace{1.5em}BOM Identification & 1.1\% \\[4pt]

\textbf{Trust, Integrity, and Security} & \textbf{16.0}\% \\
\hspace{1.5em}Vulnerability Information & 6.2\% \\
\hspace{1.5em}Cryptographic Hashes & 4.4\% \\[4pt]

\textbf{Metadata \& Provenance} & \textbf{12.8}\% \\
\hspace{1.5em}Organizational Entity Definition & 6.3\% \\
\hspace{1.5em}Contact Information & 3.8\% \\[4pt]

\textbf{Extensibility and Customization} & \textbf{6.6}\% \\
\hspace{1.5em}Extensibility via Properties & 3.8\% \\
\hspace{1.5em}Property Taxonomies & 2.8\% \\[4pt]

\textbf{Core Inventory \& Attributes} & \textbf{6.4}\% \\
\hspace{1.5em}Descriptive Metadata & 2.1\% \\
\hspace{1.5em}Standardized Ext. Identifiers & 2.1\% \\[4pt]

\textbf{Relationships \& Composition} & \textbf{5.2}\% \\
\hspace{1.5em}External References & 2.7\% \\
\hspace{1.5em}Dependency Graph Representation & 1.3\% \\

\bottomrule
\end{tabular}
%}
\end{table}

The analysis highlights that CycloneDX allocates the largest portion of its normative text (35.3\%) to \textbf{Advanced and Specialized Data Models}, specifically for Cryptography (CBOM) and Build Formulation. In contrast, the \textbf{Core Inventory} theme—which covers basic component definitions—comprises only 6.4\% of the requirements. This structural imbalance suggests the standard is optimized for complex, high-maturity security use cases rather than basic inventory management.

% \subsubsection{CycloneDX Revisited Through a Security Lens}
% \label{subsec:cdx_security_lens}

\subsubsection{CycloneDX Security Relevant Guardrails}
\label{subsec:cdx_security_results}

The thematic distribution in Table~\ref{tab:cdx_theme_distribution} shows where CycloneDX 1.6 allocates normative attention, but it does not by itself show whether these requirements provide strong baseline protection against the failures identified in Section~\ref{subsec:systematization}. We therefore re examined the extracted requirements with a narrower question: which known SBOM failure modes are directly constrained by CycloneDX, how strong those constraints are, and whether they can be checked from the SBOM artifact itself.

This second pass shows a consistent pattern. CycloneDX is strict once a producer chooses to populate a field or object, but it is often permissive about whether the security relevant object must appear at all. The result is that local object integrity is usually well constrained, while baseline security sufficiency is not.

\paragraph{Minimum elements are weakly enforced.}
CycloneDX contains fields for provenance and authorship, but it does not require them at the metadata level. In particular, \texttt{metadata.supplier}, \texttt{metadata.authors}, and \texttt{metadata.timestamp} are optional. This is a concrete weakness for the first failure mode in Section~\ref{subsec:systematization}, since these fields are central to the CISA minimum elements. The implication is direct: a CycloneDX document may be valid while still omitting core provenance information needed for policy and vulnerability management workflows. This is not merely a theoretical concern. Our schema comparison in Section 4.3.1 shows that the official JSON schema also leaves these fields non mandatory, so this weakness is preserved in actual validation practice.

\paragraph{Dependency completeness is only partly constrained.}
CycloneDX contains an explicit dependency graph model through the root \texttt{dependencies} array. When this graph is present, the specification is locally strict. Each item must be a Dependency object, each dependency must contain a \texttt{ref}, and components or services without dependencies must still appear as empty elements in the graph. However, the root \texttt{dependencies} object itself remains optional, and the stronger statement about completeness is phrased only as guidance: SBOMs should ideally contain all direct and transitive components and the dependency relationships between them. This means the standard constrains dependency graphs if they are present, but does not require a producer to provide one. As a result, CycloneDX offers only partial protection against transitive dependency omission.

\paragraph{Population semantics remain underspecified.}
A key limitation is that CycloneDX often specifies representation without clearly specifying population. This point is supported by prior empirical work on Java SBOM production \cite{balliu2023sbomjava}. Balliu et al. show that producers generate CycloneDX SBOMs at different points in the software lifecycle, including source, build, and post packaging stages, and note that the standard does not clearly require producers to state or justify the production step they use. This matters because the set of observable dependencies can change substantially across these stages. The same study also shows disagreement in the use of the \texttt{scope} field. For the same dependency, some producers report \texttt{optional}, others report \texttt{required}, and others omit the field entirely. Because the specification does not clearly define how scope should be computed, these outputs cannot be reliably adjudicated against the standard. This is concrete evidence that CycloneDX can encode security relevant distinctions while still leaving the population process underspecified.

\paragraph{Advanced security objects exist, but they are dormant by default.}
CycloneDX 1.6 includes rich structures for vulnerability communication, build provenance, completeness assertions, and higher assurance use cases. Examples include \texttt{vulnerabilities}, \texttt{analysis}, \texttt{formulation}, and \texttt{compositions}. These objects are important because they relate directly to several of the failure modes in Section~\ref{subsec:systematization}, including reproducibility, checkbox compliance, and vulnerability context. However, these structures remain optional at the root level. This means the standard has the vocabulary needed to express important security properties, but it does not make those properties part of the baseline SBOM. In practical terms, these guardrails remain dormant unless the producer voluntarily opts into them.

\paragraph{Normalization is stronger than semantic consistency.}
CycloneDX provides useful normalization mechanisms for package identity. Fields such as \texttt{purl}, \texttt{cpe}, \texttt{swhid}, \texttt{omniborId}, and \texttt{swid} must conform to external specifications when present. This is a genuine strength for reducing package naming inconsistency. However, the same level of discipline is not applied to the \texttt{properties} mechanism. The specification recommends use of the CycloneDX Property Taxonomy, but formal registration remains optional. This gives producers a flexible extension mechanism, but also leaves room for semantic fragmentation across tools. Thus, CycloneDX is stronger at normalizing identifiers than at normalizing producer defined metadata.

These results suggest that CycloneDX is best understood as a strong representation standard with weak baseline guarantees for security sufficient SBOM generation. Its main limitation is not lack of expressiveness. Rather, the limitation is that many of its most security relevant controls are optional, conditional, or underspecified at the point where tools must actually populate them. This helps explain why tool inconsistency can persist even when tools produce schema valid and standard conformant output.

\begin{table*}[t]
\caption{CycloneDX guardrails against known SBOM failure modes}
\label{tab:cdx_security_guardrails}
\centering
\small
\begin{tabular}{p{3.4cm} p{5.1cm} p{2.2cm} p{3.0cm}}
\toprule
\textbf{Failure mode} & \textbf{Relevant CycloneDX mechanism} & \textbf{Strength} & \textbf{Verifiability} \\
\midrule
Failure to meet minimum elements &
\texttt{metadata.supplier}, \texttt{metadata.authors}, and \texttt{metadata.timestamp} exist, but all are optional &
Weak &
Artifact verifiable when present \\
\addlinespace[2pt]

Transitive dependency omission &
\texttt{dependencies} supports graph representation, but the object is optional and transitive completeness is only recommended &
Weak to Moderate &
Partly artifact verifiable \\
\addlinespace[2pt]

Metadata parsing divergence &
The standard provides little guidance on how metadata should be extracted from source, environment, or build context &
None to Very Weak &
Not artifact verifiable \\
\addlinespace[2pt]

Interoperability loss &
Typed identifiers and references are strongly constrained when present, but \texttt{properties} remain loosely governed &
Mixed &
Partly artifact verifiable \\
\addlinespace[2pt]

Reproducibility gap &
\texttt{formulation} can represent build provenance and workflow detail, but it is optional &
Dormant &
Artifact verifiable when present \\
\addlinespace[2pt]

Checkbox compliance &
\texttt{compositions} can express completeness claims, but it is optional &
Weak &
Artifact verifiable when present \\
\addlinespace[2pt]

Package naming inconsistency &
\texttt{purl}, \texttt{cpe}, \texttt{swhid}, \texttt{omniborId}, and \texttt{swid} support normalized identity &
Moderate &
Artifact verifiable \\
\addlinespace[2pt]

Runtime blind spot &
The model can represent runtime relevant information, but it does not require a baseline distinction between present and actually used components &
Weak &
Requires external context \\
\bottomrule
\end{tabular}
\end{table*}


\subsection{Practical applicability of the standards}

\subsubsection{Intra-specification consistency}

Our analysis revealed significant discrepancies in both specifications, indicating that the official schemas often diverge from the normative text.

\begin{itemize}
    \item \textbf{SPDX 3.0.1:} No differences were found in Definition Presence and Property Presence. However, a total of 30 differences were found in Property Type. In 14 cases, the official schema was more lax than the normative text, allowing a property to be a constant/ string as well as an object using the 'oneOf' condition. In 16 cases, the official schema was more strict than the normative text, where it applied 2 regexes instead of 1 using the 'allOf' condition in DateTime strings.
    
    \item \textbf{CycloneDX 1.6:} Our differential analysis between the prescriptive prose and the official JSON schema reveals a critical \textbf{CISA Compliance Gap}. 
        
    The CISA guidelines mark "Supplier Name", "Author Name", and "Timestamp" as \textbf{REQUIRED}. However, the official CycloneDX 1.6 JSON Schema defines \texttt{metadata.supplier}, \texttt{metadata.authors}, and \texttt{metadata.timestamp} as non-mandatory fields (no \texttt{required} constraint in JSON Schema). 
        
    Consequently, a JSON file can validate perfectly against the CycloneDX schema while failing to meet the federal minimum requirements. Additionally, our automated check found 38 granular constraint mismatches, including \texttt{specVersion} not enforcing the value '1.6' in the schema, despite the text mandating it.
    
\end{itemize}

\subsubsection{Conditionality analysis}

Our findings demonstrate that both specifications are overwhelmingly conditional, though they achieve this through different architectural patterns:
\begin{itemize}
    \item \textbf{SPDX 3.0.1:} Out of 429 extracted requirements, only \textbf{69 (16\%)} are applicable to the minimum template SBOM. The majority of requirements are conditional based on \textit{Class Instantiation} (242 cases) or \textit{Profile Conformance} (93 cases). This structural heavy-handedness allows for "valid but empty" SBOMs, where the topology is enforced, but data richness is optional.
    
    \item \textbf{CycloneDX 1.6:} Out of 1,724 requirements, only \textbf{6 (0.35\%)} are universally applicable to the minimum purposeful SBOM.

    The standard utilizes an architecture where requirements are conditional upon the presence of optional root-level objects. Our analysis identified exactly \textbf{56} normative requirements governing Machine Learning Model Cards (ML-BOM) and \textbf{151} requirements governing Formulation (build reproducibility). However, because the root \texttt{modelCard} and \texttt{formulation} objects are defined as \textbf{OPTIONAL} (MAY), these 207 combined requirements remain dormant unless a user voluntarily attempts to implement those specific features.
    
    This confirms that CycloneDX conformance is highly dynamic: a tool can be compliant while implementing less than 1\% of the specification, provided it does not attempt to use advanced features incorrectly.
    
\end{itemize}

To further investigate the structural mechanisms enabling this conditionality, we performed a topological analysis of the Prescriptive Schema. We calculated the Breadth (direct reuse count), Ancestor Count (complexity), and Max Depth for all CycloneDX classes. Table~\ref{tab:cdx_metrics} presents the metrics for the most structurally critical classes.

Three key architectural patterns emerge from this data:
\begin{itemize}
    \item \textbf{Graph Connectivity:} The \texttt{refType} class is the most reused definition (Breadth 25). This confirms the standard operates as a loosely connected graph of string references rather than a strict hierarchy.
    \item \textbf{Generic Extensions:} The \texttt{property} class is the second most reused structure (Breadth 17). This indicates a systemic reliance on generic key-value pairs over standardized schema fields.
    \item \textbf{Isolated Roots:} Major functional classes like \texttt{vulnerability} and \texttt{formula} exhibit zero Breadth, confirming they exist as isolated "silos" that do not enforce structural dependencies on the core component inventory.
\end{itemize}

\begin{table}[h]
\caption{Structural Metrics of Top 10 Critical CycloneDX 1.6 Classes.}
\label{tab:cdx_metrics}
\centering
\small
\begin{tabular}{@{}l c c l@{}}
\toprule
\textbf{Class Name} & \textbf{Breadth} & \textbf{Anc.} & \textbf{Structural Role} \\
\midrule
refType & 25 & 41 & Graph Connectivity \\
property & 17 & 25 & Generic Extension \\
signature & 12 & 18 & Integrity \\
organizationalEntity & 10 & 25 & Entity Definition \\
attachmentText & 10 & 31 & Inline Data \\
component & 6 & 8 & Core Inventory \\
vulnerability & 0 & 0 & Isolated Root \\
\bottomrule
\end{tabular}
\end{table}

\begin{table}[t]
\caption{Distribution of SPDX 3.0.1 Conditional Requirements by Dependency Type}
\label{tab:spdx_dependency_types}
\centering
\small
\begin{tabular}{@{}lcl@{}}
\toprule
\textbf{Type} & \textbf{Number of Cases} & \textbf{Description} \\
\midrule
Class & 242 & Instantiation of a class. \\
Profile & 93 & Conformance to a profile. \\
Property & 56 & Presence of a property. \\
DataType & 3 & Presence of a DataType. \\
Serialization & 5 & Specific serialization used. \\
\bottomrule
\end{tabular}
\end{table}

\subsubsection{Comparison with CISA minimum elements}

Our extraction of 133 normative requirements from the CISA "Framing" document reveals a distinct bifurcation in prescriptive intent. The thematic distribution is heavily skewed toward two categories: \textbf{Component \& SBOM Attributes} (36\%) and \textbf{SBOM Operations \& Lifecycle} (29\%).

Critically, we observe a divergence in the normative keywords used between these themes:
\begin{itemize}
    \item \textbf{Operations are Mandatory:} The \textit{Operations} theme is dominated by \textbf{REQUIRED} keywords (e.g., "An SBOM needs to be created when a Component is released"). This establishes a rigid policy baseline for \textit{when} and \textit{how} SBOMs are exchanged.
    \item \textbf{Data Quality is Aspirational:} The \textit{Component Attributes} theme frequently uses \textbf{SHOULD} or \textbf{RECOMMENDED} (e.g., "Supplier Name should be identified carefully" and "list as many globally unique identifiers as available"). 
\end{itemize}

This creates a regulatory concern where the process of generating an SBOM is strictly enforced, but the data quality within that SBOM is often relegated to "Recommended Practice" rather than "Minimum Expectation," allowing tools to produce operationally valid but semantically poor data.

\subsection{Dependency resolution mechanisms in action}

\subsubsection{Results - SPDX 3.0.1\\\\}
\textbf{Analysis of requirements} 

A dependency graph contains two parts in SPDX: the edges of the graph are expressed by using the 'Relationship' class in SPDX 3.0.1. The summary of relationship is as follows:

\begin{quote}
    "Describes a relationship between one or more elements."
\end{quote}

The nodes of the graph are represented by the abstract class ‘Element’. The description states the following:

\begin{quote}
	“Within SPDX-3.0 structure this is the base class acting as a consistent, unifying, and interoperable foundation for all explicit and inter-relatable content objects.”
\end{quote}

In order to investigate dependency resolution, we isolate all requirements which refer to the relationship class or the \textbf{resolution} of the Element class or any of its subclasses. A total of 17 requirements were selected which encompassed the relationship class, the requirements reveal that the relationship class have a mandatory field 'relationshipType' of type 'RelationshipType', an enumeration of 62 possible types. Out of the 62 types, we choose \textbf{'dependsOn'} as the type to signal a dependency, which is consistent with the report in \cite{cmuplugfest}. Additionally, we also choose \textbf{‘contains’} to signal a dependency.

Out of the 17 requirements, they can be classified as the following:
\begin{enumerate}
    \item \textbf{SHOULD: 3 cases}. E.g: "To explicitly assert that no such relationships exist, the to property SHOULD contain the NoneElement individual and no other elements."
    \item \textbf{MUST: 2 cases}. E.g: "relationshipType $|$ RelationshipType $|$ 1 $|$ 1 (relationship MUST have a relationshipType)."
    \item \textbf{Class based requirements: 8 cases}.
    \item \textbf{Dependent MUST: 3 cases}. E.g: "The Licensing profile only contains the additional requirement that any Software Artifact MUST have a Relationship of type hasConcludedLicense."
    \item \textbf{Redundancy: 1 case}.\\
\end{enumerate}

\textbf{Test cases}

5 test cases were constructed using a python script, based on the MUST requirements. The 6th test case was added to replicate the testing done in \cite{cmuplugfest}. The 7th test case was added to identify the breadth of use of the relationship class in SPDX. These were the following final test cases:
\begin{enumerate}
    \item A relationship MUST not contain any additional elements to NoneElement in the ‘to’ property
    \item Relationship MUST have a relationshipType
    \item IF Licensing Profile THEN Software Artifact MUST have a type “hasConcludedLicense”
    \item IF Build Profile THEN Build element MUST have relationship of types: “hasInput”, “hasOutput”, and “invokedBy“
    \item IF Lite Profile THEN Software Package MUST have relationship of types “hasConcludedLicense” and “hasDeclaredLicense”
    \item Maximum depth of the dependency graph (based on relationshipType: dependsOn).
    \item Number of different types of relationshipTypes present.
\end{enumerate}

The test cases were then used on a dataset of 4 SBOMs. 3 were extracted from a GitHub repository officially recognised by the Linux foundation. The 4th one was generated using microsoft/sbom-tool. The results of the test cases are present in Table 2.

\textbf{Limitations\\}
Given how none of the SBOMs in the dataset were using the Licensing, Build, and Lite profile, it resulted in none of the dependent tests being applicable. Moreover, in test 6 for generated 1, the relationshipClass was actually 'DEPENDS\_ON' instead of 'dependsOn' in the specifications which led to the test case failing at first, before this being rectified after manual analysis. The relationshipTypes for generated 1 were all listed differently than in the specifications.

\begin{table}[h!]
\centering
\begin{tabular}{lccccc|cc}
\toprule
\textbf{SBOM} & \textbf{T1} & \textbf{T2} & \textbf{T3} & \textbf{T4} & \textbf{T5} & \textbf{T6} & \textbf{T7} \\
\midrule
Example 1 & $\checkmark$ & $\checkmark$ & $\circ$ & $\circ$ & $\circ$ & $\circ$ & 1 \\
Example 2 & $\checkmark$ & $\checkmark$ & $\circ$ & $\circ$ & $\circ$ & 2 & 6 \\
Example 3 & $\checkmark$ & $\checkmark$ & $\circ$ & $\circ$ & $\circ$ & $\circ$ & 8 \\
Generated 1 & $\checkmark$ & $\checkmark$ & $\circ$ & $\circ$ & $\circ$ & 3 & 4 \\
\bottomrule
\end{tabular}
\caption{Results of test cases from 4.4.1}
\end{table}

\subsubsection{Results - CycloneDX 1.6\\}
\label{subsec:dep_res_cdx}

\textbf{Analysis of requirements\\}
In CycloneDX, dependency relationships are explicitly modeled within the root-level \texttt{dependencies} array. The specification states, "Each item of this array must be a Dependency object." Our extraction yielded 24 normative requirements related to the \texttt{dependencies} object and its properties.

The core of the dependency graph is the \texttt{dependency} object, which has one REQUIRED property, \texttt{ref}, and one key optional property, \texttt{dependsOn}. A critical rule from the specification (Section 11.1) states:
\begin{quote}
    "Components or services that do not have their own dependencies MUST be declared as empty elements within the graph."
\end{quote}
This implies that every component listed in the main \texttt{components} array should have a corresponding entry in the \texttt{dependencies} graph, even if its \texttt{dependsOn} array is empty. Furthermore, the specification includes a key recommendation (Section 5.2):
\begin{quote}
    "SBOMs SHOULD ideally contain all direct and transitive components and the dependency relationships between them."
\end{quote}
These rules, particularly the ambiguity between the strict \texttt{MUST} for leaf node declaration and the softer \texttt{SHOULD} for transitive completeness, form the basis for our test cases, which are designed to detect common failures in graph integrity.

\textbf{Test cases}
Based on the normative requirements and the failures observed in prior empirical work \cite{sei-harmonization-report, jbomaudit}, we designed three pilot test cases to probe the structural and semantic integrity of dependency graphs in CycloneDX SBOMs.
\begin{description}
    \item[Test Case 1: The "Dangling Component."] This test verifies the \texttt{MUST} requirement from Section 11.1. It checks for any component listed in the main \texttt{components} array that does not have a corresponding entry in the \texttt{dependencies} array. Such a component is "dangling" because its dependency status is not explicitly declared, making the graph incomplete and violating a mandatory rule.
    
    \item[Test Case 2: The "Implicitly Missing Transitive Dependency."] This test targets the \texttt{SHOULD ideally} clause. The test SBOM correctly lists a direct dependency (e.g., \texttt{requests}) but omits a known transitive dependency (e.g., \texttt{urllib3}) while incorrectly declaring the direct dependency as a leaf node (\texttt{"dependsOn": []}). This scenario represents a critical vulnerability blind spot and is the exact problem identified in related work as a primary cause of "dependency depth variance."
    
    \item[Test Case 3: The "Detached Dependency Graph."] This test verifies the implicit structural rule that the dependency graph must connect to the primary component described by the SBOM (often defined in \texttt{metadata.component}). The test SBOM defines a main component in the metadata, but its \texttt{dependencies} graph is internally consistent but has no link back to this main component, making it a "detached" and contextually meaningless graph.
\end{description}
These test cases form the foundation of our proposed automated conformance framework. They move beyond simple schema validation to test for the deeper structural and semantic integrity required for reliable security analysis.

\subsection{Empirical verification of the issues present}

\subsubsection{Design of test cases\\\\}

\textbf{SPDX 3.0.1}:

\paragraph{(1) Failure to meet the minimum elements specified by the CISA guidelines}: SPDX v3.0.1 directly addresses compliance failures through the introduction of the Lite Profile. Recognizing that the complexity of the full standard often leads to incomplete SBOMs, the Lite Profile captures the absolute minimum set of information required for license compliance, meeting the CISA minimum elements in the way: \texttt{copyrightText}, \texttt{creationInfo}, \texttt{name}, \texttt{packageVersion}, \texttt{spdxId}, and \texttt{suppliedBy}.

By explicitly mapping these mandatory fields to the minimum elements defined by CISA, the standard removes the ambiguity that previously allowed tools to generate "compliant" but empty SBOMs. Thus, as long as an SBOM is conformant to the Lite Profile it follows the CISA guidelines.

However, given that conformance to the Lite Profile is not mandatory and only the Core Profile is, it still remains the case that an SBOM can be created in the SPDX 3.0.1 format which is fully conformant to the standard but does not meet the CISA guidelines.

\paragraph{(2) Transitive dependencies are missed:}
While static analysis tools often miss transitive dependencies in dynamic languages (e.g., Python, JavaScript), SPDX v3.0.1 addresses this via the \textbf{Build Profile} (Section 14). Unlike previous versions that relied heavily on static file manifest parsing, the Build Profile models the actual build instance. This data model encourages tools to record dependencies observed during the build process rather than estimating them from static manifest files, significantly reducing missed transitive components.

Furthermore, explicit Relationship Types such as \texttt{hasPrerequisite}, \texttt{hasDynamicLink}, and \texttt{hasStaticLink}, allow tools to distinguish between direct source dependencies and transitive runtime dependencies.

However, this requires tooling which can capture this relationship. Since most SBOM tools only support estimating dependencies from static manifest files, most SBOM generation tools will still miss transitive dependencies \cite{sbomlandscape}.

\paragraph{(3) Tools employ different methodologies for parsing metadata:}

Although the standard provides ways of making sure that any components extracted can be represented and verified in a universal manner by using the Package URL (purl) or Hash algorithms, they do not contain any information on best ways to parse metadata. This provides a hole for SBOM generation tools to fill, which leads to inconsistencies since they can choose a variety of going about it.\\
Although SPDX 3.0.1 allows metadata to be mapped to a universal graph using the Resource Description Framework (RDF), it contains no fields where it can be noted what metadata should be preferred or used in component extraction. Considering how depending on whether an SBOM is created from a 'requirements.txt' file, a python environment, or a docker container, it can have a different output, this will lead to different SBOMs given that each SBOM generation tool will choose their own preferential option.

Additionally, given that there exists no property in SPDX which lists down which metadata option was chosen when creating the SBOM, it divorces the SBOM from the method of its creation, and creates an information gap between the SBOM generation tool itself and the created SBOM.

\paragraph{(4) Interoperability issues where one tool produces a better SBOM for one format over another:}
Interoperability issues, particularly between SPDX and CycloneDX, are explicitly addressed in the Extension Profile. The specification acknowledges that tools often specialize in one format, leading to data loss during conversion.

The \texttt{CdxPropertiesExtension} class is a standardized extension point which is intended to be compatible with CycloneDX properties, allowing an SPDX document to carry data generated by tools designed for the competing standard without loss. Additionally, the modular nature of the profiles allows tools to support specific subsets of the standard reliably, rather than failing to support the entire monolithic specification.

\paragraph{(5) Lack of reproducibility in the builds on which SBOMs are created:} The SPDX 3.0.1 specification directly addresses build reproducibility through two mechanisms. First, the \texttt{CreationInfo} class notes that the \texttt{created} timestamp should reflect the date of last change (e.g., a git commit date) rather than the date the SPDX data was generated, explicitly stating this supports reproducible builds.'' Second, the \texttt{Build} profile introduces a dedicated \texttt{Build} class that encapsulates all metadata related to a build process---its inputs, outputs, builders, and related identities---providing a structured, traceable record of the build from which the SBOM was generated. Crucially, \texttt{buildStartTime} and \texttt{buildEndTime} are described as optional and may be omitted to simplify creating reproducible builds,'' since timestamping the build process itself can introduce non-determinism.

\paragraph{(6) View of SBOMs as unnecessary and merely a compliance checkbox:}
The specification counters this perception architecturally through the \texttt{Lite Profile}, which is described as capturing the minimum information required for license compliance in the software supply chain, and through the modular profile system more broadly. By defining nine distinct compliance points, Core, Software, Security, Licensing, Dataset, AI, Build, Lite, and Extension, the specification frames SBOMs not as monolithic compliance documents but as targeted, functional artifacts serving real operational purposes. The \texttt{Security Profile}, for instance, enables interchange of vulnerability data between tools, making an SBOM an active security instrument rather than a passive document. The \texttt{Build Profile} similarly ties the SBOM to a verifiable build process, reinforcing its role as an auditable engineering artifact.

\paragraph{(7) Inconsistencies in the naming of packages:} The specification addresses package naming inconsistencies through two complementary mechanisms. The \texttt{packageUrl} property (part of the Software Profile) adopts the Package URL (\texttt{purl}) standard, described as an attempt to standardize package representations in order to reliably identify and locate software packages'' in a mostly universal and uniform way across programming languages, package managers, packaging conventions, tools, APIs and databases.'' The \texttt{purl} follows a structured schema that normalises identification across ecosystems. Complementarily, the \texttt{ExternalIdentifier} class supports referencing packages via established external naming schemes including \texttt{cpe22}, \texttt{cpe23}, \texttt{packageUrl}, \texttt{swid}, and \texttt{swhid}, providing a mapping from SPDX elements to authoritative, domain-specific identifiers and thereby reducing ambiguity from cross-ecosystem naming divergence.

\paragraph{(8) Inability to capture whether a library was actually loaded into memory or not due to the static nature of an SBOM:} The specification addresses this limitation through two related features. First, the \texttt{SBOMType} enumeration includes a \texttt{runtime} type, defined as an SBOM generated through instrumenting the system running the software, to capture only components present in the system, as well as external call-outs or dynamically loaded components''---also referred to as an Instrumented or Dynamic SBOM. This allows producers to explicitly distinguish a runtime-observed SBOM from a static analysis SBOM. Second, the \texttt{RelationshipType} enumeration provides \texttt{hasDynamicLink} (the from Element dynamically links in each to Element'') and \texttt{hasStaticLink} as distinct relationship types, scoped further by the \texttt{LifecycleScopeType}, which includes a \texttt{runtime} value defined as covering the execution phase of an element.'' Together, these allow an SBOM to express not merely what libraries are present in a package, but which were dynamically linked and active during execution, partially bridging the static/dynamic observability gap.

\textbf{CycloneDX}

\paragraph{(1) Failure to meet CISA Minimum Elements:}
Our intra-specification analysis reveals a direct conflict between the CISA guidelines and the CycloneDX normative requirements regarding the "Supplier" field. 

The CISA Minimum Elements explicitly list "Supplier Name" as \textbf{REQUIRED}. However, our extraction of the CycloneDX 1.6 specification confirms that the \texttt{supplier} property is defined as \textbf{OPTIONAL} (Normative Keyword: MAY) in lines 198, 242, and 264 of the specification data. Furthermore, the official JSON schema does not enforce the presence of metadata.supplier. 

This creates a systemic root cause for non-compliance. Our empirical analysis (Section 4.6) confirms this, showing that \textbf{96.1\%} of real-world SBOMs omit the supplier field because the schema permits it.

% \paragraph{(2) Transitive dependencies are missed:}
% CycloneDX utilizes a nested \texttt{components} array or a flattened \texttt{dependencies} graph. However, the specification relies heavily on the \texttt{metadata.tools} and \texttt{formulation} objects to describe the build environment. Our thematic analysis shows that while \textbf{Formulation} accounts for 9\% of the spec, it is almost entirely optional (\textbf{MAY}). Tools perform shallow scans (e.g., parsing \texttt{package.json}) because the specification does not mandate the complex formulation analysis required to capture transitive build-time dependencies.

\paragraph{(2) Lack of standardized metadata:}
CycloneDX addresses metadata via the \texttt{properties} object (a key-value store). Our thematic coding of the "Extensibility" theme reveals that while the standard "RECOMMENDS" registering properties in a taxonomy, it effectively allows ad-hoc strings. This results in the same fragmentation seen in the Python ecosystem \cite{pythonsboms}, where tools create arbitrary property names (e.g., \texttt{cdx:property:build\_host} vs \texttt{ex:build\_server}) that cannot be parsed universally. Our measurement study found that \textbf{21.7\%} of properties in the wild use ad-hoc, unregistered namespaces, confirming this fragmentation.

\paragraph{(3) Interoperability issues:}
The high degree of flexibility in CycloneDX (53\% \textbf{MAY}) creates interoperability friction. For example, the \texttt{licenseChoice} element allows an author to provide either an SPDX ID, a proprietary license name, or a license expression. A consumer tool expecting an SPDX ID (to automate policy checks) will fail when encountering a valid CycloneDX file that uses proprietary names. The specification prioritizes expressiveness over strict interoperability, requiring consumption tools to implement complex normalization logic \cite{bomsaway}. However, our empirical data suggests the ecosystem is self-correcting: \textbf{88.3\%} of analyzed SBOMs voluntarily use standard SPDX identifiers despite the specification allowing proprietary names.

\begin{table}[h]
\centering
\normalsize
\resizebox{0.5\textwidth}{!}{%
\begin{tabular}{|l|p{3.2cm}|p{3.2cm}|p{3.2cm}|}
\hline
 & \textbf{SPDX Guardrail} & \textbf{CycloneDX Guardrail} & \textbf{Test for issue} \\ \hline
1 & Lite profile presence 
  & Presence of \texttt{metadata.supplier}, \texttt{timestamp}, and \texttt{authors} 
  & Percentage of minimum elements included \\ \hline

2 & NULL 
  & NULL
  & Depth of dependency graph \\ \hline

3 & NULL 
  & NULL
  & Divergence between statically and dynamically created SBOM \\ \hline

4 & CycloneDX extension property presence 
  & Taxonomy usage (e.g., \texttt{cdx:} prefix) 
  & Degree of lossyness of conversion \\ \hline

5 & Build profile presence 
  & Presence of \texttt{formulation} or \texttt{annotations} 
  & NULL \\ \hline

6 & profileConformance presence 
  & Presence of \texttt{formulation.workflow} 
  & Percentage of noAssertion fields out of total fields \\ \hline

7 & PURL format correctly followed 
  & Presence of \texttt{compositions} 
  & Divergence between packages representing the same dependency but using different tools \\ \hline

8 & relationshipType presence 
  & Valid Package URL (purl) syntax 
  & Profileration of static injection of library not used in code \\ \hline
\end{tabular}
}
\caption{SPDX and CycloneDX mitigation checks and corresponding problem tests}
\label{tab:combined_sbom_checks}
\end{table}
% \begin{table}[h]
% \centering
% \begin{tabular}{|l|p{3.5cm}|p{3.5cm}|}
% \hline
%  & \textbf{Check for guardrails} & \textbf{Test for issue} \\ \hline
% 1 & Lite profile presence & Percentage of minimum elements included \\ \hline
% 2 & Set of 'relationshipType' present & Depth of relationship graph \\ \hline
% 3 & NULL & Divergence between statically and dynamically created SBOM \\ \hline
% 4 & CycloneDX extension property presence & Degree of lossyness of conversion \\ \hline
% 5 & Build profile presence & Measuring reproducibility of build \\ \hline
% 6 & profileConformance presence & Percentage of noAssertion fields out of total fields \\ \hline
% 7 & PURL format correctly followed & Divergence between packages representing the same dependency but using different tools \\ \hline
% 8 & relationshipType presence & Profileration of static injection of library not used in code \\ \hline
% \end{tabular}
% \caption{SPDX mitigation checks and corresponding problem tests}
% \end{table}

% \begin{table}[h]
% \centering
% \resizebox{\columnwidth}{!}{%
% \begin{tabular}{|l|p{3.8cm}|p{3.8cm}|}
% \hline
%  & \textbf{Check for guardrails} & \textbf{Test for issue} \\ \hline
% 1 & Presence of \texttt{metadata.supplier}, \texttt{timestamp}, and \texttt{authors} & Percentage of CISA required elements (7 fields) present \\ \hline
% 2 & Dependency graph depth $>1$ & Coverage of components appearing in the dependency graph \\ \hline
% 3 & N/A (No spec solution) & Standardization score (PURL + Hash presence) \\ \hline
% 4 & Taxonomy usage (e.g., \texttt{cdx:} prefix) & Fragmentation score (ad-hoc vs registered property names) \\ \hline
% 5 & Presence of \texttt{formulation} or \texttt{annotations} & Usage rate of advanced CycloneDX features \\ \hline
% 6 & Presence of \texttt{formulation.workflow} & Reproducibility score (hashes + environment data) \\ \hline
% 7 & Presence of \texttt{compositions} & Rate of missing completeness assertions \\ \hline
% 8 & Valid Package URL (purl) syntax & PURL coverage rate per SBOM \\ \hline
% \end{tabular}
% }
% \caption{CycloneDX Mitigation checks and corresponding problem measurements}
% \label{tab:cdx_test_cases}
% \end{table}

\newpage

\subsubsection{Use of test cases\\}

\textbf{\\SPDX\\}

The results of the test cases are present in table \ref{tab:spdx_test_results}.

\textbf{\\CycloneDX\\}

To validate the practical impact of the structural issues identified in Section 4.3.2, we developed a corresponding test suite for CycloneDX. We utilized the GitHub Code Search API to collect a dataset of 128 valid CycloneDX 1.6 SBOMs from public repositories.

We applied the test cases defined in Table \ref{tab:combined_sbom_checks} to our dataset of 128 CycloneDX 1.6 SBOMs. The analysis reveals a significant gap between specification capabilities and real-world adoption.

\paragraph{CISA Compliance Gap (TC1):}
Our measurement confirms the structural weakness identified in Section 4.3.2. Only \textbf{2.3\%} (3/128) of the analyzed SBOMs met the full CISA minimum requirements. The \texttt{supplier} field, which is optional in the CycloneDX schema, was missing in 96.1\% of the samples. This validates that optionality in the standard leads directly to non-compliance in practice.

\paragraph{Transitive Dependency Blindness (TC2):}
Despite the graph-based capabilities of CycloneDX, \textbf{57\%} of SBOMs either lacked a dependency graph entirely or only captured direct dependencies (Depth $\le 1$). This creates a "shallow visibility" problem where vulnerabilities in transitive dependencies (e.g., Log4j) remain undetectable.

\paragraph{The Reproducibility Void (TC6):}
While CycloneDX 1.6 introduced the \texttt{formulation} object to address build integrity \cite{reproduciblebuildsforne}, we found \textbf{0\%} adoption of this feature in the wild. This suggests that complex, optional security features in specifications are ignored by tool developers in favor of basic inventory generation.

\paragraph{Checkbox Compliance (TC7):}
We measured the usage of \texttt{compositions} to assert completeness. \textbf{98.4\%} of SBOMs made no assertion regarding their completeness (neither "complete" nor "incomplete"). This creates an ambiguity where consumers cannot distinguish between a thorough SBOM and a partial one, validating concerns regarding "checkbox compliance" \cite{maintainersvulnmgmtwermke}.

\paragraph{Standardization Success (TC8):}
Conversely, we found high adherence to Package URL (PURL) standards. \textbf{63.3\%} of SBOMs achieved high PURL coverage ($>80\%$), and cross-tool consistency was high ($>92\%$). This indicates that extensive specification guidance (as seen with PURL in the appendices) effectively drives standardization, whereas loose optional fields (like \texttt{properties}) lead to fragmentation.

\begin{table*}[ht]
\centering
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}|l|c c c c | c c c c|}
\hline
& \textbf{Guardrails} & & & & \textbf{Issues} & & & \\
\hline
& \textbf{microsoft tool} & \textbf{spdx-generator} & \textbf{syft} & \textbf{trivy} & \textbf{microsoft tool} & \textbf{spdx-generator} & \textbf{syft} & \textbf{trivy} \\
\hline
\textbf{Minimum elements} & 0\% & - & - & - & 91.7\% & 58.3\% & 41.7\% & 66.7\% \\
\textbf{Transitive dependencies} & 4 & 6 & 6 & 6 & 3 & 3 & 2 & 2 \\
\textbf{Metadata parsing} & - & - & - & - & 62\% & 39\% & 28\% & 27\% \\
\textbf{Interoperability} & 0\% & - & - & - & 19\% & 22\% & 27\% & 26\% \\
\textbf{Reproducibility} & 0\% & - & - & - & ? & ? & ? & ? \\
\textbf{Superficial compliance} & 100\% & - & - & - & 18\% & 28\% & 8\% & 5\% \\
\textbf{Package naming} & 12\% & 10\% & 16\% & 25\% & 0\% & 0\% & 0\% & 0\% \\
\textbf{Dynamic dependencies} & 100\% & 100\% & 100\% & 100\% & 100\% & 100\% & 100\% & 100\% \\
\hline
\end{tabular*}
\caption{Results of SPDX test cases}
\label{tab:spdx_test_results}
\end{table*}"

now does it fully incorporate the advisor's feedback?:"Dear Professors Mohannad Alhanahnah, Sazzadur Rahaman, and Ashish Gehani, apologies for late updates, we both have been travelling for the past few days. We took a deeper pass through the papers discussed with Dr. Mohannad with the question of what our paper is still missing if we want the novelty to stay specification-driven rather than drift back into a tool-measurement paper.
 
My current understanding is:
 
The IoT guidelines paper (https://arxiv.org/pdf/2310.01653) is useful because it does not stop at taxonomy. It turns the qualitative coding into evaluative dimensions such as coverage, actionability, specificity, and usefulness against real failures. That exposed a gap in our current paper: our spec analysis is still mostly descriptive, so it tells us what is in the standards, but not how strong or security-useful those requirements actually are.
ProtocolGuard (https://www.ndss-symposium.org/wp-content/uploads/2026-f521-paper.pdf) is useful less because of the LLM angle and more because it treats natural-language requirements as something that should become operational or checkable. For us, that suggests a missing lens: many SBOM requirements may exist in the standard, but they may still be weak guardrails if they are optional, conditional, or not verifiable from the artifact itself.
The SAP paper (https://dl.acm.org/doi/pdf/10.1145/3788692) already covers large-scale adherence measurement between standards and tools. That means if we lean too heavily on measurement again, we risk moving closer to an already occupied space. The stronger gap for us is to explain why tool inconsistency persists by looking at the standards themselves: whether the standards actually provide strong, baseline, and operationally checkable guardrails.
Our own paper is strongest when it treats the standard not just as an output format, but as a possible root cause of inconsistency. The missing analytical layer is a security-oriented reading of the requirements: which known SBOM failure modes the standard addresses, how strongly it addresses them, and whether those safeguards are actually checkable.
 
Based on that, I was working on drafting a new CycloneDX subsection for the Results section. The new subsection reframes the thematic analysis with a security lens and argues that CycloneDX is strong at regulating the internal structure of objects once they are present, but weak at forcing the presence of the objects that matter for security usefulness. In particular, it distinguishes between strong local structural guardrails, weak baseline security guardrails, dormant advanced guardrails, and aspirational guidance that is not enforceable.


The subsection also adds a table that maps the main SBOM failure modes in prior literature to the corresponding CycloneDX guardrails, their strength, and whether they are artifact-verifiable or require external context.
 
My hope is that this gives the paper a more meaningful specification-driven contribution: instead of only saying that the standard is lenient or that tools are inconsistent, it explains which security failures the standard meaningfully constrains, which ones it only gestures toward, and which ones it leaves largely to tool builders. I would really appreciate any feedback on it (in form of comments on overleaf). This writeup is under the Section 4.2 Reproducible thematic analysis, starting specifically from "4.2.3 CycloneDX Revisited Through a Security Lens."
 
In view of our travel, it would be helpful if we can skip today's meeting and we can have your thoughts on the updates above asynchronously instead. An update from Huzaifa will also follow.
 
thx for the summary, 
I disagree with the perception about ProtocolGuard, LLM used here as a utility to facilitate the analysis not as a contribution of the work. Also, isn't SBOM spec supposed to provide something operational and checkable? The main contribution of ProtocolGuard is the discovery of implementation bugs that violates the spec.
 
I skimmed over the new content, i don't see any results, in the best cases fits as a discussion. The style is anecdotal, no clear evidence, example, etc.... I also didn't understand the brief mention of VEX, though I think it's an interesting angle to consider. 
 
I hope a follow up will be take soon, otherwise, this context and conversation will be lost, and progress will not be achieved. 
 
has any of you inspected the implementation of SBOM generation tools? and how the spec is propulated
 
we mentioned also comparison with SBOM quality tools, but I don't see it has been addressed
 
pls chk 2nd column, P6 in this https://arxiv.org/pdf/2303.11102
 
provides interesting concrete discussion supported by evidences about mismatch between spec and sbom producers
 
Thank you Dr. Mohannad Alhanahnah, this is helpful. I see the issue with the current subsection. I believe I'll need to support each claim with clearer evidence from the specification, prior empirical work, and concrete examples. I will revise the subsection 4.2.3 accordingly and update you by EOD, including the concrete issues around production step and scope discussed in Balliu et al.
 
I have not yet inspected SBOM generator implementations directly, but we can do that next. I can trace how selected generators populate dependency graphs, supplier, timestamp, and authors, and scope and completeness related fields. 
 
I also take the point about SBOM quality tools. At the moment, the main one we have identified is sbomqs, so we can position our work against what sbomqs checks well and what it cannot check when the specification itself is underspecified. I think Mohammad Huzaifa did some sort of experiment around this earlier. We then are also required follow up with a smaller implementation focused comparison rather than a broad measurement study.
 "

Section ID & Heading	Recommendation / Requirement	Normative Keyword	Subtheme
2.2 Implementation Conformance	A consumer must interpret and process the contents of CycloneDX BOMs in a manner conforming to this standard.	REQUIRED	Specification Conformance
2.2 Implementation Conformance	A consumer should instantiate a warning or error condition when a CycloneDX BOM is not conforming to this standard.	RECOMMENDED	Specification Conformance
2.2 Implementation Conformance	A consumer must not instantiate an error condition in response to a CycloneDX BOM conforming to this standard.	REQUIRED	Specification Conformance
2.2 Implementation Conformance	When optional or recommended features contained within CycloneDX BOMs are accessed by a consumer, the consumer must interpret and process those features in a manner conforming to this standard.	REQUIRED	Specification Conformance
2.2 Implementation Conformance	Any CycloneDX BOM a producer creates must conform to this standard.	REQUIRED	Specification Conformance
2.2 Implementation Conformance	A producer must not introduce any non-conforming CycloneDX content when modifying or enriching a CycloneDX BOM.	REQUIRED	Specification Conformance
2.2 Implementation Conformance	When a producer chooses to use an optional or recommended feature in an CycloneDX BOM, then the producer must create or modify that feature in a manner conforming to this standard.	REQUIRED	Specification Conformance
5.2 High-Level SBOM Use Cases	SBOMs should ideally contain all direct and transitive components and the dependency relationships between them.	RECOMMENDED	Dependency Graph Representation
5.3.1 Software Bill of Materials (SBOM)	SBOMs should ideally contain all direct and transitive components and the dependency relationships between them.	RECOMMENDED	Dependency Graph Representation
5.4.1.1 Serial Number	Every BOM generated should have a unique serial number, even if the contents of the BOM have not changed over time.	RECOMMENDED	BOM Identification
5.4.1.1 Serial Number	If specified, the serial number must conform to RFC-4122.	REQUIRED	BOM Identification
5.4.1.1 Serial Number	The use of serial numbers is recommended.	RECOMMENDED	BOM Identification
5.4.1.2 Version	Whenever an existing BOM is modified, either manually or through automated processes, the version of the BOM should be incremented by 1.	RECOMMENDED	BOM Identification
5.4.1.2 Version	When a system is presented with multiple BOMs with identical serial numbers, the system should use the most recent version of the BOM.	RECOMMENDED	BOM Identification
6 CycloneDX Bill of Materials Standard	The bomFormat property is Required.	REQUIRED	BOM Format and Versioning
6 CycloneDX Bill of Materials Standard	The value of bomFormat must be "CycloneDX".	REQUIRED	BOM Format and Versioning
6 CycloneDX Bill of Materials Standard	The specVersion property is Required.	REQUIRED	BOM Format and Versioning
6 CycloneDX Bill of Materials Standard	The serialNumber property is Optional.	MAY	BOM Identification
6 CycloneDX Bill of Materials Standard	Every BOM generated SHOULD have a unique serial number, even if the contents of the BOM have not changed over time.	RECOMMENDED	BOM Identification
6 CycloneDX Bill of Materials Standard	If specified, the serial number must conform to RFC 4122.	REQUIRED	BOM Identification
6 CycloneDX Bill of Materials Standard	Use of serial numbers is recommended.	RECOMMENDED	BOM Identification
6 CycloneDX Bill of Materials Standard	The version property is Optional.	MAY	BOM Identification
6 CycloneDX Bill of Materials Standard	Whenever an existing BOM is modified, either manually or through automated processes, the version of the BOM SHOULD be incremented by 1.	RECOMMENDED	BOM Identification
6 CycloneDX Bill of Materials Standard	When a system is presented with multiple BOMs with identical serial numbers, the system SHOULD use the most recent version of the BOM.	RECOMMENDED	BOM Identification
6 CycloneDX Bill of Materials Standard	The metadata property is Optional.	MAY	Root Object Model
6 CycloneDX Bill of Materials Standard	The components property is Optional.	MAY	Root Object Model
6 CycloneDX Bill of Materials Standard	The services property is Optional.	MAY	Root Object Model
6 CycloneDX Bill of Materials Standard	The externalReferences property is Optional.	MAY	Root Object Model
6 CycloneDX Bill of Materials Standard	The dependencies property is Optional.	MAY	Root Object Model
6 CycloneDX Bill of Materials Standard	The compositions property is Optional.	MAY	Root Object Model
6 CycloneDX Bill of Materials Standard	The vulnerabilities property is Optional.	MAY	Root Object Model
6 CycloneDX Bill of Materials Standard	The annotations property is Optional.	MAY	Root Object Model
6 CycloneDX Bill of Materials Standard	The formulation property is Optional.	MAY	Root Object Model
6 CycloneDX Bill of Materials Standard	The declarations property is Optional.	MAY	Root Object Model
6 CycloneDX Bill of Materials Standard	The definitions property is Optional.	MAY	Root Object Model
6.1 BOM Format	The bomFormat property is Required.	REQUIRED	BOM Format and Versioning
6.1 BOM Format	The value of bomFormat must be "CycloneDX".	REQUIRED	BOM Format and Versioning
6.2 CycloneDX Specification Version	The specVersion property is Required.	REQUIRED	BOM Format and Versioning
6.3 BOM Serial Number	The serialNumber property is Optional.	MAY	BOM Identification
6.3 BOM Serial Number	Every BOM generated SHOULD have a unique serial number, even if the contents of the BOM have not changed over time.	RECOMMENDED	BOM Identification
6.3 BOM Serial Number	If specified, the serial number must conform to RFC 4122.	REQUIRED	BOM Identification
6.3 BOM Serial Number	Use of serial numbers is recommended.	RECOMMENDED	BOM Identification
6.4 BOM Version	The version property is Optional.	MAY	BOM Identification
6.4 BOM Version	Whenever an existing BOM is modified, either manually or through automated processes, the version of the BOM SHOULD be incremented by 1.	RECOMMENDED	BOM Identification
6.4 BOM Version	When a system is presented with multiple BOMs with identical serial numbers, the system SHOULD use the most recent version of the BOM.	RECOMMENDED	BOM Identification
7 BOM Metadata	The metadata property is Optional.	MAY	BOM Metadata
7 BOM Metadata	The tools property is Optional.	MAY	BOM Metadata
7 BOM Metadata	The manufacturer property is Optional.	MAY	BOM Metadata
7 BOM Metadata	The authors property is Optional.	MAY	BOM Metadata
7 BOM Metadata	The component property is Optional.	MAY	BOM Metadata
7 BOM Metadata	The manufacture property is Optional and Deprecated.	MAY	BOM Metadata
7 BOM Metadata	The supplier property is Optional.	MAY	BOM Metadata
7 BOM Metadata	The licenses property is Optional.	MAY	BOM Metadata
7.1 Timestamp	The timestamp property is Optional.	MAY	Timestamping
7.2 Lifecycles	The lifecycles property is Optional.	MAY	Lifecycle Information
7.2 Lifecycles	Each item of this array must be a Lifecycle object.	REQUIRED	Lifecycle Information
7.2.1 Lifecycle	The Lifecycle object Must be one of: Pre-Defined Phase.	REQUIRED	Lifecycle Information
7.2.1 Lifecycle	The Lifecycle object Must be one of: Custom Phase.	REQUIRED	Lifecycle Information
7.2.2 Pre-Defined Phase	The phase property is Required.	REQUIRED	Lifecycle Information
7.2.3 Custom Phase	The name property is Required.	REQUIRED	Lifecycle Information
7.2.3 Custom Phase	The description property is Optional.	MAY	Lifecycle Information
7.2.4 Phase	The lifecycles property is Required.	REQUIRED	Lifecycle Information
7.2.5 Name	The lifecycles property is Required.	REQUIRED	Lifecycle Information
7.2.6 Description	The lifecycles property is Optional.	MAY	Lifecycle Information
7.3 Tools	The tools property is Optional.	MAY	Tooling Information
7.3 Tools	The tools object Must be one of: Tools.	REQUIRED	Tooling Information
7.3 Tools	The tools object Must be one of: Tools (legacy).	REQUIRED	Tooling Information
7.3.1 Tools	The components property is Optional.	MAY	Tooling Information
7.3.1 Tools	The services property is Optional.	MAY	Tooling Information
7.3.3 Components	The tools property is Optional.	MAY	Tooling Information
7.3.3 Components	Each item of this array must be a Component object.	REQUIRED	Tooling Information
7.3.3.1 Component	All items must be unique.	REQUIRED	Tooling Information
7.3.4 Services	The tools property is Optional.	MAY	Tooling Information
7.3.4 Services	Each item of this array must be a Service object.	REQUIRED	Tooling Information
7.3.4.1 Service	All items must be unique.	REQUIRED	Tooling Information
7.3.4.1.1 Tools (legacy)	Each item of this array must be a Tool object.	REQUIRED	Tooling Information
7.3.5 Tool	The vendor property is Optional.	MAY	Tooling Information
7.3.5 Tool	The name property is Optional.	MAY	Tooling Information
7.3.5 Tool	The version property is Optional.	MAY	Tooling Information
7.3.5 Tool	The hashes property is Optional.	MAY	Tooling Information
7.3.5 Tool	The externalReferences property is Optional.	MAY	Tooling Information
7.3.5.1 Tool Vendor	The vendor property is Optional.	MAY	Tooling Information
7.3.5.2 Tool Name	The name property is Optional.	MAY	Tooling Information
7.3.5.3 Tool Version	The version property is Optional.	MAY	Tooling Information
7.3.5.4 Hashes	The hashes property is Optional.	MAY	Cryptographic Hashes
7.3.5.4 Hashes	Each item of this array must be a Hash object.	REQUIRED	Cryptographic Hashes
7.3.5.4.1 Hash	The alg property is Required.	REQUIRED	Cryptographic Hashes
7.3.5.4.1 Hash	The content property is Required.	REQUIRED	Cryptographic Hashes
7.3.5.4.2 Hash Algorithm	The alg property is Required.	REQUIRED	Cryptographic Hashes
7.3.5.4.2 Hash Algorithm	The hash algorithm Must be one of: MD5.	REQUIRED	Cryptographic Hashes
7.3.5.4.2 Hash Algorithm	The hash algorithm Must be one of: SHA-1.	REQUIRED	Cryptographic Hashes
7.3.5.4.2 Hash Algorithm	The hash algorithm Must be one of: SHA-256.	REQUIRED	Cryptographic Hashes
7.3.5.4.2 Hash Algorithm	The hash algorithm Must be one of: SHA-384.	REQUIRED	Cryptographic Hashes
7.3.5.4.2 Hash Algorithm	The hash algorithm Must be one of: SHA-512.	REQUIRED	Cryptographic Hashes
7.3.5.4.2 Hash Algorithm	The hash algorithm Must be one of: SHA3-256.	REQUIRED	Cryptographic Hashes
7.3.5.4.2 Hash Algorithm	The hash algorithm Must be one of: SHA3-384.	REQUIRED	Cryptographic Hashes
7.3.5.4.2 Hash Algorithm	The hash algorithm Must be one of: SHA3-512.	REQUIRED	Cryptographic Hashes
7.3.5.4.2 Hash Algorithm	The hash algorithm Must be one of: BLAKE2b-256.	REQUIRED	Cryptographic Hashes
7.3.5.4.2 Hash Algorithm	The hash algorithm Must be one of: BLAKE2b-384.	REQUIRED	Cryptographic Hashes
7.3.5.4.2 Hash Algorithm	The hash algorithm Must be one of: BLAKE2b-512.	REQUIRED	Cryptographic Hashes
7.3.5.4.2 Hash Algorithm	The hash algorithm Must be one of: BLAKE3.	REQUIRED	Cryptographic Hashes
7.3.5.4.3 Hash Value	The content property is Required.	REQUIRED	Cryptographic Hashes
7.3.5.5 External References	The externalReferences property is Optional.	MAY	External References
7.3.5.5 External References	Each item of this array must be an External Reference object.	REQUIRED	External References
7.4 BOM Manufacturer	The manufacturer property is Optional.	MAY	Organizational Entity Definition
7.4 BOM Manufacturer	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.4 BOM Manufacturer	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.4 BOM Manufacturer	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.4 BOM Manufacturer	The name property is Optional.	MAY	Organizational Entity Definition
7.4 BOM Manufacturer	The address property is Optional.	MAY	Organizational Entity Definition
7.4 BOM Manufacturer	The url property is Optional.	MAY	Organizational Entity Definition
7.4 BOM Manufacturer	The contact property is Optional.	MAY	Organizational Entity Definition
7.4.1 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.4.1 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.4.1 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.4.2 Organization Name	The name property is Optional.	MAY	Organizational Entity Definition
7.4.3 Organization Address	The address property is Optional.	MAY	Organizational Entity Definition
7.4.3 Organization Address	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.4.3 Organization Address	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.4.3 Organization Address	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.4.3 Organization Address	The country property is Optional.	MAY	Organizational Entity Definition
7.4.3 Organization Address	The region property is Optional.	MAY	Organizational Entity Definition
7.4.3 Organization Address	The locality property is Optional.	MAY	Organizational Entity Definition
7.4.3 Organization Address	The postOfficeBoxNumber property is Optional.	MAY	Organizational Entity Definition
7.4.3 Organization Address	The postalCode property is Optional.	MAY	Organizational Entity Definition
7.4.3 Organization Address	The streetAddress property is Optional.	MAY	Organizational Entity Definition
7.4.3.1 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.4.3.1 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.4.3.1 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.4.3.2 Country	The country property is Optional.	MAY	Organizational Entity Definition
7.4.3.3 Region	The region property is Optional.	MAY	Organizational Entity Definition
7.4.3.4 Locality	The locality property is Optional.	MAY	Organizational Entity Definition
7.4.3.5 Post Office Box Number	The postOfficeBoxNumber property is Optional.	MAY	Organizational Entity Definition
7.4.3.6 Postal Code	The postalCode property is Optional.	MAY	Organizational Entity Definition
7.4.3.7 Street Address	The streetAddress property is Optional.	MAY	Organizational Entity Definition
7.4.4 Organization URL(s)	The url property is Optional.	MAY	Organizational Entity Definition
7.4.4 Organization URL(s)	Each item of this array must be a string.	REQUIRED	Organizational Entity Definition
7.4.5 Organizational Contact	The contact property is Optional.	MAY	Contact Information
7.4.5 Organizational Contact	Each item of this array must be an Organizational Contact object.	REQUIRED	Contact Information
7.4.5.1 Organizational Contact	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.4.5.1 Organizational Contact	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.4.5.1 Organizational Contact	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.4.5.1 Organizational Contact	The name property is Optional.	MAY	Contact Information
7.4.5.1 Organizational Contact	The email property is Optional.	MAY	Contact Information
7.4.5.1 Organizational Contact	The phone property is Optional.	MAY	Contact Information
7.4.5.1.1 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.4.5.1.1 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.4.5.1.1 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.4.5.1.2 Name	The name property is Optional.	MAY	Contact Information
7.4.5.1.3 Email Address	The email property is Optional.	MAY	Contact Information
7.4.5.1.4 Phone	The phone property is Optional.	MAY	Contact Information
7.5 BOM Authors	The authors property is Optional.	MAY	Organizational Entity Definition
7.5 BOM Authors	Each item of this array must be an Organizational Contact object.	REQUIRED	Organizational Entity Definition
7.5.1 Organizational Contact	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.5.1 Organizational Contact	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.5.1 Organizational Contact	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.5.1 Organizational Contact	The name property is Optional.	MAY	Contact Information
7.5.1 Organizational Contact	The email property is Optional.	MAY	Contact Information
7.5.1 Organizational Contact	The phone property is Optional.	MAY	Contact Information
7.5.1.1 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.5.1.1 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.5.1.1 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.5.1.2 Name	The name property is Optional.	MAY	Contact Information
7.5.1.3 Email Address	The email property is Optional.	MAY	Contact Information
7.5.1.4 Phone	The phone property is Optional.	MAY	Contact Information
7.6 Component	The component property is Optional.	MAY	BOM Metadata
7.7 Component Manufacture (legacy)	The manufacture property is Optional and Deprecated.	MAY	Organizational Entity Definition
7.7 Component Manufacture (legacy)	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.7 Component Manufacture (legacy)	The name property is Optional.	MAY	Organizational Entity Definition
7.7 Component Manufacture (legacy)	The address property is Optional.	MAY	Organizational Entity Definition
7.7 Component Manufacture (legacy)	The url property is Optional.	MAY	Organizational Entity Definition
7.7 Component Manufacture (legacy)	The contact property is Optional.	MAY	Organizational Entity Definition
7.7.1 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.7.1 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.7.1 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.7.2 Organization Name	The name property is Optional.	MAY	Organizational Entity Definition
7.7.3 Organization Address	The address property is Optional.	MAY	Organizational Entity Definition
7.7.3 Organization Address	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.7.3 Organization Address	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.7.3 Organization Address	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.7.3 Organization Address	The country property is Optional.	MAY	Organizational Entity Definition
7.7.3 Organization Address	The region property is Optional.	MAY	Organizational Entity Definition
7.7.3 Organization Address	The locality property is Optional.	MAY	Organizational Entity Definition
7.7.3 Organization Address	The postOfficeBoxNumber property is Optional.	MAY	Organizational Entity Definition
7.7.3 Organization Address	The postalCode property is Optional.	MAY	Organizational Entity Definition
7.7.3 Organization Address	The streetAddress property is Optional.	MAY	Organizational Entity Definition
7.7.3.1 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.7.3.1 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.7.3.1 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.7.4 Organization URL(s)	The url property is Optional.	MAY	Organizational Entity Definition
7.7.4 Organization URL(s)	Each item of this array must be a string.	REQUIRED	Organizational Entity Definition
7.7.5 Organizational Contact	The contact property is Optional.	MAY	Contact Information
7.7.5 Organizational Contact	Each item of this array must be an Organizational Contact object.	REQUIRED	Contact Information
7.7.5.1 Organizational Contact	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.7.5.1 Organizational Contact	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.7.5.1 Organizational Contact	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.7.5.1 Organizational Contact	The name property is Optional.	MAY	Contact Information
7.7.5.1 Organizational Contact	The email property is Optional.	MAY	Contact Information
7.8 Supplier	The supplier property is Optional.	MAY	Organizational Entity Definition
7.8 Supplier	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.8 Supplier	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.8 Supplier	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.8 Supplier	The name property is Optional.	MAY	Organizational Entity Definition
7.8 Supplier	The address property is Optional.	MAY	Organizational Entity Definition
7.8 Supplier	The url property is Optional.	MAY	Organizational Entity Definition
7.8 Supplier	The contact property is Optional.	MAY	Organizational Entity Definition
7.8.1 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.8.1 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.8.1 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.8.2 Organization Name	The name property is Optional.	MAY	Organizational Entity Definition
7.8.3 Organization Address	The address property is Optional.	MAY	Organizational Entity Definition
7.8.3 Organization Address	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.8.3 Organization Address	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.8.3 Organization Address	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.8.3 Organization Address	The country property is Optional.	MAY	Organizational Entity Definition
7.8.3 Organization Address	The region property is Optional.	MAY	Organizational Entity Definition
7.8.3 Organization Address	The locality property is Optional.	MAY	Organizational Entity Definition
7.8.3 Organization Address	The postOfficeBoxNumber property is Optional.	MAY	Organizational Entity Definition
7.8.3 Organization Address	The postalCode property is Optional.	MAY	Organizational Entity Definition
7.8.3 Organization Address	The streetAddress property is Optional.	MAY	Organizational Entity Definition
7.8.3.1 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.8.3.1 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.8.3.1 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.8.4 Organization URL(s)	The url property is Optional.	MAY	Organizational Entity Definition
7.8.4 Organization URL(s)	Each item of this array must be a string.	REQUIRED	Organizational Entity Definition
7.8.5 Organizational Contact	The contact property is Optional.	MAY	Contact Information
7.8.5 Organizational Contact	Each item of this array must be an Organizational Contact object.	REQUIRED	Contact Information
7.8.5.1 Organizational Contact	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
7.8.5.1 Organizational Contact	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
7.8.5.1 Organizational Contact	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
7.8.5.1 Organizational Contact	The name property is Optional.	MAY	Contact Information
7.8.5.1 Organizational Contact	The email property is Optional.	MAY	Contact Information
7.9 BOM Licence(s)	The licenses property is Optional.	MAY	Licensing and Copyright
7.10 Properties	The properties property is Optional.	MAY	Extensibility via Properties
7.10 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
7.10 Properties	Formal registration is optional.	MAY	Property Taxonomies
7.10 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
8.1 Component	The type property is Required.	REQUIRED	Component and Service Typing
8.1 Component	The mime-type property is Optional.	MAY	Descriptive Metadata
8.1 Component	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
8.1 Component	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
8.1 Component	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
8.1 Component	The supplier property is Optional.	MAY	Organizational Entity Definition
8.1 Component	The manufacturer property is Optional.	MAY	Organizational Entity Definition
8.1 Component	The authors property is Optional.	MAY	Organizational Entity Definition
8.1 Component	The author property is Optional and Deprecated.	MAY	Organizational Entity Definition
8.1 Component	The publisher property is Optional.	MAY	Organizational Entity Definition
8.1 Component	The group property is Optional.	MAY	Component and Service Identification
8.1 Component	Whitespace and special characters should be avoided in the group property.	RECOMMENDED	Component and Service Identification
8.1 Component	The name property is Required.	REQUIRED	Component and Service Identification
8.1 Component	The version property is Optional.	MAY	Component and Service Identification
8.1 Component	The version should ideally comply with semantic versioning but is not enforced.	RECOMMENDED	Component and Service Identification
8.1 Component	The description property is Optional.	MAY	Descriptive Metadata
8.1 Component	The scope property is Optional.	MAY	Component Scope
8.1 Component	If scope is not specified, 'required' scope SHOULD be assumed by the consumer of the BOM.	RECOMMENDED	Component Scope
8.1.1 Component Type	The type property is Required.	REQUIRED	Component and Service Typing
8.1.1 Component Type	For software components, classify as application if no more specific appropriate classification is available or cannot be determined for the component.	RECOMMENDED	Component and Service Typing
8.1.1 Component Type	If the library also has key features of a framework, then it should be classified as a framework.	RECOMMENDED	Component and Service Typing
8.1.1 Component Type	If the classification is unknown, then specifying library is recommended.	RECOMMENDED	Component and Service Typing
8.1.1 Component Type	A hardware device containing firmware SHOULD include a component for the physical hardware itself and another component of type 'firmware' or 'operating-system' (whichever is relevant), describing information about the software running on the device.	RECOMMENDED	Component and Service Typing
8.1.2 Mime-Type	The mime-type property is Optional.	MAY	Descriptive Metadata
8.1.3 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
8.1.3 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
8.1.3 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
8.1.4 Component Supplier	The supplier property is Optional.	MAY	Organizational Entity Definition
8.1.5 Component Manufacturer	The manufacturer property is Optional.	MAY	Organizational Entity Definition
8.1.6 Component Authors	The authors property is Optional.	MAY	Organizational Entity Definition
8.1.7 Component Author (legacy)	The author property is Optional and Deprecated.	MAY	Organizational Entity Definition
8.1.8 Component Publisher	The publisher property is Optional.	MAY	Organizational Entity Definition
8.1.9 Component Group	The group property is Optional.	MAY	Component and Service Identification
8.1.9 Component Group	Whitespace and special characters should be avoided.	RECOMMENDED	Component and Service Identification
8.1.10 Component Name	The name property is Required.	REQUIRED	Component and Service Identification
8.1.11 Component Version	The version property is Optional.	MAY	Component and Service Identification
8.1.11 Component Version	The version should ideally comply with semantic versioning but is not enforced.	RECOMMENDED	Component and Service Identification
8.1.12 Component Description	The description property is Optional.	MAY	Descriptive Metadata
8.1.13 Component Scope	The scope property is Optional.	MAY	Component Scope
8.1.13 Component Scope	If scope is not specified, 'required' scope SHOULD be assumed by the consumer of the BOM.	RECOMMENDED	Component Scope
8.1.14 Component Hashes	The hashes property is Optional.	MAY	Cryptographic Hashes
8.1.14 Component Hashes	Each item of this array must be a Hash object.	REQUIRED	Cryptographic Hashes
8.1.14.1 Hash	The alg property for the hashes object is Required.	REQUIRED	Cryptographic Hashes
8.1.14.1 Hash	The alg property must define the algorithm that generated the hash value.	REQUIRED	Cryptographic Hashes
8.1.14.1 Hash	The content property for the hashes object is Required.	REQUIRED	Cryptographic Hashes
8.1.14.1 Hash	The content property must define the value of the hash.	REQUIRED	Cryptographic Hashes
8.1.14.1.1 Hash Algorithm	The alg property is Required.	REQUIRED	Cryptographic Hashes
8.1.14.1.1 Hash Algorithm	The alg value Must be one of: MD5.	REQUIRED	Cryptographic Hashes
8.1.14.1.1 Hash Algorithm	The alg value Must be one of: SHA-1.	REQUIRED	Cryptographic Hashes
8.1.14.1.1 Hash Algorithm	The alg value Must be one of: SHA-256.	REQUIRED	Cryptographic Hashes
8.1.14.1.1 Hash Algorithm	The alg value Must be one of: SHA-384.	REQUIRED	Cryptographic Hashes
8.1.14.1.1 Hash Algorithm	The alg value Must be one of: SHA-512.	REQUIRED	Cryptographic Hashes
8.1.14.1.1 Hash Algorithm	The alg value Must be one of: SHA3-256.	REQUIRED	Cryptographic Hashes
8.1.14.1.1 Hash Algorithm	The alg value Must be one of: SHA3-384.	REQUIRED	Cryptographic Hashes
8.1.14.1.1 Hash Algorithm	The alg value Must be one of: SHA3-512.	REQUIRED	Cryptographic Hashes
8.1.14.1.1 Hash Algorithm	The alg value Must be one of: BLAKE2b-256.	REQUIRED	Cryptographic Hashes
8.1.14.1.1 Hash Algorithm	The alg value Must be one of: BLAKE2b-384.	REQUIRED	Cryptographic Hashes
8.1.14.1.1 Hash Algorithm	The alg value Must be one of: BLAKE2b-512.	REQUIRED	Cryptographic Hashes
8.1.14.1.1 Hash Algorithm	The alg value Must be one of: BLAKE3.	REQUIRED	Cryptographic Hashes
8.1.14.1.2 Hash Value	The content property is Required.	REQUIRED	Cryptographic Hashes
8.1.15 Component Licence(s)	The licenses property is Optional.	MAY	Licensing and Copyright
8.1.15 Component Licence(s)	The licenses property Must be one of: Multiple licenses.	REQUIRED	Licensing and Copyright
8.1.15 Component Licence(s)	The licenses property Must be one of: SPDX License Expression.	REQUIRED	Licensing and Copyright
8.1.16 Multiple licences	Multiple licences must be a list of SPDX licences and/or named licences.	REQUIRED	Licensing and Copyright
8.1.17 SPDX Licence Expression	SPDX Licence Expression must be a tuple of exactly one SPDX Licence Expression.	REQUIRED	Licensing and Copyright
8.1.18 Multiple licences	Each item of this array must be a Licence object.	REQUIRED	Licensing and Copyright
8.1.18.1 Licence	The license property is Required.	REQUIRED	Licensing and Copyright
8.1.18.1 Licence	The license property must specify the details and attributes related to a software license.	REQUIRED	Licensing and Copyright
8.1.18.1.1 Licence	The license property is Required.	REQUIRED	Licensing and Copyright
8.1.18.1.1 Licence	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
8.1.18.1.1 Licence	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
8.1.18.1.1 Licence	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
8.1.18.1.1 Licence	The id property is Optional.	MAY	Licensing and Copyright
8.1.18.1.1 Licence	If the id property is specified, its value must be one of the enumeration of valid SPDX license identifiers defined in the spdx.schema.json (or spdx.xml) subschema which is synchronized with the official SPDX license list.	REQUIRED	Licensing and Copyright
8.1.18.1.1 Licence	The name property is Optional.	MAY	Licensing and Copyright
8.1.18.1.1 Licence	The acknowledgement property is Optional.	MAY	Licensing and Copyright
8.1.18.1.1 Licence	The text property is Optional.	MAY	Licensing and Copyright
8.1.18.1.1 Licence	The url property is Optional.	MAY	Licensing and Copyright
8.1.18.1.1 Licence	If url is specified, a 'license' externalReference should also be specified for completeness.	RECOMMENDED	Licensing and Copyright
8.1.18.1.1 Licence	The licensing property is Optional.	MAY	Licensing and Copyright
8.1.18.1.1 Licence	The properties property is Optional.	MAY	Extensibility via Properties
8.1.18.1.1 Licence	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
8.1.18.1.1 Licence	Formal registration for properties is optional.	MAY	Property Taxonomies
8.1.18.1.2 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
8.1.18.1.2 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
8.1.18.1.2 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
8.1.18.1.3 Licence ID (SPDX)	The id property is Optional.	MAY	Licensing and Copyright
8.1.18.1.3 Licence ID (SPDX)	If specified, this value must be one of the enumeration of valid SPDX licence identifiers defined in the spdx.schema.json (or spdx.xml) subschema which is synchronized with the official SPDX licence list.	REQUIRED	Licensing and Copyright
8.1.18.1.4 Licence Name	The name property is Optional.	MAY	Licensing and Copyright
8.1.18.1.5 Licence Acknowledgement	The acknowledgement property is Optional.	MAY	Licensing and Copyright
8.1.18.1.6 Licence text	The text property is Optional.	MAY	Licensing and Copyright
8.1.18.1.6 Licence text	The content property for the text object is Required.	REQUIRED	Licensing and Copyright
8.1.18.1.6 Licence text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text for the attachment data.	RECOMMENDED	Licensing and Copyright
8.1.18.1.7 Content-Type	The contentType property is Optional.	MAY	Licensing and Copyright
8.1.18.1.8 Encoding	The encoding property is Optional.	MAY	Licensing and Copyright
8.1.18.1.9 Attachment Text	The content property is Required.	REQUIRED	Licensing and Copyright
8.1.18.1.9 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Licensing and Copyright
8.1.18.1.10 Licence URL	The url property is Optional.	MAY	Licensing and Copyright
8.1.18.1.10 Licence URL	If specified, a 'licence' externalReference should also be specified for completeness.	RECOMMENDED	Licensing and Copyright
8.1.18.1.11 Licencing information	The licensing property is Optional.	MAY	Licensing and Copyright
8.1.18.1.89 Properties	The properties property is Optional.	MAY	Extensibility via Properties
8.1.18.1.89 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
8.1.18.1.89 Properties	Formal registration is optional for properties.	MAY	Property Taxonomies
8.1.18.1.89 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
8.1.19 SPDX Licence Expression	The licenses array must be a tuple of exactly one SPDX Licence Expression.	REQUIRED	Licensing and Copyright
8.1.20 Component Copyright	The copyright property is Optional.	MAY	Licensing and Copyright
8.1.21 Common Platform Enumeration (CPE)	The cpe property is Optional.	MAY	Standardized External Identifiers
8.1.21 Common Platform Enumeration (CPE)	The CPE must conform to the CPE 2.2 or 2.3 specification.	REQUIRED	Standardized External Identifiers
8.1.22 Package URL (purl)	The purl property is Optional.	MAY	Standardized External Identifiers
8.1.22 Package URL (purl)	The purl, if specified, must be valid and conform to the specification defined at: https://github.com/package-url/purl-spec.	REQUIRED	Standardized External Identifiers
8.1.23 OmniBOR Artefact Identifier (gitoid)	The omniborId property is Optional.	MAY	Standardized External Identifiers
8.1.23 OmniBOR Artefact Identifier (gitoid)	The OmniBOR, if specified, must be valid and conform to the specification defined at: https://www.iana.org/assignments/uri-schemes/prov/gitoid.	REQUIRED	Standardized External Identifiers
8.1.24 Software Heritage Identifier	The swhid property is Optional.	MAY	Standardized External Identifiers
8.1.24 Software Heritage Identifier	The SWHID, if specified, must be valid and conform to the specification defined at: https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html.	REQUIRED	Standardized External Identifiers
8.1.24 Software Heritage Identifier	Each item of the swhid array must be a string.	REQUIRED	Standardized External Identifiers
8.1.25 SWID Tag	The swid property is Optional.	MAY	Standardized External Identifiers
8.1.25 SWID Tag	The tagId property for the swid object is Required.	REQUIRED	Standardized External Identifiers
8.1.25 SWID Tag	The tagId property must map to the tagId of a SoftwareIdentity.	REQUIRED	Standardized External Identifiers
8.1.25 SWID Tag	The name property for the swid object is Required.	REQUIRED	Standardized External Identifiers
8.1.25 SWID Tag	The name property must map to the name of a SoftwareIdentity.	REQUIRED	Standardized External Identifiers
8.1.25 SWID Tag	The version property is Optional.	MAY	Standardized External Identifiers
8.1.25 SWID Tag	The tagVersion property is Optional.	MAY	Standardized External Identifiers
8.1.25 SWID Tag	The patch property is Optional.	MAY	Standardized External Identifiers
8.1.25 SWID Tag	The text property is Optional.	MAY	Standardized External Identifiers
8.1.25 SWID Tag	The url property is Optional.	MAY	Standardized External Identifiers
8.1.25.1 Tag ID	The tagId property is Required.	REQUIRED	Standardized External Identifiers
8.1.25.1 Tag ID	The tagId property must map to the tagId of a SoftwareIdentity.	REQUIRED	Standardized External Identifiers
8.1.25.2 Name	The name property is Required.	REQUIRED	Standardized External Identifiers
8.1.25.2 Name	The name property must map to the name of a SoftwareIdentity.	REQUIRED	Standardized External Identifiers
8.1.25.3 Version	The version property is Optional.	MAY	Standardized External Identifiers
8.1.25.4 Tag Version	The tagVersion property is Optional.	MAY	Standardized External Identifiers
8.1.25.5 Patch	The patch property is Optional.	MAY	Standardized External Identifiers
8.1.25.6 Attachment text	The text property is Optional.	MAY	Standardized External Identifiers
8.1.25.6 Attachment text	The contentType property for the SWID tag text object is Optional.	MAY	Standardized External Identifiers
8.1.25.6 Attachment text	The encoding property for the SWID tag text object is Optional.	MAY	Standardized External Identifiers
8.1.25.6 Attachment text	The content property for the SWID tag text object is Required.	REQUIRED	Standardized External Identifiers
8.1.25.6 Attachment text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Standardized External Identifiers
8.1.25.6.1 Content-Type	The contentType property is Optional.	MAY	Standardized External Identifiers
8.1.25.6.2 Encoding	The encoding property is Optional.	MAY	Standardized External Identifiers
8.1.25.6.3 Attachment Text	The content property is Required.	REQUIRED	Standardized External Identifiers
8.1.25.6.3 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Standardized External Identifiers
8.1.25.7 URL	The url property is Optional.	MAY	Standardized External Identifiers
8.1.26 Component Modified From Original	The modified property is Optional and Deprecated.	MAY	Component Pedigree and Provenance
8.1.27 Component Pedigree	The pedigree property is Optional.	MAY	Component Pedigree and Provenance
8.1.27 Component Pedigree	The ancestors property is Optional.	MAY	Component Pedigree and Provenance
8.1.27 Component Pedigree	The descendants property is Optional.	MAY	Component Pedigree and Provenance
8.1.27 Component Pedigree	The variants property is Optional.	MAY	Component Pedigree and Provenance
8.1.27 Component Pedigree	The commits property is Optional.	MAY	Component Pedigree and Provenance
8.1.27 Component Pedigree	The patches property is Optional.	MAY	Component Pedigree and Provenance
8.1.27 Component Pedigree	The notes property is Optional.	MAY	Component Pedigree and Provenance
8.1.27.1 Ancestors	Each item of the ancestors array must be a Component object.	REQUIRED	Component Pedigree and Provenance
8.1.27.2 Descendants	Each item of the descendants array must be a Component object.	REQUIRED	Component Pedigree and Provenance
8.1.27.3 Variants	The variants property is Optional.	MAY	Component Pedigree and Provenance
8.1.27.3 Variants	Each item of the variants array must be a Component object.	REQUIRED	Component Pedigree and Provenance
8.1.27.4 Commits	Each item of the commits array must be a Commit object.	REQUIRED	Component Pedigree and Provenance
8.1.27.4 Commits	The uid property is Optional.	MAY	Component Pedigree and Provenance
8.1.27.4 Commits	The url property is Optional.	MAY	Component Pedigree and Provenance
8.1.27.4 Commits	The author property is Optional.	MAY	Component Pedigree and Provenance
8.1.27.4 Commits	The committer property is Optional.	MAY	Component Pedigree and Provenance
8.1.27.4 Commits	The message property is Optional.	MAY	Component Pedigree and Provenance
8.1.27.4.4 Author	The timestamp property for the author object is Optional.	MAY	Component Pedigree and Provenance
8.1.27.4.4 Author	The name property for the author object is Optional.	MAY	Component Pedigree and Provenance
8.1.27.4.4 Author	The email property for the author object is Optional.	MAY	Component Pedigree and Provenance
8.1.27.4.8 Committer	The committer property is Optional.	MAY	Component Pedigree and Provenance
8.1.27.4.8 Committer	The timestamp property for the committer object is Optional.	MAY	Component Pedigree and Provenance
8.1.27.4.8 Committer	The name property for the committer object is Optional.	MAY	Component Pedigree and Provenance
8.1.27.4.8 Committer	The email property for the committer object is Optional.	MAY	Component Pedigree and Provenance
8.1.27.5 Patches	The patches property is Optional.	MAY	Component Pedigree and Provenance
8.1.27.5 Patches	Each item of the patches array must be a Patch object.	REQUIRED	Component Pedigree and Provenance
8.1.27.5.7 Attachment Text	The content property for the attachment data is Required.	REQUIRED	Component Pedigree and Provenance
8.1.27.5.7 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Component Pedigree and Provenance
8.1.27.5.9 Resolves	The resolves property is Optional.	MAY	Component Pedigree and Provenance
8.1.27.5.15 Source	The name property for the source object is Optional.	MAY	Component Pedigree and Provenance
8.1.27.5.15 Source	The url property for the source object is Optional.	MAY	Component Pedigree and Provenance
8.1.27.5.18 References	The references property is Optional.	MAY	Component Pedigree and Provenance
8.1.27.5.18 References	Each item of the references array must be a string.	REQUIRED	Component Pedigree and Provenance
8.1.27.6 Notes	The notes property is Optional.	MAY	Component Pedigree and Provenance
8.1.28 External References	The externalReferences property is Optional.	MAY	External References
8.1.28 External References	Each item of the externalReferences array must be an External Reference object.	REQUIRED	External References
8.1.29 Components	All items in the nested components list must be unique.	REQUIRED	Component Assemblies (Nesting)
8.1.30 Evidence	The evidence property is Optional.	MAY	Evidence and Substantiation
8.1.30 Evidence	The identity property is Optional.	MAY	Evidence and Substantiation
8.1.30 Evidence	It is recommended that all implementations use arrays [for identity evidence], even if only one identity object is specified.	RECOMMENDED	Evidence and Substantiation
8.1.30 Evidence	The occurrences property is Optional.	MAY	Evidence and Substantiation
8.1.30 Evidence	The callstack property is Optional.	MAY	Evidence and Substantiation
8.1.30 Evidence	The licenses property is Optional.	MAY	Evidence and Substantiation
8.1.30 Evidence	The copyright property is Optional.	MAY	Evidence and Substantiation
8.1.30.1 Identity Evidence	The field property for identity evidence is Required.	REQUIRED	Evidence and Substantiation
8.1.30.1 Identity Evidence	The confidence property is Optional.	MAY	Evidence and Substantiation
8.1.30.1 Identity Evidence	The concludedValue property is Optional.	MAY	Evidence and Substantiation
8.1.30.1 Identity Evidence	The methods property is Optional.	MAY	Evidence and Substantiation
8.1.30.1 Identity Evidence	The tools property is Optional.	MAY	Evidence and Substantiation
8.1.31 Release notes	The releaseNotes property is Optional.	MAY	Descriptive Metadata
8.1.31 Release notes	The type property is Required.	REQUIRED	Descriptive Metadata
8.1.31 Release notes	The title property is Optional.	MAY	Descriptive Metadata
8.1.31 Release notes	The featuredImage property is Optional.	MAY	Descriptive Metadata
8.1.31 Release notes	The socialImage property is Optional.	MAY	Descriptive Metadata
8.1.31 Release notes	The description property is Optional.	MAY	Descriptive Metadata
8.1.31 Release notes	The timestamp property is Optional.	MAY	Descriptive Metadata
8.1.31 Release notes	The aliases property is Optional.	MAY	Descriptive Metadata
8.1.31 Release notes	The tags property is Optional.	MAY	Descriptive Metadata
8.1.31 Release notes	The resolves property is Optional.	MAY	Descriptive Metadata
8.1.31 Release notes	The notes property is Optional.	MAY	Descriptive Metadata
8.1.31 Release notes	The properties property is Optional.	MAY	Extensibility via Properties
8.1.31 Release notes	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
8.1.31 Release notes	Formal registration of properties is optional.	MAY	Property Taxonomies
8.1.31 Release notes	Each item of the properties array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
8.1.31.1 Type	The type property is Required.	REQUIRED	Descriptive Metadata
8.1.31.7 Aliases	Each item of the aliases array must be a string.	REQUIRED	Descriptive Metadata
8.1.31.8 Tags	Each item of the tags array must be a string.	REQUIRED	Descriptive Metadata
8.1.31.9 Resolves	Each item of the resolves array must be an Issue object.	REQUIRED	Descriptive Metadata
8.1.31.9.1 Issue	The type property for an Issue object is Required.	REQUIRED	Descriptive Metadata
8.1.31.9.2 Issue Type	The type property is Required.	REQUIRED	Descriptive Metadata
8.1.31.9.9 References	Each item of the references array must be a string.	REQUIRED	Descriptive Metadata
8.1.31.10 Notes	Each item of the notes array must be a Note object.	REQUIRED	Annotations
8.1.31.10.1 Note	The text object in a Note is Required.	REQUIRED	Annotations
8.1.31.10.3 Release note content	The text property is Required.	REQUIRED	Descriptive Metadata
8.1.31.10.6 Attachment Text	The content property is Required.	REQUIRED	Descriptive Metadata
8.1.31.10.6 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Descriptive Metadata
8.1.31.11 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
8.1.31.11 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
8.1.31.11 Properties	Formal registration is optional.	MAY	Property Taxonomies
8.1.31.11.2 Name	The name property is Required.	REQUIRED	Extensibility via Properties
8.1.31.11.3 Value	The value property is Optional.	MAY	Extensibility via Properties
8.1.32 AI/ML Model Card	The modelCard property is Optional.	MAY	AI/ML Model Cards (ML-BOM)
8.1.32 AI/ML Model Card	This object SHOULD be specified for any component of type machine-learning-model.	RECOMMENDED	AI/ML Model Cards (ML-BOM)
8.1.32 AI/ML Model Card	This object must not be specified for other component types.	REQUIRED	AI/ML Model Cards (ML-BOM)
8.1.32 AI/ML Model Card	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
8.1.32 AI/ML Model Card	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
8.1.32 AI/ML Model Card	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
8.1.32 AI/ML Model Card	The modelParameters property is Optional.	MAY	AI/ML Model Cards (ML-BOM)
8.1.32 AI/ML Model Card	The quantitativeAnalysis property is Optional.	MAY	AI/ML Model Cards (ML-BOM)
8.1.32 AI/ML Model Card	The considerations property is Optional.	MAY	AI/ML Model Cards (ML-BOM)
8.1.32 AI/ML Model Card	The properties property is Optional.	MAY	Extensibility via Properties
8.1.32 AI/ML Model Card	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
8.1.32 AI/ML Model Card	Formal registration of properties is optional.	MAY	Property Taxonomies
8.1.32 AI/ML Model Card	Each item of the properties array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
8.1.32.2 Model Parameters	The approach property is Optional.	MAY	AI/ML Model Cards (ML-BOM)
8.1.32.2 Model Parameters	The task property is Optional.	MAY	AI/ML Model Cards (ML-BOM)
8.1.32.2 Model Parameters	The architectureFamily property is Optional.	MAY	AI/ML Model Cards (ML-BOM)
8.1.32.2 Model Parameters	The modelArchitecture property is Optional.	MAY	AI/ML Model Cards (ML-BOM)
8.1.32.2 Model Parameters	The datasets property is Optional.	MAY	AI/ML Model Cards (ML-BOM)
8.1.32.2 Model Parameters	The inputs property is Optional.	MAY	AI/ML Model Cards (ML-BOM)
8.1.32.2 Model Parameters	The outputs property is Optional.	MAY	AI/ML Model Cards (ML-BOM)
8.1.32.2.1 Approach	The approach property is Optional.	MAY	AI/ML Model Cards (ML-BOM)
8.1.32.2.1 Approach	The type property is Optional.	MAY	AI/ML Model Cards (ML-BOM)
8.1.32.2.6 Datasets	Each item in datasets Must be one of: Inline Data Information.	REQUIRED	Data Components and Governance
8.1.32.2.6 Datasets	Each item in datasets Must be one of: Data Reference.	REQUIRED	Data Components and Governance
8.1.32.2.7 Inline Data Information	The bom-ref property for inline data information is Optional.	MAY	Internal Referencing (bom-ref)
8.1.32.2.7 Inline Data Information	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
8.1.32.2.7 Inline Data Information	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
8.1.32.2.7 Inline Data Information	The type property for inline data information is Required.	REQUIRED	Data Components and Governance
8.1.32.2.7 Inline Data Information	The name property for inline data information is Optional.	MAY	Data Components and Governance
8.1.32.2.7 Inline Data Information	The contents property for inline data information is Optional.	MAY	Data Components and Governance
8.1.32.2.7 Inline Data Information	The classification property for inline data information is Optional.	MAY	Data Components and Governance
8.1.32.2.7 Inline Data Information	The sensitiveData property for inline data information is Optional.	MAY	Data Components and Governance
8.1.32.2.7 Inline Data Information	The graphics property for inline data information is Optional.	MAY	Data Components and Governance
8.1.32.2.7 Inline Data Information	The description property for inline data information is Optional.	MAY	Data Components and Governance
8.1.32.2.7 Inline Data Information	The governance property for inline data information is Optional.	MAY	Data Components and Governance
8.1.32.2.8 Data Reference	The ref property for a Data Reference is Optional.	MAY	Data Components and Governance
8.1.32.2.10 Type of Data	The type property (under datasets) is Required.	REQUIRED	Data Components and Governance
8.1.32.2.12 Data Contents	The attachment property for data contents is Optional.	MAY	Data Components and Governance
8.1.32.2.12 Data Contents	The url property for data contents is Optional.	MAY	Data Components and Governance
8.1.32.2.12 Data Contents	The properties property for data contents is Optional.	MAY	Extensibility via Properties
8.1.32.2.13 Data Attachment	The content property for attachment data is Required.	REQUIRED	Data Components and Governance
8.1.32.2.13 Data Attachment	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Data Components and Governance
8.1.32.2.16 Attachment Text	The content property is Required.	REQUIRED	Data Components and Governance
8.1.32.2.16 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Data Components and Governance
8.1.32.2.18 Configuration Properties	Each item of the properties array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
8.1.32.2.19 Lightweight name-value pair	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
8.1.32.2.19 Lightweight name-value pair	Formal registration of properties is optional.	MAY	Property Taxonomies
8.1.32.2.20 Name	The name property is Required.	REQUIRED	Extensibility via Properties
8.1.32.2.21 Value	The value property is Optional.	MAY	Extensibility via Properties
8.1.32.2.23 Sensitive Data	Each item of the sensitiveData array must be a string.	REQUIRED	Data Components and Governance
8.1.32.2.32 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Data Components and Governance
8.1.32.2.32 Attachment Text	The content property is Required.	REQUIRED	Data Components and Governance
8.1.32.2.35 Data Custodians	The custodians property is Optional.	MAY	Data Components and Governance
8.1.32.2.83 Data Owners	The owners property is Optional.	MAY	Data Components and Governance
8.1.32.2.110 Inputs	Each item of the inputs array must be an Input and Output Parameters object.	REQUIRED	AI/ML Model Cards (ML-BOM)
8.1.32.2.113 Outputs	Each item of the outputs array must be an Input and Output Parameters object.	REQUIRED	AI/ML Model Cards (ML-BOM)
8.1.33 Data	The data property is Optional.	MAY	Data Components and Governance
8.1.33 Data	This object SHOULD be specified for any component of type data.	RECOMMENDED	Data Components and Governance
8.1.33 Data	This object must not be specified for other component types.	REQUIRED	Data Components and Governance
8.1.33 Data	Each item of the data array must be a Data object.	REQUIRED	Data Components and Governance
8.1.33 Data	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
8.1.33 Data	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
8.1.33 Data	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
8.1.33 Data	The type property is Required.	REQUIRED	Data Components and Governance
8.1.33 Data	The name property is Optional.	MAY	Data Components and Governance
8.1.33 Data	The contents property is Optional.	MAY	Data Components and Governance
8.1.33 Data	The classification property is Optional.	MAY	Data Components and Governance
8.1.33 Data	The sensitiveData property is Optional.	MAY	Data Components and Governance
8.1.33 Data	The graphics property is Optional.	MAY	Data Components and Governance
8.1.33 Data	The description property is Optional.	MAY	Data Components and Governance
8.1.33 Data	The governance property is Optional.	MAY	Data Components and Governance
8.1.33.1.2 Type of Data	The type property is Required.	REQUIRED	Data Components and Governance
8.1.33.1.4 Data Contents	The attachment property is Optional.	MAY	Data Components and Governance
8.1.33.1.4 Data Contents	The url property is Optional.	MAY	Data Components and Governance
8.1.33.1.4 Data Contents	The properties property is Optional.	MAY	Extensibility via Properties
8.1.33.1.5 Data Attachment	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Data Components and Governance
8.1.33.1.10 Configuration Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
8.1.33.1.11 Lightweight name-value pair	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
8.1.33.1.11 Lightweight name-value pair	Formal registration is optional.	MAY	Property Taxonomies
8.1.33.1.12 Name	The name property is Required.	REQUIRED	Extensibility via Properties
8.1.33.1.13 Value	The value property is Optional.	MAY	Extensibility via Properties
8.1.33.1.15 Sensitive Data	Each item of the sensitiveData array must be a string.	REQUIRED	Data Components and Governance
8.1.33.1.16 Graphics Collection	The collection property is Optional.	MAY	Data Components and Governance
8.1.33.1.27 Data Custodians	The custodians property is Optional.	MAY	Data Components and Governance
8.1.33.1.75 Data Owners	The owners property is Optional.	MAY	Data Components and Governance
8.1.34 Cryptographic Properties	The cryptoProperties property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34 Cryptographic Properties	The assetType property is Required.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34 Cryptographic Properties	The algorithmProperties property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34 Cryptographic Properties	The certificateProperties property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34 Cryptographic Properties	The relatedCryptoMaterialProperties property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34 Cryptographic Properties	The protocolProperties property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34 Cryptographic Properties	The oid property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.1 Asset Type	The assetType property is Required.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.1 Asset Type	The assetType value Must be one of: algorithm.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.1 Asset Type	The assetType value Must be one of: certificate.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.1 Asset Type	The assetType value Must be one of: protocol.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.1 Asset Type	The assetType value Must be one of: related-crypto-material.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2 Algorithm Properties	The algorithmProperties property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2 Algorithm Properties	The primitive property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2 Algorithm Properties	The parameterSetIdentifier property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2 Algorithm Properties	The curve property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2 Algorithm Properties	The executionEnvironment property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2 Algorithm Properties	The implementationPlatform property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2 Algorithm Properties	The certificationLevel property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2 Algorithm Properties	The mode property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2 Algorithm Properties	The padding property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2 Algorithm Properties	The cryptoFunctions property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2 Algorithm Properties	The classicalSecurityLevel property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2 Algorithm Properties	The nistQuantumSecurityLevel property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: drbg.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: mac.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: block-cipher.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: stream-cipher.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: signature.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: hash.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: pke.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: xof.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: kdf.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: key-agree.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: kem.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: ae.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: combiner.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: other.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.1 primitive	The primitive value Must be one of: unknown.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.3 Elliptic Curve	The curve property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2.3 Elliptic Curve	CycloneDX recommends using curve names as defined at https://neuromancer.sk/std/.	RECOMMENDED	Cryptographic Asset Management (CBOM)
8.1.34.2.4 Execution Environment	The executionEnvironment property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2.4 Execution Environment	The executionEnvironment value Must be one of: software-plain-ram.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.4 Execution Environment	The executionEnvironment value Must be one of: software-encrypted-ram.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.4 Execution Environment	The executionEnvironment value Must be one of: software-tee.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.4 Execution Environment	The executionEnvironment value Must be one of: hardware.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.4 Execution Environment	The executionEnvironment value Must be one of: other.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.4 Execution Environment	The executionEnvironment value Must be one of: unknown.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform value Must be one of: generic.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform value Must be one of: x86_32.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform value Must be one of: x86_64.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform value Must be one of: armv7-a.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform value Must be one of: armv7-m.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform value Must be one of: armv8-a.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform value Must be one of: armv8-m.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform value Must be one of: armv9-a.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform value Must be one of: armv9-m.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform value Must be one of: s390x.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform value Must be one of: ppc64.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform value Must be one of: ppc64le.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform value Must be one of: other.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.5 Implementation platform	The implementationPlatform value Must be one of: unknown.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certificationLevel property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	Each item of the certificationLevel array must be a string.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: none.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: fips140-1-l1.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: fips140-1-l2.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: fips140-1-l3.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: fips140-1-l4.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: fips140-2-l1.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: fips140-2-l2.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: fips140-2-l3.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: fips140-2-l4.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: fips140-3-l1.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: fips140-3-l2.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: fips140-3-l3.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: fips140-3-l4.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: cc-eal1.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: cc-eal1+.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: cc-eal2.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: cc-eal2+.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: cc-eal3.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: cc-eal3+.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: cc-eal4.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: cc-eal4+.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: cc-eal5.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: cc-eal5+.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: cc-eal6.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: cc-eal6+.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: cc-eal7.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: cc-eal7+.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: other.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.6 Certification Level	The certification level value Must be one of: unknown.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.7 Mode	The mode property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2.7 Mode	The mode value Must be one of: cbc.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.7 Mode	The mode value Must be one of: ecb.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.7 Mode	The mode value Must be one of: ccm.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.7 Mode	The mode value Must be one of: gcm.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.7 Mode	The mode value Must be one of: cfb.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.7 Mode	The mode value Must be one of: ofb.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.7 Mode	The mode value Must be one of: ctr.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.7 Mode	The mode value Must be one of: other.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.7 Mode	The mode value Must be one of: unknown.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.8 Padding	The padding property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2.8 Padding	The padding value Must be one of: pkcs5.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.8 Padding	The padding value Must be one of: pkcs7.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.8 Padding	The padding value Must be one of: pkcs1v15.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.8 Padding	The padding value Must be one of: oaep.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.8 Padding	The padding value Must be one of: raw.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.8 Padding	The padding value Must be one of: other.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.8 Padding	The padding value Must be one of: unknown.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	The cryptoFunctions property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	Each item of this array must be a string.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	The cryptoFunctions value Must be one of: generate.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	The cryptoFunctions value Must be one of: keygen.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	The cryptoFunctions value Must be one of: encrypt.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	The cryptoFunctions value Must be one of: decrypt.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	The cryptoFunctions value Must be one of: digest.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	The cryptoFunctions value Must be one of: tag.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	The cryptoFunctions value Must be one of: keyderive.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	The cryptoFunctions value Must be one of: sign.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	The cryptoFunctions value Must be one of: verify.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	The cryptoFunctions value Must be one of: encapsulate.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	The cryptoFunctions value Must be one of: decapsulate.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	The cryptoFunctions value Must be one of: other.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.2.9 Cryptographic functions	The cryptoFunctions value Must be one of: unknown.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.3 Certificate Properties	The certificateProperties property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.3 Certificate Properties	The subjectName property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.3 Certificate Properties	The issuerName property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.3 Certificate Properties	The notValidBefore property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.3 Certificate Properties	The notValidAfter property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.3 Certificate Properties	The signatureAlgorithmRef property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.3 Certificate Properties	The subjectPublicKeyRef property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.3 Certificate Properties	The certificateFormat property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.3 Certificate Properties	The certificateExtension property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4 Related Cryptographic Material Properties	The relatedCryptoMaterialProperties property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4 Related Cryptographic Material Properties	The type property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4 Related Cryptographic Material Properties	The id property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4 Related Cryptographic Material Properties	The state property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4 Related Cryptographic Material Properties	The algorithmRef property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4 Related Cryptographic Material Properties	The creationDate property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4 Related Cryptographic Material Properties	The activationDate property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4 Related Cryptographic Material Properties	The updateDate property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4 Related Cryptographic Material Properties	The expirationDate property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4 Related Cryptographic Material Properties	The value property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4 Related Cryptographic Material Properties	The size property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4 Related Cryptographic Material Properties	The format property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4 Related Cryptographic Material Properties	The securedBy property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: private-key.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: public-key.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: secret-key.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: key.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: ciphertext.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: signature.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: digest.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: initialization-vector.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: nonce.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: seed.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: salt.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: shared-secret.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: tag.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: additional-data.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: password.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: credential.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: token.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: other.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.1 relatedCryptoMaterialType	The type value Must be one of: unknown.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.3 State	The state property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4.3 State	The state value Must be one of: pre-activation.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.3 State	The state value Must be one of: active.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.3 State	The state value Must be one of: suspended.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.3 State	The state value Must be one of: deactivated.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.3 State	The state value Must be one of: compromised.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.3 State	The state value Must be one of: destroyed.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.4.12 Secured By	The mechanism property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4.12 Secured By	The algorithmRef property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4.13 Mechanism	The mechanism property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.4.14 Algorithm Reference	The algorithmRef property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5 Protocol Properties	The protocolProperties property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5 Protocol Properties	The type property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5 Protocol Properties	The version property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5 Protocol Properties	The cipherSuites property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5 Protocol Properties	The ikev2TransformTypes property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5 Protocol Properties	The cryptoRefArray property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5.1 Type	The type property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5.1 Type	The type value Must be one of: tls.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.1 Type	The type value Must be one of: ssh.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.1 Type	The type value Must be one of: ipsec.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.1 Type	The type value Must be one of: ike.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.1 Type	The type value Must be one of: sstp.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.1 Type	The type value Must be one of: wpa.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.1 Type	The type value Must be one of: other.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.1 Type	The type value Must be one of: unknown.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.3 Cipher Suites	Each item of this array must be a Cipher Suite object.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.4 Cipher Suite	The name property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5.4 Cipher Suite	The algorithms property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5.4 Cipher Suite	The identifiers property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5.6 Related Algorithms	Each item of the algorithms array must be a string.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.7 Cipher Suite Identifiers	Each item of this array must be a string.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.8 IKEv2 Transform Types	The encr property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5.8 IKEv2 Transform Types	The prf property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5.8 IKEv2 Transform Types	The integ property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5.8 IKEv2 Transform Types	The ke property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5.8 IKEv2 Transform Types	The esn property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5.8 IKEv2 Transform Types	The auth property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5.9 Encryption Algorithm (ENCR)	The encr Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Cryptographic Asset Management (CBOM)
8.1.34.5.9 Encryption Algorithm (ENCR)	Each item of this array must be a string.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.10 Pseudorandom Function (PRF)	The prf Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Cryptographic Asset Management (CBOM)
8.1.34.5.10 Pseudorandom Function (PRF)	Each item of this array must be a string.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.11 Integrity Algorithm (INTEG)	The integ Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Cryptographic Asset Management (CBOM)
8.1.34.5.11 Integrity Algorithm (INTEG)	Each item of this array must be a string.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.12 Key Exchange Method (KE)	The ke Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Cryptographic Asset Management (CBOM)
8.1.34.5.12 Key Exchange Method (KE)	Each item of this array must be a string.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.14 IKEv2 Authentication method	The auth Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Cryptographic Asset Management (CBOM)
8.1.34.5.14 IKEv2 Authentication method	Each item of this array must be a string.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.34.5.15 Cryptographic References	The cryptoRefArray property is Optional.	MAY	Cryptographic Asset Management (CBOM)
8.1.34.5.15 Cryptographic References	The cryptoRefArray Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Cryptographic Asset Management (CBOM)
8.1.34.5.15 Cryptographic References	Each item of this array must be a string.	REQUIRED	Cryptographic Asset Management (CBOM)
8.1.35 Properties	The properties property is Optional.	MAY	Extensibility via Properties
8.1.35 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
8.1.35 Properties	Formal registration is optional.	MAY	Property Taxonomies
8.1.35 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
8.1.35 Properties	The name property is Required.	REQUIRED	Extensibility via Properties
8.1.35 Properties	The value property is Optional.	MAY	Extensibility via Properties
8.1.35.1.1 Name	The name property is Required.	REQUIRED	Extensibility via Properties
8.1.35.1.2 Value	The value property is Optional.	MAY	Extensibility via Properties
8.1.36 Tags	The tags property is Optional.	MAY	Descriptive Metadata
8.1.36 Tags	Each item of this array must be a string.	REQUIRED	Descriptive Metadata
8.1.37 Signature	The signature property is Optional.	MAY	Digital Signatures
8.1.37 Signature	All items must be unique.	REQUIRED	Digital Signatures
9 Services	The services property is Optional.	MAY	Root Object Model
9 Services	Each item of this array must be a Service object.	REQUIRED	Root Object Model
9.1 Service	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
9.1 Service	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
9.1 Service	The provider property is Optional.	MAY	Organizational Entity Definition
9.1 Service	The group property is Optional.	MAY	Component and Service Identification
9.1 Service	Whitespace and special characters should be avoided in the group property.	RECOMMENDED	Component and Service Identification
9.1 Service	The name property is Required.	REQUIRED	Component and Service Identification
9.1 Service	The version property is Optional.	MAY	Component and Service Identification
9.1 Service	The description property is Optional.	MAY	Descriptive Metadata
9.1 Service	The endpoints property is Optional.	MAY	Component and Service Definition
9.1 Service	The authenticated property is Optional.	MAY	Component and Service Definition
9.1 Service	The x-trust-boundary property is Optional.	MAY	Component and Service Definition
9.1 Service	The trustZone property is Optional.	MAY	Component and Service Definition
9.1 Service	The data property is Optional.	MAY	Data Components and Governance
9.1 Service	The licenses property is Optional.	MAY	Licensing and Copyright
9.1 Service	The externalReferences property is Optional.	MAY	External References
9.1 Service	The nested services property is Optional.	MAY	Component Assemblies (Nesting)
9.1 Service	The releaseNotes property is Optional.	MAY	Descriptive Metadata
9.1 Service	The properties property is Optional.	MAY	Extensibility via Properties
9.1 Service	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
9.1 Service	Formal registration of properties is optional.	MAY	Property Taxonomies
9.1 Service	The tags property is Optional.	MAY	Descriptive Metadata
9.1 Service	The signature property is Optional.	MAY	Digital Signatures
9.1.1 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
9.1.1 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
9.1.2 Provider	The provider property is Optional.	MAY	Organizational Entity Definition
9.1.2 Provider	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
9.1.2 Provider	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
9.1.2 Provider	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
9.1.2 Provider	The name property is Optional.	MAY	Organizational Entity Definition
9.1.2 Provider	The address property is Optional.	MAY	Organizational Entity Definition
9.1.2 Provider	The url property is Optional.	MAY	Organizational Entity Definition
9.1.2 Provider	The contact property is Optional.	MAY	Organizational Entity Definition
9.1.2.1 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
9.1.2.1 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
9.1.2.1 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
9.1.2.2 Organization Name	The name property is Optional.	MAY	Organizational Entity Definition
9.1.2.3 Organization Address	The address property is Optional.	MAY	Organizational Entity Definition
9.1.2.3 Organization Address	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
9.1.2.3 Organization Address	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
9.1.2.3 Organization Address	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
9.1.2.5 Organizational Contact	The contact property is Optional.	MAY	Contact Information
9.1.2.5 Organizational Contact	Each item of the contact array must be an Organizational Contact object.	REQUIRED	Contact Information
9.1.2.5.1 Organizational Contact	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
9.1.2.5.1 Organizational Contact	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
9.1.2.5.1 Organizational Contact	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
9.1.2.5.1 Organizational Contact	The name property is Optional.	MAY	Contact Information
9.1.2.5.1 Organizational Contact	The email property is Optional.	MAY	Contact Information
9.1.2.5.1 Organizational Contact	The phone property is Optional.	MAY	Contact Information
9.1.3 Service Group	The group property is Optional.	MAY	Component and Service Identification
9.1.3 Service Group	Whitespace and special characters should be avoided in the group property.	RECOMMENDED	Component and Service Identification
9.1.4 Service Name	The name property is Required.	REQUIRED	Component and Service Identification
9.1.5 Service Version	The version property is Optional.	MAY	Component and Service Identification
9.1.6 Service Description	The description property is Optional.	MAY	Descriptive Metadata
9.1.7 Endpoints	The endpoints property is Optional.	MAY	Component and Service Definition
9.1.7 Endpoints	Each item of this array must be a string.	REQUIRED	Component and Service Definition
9.1.8 Authentication Required	The authenticated property is Optional.	MAY	Component and Service Definition
9.1.9 Crosses Trust Boundary	The x-trust-boundary property is Optional.	MAY	Component and Service Definition
9.1.10 Trust Zone	The trustZone property is Optional.	MAY	Component and Service Definition
9.1.11 Data	The data property is Optional.	MAY	Data Components and Governance
9.1.11.1.1 Directional Flow	The flow property is Required.	REQUIRED	Data Components and Governance
9.1.11.1.1 Directional Flow	The flow value Must be one of: inbound.	REQUIRED	Data Components and Governance
9.1.11.1.1 Directional Flow	The flow value Must be one of: outbound.	REQUIRED	Data Components and Governance
9.1.11.1.1 Directional Flow	The flow value Must be one of: bi-directional.	REQUIRED	Data Components and Governance
9.1.11.1.1 Directional Flow	The flow value Must be one of: unknown.	REQUIRED	Data Components and Governance
9.1.11.1.2 Data Classification	The classification property is Required.	REQUIRED	Data Components and Governance
9.1.11.1.3 Name	The name property is Optional.	MAY	Data Components and Governance
9.1.11.1.4 Description	The description property is Optional.	MAY	Data Components and Governance
9.1.11.1.5 Data Governance	The governance property is Optional.	MAY	Data Components and Governance
9.1.11.1.7 Organization	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
9.1.11.1.7 Organization	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
9.1.11.1.7 Organization	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
9.1.11.1.7 Organization	The name property is Optional.	MAY	Organizational Entity Definition
9.1.11.1.7 Organization	The address property is Optional.	MAY	Organizational Entity Definition
9.1.11.1.7 Organization	The url property is Optional.	MAY	Organizational Entity Definition
9.1.11.1.7 Organization	The contact property is Optional.	MAY	Organizational Entity Definition
9.1.11.1.8 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
9.1.11.1.8 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
9.1.11.1.8 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
9.1.11.1.11 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
9.1.11.1.11 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
9.1.11.1.11 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
9.1.11.1.20 Organizational Contact	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
9.1.11.1.20 Organizational Contact	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
9.1.11.1.20 Organizational Contact	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
9.1.11.1.20 Organizational Contact	The name property is Optional.	MAY	Contact Information
9.1.11.1.20 Organizational Contact	The email property is Optional.	MAY	Contact Information
9.1.11.1.20 Organizational Contact	The phone property is Optional.	MAY	Contact Information
9.1.11.1.78 Source	The source property is Optional.	MAY	Data Components and Governance
9.1.11.1.78 Source	Each item of the source array Must be any of: URL.	REQUIRED	Data Components and Governance
9.1.11.1.78 Source	Each item of the source array Must be any of: BOM-Link Element.	REQUIRED	Data Components and Governance
9.1.11.1.81 Destination	The destination property is Optional.	MAY	Data Components and Governance
9.1.11.1.81 Destination	Each item of the destination array Must be any of: URL.	REQUIRED	Data Components and Governance
9.1.11.1.81 Destination	Each item of the destination array Must be any of: BOM-Link Element.	REQUIRED	Data Components and Governance
9.1.12 Service Licence(s)	The licenses property is Optional.	MAY	Licensing and Copyright
9.1.13 External References	The externalReferences property is Optional.	MAY	External References
9.1.13 External References	Each item of this array must be an External Reference object.	REQUIRED	External References
9.1.14 Services	The nested services property is Optional.	MAY	Component Assemblies (Nesting)
9.1.14 Services	Each item of this array must be a Service object.	REQUIRED	Component Assemblies (Nesting)
9.1.14.1 Service	All items must be unique.	REQUIRED	Component Assemblies (Nesting)
9.1.15 Release notes	The releaseNotes property is Optional.	MAY	Descriptive Metadata
9.1.15 Release notes	The type property is Required.	REQUIRED	Descriptive Metadata
9.1.15 Release notes	The title property is Optional.	MAY	Descriptive Metadata
9.1.15.8 Tags	The tags property is Optional.	MAY	Descriptive Metadata
9.1.15.8 Tags	Each item of this array must be a string.	REQUIRED	Descriptive Metadata
9.1.15.9 Resolves	The resolves property is Optional.	MAY	Descriptive Metadata
9.1.15.10 Notes	The notes property is Optional.	MAY	Annotations
9.1.15.10 Notes	Each item of this array must be a Note object.	REQUIRED	Annotations
9.1.15.11 Properties	The properties property is Optional.	MAY	Extensibility via Properties
9.1.15.11 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
9.1.15.11 Properties	Formal registration is optional for properties.	MAY	Property Taxonomies
9.1.15.11 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
9.1.18 Signature	All items in the signature array must be unique.	REQUIRED	Digital Signatures
10 External References	The externalReferences property is Optional.	MAY	External References
10 External References	Each item of this array must be an External Reference object.	REQUIRED	External References
10.1 External Reference	The url property is Required.	REQUIRED	External References
10.1 External Reference	The comment property is Optional.	MAY	External References
10.1 External Reference	The type property is Required.	REQUIRED	External References
10.1 External Reference	The hashes property is Optional.	MAY	External References
10.1.1 URL	The url property is Required.	REQUIRED	External References
10.1.1 URL	The url property Must be any of: URL.	REQUIRED	External References
10.1.4 Comment	The comment property is Optional.	MAY	External References
10.1.5 Type	The type property is Required.	REQUIRED	External References
10.1.6 Hashes	The hashes property is Optional.	MAY	Cryptographic Hashes
10.1.6 Hashes	Each item of this array must be a Hash object.	REQUIRED	Cryptographic Hashes
10.1.6.1 Hash	The alg property for the hash object is Required.	REQUIRED	Cryptographic Hashes
10.1.6.1 Hash	The alg property must define the algorithm that generated the hash value.	REQUIRED	Cryptographic Hashes
10.1.6.1 Hash	The content property for the hash object is Required.	REQUIRED	Cryptographic Hashes
10.1.6.1 Hash	The content property must define the value of the hash.	REQUIRED	Cryptographic Hashes
10.1.6.1.1 Hash Algorithm	The alg property is Required.	REQUIRED	Cryptographic Hashes
10.1.6.1.1 Hash Algorithm	The alg value Must be one of: MD5.	REQUIRED	Cryptographic Hashes
10.1.6.1.1 Hash Algorithm	The alg value Must be one of: SHA-1.	REQUIRED	Cryptographic Hashes
10.1.6.1.1 Hash Algorithm	The alg value Must be one of: SHA-256.	REQUIRED	Cryptographic Hashes
10.1.6.1.1 Hash Algorithm	The alg value Must be one of: SHA-384.	REQUIRED	Cryptographic Hashes
10.1.6.1.1 Hash Algorithm	The alg value Must be one of: SHA-512.	REQUIRED	Cryptographic Hashes
10.1.6.1.1 Hash Algorithm	The alg value Must be one of: SHA3-256.	REQUIRED	Cryptographic Hashes
10.1.6.1.1 Hash Algorithm	The alg value Must be one of: SHA3-384.	REQUIRED	Cryptographic Hashes
10.1.6.1.1 Hash Algorithm	The alg value Must be one of: SHA3-512.	REQUIRED	Cryptographic Hashes
10.1.6.1.1 Hash Algorithm	The alg value Must be one of: BLAKE2b-256.	REQUIRED	Cryptographic Hashes
10.1.6.1.1 Hash Algorithm	The alg value Must be one of: BLAKE2b-384.	REQUIRED	Cryptographic Hashes
10.1.6.1.1 Hash Algorithm	The alg value Must be one of: BLAKE2b-512.	REQUIRED	Cryptographic Hashes
10.1.6.1.1 Hash Algorithm	The alg value Must be one of: BLAKE3.	REQUIRED	Cryptographic Hashes
10.1.6.1.2 Hash Value	The content property is Required.	REQUIRED	Cryptographic Hashes
11 Dependencies	The dependencies property is Optional.	MAY	Dependency Graph Representation
11 Dependencies	Each item of the dependencies array must be a Dependency object.	REQUIRED	Dependency Graph Representation
11.1 Dependency	Components or services that do not have their own dependencies must be declared as empty elements within the graph.	REQUIRED	Dependency Graph Representation
11.1 Dependency	It is recommended that implementations assume opaque dependency components or services to not be an indicator of an object being dependency-free.	RECOMMENDED	Dependency Graph Representation
11.1 Dependency	It is recommended to leverage compositions to indicate unknown dependency graphs.	RECOMMENDED	Composition and Completeness
11.1 Dependency	The ref property is Required.	REQUIRED	Dependency Graph Representation
11.1 Dependency	The dependsOn property is Optional.	MAY	Dependency Graph Representation
11.1 Dependency	The provides property is Optional.	MAY	Dependency Graph Representation
11.1.1 Reference	The ref property is Required.	REQUIRED	Dependency Graph Representation
11.1.2 Depends On	The dependsOn property is Optional.	MAY	Dependency Graph Representation
11.1.2 Depends On	Each item of the dependsOn array must be a string.	REQUIRED	Dependency Graph Representation
11.1.2 Depends On	All items in the dependsOn array must be unique.	REQUIRED	Dependency Graph Representation
11.1.3 Provides	The provides property is Optional.	MAY	Dependency Graph Representation
11.1.3 Provides	Each item of the provides array must be a string.	REQUIRED	Dependency Graph Representation
11.1.3 Provides	All items in the provides array must be unique.	REQUIRED	Dependency Graph Representation
12 Compositions	The compositions property is Optional.	MAY	Composition and Completeness
12 Compositions	Each item of the compositions array must be a Compositions object.	REQUIRED	Composition and Completeness
12.1 Compositions	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
12.1 Compositions	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
12.1 Compositions	The aggregate property is Required.	REQUIRED	Composition and Completeness
12.1 Compositions	The assemblies property is Optional.	MAY	Composition and Completeness
12.1 Compositions	The dependencies property is Optional.	MAY	Composition and Completeness
12.1 Compositions	The vulnerabilities property is Optional.	MAY	Composition and Completeness
12.1 Compositions	The signature property is Optional.	MAY	Digital Signatures
12.1.3 BOM references	The assemblies property is Optional.	MAY	Composition and Completeness
12.1.3 BOM references	Each item in the assemblies array Must be any of: Ref or BOM-Link Element.	REQUIRED	Composition and Completeness
12.1.3 BOM references	All items in the assemblies array must be unique.	REQUIRED	Composition and Completeness
12.1.4 BOM references	The dependencies property is Optional.	MAY	Composition and Completeness
12.1.4 BOM references	Each item of the dependencies array must be a string.	REQUIRED	Composition and Completeness
12.1.4 BOM references	All items in the dependencies array must be unique.	REQUIRED	Composition and Completeness
12.1.5 BOM references	The vulnerabilities property is Optional.	MAY	Composition and Completeness
12.1.5 BOM references	Each item of the vulnerabilities array must be a string.	REQUIRED	Composition and Completeness
12.1.5 BOM references	All items in the vulnerabilities array must be unique.	REQUIRED	Composition and Completeness
12.1.6 Signature	The signature property is Optional.	MAY	Digital Signatures
13 Vulnerabilities	The vulnerabilities property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13 Vulnerabilities	Each item of the vulnerabilities array must be a Vulnerability object.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
13.1 Vulnerability	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
13.1 Vulnerability	The id property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The source property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The references property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The ratings property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The cwes property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The description property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The detail property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The recommendation property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The workaround property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The proofOfConcept property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The advisories property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The created property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The published property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The updated property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The rejected property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The credits property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The tools property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The analysis property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The affects property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1 Vulnerability	The properties property is Optional.	MAY	Extensibility via Properties
13.1 Vulnerability	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
13.1 Vulnerability	Formal registration is optional.	MAY	Property Taxonomies
13.1.1 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
13.1.1 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
13.1.2 ID	The id property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.3 Source	The source property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.3 Source	The url property for the source object is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.3 Source	The name property for the source object is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.3.1 URL	The url property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.3.2 Name	The name property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.4 References	The references property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.4.1.1 ID	The id property is Required.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.4.1.2 Source	The source property is Required.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.4.1.2 Source	The url property for the source object is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.4.1.2 Source	The name property for the source object is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.4.1.3 URL	The url property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.4.1.4 Name	The name property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5 Ratings	The ratings property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5 Ratings	Each item of the ratings array must be a Rating object.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.5.1 Rating	The source property for the rating is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1 Rating	The score property for the rating is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1 Rating	The severity property for the rating is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1 Rating	The method property for the rating is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1 Rating	The vector property for the rating is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1 Rating	The justification property for the rating is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1.1 Source	The source property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1.1 Source	The url property for the source is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1.1 Source	The name property for the source is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1.2 URL	The url property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1.3 Name	The name property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1.4 Score	The score property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1.5 Severity	The severity property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1.6 Method	The method property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1.7 Vector	The vector property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.5.1.8 Justification	The justification property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.6 CWEs	The cwes property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.6 CWEs	The minimum value for items in the cwes array is 1.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.6 CWEs	Each item of the cwes array must be an integer.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.7 Description	The description property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.8 Details	The detail property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.9 Recommendation	The recommendation property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.10 Workarounds	The workaround property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.11 Proof of Concept	The proofOfConcept property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.11.1 Steps to Reproduce	The reproductionSteps property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.11.2 Environment	The environment property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.11.3 Supporting Material	The supportingMaterial property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.11.3 Supporting Material	Each item of the supportingMaterial array must be an Attachment object.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.11.3.1 Attachment	The contentType property for the attachment object is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.11.3.1 Attachment	The encoding property for the attachment object is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.11.3.1 Attachment	The content property for the attachment data is Required.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.11.3.1 Attachment	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Vulnerability Information (Vulnerability Object)
13.1.11.3.2 Content-Type	The contentType property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.11.3.3 Encoding	The encoding property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.11.3.4 Attachment Text	The content property is Required.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.11.3.4 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Vulnerability Information (Vulnerability Object)
13.1.12 Advisories	The advisories property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.12 Advisories	Each item of the advisories array must be an Advisory object.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.12.1 Advisory	The title property for the advisory object is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.12.1 Advisory	The url property for the advisory object is Required.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.12.1.1 Title	The title property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.12.1.2 URL	The url property is Required.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.13 Created	The created property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.14 Published	The published property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.15 Updated	The updated property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.16 Rejected	The rejected property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.17 Credits	The credits property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.17 Credits	The organizations property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.17 Credits	The individuals property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.17.1 Organizations	The organizations property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.17.1 Organizations	Each item of the organizations array must be an Organizational Entity object.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.17.1.1 Organizational Entity	The bom-ref property for the organizational entity is Optional.	MAY	Internal Referencing (bom-ref)
13.1.17.1.1 Organizational Entity	Every bom-ref for the organizational entity must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
13.1.17.1.1 Organizational Entity	The bom-ref Value for the organizational entity SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
13.1.17.1.1 Organizational Entity	The name property for the organizational entity is Optional.	MAY	Organizational Entity Definition
13.1.17.1.1 Organizational Entity	The address property for the organizational entity is Optional.	MAY	Organizational Entity Definition
13.1.17.1.1 Organizational Entity	The url property for the organizational entity is Optional.	MAY	Organizational Entity Definition
13.1.17.1.1 Organizational Entity	The contact property for the organizational entity is Optional.	MAY	Organizational Entity Definition
13.1.17.1.2 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
13.1.17.1.2 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
13.1.17.1.2 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
13.1.17.1.3 Organization Name	The name property is Optional.	MAY	Organizational Entity Definition
13.1.17.1.4 Organization Address	The address property is Optional.	MAY	Organizational Entity Definition
13.1.17.1.4 Organization Address	The bom-ref property for the address is Optional.	MAY	Internal Referencing (bom-ref)
13.1.17.1.4 Organization Address	Every bom-ref for the address must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
13.1.17.1.4 Organization Address	The bom-ref Value for the address SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
13.1.17.1.4 Organization Address	The country property is Optional.	MAY	Organizational Entity Definition
13.1.17.1.4 Organization Address	The region property is Optional.	MAY	Organizational Entity Definition
13.1.17.1.4 Organization Address	The locality property is Optional.	MAY	Organizational Entity Definition
13.1.17.1.4 Organization Address	The postOfficeBoxNumber property is Optional.	MAY	Organizational Entity Definition
13.1.17.1.4 Organization Address	The postalCode property is Optional.	MAY	Organizational Entity Definition
13.1.17.1.4 Organization Address	The streetAddress property is Optional.	MAY	Organizational Entity Definition
13.1.17.1.5 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
13.1.17.1.5 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
13.1.17.1.5 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
13.1.17.1.6 Country	The country property is Optional.	MAY	Organizational Entity Definition
13.1.17.1.7 Region	The region property is Optional.	MAY	Organizational Entity Definition
13.1.17.1.8 Locality	The locality property is Optional.	MAY	Organizational Entity Definition
13.1.17.1.11 Street Address	The streetAddress property is Optional.	MAY	Organizational Entity Definition
13.1.17.1.12 Organization URL(s)	The url property is Optional.	MAY	Organizational Entity Definition
13.1.17.1.12 Organization URL(s)	Each item of the url array must be a string.	REQUIRED	Organizational Entity Definition
13.1.17.1.13 Organizational Contact	The contact property is Optional.	MAY	Contact Information
13.1.17.1.13 Organizational Contact	Each item of the contact array must be an Organizational Contact object.	REQUIRED	Contact Information
13.1.17.1.14 Organizational Contact	The bom-ref property for the contact is Optional.	MAY	Internal Referencing (bom-ref)
13.1.17.1.14 Organizational Contact	Every bom-ref for the contact must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
13.1.17.1.14 Organizational Contact	The bom-ref Value for the contact SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
13.1.17.1.14 Organizational Contact	The name property for the contact is Optional.	MAY	Contact Information
13.1.17.1.14 Organizational Contact	The email property for the contact is Optional.	MAY	Contact Information
13.1.17.1.14 Organizational Contact	The phone property for the contact is Optional.	MAY	Contact Information
13.1.17.1.15 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
13.1.17.1.15 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
13.1.17.1.15 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
13.1.17.1.16 Name	The name property is Optional.	MAY	Contact Information
13.1.17.1.17 Email Address	The email property is Optional.	MAY	Contact Information
13.1.17.1.18 Phone	The phone property is Optional.	MAY	Contact Information
13.1.17.2 Individuals	The individuals property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.17.2 Individuals	Each item of the individuals array must be an Organizational Contact object.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.17.2.1 Organizational Contact	The bom-ref property for the organizational contact is Optional.	MAY	Internal Referencing (bom-ref)
13.1.17.2.1 Organizational Contact	Every bom-ref for the organizational contact must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
13.1.17.2.1 Organizational Contact	The bom-ref Value for the organizational contact SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
13.1.17.2.1 Organizational Contact	The name property for the contact is Optional.	MAY	Contact Information
13.1.17.2.1 Organizational Contact	The email property for the contact is Optional.	MAY	Contact Information
13.1.17.2.1 Organizational Contact	The phone property for the contact is Optional.	MAY	Contact Information
13.1.17.2.2 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
13.1.17.2.2 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
13.1.17.2.2 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
13.1.17.2.3 Name	The name property is Optional.	MAY	Contact Information
13.1.17.2.4 Email Address	The email property is Optional.	MAY	Contact Information
13.1.17.2.5 Phone	The phone property is Optional.	MAY	Contact Information
13.1.18 Tools	The tools property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.18 Tools	The tools object Must be one of: Tools or Tools (legacy).	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.19 Tools	The components property for tools is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.19 Tools	The services property for tools is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.20.1 Components	The components list within Tools (legacy) is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.20.1 Components	Each item of the components array must be a Component object.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.20.1.1 Component	All items in the components list must be unique.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.20.2 Services	The services list within Tools (legacy) is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.20.2 Services	Each item of the services array must be a Service object.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.20.2.1 Service	All items in the services list must be unique.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.21 Tools (legacy)	Each item of the Tools (legacy) array must be a Tool object.	REQUIRED	Tooling Information
13.1.21.1 Tool	The vendor property for the tool is Optional.	MAY	Tooling Information
13.1.21.1 Tool	The name property for the tool is Optional.	MAY	Tooling Information
13.1.21.1 Tool	The version property for the tool is Optional.	MAY	Tooling Information
13.1.21.1 Tool	The hashes property for the tool is Optional.	MAY	Tooling Information
13.1.21.1 Tool	The externalReferences property for the tool is Optional.	MAY	Tooling Information
13.1.21.1.4 Hashes	The hashes property is Optional.	MAY	Cryptographic Hashes
13.1.21.1.4 Hashes	Each item of the hashes array must be a Hash object.	REQUIRED	Cryptographic Hashes
13.1.21.1.5 Hash	The alg property for the hash object is Required.	REQUIRED	Cryptographic Hashes
13.1.21.1.5 Hash	The content property for the hash object is Required.	REQUIRED	Cryptographic Hashes
13.1.21.1.6 Hash Algorithm	The alg property is Required.	REQUIRED	Cryptographic Hashes
13.1.21.1.6 Hash Algorithm	The alg value Must be one of: MD5.	REQUIRED	Cryptographic Hashes
13.1.21.1.6 Hash Algorithm	The alg value Must be one of: SHA-1.	REQUIRED	Cryptographic Hashes
13.1.21.1.6 Hash Algorithm	The alg value Must be one of: SHA-256.	REQUIRED	Cryptographic Hashes
13.1.21.1.6 Hash Algorithm	The alg value Must be one of: SHA-384.	REQUIRED	Cryptographic Hashes
13.1.21.1.6 Hash Algorithm	The alg value Must be one of: SHA-512.	REQUIRED	Cryptographic Hashes
13.1.21.1.6 Hash Algorithm	The alg value Must be one of: SHA3-256.	REQUIRED	Cryptographic Hashes
13.1.21.1.6 Hash Algorithm	The alg value Must be one of: SHA3-384.	REQUIRED	Cryptographic Hashes
13.1.21.1.6 Hash Algorithm	The alg value Must be one of: SHA3-512.	REQUIRED	Cryptographic Hashes
13.1.21.1.6 Hash Algorithm	The alg value Must be one of: BLAKE2b-256.	REQUIRED	Cryptographic Hashes
13.1.21.1.6 Hash Algorithm	The alg value Must be one of: BLAKE2b-384.	REQUIRED	Cryptographic Hashes
13.1.21.1.6 Hash Algorithm	The alg value Must be one of: BLAKE2b-512.	REQUIRED	Cryptographic Hashes
13.1.21.1.6 Hash Algorithm	The alg value Must be one of: BLAKE3.	REQUIRED	Cryptographic Hashes
13.1.21.1.7 Hash Value	The content property is Required.	REQUIRED	Cryptographic Hashes
13.1.21.1.8 External References	The externalReferences property is Optional.	MAY	External References
13.1.21.1.8 External References	Each item of the externalReferences array must be an External Reference object.	REQUIRED	External References
13.1.22 Impact Analysis	The analysis property is Optional.	MAY	Vulnerability Impact Analysis (VEX)
13.1.22.1 Impact Analysis State	The state property is Optional.	MAY	Vulnerability Impact Analysis (VEX)
13.1.22.1 Impact Analysis State	The justification property is Optional.	MAY	Vulnerability Impact Analysis (VEX)
13.1.22.1 Impact Analysis State	The response property is Optional.	MAY	Vulnerability Impact Analysis (VEX)
13.1.22.1 Impact Analysis State	Responses are strongly encouraged for vulnerabilities where the analysis state is exploitable.	RECOMMENDED	Vulnerability Impact Analysis (VEX)
13.1.22.1 Impact Analysis State	The detail property is Optional.	MAY	Vulnerability Impact Analysis (VEX)
13.1.22.1 Impact Analysis State	The firstIssued property is Optional.	MAY	Vulnerability Impact Analysis (VEX)
13.1.22.1 Impact Analysis State	The lastUpdated property is Optional.	MAY	Vulnerability Impact Analysis (VEX)
13.1.22.1 Impact Analysis State	Justification should be specified for all not_affected cases.	RECOMMENDED	Vulnerability Impact Analysis (VEX)
13.1.22.2 Impact Analysis Justification	The justification property is Optional.	MAY	Vulnerability Impact Analysis (VEX)
13.1.22.3 Response	The response property is Optional.	MAY	Vulnerability Impact Analysis (VEX)
13.1.22.3 Response	More than one response is allowed.	MAY	Vulnerability Impact Analysis (VEX)
13.1.22.3 Response	Responses are strongly encouraged for vulnerabilities where the analysis state is exploitable.	RECOMMENDED	Vulnerability Impact Analysis (VEX)
13.1.22.3 Response	Each item of the response array must be a string.	REQUIRED	Vulnerability Impact Analysis (VEX)
13.1.22.4 Detail	The detail property is Optional.	MAY	Vulnerability Impact Analysis (VEX)
13.1.22.4 Detail	If a vulnerability is not exploitable, the detail field should include specific details on why the component or service is not impacted by this vulnerability.	RECOMMENDED	Vulnerability Impact Analysis (VEX)
13.1.22.5 First Issued	The firstIssued property is Optional.	MAY	Vulnerability Impact Analysis (VEX)
13.1.22.6 Last Updated	The lastUpdated property is Optional.	MAY	Vulnerability Impact Analysis (VEX)
13.1.23 Affects	The affects property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.23.1.1 Reference	The ref property is Required.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.23.1.1 Reference	The ref property Must be any of: Ref or BOM-Link Element.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.23.1.4 Versions	The versions property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.23.1.5 Version	The version property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.23.1.6 Version Range	The range property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.23.1.7 Status	The status property is Optional.	MAY	Vulnerability Information (Vulnerability Object)
13.1.23.1.7 Status	All items in the versions array must be unique.	REQUIRED	Vulnerability Information (Vulnerability Object)
13.1.24 Properties	The properties property is Optional.	MAY	Extensibility via Properties
13.1.24 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
13.1.24 Properties	Formal registration is optional.	MAY	Property Taxonomies
13.1.24 Properties	Each item of the properties array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
13.1.24.1 Lightweight name-value pair	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
13.1.24.1 Lightweight name-value pair	Formal registration is optional.	MAY	Property Taxonomies
13.1.24.1.1 Name	The name property is Required.	REQUIRED	Extensibility via Properties
13.1.24.1.2 Value	The value property is Optional.	MAY	Extensibility via Properties
13.1.24.1.2 Value	All items in the properties array must be unique.	REQUIRED	Extensibility via Properties
14 Annotations	The annotations property is Optional.	MAY	Annotations
14 Annotations	Each item of this array must be an Annotations object.	REQUIRED	Annotations
14.1 Annotations	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
14.1 Annotations	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
14.1 Annotations	The subjects property is Required.	REQUIRED	Annotations
14.1 Annotations	The annotator property is Required.	REQUIRED	Annotations
14.1 Annotations	The timestamp property is Required.	REQUIRED	Annotations
14.1 Annotations	The text property is Required.	REQUIRED	Annotations
14.1 Annotations	The signature property is Optional.	MAY	Annotations
14.1.1 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
14.1.1 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
14.1.2 Subjects	The subjects property is Required.	REQUIRED	Annotations
14.1.2 Subjects	The subject Must be any of: Ref.	REQUIRED	Annotations
14.1.2 Subjects	The subject Must be any of: BOM-Link Element.	REQUIRED	Annotations
14.1.2.2 BOM-Link Element	All items must be unique.	REQUIRED	Annotations
14.1.3 Annotator	The annotator property is Required.	REQUIRED	Annotations
14.1.3.1 Organizational Entity	The organization property is Optional.	MAY	Annotations
14.1.3.1 Organizational Entity	The individual property is Optional.	MAY	Annotations
14.1.3.1 Organizational Entity	The component property is Optional.	MAY	Annotations
14.1.3.1 Organizational Entity	The service property is Optional.	MAY	Annotations
14.1.3.1.1 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
14.1.3.1.1 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
14.1.3.1.1 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
14.1.3.1.2 Organization Name	The name property is Optional.	MAY	Organizational Entity Definition
14.1.3.1.3 Organization Address	The address property is Optional.	MAY	Organizational Entity Definition
14.1.3.1.3 Organization Address	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
14.1.3.1.3 Organization Address	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
14.1.3.1.3 Organization Address	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
14.1.3.1.3 Organization Address	The country property is Optional.	MAY	Organizational Entity Definition
14.1.3.1.3 Organization Address	The region property is Optional.	MAY	Organizational Entity Definition
14.1.3.1.3 Organization Address	The locality property is Optional.	MAY	Organizational Entity Definition
14.1.3.1.3 Organization Address	The postOfficeBoxNumber property is Optional.	MAY	Organizational Entity Definition
14.1.3.1.3 Organization Address	The postalCode property is Optional.	MAY	Organizational Entity Definition
14.1.3.1.3 Organization Address	The streetAddress property is Optional.	MAY	Organizational Entity Definition
14.1.3.1.4 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
14.1.3.1.4 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
14.1.3.1.4 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
14.1.3.1.5 Country	The country property is Optional.	MAY	Organizational Entity Definition
14.1.3.1.6 Region	The region property is Optional.	MAY	Organizational Entity Definition
14.1.3.1.7 Locality	The locality property is Optional.	MAY	Organizational Entity Definition
14.1.3.1.11 Organization URL(s)	The url property is Optional.	MAY	Organizational Entity Definition
14.1.3.1.11 Organization URL(s)	Multiple URLs are allowed.	MAY	Organizational Entity Definition
14.1.3.1.12 Organizational Contact	The contact property is Optional.	MAY	Contact Information
14.1.3.1.12 Organizational Contact	Multiple contacts are allowed.	MAY	Contact Information
14.1.3.1.12 Organizational Contact	Each item of this array must be an Organizational Contact object.	REQUIRED	Contact Information
14.1.3.1.13 Organizational Contact	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
14.1.3.1.13 Organizational Contact	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
14.1.3.1.13 Organizational Contact	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
14.1.3.1.13 Organizational Contact	The name property is Optional.	MAY	Contact Information
14.1.3.1.13 Organizational Contact	The email property is Optional.	MAY	Contact Information
14.1.3.1.13 Organizational Contact	The phone property is Optional.	MAY	Contact Information
14.1.3.1.14 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
14.1.3.1.14 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
14.1.3.1.14 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
14.1.3.1.15 Name	The name property is Optional.	MAY	Contact Information
14.1.3.1.16 Email Address	The email property is Optional.	MAY	Contact Information
14.1.3.1.17 Phone	The phone property is Optional.	MAY	Contact Information
14.1.3.2 Organizational Contact	The individual property is Optional.	MAY	Annotations
14.1.3.2 Organizational Contact	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
14.1.3.2 Organizational Contact	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
14.1.3.2 Organizational Contact	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
14.1.3.2 Organizational Contact	The name property is Optional.	MAY	Contact Information
14.1.3.2 Organizational Contact	The email property is Optional.	MAY	Contact Information
14.1.3.2 Organizational Contact	The phone property is Optional.	MAY	Contact Information
14.1.3.2.1 BOM Reference	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
14.1.3.2.1 BOM Reference	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
14.1.3.2.1 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
14.1.3.2.2 Name	The name property is Optional.	MAY	Contact Information
14.1.3.2.3 Email Address	The email property is Optional.	MAY	Contact Information
14.1.3.2.4 Phone	The phone property is Optional.	MAY	Contact Information
14.1.3.3 Component	The component property is Optional.	MAY	Annotations
14.1.3.4 Service	The service property is Optional.	MAY	Annotations
14.1.4 Timestamp	The timestamp property is Required.	REQUIRED	Timestamping
14.1.5 Text	The text property is Required.	REQUIRED	Annotations
14.1.6 Signature	The signature property is Optional.	MAY	Digital Signatures
14.1.6 Signature	All items must be unique.	REQUIRED	Digital Signatures
15 Formulation	The formulation property is Optional.	MAY	Formulation and Reproducible Builds
15 Formulation	Each item of this array must be a Formula object.	REQUIRED	Formulation and Reproducible Builds
15.1 Formula	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.2 Components	The components property is Optional.	MAY	Formulation and Reproducible Builds
15.1.3 Services	The services property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4 Workflows	The workflows property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.7 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.7 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.7 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.13 BOM Reference	The bom-ref property is Required.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.13 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
15.1.4.1.14 Unique Identifier (UID)	The uid property is Required.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.18 Resource reference choice	The ref property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.18 Resource reference choice	The externalReference property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.19 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.19 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.19 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.31 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.44 Resource reference choice	The ref property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.44 Resource reference choice	The externalReference property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.45 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.45 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.50 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.50 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.50 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.53 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.66 Data Attachment	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Data Components and Governance
15.1.4.1.67 Content-Type	The contentType property is Optional.	MAY	Data Components and Governance
15.1.4.1.68 Encoding	The encoding property is Optional.	MAY	Data Components and Governance
15.1.4.1.69 Attachment Text	The content property is Required.	REQUIRED	Data Components and Governance
15.1.4.1.69 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Data Components and Governance
15.1.4.1.70 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.70 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.70 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.74 Resource reference choice	The externalReference property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.75 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.75 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.75 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.79 Resource reference choice	The externalReference property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.80 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.80 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.80 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.83 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.84 Parameters	The parameters property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.84 Parameters	Each item of this array must be a Parameter object.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.85 Parameter	The name property is Required.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.85 Parameter	The value property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.89 Environment variables	The environmentVars property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.90 Lightweight name-value pair	The name property is Required.	REQUIRED	Extensibility via Properties
15.1.4.1.91 Value	The value property is Optional.	MAY	Extensibility via Properties
15.1.4.1.92 Value	All items must be unique.	REQUIRED	Extensibility via Properties
15.1.4.1.93 Attachment	The data property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.94 Content-Type	The contentType property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.95 Encoding	The encoding property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.96 Attachment Text	The content property is Required.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.96 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Formulation and Reproducible Builds
15.1.4.1.97 Properties	The properties property is Optional.	MAY	Extensibility via Properties
15.1.4.1.97 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
15.1.4.1.97 Properties	Formal registration is optional.	MAY	Property Taxonomies
15.1.4.1.97 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
15.1.4.1.103 Resource reference choice	The type property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.103 Resource reference choice	The source property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.103 Resource reference choice	The target property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.103 Resource reference choice	The resource property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.104 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.104 BOM Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.108 Resource reference choice	The externalReference property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.109 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.109 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.109 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.113 Resource reference choice	The externalReference property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.114 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.114 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.114 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.117 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.118 Attachment	The data property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.119 Content-Type	The contentType property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.120 Encoding	The encoding property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.121 Attachment Text	The content property is Required.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.121 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Formulation and Reproducible Builds
15.1.4.1.122 Environment variables	The environmentVars property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.122 Environment variables	The environment variables Must be one of: Lightweight name-value pair.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.134 Steps	The steps property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.137 Commands	The commands property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.137 Commands	Each item of the commands array must be an object (Command object).	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.138 Executed	The executed property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.139 Properties	The properties property is Optional.	MAY	Extensibility via Properties
15.1.4.1.139 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
15.1.4.1.139 Properties	Formal registration is optional.	MAY	Property Taxonomies
15.1.4.1.139 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
15.1.4.1.141 Inputs	The inputs property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.141 Inputs	Each item of the inputs array must be an object (Input object).	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.149 Resource reference choice	The source property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.149 Resource reference choice	The target property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.149 Resource reference choice	The resource property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.150 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.150 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.150 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.153 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.155 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.155 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.155 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.158 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.160 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.160 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.160 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.163 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.164 Parameters	The parameters property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.168 Environment variables	The environmentVars property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.172 Value	All items must be unique.	REQUIRED	Extensibility via Properties
15.1.4.1.173 Attachment	The data property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.173 Attachment	The contentType property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.173 Attachment	The encoding property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.176 Attachment Text	The content property is Required.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.176 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Formulation and Reproducible Builds
15.1.4.1.177 Properties	The properties property is Optional.	MAY	Extensibility via Properties
15.1.4.1.177 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
15.1.4.1.177 Properties	Formal registration is optional.	MAY	Property Taxonomies
15.1.4.1.177 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
15.1.4.1.179 Outputs	The outputs property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.179 Outputs	Each item of the outputs array must be an object (Output object).	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.182 Type	The type property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.182 Type	The type value Must be one of: artifact.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.182 Type	The type value Must be one of: attestation.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.182 Type	The type value Must be one of: log.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.182 Type	The type value Must be one of: evidence.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.182 Type	The type value Must be one of: metrics.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.182 Type	The type value Must be one of: other.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.183 Resource reference choice	The source property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.183 Resource reference choice	The target property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.183 Resource reference choice	The resource property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.184 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.184 BOM Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.188 Resource reference choice	The externalReference property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.189 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.189 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.189 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.193 Resource reference choice	The externalReference property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.194 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.194 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.194 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.197 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.198 Attachment	The data property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.199 Content-Type	The contentType property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.200 Encoding	The encoding property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.201 Attachment Text	The content property is Required.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.201 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Formulation and Reproducible Builds
15.1.4.1.202 Environment variables	The environmentVars property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.202 Environment variables	The environment variables Must be one of: Lightweight name-value pair.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.214 BOM Reference	The bom-ref property is Required.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.214 BOM Reference	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
15.1.4.1.215 Unique Identifier (UID)	The uid property is Required.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.219 Resource reference choice	The resourceReferences array is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.220 Resource reference choice	The ref property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.220 Resource reference choice	The externalReference property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.221 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.221 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.221 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.224 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.224 External Reference	All items must be unique.	REQUIRED	External References
15.1.4.1.244 Value	All items must be unique.	REQUIRED	Extensibility via Properties
15.1.4.1.245 Runtime topology	The runtimeTopology property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.245 Runtime topology	Each item of this array must be a Dependency object.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.246 Dependency	The ref property is Required.	REQUIRED	Dependency Graph Representation
15.1.4.1.246 Dependency	The dependsOn property is Optional.	MAY	Dependency Graph Representation
15.1.4.1.246 Dependency	The provides property is Optional.	MAY	Dependency Graph Representation
15.1.4.1.249 Provides	Each item of this array must be a string.	REQUIRED	Dependency Graph Representation
15.1.4.1.250 Task Dependencies	The taskDependencies property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.250 Task Dependencies	The ref property is Required.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.250 Task Dependencies	The dependsOn property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.250 Task Dependencies	The provides property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.258 Provides	Each item of this array must be a string.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.267 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.267 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.267 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.272 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Formulation and Reproducible Builds
15.1.4.1.272 Attachment Text	The content property is Required.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.280 Resource reference choice	The ref property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.280 Resource reference choice	The externalReference property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.280 Resource reference choice	Each item of the ref array must be a string.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.286 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.286 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.286 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.289 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.290 Properties	The properties property is Optional.	MAY	Extensibility via Properties
15.1.4.1.290 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
15.1.4.1.290 Properties	Formal registration is optional.	MAY	Property Taxonomies
15.1.4.1.290 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
15.1.4.1.292 Inputs	The inputs property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.306 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.306 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.306 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.311 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.311 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.311 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.314 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.316 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.316 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.316 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.319 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.323 Parameters	The parameters property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.327 Environment variables	The environmentVars property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.328 Value	All items must be unique.	REQUIRED	Extensibility via Properties
15.1.4.1.329 Attachment	The data property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.329 Attachment	The contentType property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.332 Attachment Text	The content property is Required.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.332 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Formulation and Reproducible Builds
15.1.4.1.333 Properties	The properties property is Optional.	MAY	Extensibility via Properties
15.1.4.1.333 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
15.1.4.1.333 Properties	Formal registration is optional.	MAY	Property Taxonomies
15.1.4.1.333 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
15.1.4.1.334 Outputs	The outputs property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.338 Type	The type property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.338 Type	The type value Must be one of: artifact.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.338 Type	The type value Must be one of: attestation.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.338 Type	The type value Must be one of: log.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.338 Type	The type value Must be one of: evidence.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.338 Type	The type value Must be one of: metrics.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.338 Type	The type value Must be one of: other.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.339 Resource reference choice	The source property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.339 Resource reference choice	The target property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.339 Resource reference choice	The resource property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.340 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.340 BOM Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.344 Resource reference choice	The externalReference property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.345 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.345 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.345 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.349 Resource reference choice	The externalReference property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.350 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.350 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.350 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.353 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.354 Attachment	The data property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.355 Content-Type	The contentType property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.356 Encoding	The encoding property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.357 Attachment Text	The content property is Required.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.357 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Formulation and Reproducible Builds
15.1.4.1.358 Environment variables	The environmentVars property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.358 Environment variables	The environment variables Must be one of: Lightweight name-value pair.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.370 Steps	The steps property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.373 Commands	The commands property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.373 Commands	Each item of the commands array must be an object (Command object).	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.374 Executed	The executed property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.375 Properties	The properties property is Optional.	MAY	Extensibility via Properties
15.1.4.1.375 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
15.1.4.1.375 Properties	Formal registration is optional.	MAY	Property Taxonomies
15.1.4.1.375 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
15.1.4.1.377 Inputs	The inputs property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.377 Inputs	Each item of the inputs array must be an object (Input object).	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.383 Resource reference choice	The source property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.383 Resource reference choice	The target property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.383 Resource reference choice	The resource property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.386 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.386 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.386 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.391 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.391 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.391 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.394 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.396 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.396 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.396 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.399 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.401 Parameters	The parameters property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.405 Environment variables	The environmentVars property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.408 Value	All items must be unique.	REQUIRED	Extensibility via Properties
15.1.4.1.409 Attachment	The data property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.409 Attachment	The contentType property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.412 Attachment Text	The content property is Required.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.412 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Formulation and Reproducible Builds
15.1.4.1.413 Properties	The properties property is Optional.	MAY	Extensibility via Properties
15.1.4.1.413 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
15.1.4.1.413 Properties	Formal registration is optional.	MAY	Property Taxonomies
15.1.4.1.413 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
15.1.4.1.415 Outputs	The outputs property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.415 Outputs	Each item of the outputs array must be an object (Output object).	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.418 Type	The type property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.418 Type	The type value Must be one of: artifact.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.418 Type	The type value Must be one of: attestation.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.418 Type	The type value Must be one of: log.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.418 Type	The type value Must be one of: evidence.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.418 Type	The type value Must be one of: metrics.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.418 Type	The type value Must be one of: other.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.419 Resource reference choice	The source property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.419 Resource reference choice	The target property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.419 Resource reference choice	The resource property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.420 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.420 BOM Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.424 Resource reference choice	The externalReference property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.425 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.425 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.425 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.429 Resource reference choice	The externalReference property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.430 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.430 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.430 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.433 External Reference	The externalReference property is Optional.	MAY	External References
15.1.4.1.434 Attachment	The data property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.435 Content-Type	The contentType property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.436 Encoding	The encoding property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.437 Attachment Text	The content property is Required.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.437 Attachment Text	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Formulation and Reproducible Builds
15.1.4.1.438 Environment variables	The environmentVars property is Optional.	MAY	Formulation and Reproducible Builds
15.1.4.1.438 Environment variables	The environment variables Must be one of: Lightweight name-value pair.	REQUIRED	Formulation and Reproducible Builds
15.1.4.1.457 BOM Reference	The ref property is Optional.	MAY	Internal Referencing (bom-ref)
15.1.4.1.457 BOM Reference	The ref must be any of: Ref.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.457 BOM Reference	The ref must be any of: BOM-Link Element.	REQUIRED	Internal Referencing (bom-ref)
15.1.4.1.483 Reference	The ref property is Required.	REQUIRED	Dependency Graph Representation
15.1.4.1.484 Depends On	The dependsOn property is Optional.	MAY	Dependency Graph Representation
15.1.4.1.485 Provides	The provides property is Optional.	MAY	Dependency Graph Representation
15.1.5 Properties	The properties property is Optional.	MAY	Extensibility via Properties
15.1.5 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
15.1.5 Properties	Formal registration is optional.	MAY	Property Taxonomies
15.1.5 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
16 Declarations	The declarations property is Optional.	MAY	Attestations and Declarations
16.1 Assessors	The assessors property is Optional.	MAY	Attestations and Declarations
16.1 Assessors	Each item of this array must be an Assessor object.	REQUIRED	Attestations and Declarations
16.1.1 Assessor	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
16.1.1 Assessor	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
16.1.1 Assessor	The thirdParty property is Optional.	MAY	Attestations and Declarations
16.1.1 Assessor	The organization property is Optional.	MAY	Attestations and Declarations
16.2 Attestations	The attestations property is Optional.	MAY	Attestations and Declarations
16.2 Attestations	Each item of this array must be an Attestation object.	REQUIRED	Attestations and Declarations
16.2.1 Attestation	The summary property is Optional.	MAY	Attestations and Declarations
16.2.1 Attestation	The assessor property is Optional.	MAY	Attestations and Declarations
16.2.1 Attestation	The map property is Optional.	MAY	Attestations and Declarations
16.2.1 Attestation	The signature property is Optional.	MAY	Digital Signatures
16.2.1.3 Map	The map property is Optional.	MAY	Attestations and Declarations
16.2.1.3 Map	Each item of this array must be a Map object.	REQUIRED	Attestations and Declarations
16.2.1.3.1 Map	The requirement property is Optional.	MAY	Attestations and Declarations
16.2.1.3.1 Map	The claims property is Optional.	MAY	Attestations and Declarations
16.2.1.3.1 Map	The counterClaims property is Optional.	MAY	Attestations and Declarations
16.2.1.3.1 Map	The conformance property is Optional.	MAY	Attestations and Declarations
16.2.1.3.1 Map	The confidence property is Optional.	MAY	Attestations and Declarations
16.2.1.3.3 Claims	The claims property is Optional.	MAY	Attestations and Declarations
16.2.1.3.3 Claims	Each item of this array must be a string.	REQUIRED	Attestations and Declarations
16.2.1.3.4 Counter Claims	The counterClaims property is Optional.	MAY	Attestations and Declarations
16.2.1.3.4 Counter Claims	Each item of this array must be a string.	REQUIRED	Attestations and Declarations
16.2.1.3.5 Conformance	The conformance property is Optional.	MAY	Attestations and Declarations
16.2.1.3.5 Conformance	The score property is Optional.	MAY	Attestations and Declarations
16.2.1.3.5 Conformance	The rationale property is Optional.	MAY	Attestations and Declarations
16.2.1.3.5 Conformance	The mitigationStrategies property is Optional.	MAY	Attestations and Declarations
16.2.1.3.8 Mitigation Strategies	The mitigationStrategies property is Optional.	MAY	Attestations and Declarations
16.2.1.3.8 Mitigation Strategies	Each item of this array must be a string.	REQUIRED	Attestations and Declarations
16.2.1.3.9 Confidence	The confidence property is Optional.	MAY	Attestations and Declarations
16.2.1.4 Signature	The signature property is Optional.	MAY	Digital Signatures
16.3 Claims	The claims property is Optional.	MAY	Attestations and Declarations
16.3 Claims	Each item of this array must be a Claim object.	REQUIRED	Attestations and Declarations
16.3.1 Claim	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
16.3.1 Claim	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
16.3.1 Claim	The target property is Optional.	MAY	Attestations and Declarations
16.3.1 Claim	The predicate property is Optional.	MAY	Attestations and Declarations
16.3.1 Claim	The mitigationStrategies property is Optional.	MAY	Attestations and Declarations
16.3.1 Claim	The reasoning property is Optional.	MAY	Attestations and Declarations
16.3.1 Claim	The evidence property is Optional.	MAY	Attestations and Declarations
16.3.1 Claim	The counterEvidence property is Optional.	MAY	Attestations and Declarations
16.3.1 Claim	The externalReferences property is Optional.	MAY	External References
16.3.1 Claim	The signature property is Optional.	MAY	Digital Signatures
16.3.1.4 Mitigation Strategies	The mitigationStrategies property is Optional.	MAY	Attestations and Declarations
16.3.1.4 Mitigation Strategies	Each mitigation strategy should include an explanation of how any weaknesses in the evidence will be mitigated.	RECOMMENDED	Attestations and Declarations
16.3.1.4 Mitigation Strategies	Each item of this array must be a string.	REQUIRED	Attestations and Declarations
16.3.1.6 Evidence	The evidence property is Optional.	MAY	Attestations and Declarations
16.3.1.6 Evidence	Each item of this array must be a string.	REQUIRED	Attestations and Declarations
16.3.1.7 Counter Evidence	The counterEvidence property is Optional.	MAY	Attestations and Declarations
16.3.1.7 Counter Evidence	Each item of this array must be a string.	REQUIRED	Attestations and Declarations
16.3.1.8 External References	The externalReferences property is Optional.	MAY	External References
16.3.1.8 External References	Each item of this array must be an External Reference object.	REQUIRED	External References
16.3.1.9 Signature	The signature property is Optional.	MAY	Digital Signatures
16.4 Evidence	The evidence property is Optional.	MAY	Evidence and Substantiation
16.4 Evidence	Each item of this array must be an Evidence object.	REQUIRED	Evidence and Substantiation
16.4.1 Evidence	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
16.4.1 Evidence	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
16.4.1 Evidence	The propertyName property is Optional.	MAY	Evidence and Substantiation
16.4.1 Evidence	The description property is Optional.	MAY	Evidence and Substantiation
16.4.1 Evidence	The data property is Optional.	MAY	Evidence and Substantiation
16.4.1 Evidence	The created property is Optional.	MAY	Evidence and Substantiation
16.4.1 Evidence	The expires property is Optional.	MAY	Evidence and Substantiation
16.4.1 Evidence	The author property is Optional.	MAY	Evidence and Substantiation
16.4.1 Evidence	The reviewer property is Optional.	MAY	Evidence and Substantiation
16.4.1 Evidence	The signature property is Optional.	MAY	Digital Signatures
16.4.1.4 Data	The data property is Optional.	MAY	Data Components and Governance
16.4.1.4 Data	Each item of this array must be a Data object.	REQUIRED	Data Components and Governance
16.4.1.4.1 Data	The name property is Optional.	MAY	Data Components and Governance
16.4.1.4.1 Data	The contents property is Optional.	MAY	Data Components and Governance
16.4.1.4.1 Data	The classification property is Optional.	MAY	Data Components and Governance
16.4.1.4.1 Data	The sensitiveData property is Optional.	MAY	Data Components and Governance
16.4.1.4.1 Data	The governance property is Optional.	MAY	Data Components and Governance
16.4.1.4.3 Data Contents	The attachment property is Optional.	MAY	Data Components and Governance
16.4.1.4.3 Data Contents	The url property is Optional.	MAY	Data Components and Governance
16.4.1.4.4 Attachment	The contentType property is Optional.	MAY	Data Components and Governance
16.4.1.4.4 Attachment	The encoding property is Optional.	MAY	Data Components and Governance
16.4.1.4.4 Attachment	The content property is Required.	REQUIRED	Data Components and Governance
16.4.1.4.4 Attachment	Proactive controls such as input validation and sanitization should be employed to prevent misuse of attachment text.	RECOMMENDED	Data Components and Governance
16.4.1.4.10 Sensitive Data	The sensitiveData property is Optional.	MAY	Data Components and Governance
16.4.1.4.10 Sensitive Data	Each item of this array must be a string.	REQUIRED	Data Components and Governance
16.4.1.4.11 Data Governance	The governance property is Optional.	MAY	Data Components and Governance
16.4.1.4.12 Data Custodians	The custodians property is Optional.	MAY	Data Components and Governance
16.4.1.4.36 Data Stewards	The stewards property is Optional.	MAY	Data Components and Governance
16.4.1.4.60 Data Owners	The owners property is Optional.	MAY	Data Components and Governance
16.4.1.7 Organizational Contact	The author property is Optional.	MAY	Organizational Entity Definition
16.4.1.7 Organizational Contact	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
16.4.1.7 Organizational Contact	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
16.4.1.7 Organizational Contact	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
16.4.1.7 Organizational Contact	The name property is Optional.	MAY	Contact Information
16.4.1.7 Organizational Contact	The email property is Optional.	MAY	Contact Information
16.4.1.7 Organizational Contact	The phone property is Optional.	MAY	Contact Information
16.4.1.8 Organizational Contact	The reviewer property is Optional.	MAY	Organizational Entity Definition
16.4.1.8 Organizational Contact	The bom-ref property is Optional.	MAY	Internal Referencing (bom-ref)
16.4.1.8 Organizational Contact	Every bom-ref must be unique within the BOM.	REQUIRED	Internal Referencing (bom-ref)
16.4.1.8 Organizational Contact	The bom-ref Value SHOULD not start with the BOM-Link intro 'urn:cdx:' to avoid conflicts with BOM-Links.	RECOMMENDED	Internal Referencing (bom-ref)
16.4.1.8 Organizational Contact	The name property is Optional.	MAY	Contact Information
16.4.1.8 Organizational Contact	The email property is Optional.	MAY	Contact Information
16.4.1.8 Organizational Contact	The phone property is Optional.	MAY	Contact Information
16.4.1.9 Signature	The signature property is Optional.	MAY	Digital Signatures
16.5 Targets	The targets property is Optional.	MAY	Attestations and Declarations
16.5.1 Organizations	The organizations property is Optional.	MAY	Attestations and Declarations
16.5.1 Organizations	Each item of this array must be an Organizational Entity object.	REQUIRED	Attestations and Declarations
16.5.2 Components	The components property is Optional.	MAY	Attestations and Declarations
16.5.3 Services	The services property is Optional.	MAY	Attestations and Declarations
16.5.3 Services	Each item of this array must be a Service object.	REQUIRED	Attestations and Declarations
16.6 Affirmation	The affirmation property is Optional.	MAY	Attestations and Declarations
16.6.1 Statement	The statement property is Optional.	MAY	Attestations and Declarations
16.6.2 Signatories	The signatories property is Optional.	MAY	Attestations and Declarations
16.6.2 Signatories	Each item of this array must be a Signatory object.	REQUIRED	Attestations and Declarations
16.6.2.1 Signatory	The name property is Optional.	MAY	Attestations and Declarations
16.6.2.1 Signatory	The role property is Optional.	MAY	Attestations and Declarations
16.6.2.1 Signatory	The signature property is Optional.	MAY	Attestations and Declarations
16.6.2.1 Signatory	The organization property is Optional.	MAY	Attestations and Declarations
16.6.2.1 Signatory	The externalReference property is Optional.	MAY	Attestations and Declarations
16.6.3 Signature	The signature property is Optional.	MAY	Digital Signatures
16.7 Signature	The signature property is Optional.	MAY	Digital Signatures
17 Definitions	The definitions property is Optional.	MAY	Root Object Model
17.1 Standards	The standards property is Optional.	MAY	Attestations and Declarations
17.1 Standards	Each item of this array must be a Standard object.	REQUIRED	Attestations and Declarations
17.1.1 Standard	The version property is Optional.	MAY	Attestations and Declarations
17.1.1 Standard	The description property is Optional.	MAY	Attestations and Declarations
17.1.1 Standard	The owner property is Optional.	MAY	Attestations and Declarations
17.1.1 Standard	The requirements property is Optional.	MAY	Attestations and Declarations
17.1.1 Standard	The levels property is Optional.	MAY	Attestations and Declarations
17.1.1 Standard	The externalReferences property is Optional.	MAY	External References
17.1.1 Standard	The signature property is Optional.	MAY	Digital Signatures
17.1.1.6 Requirements	The requirements property is Optional.	MAY	Attestations and Declarations
17.1.1.6 Requirements	The title property is Optional.	MAY	Attestations and Declarations
17.1.1.6 Requirements	The text property is Optional.	MAY	Attestations and Declarations
17.1.1.6 Requirements	The descriptions property is Optional.	MAY	Attestations and Declarations
17.1.1.6 Requirements	The openCre property is Optional.	MAY	Attestations and Declarations
17.1.1.6 Requirements	The parent property is Optional.	MAY	Attestations and Declarations
17.1.1.6 Requirements	The properties property is Optional.	MAY	Extensibility via Properties
17.1.1.6 Requirements	The externalReferences property is Optional.	MAY	External References
17.1.1.6.6 Descriptions	The descriptions property is Optional.	MAY	Attestations and Declarations
17.1.1.6.6 Descriptions	Each item of this array must be a string.	REQUIRED	Attestations and Declarations
17.1.1.6.7 OWASP OpenCRE Identifier(s)	The openCre property is Optional.	MAY	Attestations and Declarations
17.1.1.6.7 OWASP OpenCRE Identifier(s)	Each item of this array must be a string.	REQUIRED	Attestations and Declarations
17.1.1.6.9 Properties	The properties property is Optional.	MAY	Extensibility via Properties
17.1.1.6.9 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
17.1.1.6.9 Properties	Formal registration is optional.	MAY	Property Taxonomies
17.1.1.6.9 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
17.1.1.6.13 External References	The externalReferences property is Optional.	MAY	External References
17.1.1.6.13 External References	Each item of this array must be an External Reference object.	REQUIRED	External References
17.1.1.8 Levels	The levels property is Optional.	MAY	Attestations and Declarations
18 Properties	The properties property is Optional.	MAY	Extensibility via Properties
18 Properties	Property names of interest to the general public are encouraged to be registered in the CycloneDX Property Taxonomy.	RECOMMENDED	Property Taxonomies
18 Properties	Formal registration is optional.	MAY	Property Taxonomies
18 Properties	Each item of this array must be a Lightweight name-value pair object.	REQUIRED	Extensibility via Properties
18.1.1 Name	The name property is Required.	REQUIRED	Extensibility via Properties
18.1.2 Value	The value property is Optional.	MAY	Extensibility via Properties
19 Signature	The signature property is Optional.	MAY	Digital Signatures
19 Signature	All items must be unique.	REQUIRED	Digital Signatures

and could i possiblymake the writeup better based on what my advisor told me? and maybe make the results more explicit like using some block or smthn? also in case somewhere it is required to put a dash like in a word like re-examined u should be putting a dash, but dont use hyphens instead of things like commas is what i meant. could the representation be more robust and writeup more in a manner that my advisor wants? could maybe maybe bold the final line of each para? just suggesting need not to obviously, just only in case itll improve the writeup that's it. also let me know what should i tell my advisor after putting into overleaf, like maybe thm like "hello could you possibly revisit the writeup" and maybe also add 1-2 lines of what's changed?

Show more
22 Apr, 15:43

Not fully yet. It is much better than before, but there are still three advisor points that are only partly addressed.

What is now better

4.2.3 is no longer purely anecdotal.
You now cite Balliu et al. for the production step and scope mismatch.
The subsection reads more like findings than before.
What is still missing

You still have not added any inspection of SBOM generator implementations.
You still have not added the comparison with sbomqs.
The results in 4.2.3 can still be made more explicit by tying each claim to exact spec sections and keywords.
My honest read
If your advisor re reads it now, I think they will say:

this is better
the Balliu evidence helps
but the paper still needs one small implementation facing piece and one quality tool facing piece
Best upgrades with low effort
I would do these next:

Make the results more explicit inside 4.2.3
Add exact section references from the spec in each paragraph. For example:
minimum elements:
Section 7 BOM Metadata, Section 7.1 Timestamp, Section 7.5 BOM Authors, Section 7.8 Supplier
dependencies:
Section 11 Dependencies, Section 11.1 Dependency
completeness:
Section 12 Compositions
reproducibility:
Section 15 Formulation
scope:
Section 8.1.13 Component Scope
VEX:
Section 13.1.22 Impact Analysis
That will make the subsection look much more evidence backed.

Add one short VEX paragraph
Your advisor explicitly noticed VEX. Right now it is still too brief.
You can add this after the paragraph on advanced security objects:

\paragraph{VEX support is present, but not baseline.}
CycloneDX 1.6 includes a dedicated mechanism for vulnerability impact communication through the \texttt{analysis} object under the vulnerability model. However, the relevant fields remain optional. Section 13 defines the root \texttt{vulnerabilities} object as optional, and Section 13.1.22 defines \texttt{analysis}, \texttt{state}, \texttt{justification}, and \texttt{response} as optional as well. The specification recommends that responses be provided for exploitable cases and that justification be specified for \texttt{not\_affected} cases, but these remain recommendations rather than baseline obligations. As a result, CycloneDX can represent VEX style statements, yet it does not require the presence of the vulnerability context needed to make those statements consistently available in ordinary SBOM generation.
Add one short sentence about your next implementation step
Somewhere in discussion or reply to advisor, state that you will inspect how selected generators actually populate:
dependency graphs
supplier, timestamp, authors
scope and completeness related fields
Add one short positioning sentence on sbomqs
You do not need a big subsection yet. Even one sentence in the email and later one paragraph in the paper is enough:
sbomqs can check surface quality and required fields
it cannot resolve underspecified population semantics such as production step, scope computation, or true transitive completeness without external context
Should you use blocks or bold takeaway lines
I would not use decorative blocks.
For this kind of paper, a cleaner way is:

keep normal paragraphs
make the first sentence of each paragraph a result sentence
optionally end each paragraph with a short explicit takeaway sentence
So this is good:

first sentence states the finding
rest gives evidence
last sentence states the implication
I would not bold the final line of every paragraph. That may look forced.

A stronger opening for 4.2.3
You can tighten the first two lines like this:

Our re-examination of the extracted CycloneDX requirements yields three concrete results. First, CycloneDX is usually strict about the internal structure of objects once they are present. Second, many security relevant objects remain optional at the baseline level. Third, several important security distinctions, such as production step and scope, are representable in the model but underspecified at the point where tools must populate them.
That sounds more like results immediately.

What to tell your advisor after updating Overleaf
Send this:

Thank you Dr. Mohannad. I have updated Section 4.2.3 in Overleaf.

The revised version now grounds the CycloneDX claims in explicit specification evidence and adds the Balliu et al. discussion on production step and scope as concrete examples of mismatch between the standard and producer behavior. I am next planning a small follow up on selected SBOM generator implementations and a short comparison with sbomqs so that we address both the implementation side and the quality tool side more directly.

If you want, I can do one more pass now and rewrite your current 4.2.3 into an even sharper version with exact section numbers from the CycloneDX extraction table woven directly into each paragraph.





22 Apr, 15:44
pls give me what i need to replace 4.2.3 with, or is it fine as of now already? ill work on sbomqs and sbom generator tools later on :"\section{Results}
\label{sec:results}

\subsection{Finding list of known issues in SBOM generation}
\label{subsec:systematization}

Below is a list of the problems that need to be addressed:
\begin{enumerate}
\item Failure to meet the minimum elements specified by the CISA guidelines \cite{cmuplugfest}.
\item Transitive dependencies are missed \cite{differentialanalysisyu}.
\item Tools employ different methodologies for parsing metadata \cite{differentialanalysisyu}. Additionally, there is a lack of standardised meta-data formats in and across languages further preventing a single methodology to encompass every possibility. \cite{pythonsboms, javasboms}
\item Interoperability issues where one tool produces a better SBOM for one format over another \cite{bomsaway}.
\item Lack of reproducibility in the builds on which SBOMs are created. \cite{reproduciblebuildsforne}
\item View of SBOMs as unncessary and merely a compliance checkbox. \cite{maintainersvulnmgmtwermke}
\item Inconsistencies in the naming of packages. \cite{differentialanalysisyu}
\item Inability to capture whether a libary was actually loaded onto memory or not due to the static nature of an SBOM. \cite{nodeshieldcornelissen}
\end{enumerate}

We analyse each of the specifications according to each of the problems above and address them. We focus on what aspects of the specifications try to address these issues, and which of these issues do the specifications not address.


\subsection{Reproducible thematic analysis}

\subsubsection{SPDX}

The SPDX standard prescribes the structure, content, and conformance requirements for SBOM generation. Profiles in SPDX 3.0.1 are central to this architecture; they represent modular subsets of the full specification that allow SBOM authors to tailor the level of expressiveness and complexity to their specific use case. There are 8 profiles available, out of which only the core profile is mandatory and all the rest are optional: core, software, security, licensing, dataset, AI, build, lite, and extension profiles. % I need to explain profiles better but I am unsure how to

The document is organized into three major sections: (1) an introduction that provides guidance on how to interpret the overall structure alongside some overarching and legal rules; (2) a detailed description of the available profiles, including the classes, properties, definitions, and special requirements associated with each; and (3) an appendix that offers practical guidance such as a Lite-profile example SBOM and an extensive discussion of Package URL (purl) syntax.


Below is a description of each of the themes that was created. A distribution of the themes is shown in Table \ref{tab:spdx_theme_distribution}:
\begin{itemize}
    \item \textbf{Class-specific rules (57\%)}: Requirements defining the structure or content of what a class in SPDX may contain. It is further split into two categories, rules defining the properties a class may contain or the rules defining what the content inside these properties may be.
    \item \textbf{Overarching conformance (22\%)}: Requirements which are generalized and cannot be associated with any other theme. These are further split into three categories, requirements which apply to the core profile (thus every SBOM), requirements which apply only to the lite profile, and requirements which apply only to any other profile, excluding the core and lite profiles.
    \item \textbf{Serialization (6\%)}: Requirements about how to format an SBOM document. These are further divided into two, requirements which apply to only JSON-LD serialization and requirements which are more general.
    \item \textbf{Syntax (13\%)}: Syntactic requirements for writing SPDX license strings, creating old-style templates to match non-standard licenses, and requirements for correctly creating, reading, and handling Package URLs (purl).
    \item \textbf{Legal (2\%)}: Requirements relating to the legal side of using SBOMs, specifically how to use the SPDX name and reusing the specification document, and requirements for comparing license texts and interpreting approval flags.
\end{itemize}

\begin{table}[t]
\caption{Distribution of Thematic Categories in SPDX 3.0.1 Requirements}
\label{tab:spdx_theme_distribution}
\centering
\begin{tabular}{@{}ll@{}}
\toprule
\textbf{Theme} & \textbf{Percentage} \\ 
\midrule

\textbf{Class-Specific Rules} & \textbf{57}\% \\
\hspace{1.5em}Class Structure Rules & 49\% \\
\hspace{1.5em}Class Content Rules & 8\% \\[4pt]

\textbf{Overarching Conformance} & \textbf{22}\% \\
\hspace{1.5em}General Conformance & 2\% \\
\hspace{1.5em}Lite Profile Conformance & 17\% \\
\hspace{1.5em}Profile-Specific Conformance & 3\% \\[4pt]

\textbf{Serialization} & \textbf{6}\% \\
\hspace{1.5em}General Serialization & 5\% \\
\hspace{1.5em}JSON-LD Serialization & 1\% \\[4pt]

\textbf{Syntax} & \textbf{13}\% \\
\hspace{1.5em}Legacy Template Syntax & 1\% \\
\hspace{1.5em}License Expression Syntax & 1\% \\
\hspace{1.5em}Package URL (purl) Syntax & 11\% \\[4pt]

\textbf{Legal} & \textbf{2}\% \\
\hspace{1.5em}Legal Requirements & 1\% \\
\hspace{1.5em}License-Matching Requirements & 1\% \\

\bottomrule
\end{tabular}
\end{table}

We conclude that the focus of the SPDX 3.0.1 specifications is mainly on class-specific rules, which it defines and then these can be used to create objects which can be used to represent different aspects of an SBOM. However, the 6:1 ratio between class structure rules and class content rules shows SPDX 3.0.1's importance over maintaining the structure of the SBOM over its semantics. We also note notable focus into lite profile conformance to give a starting point for new developers to create a basic SBOM to fulfil the basic requirements. Moreover, the purl syntax is extensively discussed, which shows an effort to ensure that the packages are kept universally consistent once included in an SBOM.

\subsubsection{CycloneDX}

Our analysis of the 1,724 normative requirements from CycloneDX 1.6 reveals a specification distinct from SPDX in its emphasis on specialized security use cases. We categorized requirements into seven high-level themes (Table \ref{tab:cdx_theme_distribution}).

\begin{table}[t]
\caption{Distribution of Thematic Categories in CycloneDX 1.6 Requirements}
\label{tab:cdx_theme_distribution}
\centering
%\resizebox{\columnwidth}{!}{%
\begin{tabular}{@{}ll@{}}
\toprule
\textbf{Theme} & \textbf{Percentage} \\ 
\midrule

\textbf{Advanced \& Specialized Data Models} & \textbf{35.3}\% \\
\hspace{1.5em}Cryptographic Asset Mgmt (CBOM) & 12.8\% \\
\hspace{1.5em}Formulation \& Reproducibility & 8.8\% \\[4pt]

\textbf{Foundational BOM Structure} & \textbf{17.8}\% \\
\hspace{1.5em}Internal Referencing (bom-ref) & 15.1\% \\
\hspace{1.5em}BOM Identification & 1.1\% \\[4pt]

\textbf{Trust, Integrity, and Security} & \textbf{16.0}\% \\
\hspace{1.5em}Vulnerability Information & 6.2\% \\
\hspace{1.5em}Cryptographic Hashes & 4.4\% \\[4pt]

\textbf{Metadata \& Provenance} & \textbf{12.8}\% \\
\hspace{1.5em}Organizational Entity Definition & 6.3\% \\
\hspace{1.5em}Contact Information & 3.8\% \\[4pt]

\textbf{Extensibility and Customization} & \textbf{6.6}\% \\
\hspace{1.5em}Extensibility via Properties & 3.8\% \\
\hspace{1.5em}Property Taxonomies & 2.8\% \\[4pt]

\textbf{Core Inventory \& Attributes} & \textbf{6.4}\% \\
\hspace{1.5em}Descriptive Metadata & 2.1\% \\
\hspace{1.5em}Standardized Ext. Identifiers & 2.1\% \\[4pt]

\textbf{Relationships \& Composition} & \textbf{5.2}\% \\
\hspace{1.5em}External References & 2.7\% \\
\hspace{1.5em}Dependency Graph Representation & 1.3\% \\

\bottomrule
\end{tabular}
%}
\end{table}

The analysis highlights that CycloneDX allocates the largest portion of its normative text (35.3\%) to \textbf{Advanced and Specialized Data Models}, specifically for Cryptography (CBOM) and Build Formulation. In contrast, the \textbf{Core Inventory} theme—which covers basic component definitions—comprises only 6.4\% of the requirements. This structural imbalance suggests the standard is optimized for complex, high-maturity security use cases rather than basic inventory management.

% \subsubsection{CycloneDX Revisited Through a Security Lens}
% \label{subsec:cdx_security_lens}

\subsubsection{CycloneDX Security Relevant Guardrails}
\label{subsec:cdx_security_results}

The thematic distribution in Table~\ref{tab:cdx_theme_distribution} shows where CycloneDX 1.6 allocates normative attention, but it does not by itself show whether these requirements provide strong baseline protection against the failures identified in Section~\ref{subsec:systematization}. We therefore re examined the extracted requirements with a narrower question: which known SBOM failure modes are directly constrained by CycloneDX, how strong those constraints are, and whether they can be checked from the SBOM artifact itself.

This second pass shows a consistent pattern. CycloneDX is strict once a producer chooses to populate a field or object, but it is often permissive about whether the security relevant object must appear at all. The result is that local object integrity is usually well constrained, while baseline security sufficiency is not.

\paragraph{Minimum elements are weakly enforced.}
CycloneDX contains fields for provenance and authorship, but it does not require them at the metadata level. In particular, \texttt{metadata.supplier}, \texttt{metadata.authors}, and \texttt{metadata.timestamp} are optional. This is a concrete weakness for the first failure mode in Section~\ref{subsec:systematization}, since these fields are central to the CISA minimum elements. The implication is direct: a CycloneDX document may be valid while still omitting core provenance information needed for policy and vulnerability management workflows. This is not merely a theoretical concern. Our schema comparison in Section 4.3.1 shows that the official JSON schema also leaves these fields non mandatory, so this weakness is preserved in actual validation practice.

\paragraph{Dependency completeness is only partly constrained.}
CycloneDX contains an explicit dependency graph model through the root \texttt{dependencies} array. When this graph is present, the specification is locally strict. Each item must be a Dependency object, each dependency must contain a \texttt{ref}, and components or services without dependencies must still appear as empty elements in the graph. However, the root \texttt{dependencies} object itself remains optional, and the stronger statement about completeness is phrased only as guidance: SBOMs should ideally contain all direct and transitive components and the dependency relationships between them. This means the standard constrains dependency graphs if they are present, but does not require a producer to provide one. As a result, CycloneDX offers only partial protection against transitive dependency omission.

\paragraph{Population semantics remain underspecified.}
A key limitation is that CycloneDX often specifies representation without clearly specifying population. This point is supported by prior empirical work on Java SBOM production \cite{balliu2023sbomjava}. Balliu et al. show that producers generate CycloneDX SBOMs at different points in the software lifecycle, including source, build, and post packaging stages, and note that the standard does not clearly require producers to state or justify the production step they use. This matters because the set of observable dependencies can change substantially across these stages. The same study also shows disagreement in the use of the \texttt{scope} field. For the same dependency, some producers report \texttt{optional}, others report \texttt{required}, and others omit the field entirely. Because the specification does not clearly define how scope should be computed, these outputs cannot be reliably adjudicated against the standard. This is concrete evidence that CycloneDX can encode security relevant distinctions while still leaving the population process underspecified.

\paragraph{Advanced security objects exist, but they are dormant by default.}
CycloneDX 1.6 includes rich structures for vulnerability communication, build provenance, completeness assertions, and higher assurance use cases. Examples include \texttt{vulnerabilities}, \texttt{analysis}, \texttt{formulation}, and \texttt{compositions}. These objects are important because they relate directly to several of the failure modes in Section~\ref{subsec:systematization}, including reproducibility, checkbox compliance, and vulnerability context. However, these structures remain optional at the root level. This means the standard has the vocabulary needed to express important security properties, but it does not make those properties part of the baseline SBOM. In practical terms, these guardrails remain dormant unless the producer voluntarily opts into them.

\paragraph{Normalization is stronger than semantic consistency.}
CycloneDX provides useful normalization mechanisms for package identity. Fields such as \texttt{purl}, \texttt{cpe}, \texttt{swhid}, \texttt{omniborId}, and \texttt{swid} must conform to external specifications when present. This is a genuine strength for reducing package naming inconsistency. However, the same level of discipline is not applied to the \texttt{properties} mechanism. The specification recommends use of the CycloneDX Property Taxonomy, but formal registration remains optional. This gives producers a flexible extension mechanism, but also leaves room for semantic fragmentation across tools. Thus, CycloneDX is stronger at normalizing identifiers than at normalizing producer defined metadata.

These results suggest that CycloneDX is best understood as a strong representation standard with weak baseline guarantees for security sufficient SBOM generation. Its main limitation is not lack of expressiveness. Rather, the limitation is that many of its most security relevant controls are optional, conditional, or underspecified at the point where tools must actually populate them. This helps explain why tool inconsistency can persist even when tools produce schema valid and standard conformant output.

\begin{table*}[t]
\caption{CycloneDX guardrails against known SBOM failure modes}
\label{tab:cdx_security_guardrails}
\centering
\small
\begin{tabular}{p{3.4cm} p{5.1cm} p{2.2cm} p{3.0cm}}
\toprule
\textbf{Failure mode} & \textbf{Relevant CycloneDX mechanism} & \textbf{Strength} & \textbf{Verifiability} \\
\midrule
Failure to meet minimum elements &
\texttt{metadata.supplier}, \texttt{metadata.authors}, and \texttt{metadata.timestamp} exist, but all are optional &
Weak &
Artifact verifiable when present \\
\addlinespace[2pt]

Transitive dependency omission &
\texttt{dependencies} supports graph representation, but the object is optional and transitive completeness is only recommended &
Weak to Moderate &
Partly artifact verifiable \\
\addlinespace[2pt]

Metadata parsing divergence &
The standard provides little guidance on how metadata should be extracted from source, environment, or build context &
None to Very Weak &
Not artifact verifiable \\
\addlinespace[2pt]

Interoperability loss &
Typed identifiers and references are strongly constrained when present, but \texttt{properties} remain loosely governed &
Mixed &
Partly artifact verifiable \\
\addlinespace[2pt]

Reproducibility gap &
\texttt{formulation} can represent build provenance and workflow detail, but it is optional &
Dormant &
Artifact verifiable when present \\
\addlinespace[2pt]

Checkbox compliance &
\texttt{compositions} can express completeness claims, but it is optional &
Weak &
Artifact verifiable when present \\
\addlinespace[2pt]

Package naming inconsistency &
\texttt{purl}, \texttt{cpe}, \texttt{swhid}, \texttt{omniborId}, and \texttt{swid} support normalized identity &
Moderate &
Artifact verifiable \\
\addlinespace[2pt]

Runtime blind spot &
The model can represent runtime relevant information, but it does not require a baseline distinction between present and actually used components &
Weak &
Requires external context \\
\bottomrule
\end{tabular}
\end{table*}


\subsection{Practical applicability of the standards}

\subsubsection{Intra-specification consistency}

Our analysis revealed significant discrepancies in both specifications, indicating that the official schemas often diverge from the normative text.

\begin{itemize}
    \item \textbf{SPDX 3.0.1:} No differences were found in Definition Presence and Property Presence. However, a total of 30 differences were found in Property Type. In 14 cases, the official schema was more lax than the normative text, allowing a property to be a constant/ string as well as an object using the 'oneOf' condition. In 16 cases, the official schema was more strict than the normative text, where it applied 2 regexes instead of 1 using the 'allOf' condition in DateTime strings.
    
    \item \textbf{CycloneDX 1.6:} Our differential analysis between the prescriptive prose and the official JSON schema reveals a critical \textbf{CISA Compliance Gap}. 
        
    The CISA guidelines mark "Supplier Name", "Author Name", and "Timestamp" as \textbf{REQUIRED}. However, the official CycloneDX 1.6 JSON Schema defines \texttt{metadata.supplier}, \texttt{metadata.authors}, and \texttt{metadata.timestamp} as non-mandatory fields (no \texttt{required} constraint in JSON Schema). 
        
    Consequently, a JSON file can validate perfectly against the CycloneDX schema while failing to meet the federal minimum requirements. Additionally, our automated check found 38 granular constraint mismatches, including \texttt{specVersion} not enforcing the value '1.6' in the schema, despite the text mandating it.
    
\end{itemize}

\subsubsection{Conditionality analysis}

Our findings demonstrate that both specifications are overwhelmingly conditional, though they achieve this through different architectural patterns:
\begin{itemize}
    \item \textbf{SPDX 3.0.1:} Out of 429 extracted requirements, only \textbf{69 (16\%)} are applicable to the minimum template SBOM. The majority of requirements are conditional based on \textit{Class Instantiation} (242 cases) or \textit{Profile Conformance} (93 cases). This structural heavy-handedness allows for "valid but empty" SBOMs, where the topology is enforced, but data richness is optional.
    
    \item \textbf{CycloneDX 1.6:} Out of 1,724 requirements, only \textbf{6 (0.35\%)} are universally applicable to the minimum purposeful SBOM.

    The standard utilizes an architecture where requirements are conditional upon the presence of optional root-level objects. Our analysis identified exactly \textbf{56} normative requirements governing Machine Learning Model Cards (ML-BOM) and \textbf{151} requirements governing Formulation (build reproducibility). However, because the root \texttt{modelCard} and \texttt{formulation} objects are defined as \textbf{OPTIONAL} (MAY), these 207 combined requirements remain dormant unless a user voluntarily attempts to implement those specific features.
    
    This confirms that CycloneDX conformance is highly dynamic: a tool can be compliant while implementing less than 1\% of the specification, provided it does not attempt to use advanced features incorrectly.
    
\end{itemize}

To further investigate the structural mechanisms enabling this conditionality, we performed a topological analysis of the Prescriptive Schema. We calculated the Breadth (direct reuse count), Ancestor Count (complexity), and Max Depth for all CycloneDX classes. Table~\ref{tab:cdx_metrics} presents the metrics for the most structurally critical classes.

Three key architectural patterns emerge from this data:
\begin{itemize}
    \item \textbf{Graph Connectivity:} The \texttt{refType} class is the most reused definition (Breadth 25). This confirms the standard operates as a loosely connected graph of string references rather than a strict hierarchy.
    \item \textbf{Generic Extensions:} The \texttt{property} class is the second most reused structure (Breadth 17). This indicates a systemic reliance on generic key-value pairs over standardized schema fields.
    \item \textbf{Isolated Roots:} Major functional classes like \texttt{vulnerability} and \texttt{formula} exhibit zero Breadth, confirming they exist as isolated "silos" that do not enforce structural dependencies on the core component inventory.
\end{itemize}

\begin{table}[h]
\caption{Structural Metrics of Top 10 Critical CycloneDX 1.6 Classes.}
\label{tab:cdx_metrics}
\centering
\small
\begin{tabular}{@{}l c c l@{}}
\toprule
\textbf{Class Name} & \textbf{Breadth} & \textbf{Anc.} & \textbf{Structural Role} \\
\midrule
refType & 25 & 41 & Graph Connectivity \\
property & 17 & 25 & Generic Extension \\
signature & 12 & 18 & Integrity \\
organizationalEntity & 10 & 25 & Entity Definition \\
attachmentText & 10 & 31 & Inline Data \\
component & 6 & 8 & Core Inventory \\
vulnerability & 0 & 0 & Isolated Root \\
\bottomrule
\end{tabular}
\end{table}

\begin{table}[t]
\caption{Distribution of SPDX 3.0.1 Conditional Requirements by Dependency Type}
\label{tab:spdx_dependency_types}
\centering
\small
\begin{tabular}{@{}lcl@{}}
\toprule
\textbf{Type} & \textbf{Number of Cases} & \textbf{Description} \\
\midrule
Class & 242 & Instantiation of a class. \\
Profile & 93 & Conformance to a profile. \\
Property & 56 & Presence of a property. \\
DataType & 3 & Presence of a DataType. \\
Serialization & 5 & Specific serialization used. \\
\bottomrule
\end{tabular}
\end{table}

\subsubsection{Comparison with CISA minimum elements}

Our extraction of 133 normative requirements from the CISA "Framing" document reveals a distinct bifurcation in prescriptive intent. The thematic distribution is heavily skewed toward two categories: \textbf{Component \& SBOM Attributes} (36\%) and \textbf{SBOM Operations \& Lifecycle} (29\%).

Critically, we observe a divergence in the normative keywords used between these themes:
\begin{itemize}
    \item \textbf{Operations are Mandatory:} The \textit{Operations} theme is dominated by \textbf{REQUIRED} keywords (e.g., "An SBOM needs to be created when a Component is released"). This establishes a rigid policy baseline for \textit{when} and \textit{how} SBOMs are exchanged.
    \item \textbf{Data Quality is Aspirational:} The \textit{Component Attributes} theme frequently uses \textbf{SHOULD} or \textbf{RECOMMENDED} (e.g., "Supplier Name should be identified carefully" and "list as many globally unique identifiers as available"). 
\end{itemize}

This creates a regulatory concern where the process of generating an SBOM is strictly enforced, but the data quality within that SBOM is often relegated to "Recommended Practice" rather than "Minimum Expectation," allowing tools to produce operationally valid but semantically poor data.

\subsection{Dependency resolution mechanisms in action}

\subsubsection{Results - SPDX 3.0.1\\\\}
\textbf{Analysis of requirements} 

A dependency graph contains two parts in SPDX: the edges of the graph are expressed by using the 'Relationship' class in SPDX 3.0.1. The summary of relationship is as follows:

\begin{quote}
    "Describes a relationship between one or more elements."
\end{quote}

The nodes of the graph are represented by the abstract class ‘Element’. The description states the following:

\begin{quote}
	“Within SPDX-3.0 structure this is the base class acting as a consistent, unifying, and interoperable foundation for all explicit and inter-relatable content objects.”
\end{quote}

In order to investigate dependency resolution, we isolate all requirements which refer to the relationship class or the \textbf{resolution} of the Element class or any of its subclasses. A total of 17 requirements were selected which encompassed the relationship class, the requirements reveal that the relationship class have a mandatory field 'relationshipType' of type 'RelationshipType', an enumeration of 62 possible types. Out of the 62 types, we choose \textbf{'dependsOn'} as the type to signal a dependency, which is consistent with the report in \cite{cmuplugfest}. Additionally, we also choose \textbf{‘contains’} to signal a dependency.

Out of the 17 requirements, they can be classified as the following:
\begin{enumerate}
    \item \textbf{SHOULD: 3 cases}. E.g: "To explicitly assert that no such relationships exist, the to property SHOULD contain the NoneElement individual and no other elements."
    \item \textbf{MUST: 2 cases}. E.g: "relationshipType $|$ RelationshipType $|$ 1 $|$ 1 (relationship MUST have a relationshipType)."
    \item \textbf{Class based requirements: 8 cases}.
    \item \textbf{Dependent MUST: 3 cases}. E.g: "The Licensing profile only contains the additional requirement that any Software Artifact MUST have a Relationship of type hasConcludedLicense."
    \item \textbf{Redundancy: 1 case}.\\
\end{enumerate}

\textbf{Test cases}

5 test cases were constructed using a python script, based on the MUST requirements. The 6th test case was added to replicate the testing done in \cite{cmuplugfest}. The 7th test case was added to identify the breadth of use of the relationship class in SPDX. These were the following final test cases:
\begin{enumerate}
    \item A relationship MUST not contain any additional elements to NoneElement in the ‘to’ property
    \item Relationship MUST have a relationshipType
    \item IF Licensing Profile THEN Software Artifact MUST have a type “hasConcludedLicense”
    \item IF Build Profile THEN Build element MUST have relationship of types: “hasInput”, “hasOutput”, and “invokedBy“
    \item IF Lite Profile THEN Software Package MUST have relationship of types “hasConcludedLicense” and “hasDeclaredLicense”
    \item Maximum depth of the dependency graph (based on relationshipType: dependsOn).
    \item Number of different types of relationshipTypes present.
\end{enumerate}

The test cases were then used on a dataset of 4 SBOMs. 3 were extracted from a GitHub repository officially recognised by the Linux foundation. The 4th one was generated using microsoft/sbom-tool. The results of the test cases are present in Table 2.

\textbf{Limitations\\}
Given how none of the SBOMs in the dataset were using the Licensing, Build, and Lite profile, it resulted in none of the dependent tests being applicable. Moreover, in test 6 for generated 1, the relationshipClass was actually 'DEPENDS\_ON' instead of 'dependsOn' in the specifications which led to the test case failing at first, before this being rectified after manual analysis. The relationshipTypes for generated 1 were all listed differently than in the specifications.

\begin{table}[h!]
\centering
\begin{tabular}{lccccc|cc}
\toprule
\textbf{SBOM} & \textbf{T1} & \textbf{T2} & \textbf{T3} & \textbf{T4} & \textbf{T5} & \textbf{T6} & \textbf{T7} \\
\midrule
Example 1 & $\checkmark$ & $\checkmark$ & $\circ$ & $\circ$ & $\circ$ & $\circ$ & 1 \\
Example 2 & $\checkmark$ & $\checkmark$ & $\circ$ & $\circ$ & $\circ$ & 2 & 6 \\
Example 3 & $\checkmark$ & $\checkmark$ & $\circ$ & $\circ$ & $\circ$ & $\circ$ & 8 \\
Generated 1 & $\checkmark$ & $\checkmark$ & $\circ$ & $\circ$ & $\circ$ & 3 & 4 \\
\bottomrule
\end{tabular}
\caption{Results of test cases from 4.4.1}
\end{table}

\subsubsection{Results - CycloneDX 1.6\\}
\label{subsec:dep_res_cdx}

\textbf{Analysis of requirements\\}
In CycloneDX, dependency relationships are explicitly modeled within the root-level \texttt{dependencies} array. The specification states, "Each item of this array must be a Dependency object." Our extraction yielded 24 normative requirements related to the \texttt{dependencies} object and its properties.

The core of the dependency graph is the \texttt{dependency} object, which has one REQUIRED property, \texttt{ref}, and one key optional property, \texttt{dependsOn}. A critical rule from the specification (Section 11.1) states:
\begin{quote}
    "Components or services that do not have their own dependencies MUST be declared as empty elements within the graph."
\end{quote}
This implies that every component listed in the main \texttt{components} array should have a corresponding entry in the \texttt{dependencies} graph, even if its \texttt{dependsOn} array is empty. Furthermore, the specification includes a key recommendation (Section 5.2):
\begin{quote}
    "SBOMs SHOULD ideally contain all direct and transitive components and the dependency relationships between them."
\end{quote}
These rules, particularly the ambiguity between the strict \texttt{MUST} for leaf node declaration and the softer \texttt{SHOULD} for transitive completeness, form the basis for our test cases, which are designed to detect common failures in graph integrity.

\textbf{Test cases}
Based on the normative requirements and the failures observed in prior empirical work \cite{sei-harmonization-report, jbomaudit}, we designed three pilot test cases to probe the structural and semantic integrity of dependency graphs in CycloneDX SBOMs.
\begin{description}
    \item[Test Case 1: The "Dangling Component."] This test verifies the \texttt{MUST} requirement from Section 11.1. It checks for any component listed in the main \texttt{components} array that does not have a corresponding entry in the \texttt{dependencies} array. Such a component is "dangling" because its dependency status is not explicitly declared, making the graph incomplete and violating a mandatory rule.
    
    \item[Test Case 2: The "Implicitly Missing Transitive Dependency."] This test targets the \texttt{SHOULD ideally} clause. The test SBOM correctly lists a direct dependency (e.g., \texttt{requests}) but omits a known transitive dependency (e.g., \texttt{urllib3}) while incorrectly declaring the direct dependency as a leaf node (\texttt{"dependsOn": []}). This scenario represents a critical vulnerability blind spot and is the exact problem identified in related work as a primary cause of "dependency depth variance."
    
    \item[Test Case 3: The "Detached Dependency Graph."] This test verifies the implicit structural rule that the dependency graph must connect to the primary component described by the SBOM (often defined in \texttt{metadata.component}). The test SBOM defines a main component in the metadata, but its \texttt{dependencies} graph is internally consistent but has no link back to this main component, making it a "detached" and contextually meaningless graph.
\end{description}
These test cases form the foundation of our proposed automated conformance framework. They move beyond simple schema validation to test for the deeper structural and semantic integrity required for reliable security analysis.

\subsection{Empirical verification of the issues present}

\subsubsection{Design of test cases\\\\}

\textbf{SPDX 3.0.1}:

\paragraph{(1) Failure to meet the minimum elements specified by the CISA guidelines}: SPDX v3.0.1 directly addresses compliance failures through the introduction of the Lite Profile. Recognizing that the complexity of the full standard often leads to incomplete SBOMs, the Lite Profile captures the absolute minimum set of information required for license compliance, meeting the CISA minimum elements in the way: \texttt{copyrightText}, \texttt{creationInfo}, \texttt{name}, \texttt{packageVersion}, \texttt{spdxId}, and \texttt{suppliedBy}.

By explicitly mapping these mandatory fields to the minimum elements defined by CISA, the standard removes the ambiguity that previously allowed tools to generate "compliant" but empty SBOMs. Thus, as long as an SBOM is conformant to the Lite Profile it follows the CISA guidelines.

However, given that conformance to the Lite Profile is not mandatory and only the Core Profile is, it still remains the case that an SBOM can be created in the SPDX 3.0.1 format which is fully conformant to the standard but does not meet the CISA guidelines.

\paragraph{(2) Transitive dependencies are missed:}
While static analysis tools often miss transitive dependencies in dynamic languages (e.g., Python, JavaScript), SPDX v3.0.1 addresses this via the \textbf{Build Profile} (Section 14). Unlike previous versions that relied heavily on static file manifest parsing, the Build Profile models the actual build instance. This data model encourages tools to record dependencies observed during the build process rather than estimating them from static manifest files, significantly reducing missed transitive components.

Furthermore, explicit Relationship Types such as \texttt{hasPrerequisite}, \texttt{hasDynamicLink}, and \texttt{hasStaticLink}, allow tools to distinguish between direct source dependencies and transitive runtime dependencies.

However, this requires tooling which can capture this relationship. Since most SBOM tools only support estimating dependencies from static manifest files, most SBOM generation tools will still miss transitive dependencies \cite{sbomlandscape}.

\paragraph{(3) Tools employ different methodologies for parsing metadata:}

Although the standard provides ways of making sure that any components extracted can be represented and verified in a universal manner by using the Package URL (purl) or Hash algorithms, they do not contain any information on best ways to parse metadata. This provides a hole for SBOM generation tools to fill, which leads to inconsistencies since they can choose a variety of going about it.\\
Although SPDX 3.0.1 allows metadata to be mapped to a universal graph using the Resource Description Framework (RDF), it contains no fields where it can be noted what metadata should be preferred or used in component extraction. Considering how depending on whether an SBOM is created from a 'requirements.txt' file, a python environment, or a docker container, it can have a different output, this will lead to different SBOMs given that each SBOM generation tool will choose their own preferential option.

Additionally, given that there exists no property in SPDX which lists down which metadata option was chosen when creating the SBOM, it divorces the SBOM from the method of its creation, and creates an information gap between the SBOM generation tool itself and the created SBOM.

\paragraph{(4) Interoperability issues where one tool produces a better SBOM for one format over another:}
Interoperability issues, particularly between SPDX and CycloneDX, are explicitly addressed in the Extension Profile. The specification acknowledges that tools often specialize in one format, leading to data loss during conversion.

The \texttt{CdxPropertiesExtension} class is a standardized extension point which is intended to be compatible with CycloneDX properties, allowing an SPDX document to carry data generated by tools designed for the competing standard without loss. Additionally, the modular nature of the profiles allows tools to support specific subsets of the standard reliably, rather than failing to support the entire monolithic specification.

\paragraph{(5) Lack of reproducibility in the builds on which SBOMs are created:} The SPDX 3.0.1 specification directly addresses build reproducibility through two mechanisms. First, the \texttt{CreationInfo} class notes that the \texttt{created} timestamp should reflect the date of last change (e.g., a git commit date) rather than the date the SPDX data was generated, explicitly stating this supports reproducible builds.'' Second, the \texttt{Build} profile introduces a dedicated \texttt{Build} class that encapsulates all metadata related to a build process---its inputs, outputs, builders, and related identities---providing a structured, traceable record of the build from which the SBOM was generated. Crucially, \texttt{buildStartTime} and \texttt{buildEndTime} are described as optional and may be omitted to simplify creating reproducible builds,'' since timestamping the build process itself can introduce non-determinism.

\paragraph{(6) View of SBOMs as unnecessary and merely a compliance checkbox:}
The specification counters this perception architecturally through the \texttt{Lite Profile}, which is described as capturing the minimum information required for license compliance in the software supply chain, and through the modular profile system more broadly. By defining nine distinct compliance points, Core, Software, Security, Licensing, Dataset, AI, Build, Lite, and Extension, the specification frames SBOMs not as monolithic compliance documents but as targeted, functional artifacts serving real operational purposes. The \texttt{Security Profile}, for instance, enables interchange of vulnerability data between tools, making an SBOM an active security instrument rather than a passive document. The \texttt{Build Profile} similarly ties the SBOM to a verifiable build process, reinforcing its role as an auditable engineering artifact.

\paragraph{(7) Inconsistencies in the naming of packages:} The specification addresses package naming inconsistencies through two complementary mechanisms. The \texttt{packageUrl} property (part of the Software Profile) adopts the Package URL (\texttt{purl}) standard, described as an attempt to standardize package representations in order to reliably identify and locate software packages'' in a mostly universal and uniform way across programming languages, package managers, packaging conventions, tools, APIs and databases.'' The \texttt{purl} follows a structured schema that normalises identification across ecosystems. Complementarily, the \texttt{ExternalIdentifier} class supports referencing packages via established external naming schemes including \texttt{cpe22}, \texttt{cpe23}, \texttt{packageUrl}, \texttt{swid}, and \texttt{swhid}, providing a mapping from SPDX elements to authoritative, domain-specific identifiers and thereby reducing ambiguity from cross-ecosystem naming divergence.

\paragraph{(8) Inability to capture whether a library was actually loaded into memory or not due to the static nature of an SBOM:} The specification addresses this limitation through two related features. First, the \texttt{SBOMType} enumeration includes a \texttt{runtime} type, defined as an SBOM generated through instrumenting the system running the software, to capture only components present in the system, as well as external call-outs or dynamically loaded components''---also referred to as an Instrumented or Dynamic SBOM. This allows producers to explicitly distinguish a runtime-observed SBOM from a static analysis SBOM. Second, the \texttt{RelationshipType} enumeration provides \texttt{hasDynamicLink} (the from Element dynamically links in each to Element'') and \texttt{hasStaticLink} as distinct relationship types, scoped further by the \texttt{LifecycleScopeType}, which includes a \texttt{runtime} value defined as covering the execution phase of an element.'' Together, these allow an SBOM to express not merely what libraries are present in a package, but which were dynamically linked and active during execution, partially bridging the static/dynamic observability gap.

\textbf{CycloneDX}

\paragraph{(1) Failure to meet CISA Minimum Elements:}
Our intra-specification analysis reveals a direct conflict between the CISA guidelines and the CycloneDX normative requirements regarding the "Supplier" field. 

The CISA Minimum Elements explicitly list "Supplier Name" as \textbf{REQUIRED}. However, our extraction of the CycloneDX 1.6 specification confirms that the \texttt{supplier} property is defined as \textbf{OPTIONAL} (Normative Keyword: MAY) in lines 198, 242, and 264 of the specification data. Furthermore, the official JSON schema does not enforce the presence of metadata.supplier. 

This creates a systemic root cause for non-compliance. Our empirical analysis (Section 4.6) confirms this, showing that \textbf{96.1\%} of real-world SBOMs omit the supplier field because the schema permits it.

% \paragraph{(2) Transitive dependencies are missed:}
% CycloneDX utilizes a nested \texttt{components} array or a flattened \texttt{dependencies} graph. However, the specification relies heavily on the \texttt{metadata.tools} and \texttt{formulation} objects to describe the build environment. Our thematic analysis shows that while \textbf{Formulation} accounts for 9\% of the spec, it is almost entirely optional (\textbf{MAY}). Tools perform shallow scans (e.g., parsing \texttt{package.json}) because the specification does not mandate the complex formulation analysis required to capture transitive build-time dependencies.

\paragraph{(2) Lack of standardized metadata:}
CycloneDX addresses metadata via the \texttt{properties} object (a key-value store). Our thematic coding of the "Extensibility" theme reveals that while the standard "RECOMMENDS" registering properties in a taxonomy, it effectively allows ad-hoc strings. This results in the same fragmentation seen in the Python ecosystem \cite{pythonsboms}, where tools create arbitrary property names (e.g., \texttt{cdx:property:build\_host} vs \texttt{ex:build\_server}) that cannot be parsed universally. Our measurement study found that \textbf{21.7\%} of properties in the wild use ad-hoc, unregistered namespaces, confirming this fragmentation.

\paragraph{(3) Interoperability issues:}
The high degree of flexibility in CycloneDX (53\% \textbf{MAY}) creates interoperability friction. For example, the \texttt{licenseChoice} element allows an author to provide either an SPDX ID, a proprietary license name, or a license expression. A consumer tool expecting an SPDX ID (to automate policy checks) will fail when encountering a valid CycloneDX file that uses proprietary names. The specification prioritizes expressiveness over strict interoperability, requiring consumption tools to implement complex normalization logic \cite{bomsaway}. However, our empirical data suggests the ecosystem is self-correcting: \textbf{88.3\%} of analyzed SBOMs voluntarily use standard SPDX identifiers despite the specification allowing proprietary names.

\begin{table}[h]
\centering
\normalsize
\resizebox{0.5\textwidth}{!}{%
\begin{tabular}{|l|p{3.2cm}|p{3.2cm}|p{3.2cm}|}
\hline
 & \textbf{SPDX Guardrail} & \textbf{CycloneDX Guardrail} & \textbf{Test for issue} \\ \hline
1 & Lite profile presence 
  & Presence of \texttt{metadata.supplier}, \texttt{timestamp}, and \texttt{authors} 
  & Percentage of minimum elements included \\ \hline

2 & NULL 
  & NULL
  & Depth of dependency graph \\ \hline

3 & NULL 
  & NULL
  & Divergence between statically and dynamically created SBOM \\ \hline

4 & CycloneDX extension property presence 
  & Taxonomy usage (e.g., \texttt{cdx:} prefix) 
  & Degree of lossyness of conversion \\ \hline

5 & Build profile presence 
  & Presence of \texttt{formulation} or \texttt{annotations} 
  & NULL \\ \hline

6 & profileConformance presence 
  & Presence of \texttt{formulation.workflow} 
  & Percentage of noAssertion fields out of total fields \\ \hline

7 & PURL format correctly followed 
  & Presence of \texttt{compositions} 
  & Divergence between packages representing the same dependency but using different tools \\ \hline

8 & relationshipType presence 
  & Valid Package URL (purl) syntax 
  & Profileration of static injection of library not used in code \\ \hline
\end{tabular}
}
\caption{SPDX and CycloneDX mitigation checks and corresponding problem tests}
\label{tab:combined_sbom_checks}
\end{table}
% \begin{table}[h]
% \centering
% \begin{tabular}{|l|p{3.5cm}|p{3.5cm}|}
% \hline
%  & \textbf{Check for guardrails} & \textbf{Test for issue} \\ \hline
% 1 & Lite profile presence & Percentage of minimum elements included \\ \hline
% 2 & Set of 'relationshipType' present & Depth of relationship graph \\ \hline
% 3 & NULL & Divergence between statically and dynamically created SBOM \\ \hline
% 4 & CycloneDX extension property presence & Degree of lossyness of conversion \\ \hline
% 5 & Build profile presence & Measuring reproducibility of build \\ \hline
% 6 & profileConformance presence & Percentage of noAssertion fields out of total fields \\ \hline
% 7 & PURL format correctly followed & Divergence between packages representing the same dependency but using different tools \\ \hline
% 8 & relationshipType presence & Profileration of static injection of library not used in code \\ \hline
% \end{tabular}
% \caption{SPDX mitigation checks and corresponding problem tests}
% \end{table}

% \begin{table}[h]
% \centering
% \resizebox{\columnwidth}{!}{%
% \begin{tabular}{|l|p{3.8cm}|p{3.8cm}|}
% \hline
%  & \textbf{Check for guardrails} & \textbf{Test for issue} \\ \hline
% 1 & Presence of \texttt{metadata.supplier}, \texttt{timestamp}, and \texttt{authors} & Percentage of CISA required elements (7 fields) present \\ \hline
% 2 & Dependency graph depth $>1$ & Coverage of components appearing in the dependency graph \\ \hline
% 3 & N/A (No spec solution) & Standardization score (PURL + Hash presence) \\ \hline
% 4 & Taxonomy usage (e.g., \texttt{cdx:} prefix) & Fragmentation score (ad-hoc vs registered property names) \\ \hline
% 5 & Presence of \texttt{formulation} or \texttt{annotations} & Usage rate of advanced CycloneDX features \\ \hline
% 6 & Presence of \texttt{formulation.workflow} & Reproducibility score (hashes + environment data) \\ \hline
% 7 & Presence of \texttt{compositions} & Rate of missing completeness assertions \\ \hline
% 8 & Valid Package URL (purl) syntax & PURL coverage rate per SBOM \\ \hline
% \end{tabular}
% }
% \caption{CycloneDX Mitigation checks and corresponding problem measurements}
% \label{tab:cdx_test_cases}
% \end{table}

\newpage

\subsubsection{Use of test cases\\}

\textbf{\\SPDX\\}

The results of the test cases are present in table \ref{tab:spdx_test_results}.

\textbf{\\CycloneDX\\}

To validate the practical impact of the structural issues identified in Section 4.3.2, we developed a corresponding test suite for CycloneDX. We utilized the GitHub Code Search API to collect a dataset of 128 valid CycloneDX 1.6 SBOMs from public repositories.

We applied the test cases defined in Table \ref{tab:combined_sbom_checks} to our dataset of 128 CycloneDX 1.6 SBOMs. The analysis reveals a significant gap between specification capabilities and real-world adoption.

\paragraph{CISA Compliance Gap (TC1):}
Our measurement confirms the structural weakness identified in Section 4.3.2. Only \textbf{2.3\%} (3/128) of the analyzed SBOMs met the full CISA minimum requirements. The \texttt{supplier} field, which is optional in the CycloneDX schema, was missing in 96.1\% of the samples. This validates that optionality in the standard leads directly to non-compliance in practice.

\paragraph{Transitive Dependency Blindness (TC2):}
Despite the graph-based capabilities of CycloneDX, \textbf{57\%} of SBOMs either lacked a dependency graph entirely or only captured direct dependencies (Depth $\le 1$). This creates a "shallow visibility" problem where vulnerabilities in transitive dependencies (e.g., Log4j) remain undetectable.

\paragraph{The Reproducibility Void (TC6):}
While CycloneDX 1.6 introduced the \texttt{formulation} object to address build integrity \cite{reproduciblebuildsforne}, we found \textbf{0\%} adoption of this feature in the wild. This suggests that complex, optional security features in specifications are ignored by tool developers in favor of basic inventory generation.

\paragraph{Checkbox Compliance (TC7):}
We measured the usage of \texttt{compositions} to assert completeness. \textbf{98.4\%} of SBOMs made no assertion regarding their completeness (neither "complete" nor "incomplete"). This creates an ambiguity where consumers cannot distinguish between a thorough SBOM and a partial one, validating concerns regarding "checkbox compliance" \cite{maintainersvulnmgmtwermke}.

\paragraph{Standardization Success (TC8):}
Conversely, we found high adherence to Package URL (PURL) standards. \textbf{63.3\%} of SBOMs achieved high PURL coverage ($>80\%$), and cross-tool consistency was high ($>92\%$). This indicates that extensive specification guidance (as seen with PURL in the appendices) effectively drives standardization, whereas loose optional fields (like \texttt{properties}) lead to fragmentation.

\begin{table*}[ht]
\centering
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}|l|c c c c | c c c c|}
\hline
& \textbf{Guardrails} & & & & \textbf{Issues} & & & \\
\hline
& \textbf{microsoft tool} & \textbf{spdx-generator} & \textbf{syft} & \textbf{trivy} & \textbf{microsoft tool} & \textbf{spdx-generator} & \textbf{syft} & \textbf{trivy} \\
\hline
\textbf{Minimum elements} & 0\% & - & - & - & 91.7\% & 58.3\% & 41.7\% & 66.7\% \\
\textbf{Transitive dependencies} & 4 & 6 & 6 & 6 & 3 & 3 & 2 & 2 \\
\textbf{Metadata parsing} & - & - & - & - & 62\% & 39\% & 28\% & 27\% \\
\textbf{Interoperability} & 0\% & - & - & - & 19\% & 22\% & 27\% & 26\% \\
\textbf{Reproducibility} & 0\% & - & - & - & ? & ? & ? & ? \\
\textbf{Superficial compliance} & 100\% & - & - & - & 18\% & 28\% & 8\% & 5\% \\
\textbf{Package naming} & 12\% & 10\% & 16\% & 25\% & 0\% & 0\% & 0\% & 0\% \\
\textbf{Dynamic dependencies} & 100\% & 100\% & 100\% & 100\% & 100\% & 100\% & 100\% & 100\% \\
\hline
\end{tabular*}
\caption{Results of SPDX test cases}
\label{tab:spdx_test_results}
\end{table*}"

i dont think i shuld mention balliu et al in the text i send him, it was probably sent to me just for me to draw inspiratiino from that paper maybe? also im not putting the cyclonex ectrction table into the paper so would it make sense for me to put those numbers and names directly into the writeup? maybe a figure or a table might help more in this regard which includes selected numbers/entries? idk

you have cyclonedx table of mine already for reference in previous prompts

Show more
22 Apr, 15:49


I would still replace 4.2.3. What you have now is decent, but this version is tighter, more result driven, and more clearly tied to spec evidence.

You do not need to put raw extraction row numbers into the paper if that extraction table is not included. Referencing the relevant CycloneDX sections in the prose is enough. Also, I would keep the Balliu citation in the paper, but you do not need to mention it explicitly in the email to your advisor.

Use this as the full replacement for 4.2.3:

\subsubsection{CycloneDX Security Relevant Guardrails}
\label{subsec:cdx_security_results}

Our re-examination of the extracted CycloneDX 1.6 requirements yields three concrete results. First, CycloneDX is usually strict about the internal structure of objects once they are present. Second, many security relevant objects remain optional at the baseline level. Third, several important distinctions, such as dependency completeness, build context, and runtime relevance, are representable in the model but weakly constrained at the point where producers must populate them. This means that CycloneDX is rich as a representation format, but uneven as a baseline control document for SBOM generation.

\paragraph{Minimum elements are weakly enforced.}
CycloneDX includes the fields needed to express core provenance information, but it does not require them at the metadata level. In Section 7, the root \texttt{metadata} object is optional, and within that object the key provenance fields remain optional as well: \texttt{timestamp} in Section 7.1, \texttt{authors} in Section 7.5, and \texttt{supplier} in Section 7.8. This directly weakens protection against the first failure mode in Section~\ref{subsec:systematization}, namely failure to meet the CISA minimum elements. A CycloneDX document may therefore be structurally valid while omitting the very fields needed to establish provenance and accountability. This weakness is reinforced by our schema comparison in Section 4.3.1, which shows that the official JSON schema also leaves these fields non mandatory.

\paragraph{Dependency completeness is only conditionally governed.}
CycloneDX provides an explicit dependency graph model through the root \texttt{dependencies} object in Section 11. When that object is present, the specification becomes locally strict: each item must be a Dependency object, each dependency must contain a \texttt{ref}, and components or services with no dependencies must still be declared as empty elements within the graph. However, the graph itself is optional, and the broader completeness goal is expressed only as guidance in Sections 5.2 and 5.3.1, where SBOMs are said to ideally contain all direct and transitive components and their relationships. The result is that CycloneDX constrains dependency graphs if producers choose to provide them, but does not require a producer to expose a complete graph in the first place. This leaves only partial protection against transitive dependency omission.

\paragraph{Production semantics remain underspecified.}
A recurring limitation in CycloneDX is that the specification defines how information should be represented more clearly than it defines how that information should be obtained. This is particularly visible for build context and runtime relevance. Prior empirical work on Java SBOM generation shows that CycloneDX producers operate at different points in the software lifecycle, including source, build, and post packaging stages, and that these choices materially affect which dependencies are observed \cite{balliu2023sbomjava}. CycloneDX can represent lifecycle related information through metadata and formulation objects, but it does not impose a baseline requirement that producers clearly declare the production step used to derive the SBOM. As a result, two valid CycloneDX SBOMs may reflect different dependency universes without that distinction being obvious to consumers.

\paragraph{Scope and runtime relevance are representable but not operationally stable.}
The same problem appears in the treatment of component scope. In Section 8.1.13, CycloneDX defines \texttt{scope} as optional and states that if it is omitted, \texttt{required} should be assumed by the consumer. This creates a representational hook for distinguishing runtime relevance, but it does not clearly specify how producers should compute the field. Prior work reports that, for the same dependency, some CycloneDX producers emit \texttt{optional}, some emit \texttt{required}, and others omit the field entirely \cite{balliu2023sbomjava}. Because the population rule is underspecified, these outputs cannot be reliably adjudicated against the standard. CycloneDX therefore supports the expression of runtime relevance, but not a stable method for populating it across tools.

\paragraph{Advanced security support exists, but it is dormant by default.}
CycloneDX 1.6 includes several security relevant structures beyond basic component inventory. These include \texttt{compositions} in Section 12 for completeness assertions, \texttt{vulnerabilities} in Section 13 for vulnerability context, \texttt{analysis} in Section 13.1.22 for VEX style impact statements, and \texttt{formulation} in Section 15 for build provenance and reproducibility. Their presence shows that CycloneDX is not limited to inventory alone. However, these root objects are optional, which means the strongest security oriented parts of the specification remain dormant unless producers voluntarily opt into them. The consequence is that the standard contains the vocabulary needed to address issues such as checkbox compliance, reproducibility, and vulnerability context, but it does not make those protections part of the baseline SBOM.

\paragraph{VEX support is expressive, but not baseline.}
CycloneDX does provide a path for communicating whether a listed vulnerability actually affects a component. Section 13.1.22 defines an optional \texttt{analysis} object with optional fields such as \texttt{state}, \texttt{justification}, \texttt{response}, and \texttt{detail}. The standard recommends that justification be provided for \texttt{not\_affected} cases and that responses be provided for exploitable cases. This is valuable for downstream triage, but these remain recommendations attached to an already optional vulnerability object. Thus, CycloneDX can support VEX style reasoning, yet it does not require the baseline presence of the vulnerability context needed to make such reasoning consistently available.

\paragraph{Normalization is stronger than semantic consistency.}
CycloneDX is stronger when it comes to identifier normalization. In Section 8.1 it supports identifiers such as \texttt{purl}, \texttt{cpe}, \texttt{swhid}, \texttt{omniborId}, and \texttt{swid}, and when present these must conform to external specifications. This is a meaningful guardrail against package naming inconsistency. However, the same discipline does not apply to the \texttt{properties} mechanism in Sections 7.10, 8.1.35, 13.1.24, 15.1.5, and 18. There, taxonomy registration is encouraged but not required. This gives CycloneDX a flexible extension mechanism, but also leaves room for semantic fragmentation across tools. In practice, the specification is stronger at normalizing identifiers than at normalizing producer defined metadata.

Taken together, these results show that CycloneDX is best understood as a strong representation standard with weak baseline guarantees for security sufficient SBOM generation. Its main limitation is not lack of expressive power. Rather, the limitation is that many of its most security relevant controls are optional, conditional, or underspecified at the point where producers must populate them. This helps explain why tool inconsistency can persist even when tools emit schema valid and nominally conformant CycloneDX output.

\begin{table*}[t]
\caption{CycloneDX guardrails against known SBOM failure modes}
\label{tab:cdx_security_guardrails}
\centering
\small
\begin{tabular}{p{3.4cm} p{5.1cm} p{2.2cm} p{3.0cm}}
\toprule
\textbf{Failure mode} & \textbf{Relevant CycloneDX mechanism} & \textbf{Strength} & \textbf{Verifiability} \\
\midrule
Failure to meet minimum elements &
\texttt{metadata.supplier}, \texttt{metadata.authors}, and \texttt{metadata.timestamp} exist, but all are optional &
Weak &
Artifact verifiable when present \\
\addlinespace[2pt]

Transitive dependency omission &
\texttt{dependencies} supports graph representation, but the object is optional and transitive completeness is only recommended &
Weak to Moderate &
Partly artifact verifiable \\
\addlinespace[2pt]

Metadata parsing divergence &
The standard provides little guidance on how metadata should be extracted from source, environment, build, or post packaging context &
None to Very Weak &
Not artifact verifiable \\
\addlinespace[2pt]

Interoperability loss &
Typed identifiers and references are strongly constrained when present, but \texttt{properties} remain loosely governed &
Mixed &
Partly artifact verifiable \\
\addlinespace[2pt]

Reproducibility gap &
\texttt{formulation} can represent build provenance and workflow detail, but it is optional &
Dormant &
Artifact verifiable when present \\
\addlinespace[2pt]

Checkbox compliance &
\texttt{compositions} can express completeness claims, but it is optional &
Weak &
Artifact verifiable when present \\
\addlinespace[2pt]

Package naming inconsistency &
\texttt{purl}, \texttt{cpe}, \texttt{swhid}, \texttt{omniborId}, and \texttt{swid} support normalized identity &
Moderate &
Artifact verifiable \\
\addlinespace[2pt]

Runtime blind spot &
\texttt{scope}, lifecycle information, and related objects can express runtime relevance, but the baseline population rules are underspecified &
Weak &
Requires external context \\
\bottomrule
\end{tabular}
\end{table*}
My recommendation
Replace the current 4.2.3 with this version. It is stronger than what you have now.

On whether to add another figure or table
For now, no extra figure is necessary. Your guardrail table is already doing useful work. If you add one more display later, make it a very small evidence table, not a figure. Something like:

spec section
field or object
normative keyword
implication
But you do not need that before sending this revision.

What to tell your advisor after updating Overleaf
Send this:

I updated Section 4.2.3 in Overleaf. The revised version is now written more explicitly as a results subsection, ties the claims more directly to CycloneDX sections, and adds concrete treatment of production semantics, scope, and VEX related optionality. If you have a moment, could you please revisit the updated writeup and let me know if this is closer to the direction you had in mind?

If you want, I can also give you a very short 2 sentence version of that message.





22 Apr, 15:50





Default permissions

5.4
High



Work locally

master


Branch details

Changes

Git actions
Pull request status unavailable"

you may also study the foler structure and all files in the current folder (SSC) if u want. but the work we're going to do, i dont think itll be too related to existing files/folder, but.. anyway. let me know once youve done understanding the chat ive given you as well as the folder you're working in rn

this is my chat with my professors:"I will miss too (CCS deadline).
 
Sorry for the inconvenience.
 
Abdullah Sohail
Dear Profs, reminder for your feedback on the writeup whenever it's convenient for you all, so that we can restructure the writeup + methodology for thematic analysis accordingly, and then get started with inspecting SBOM generator tools as Dr. Mohannad Alhanahnah advised. thank you!
from my side, my understanding is that what have been modified part is about section 4.2.3 and nothing else. Yes, the write up is a bit clear, however, 
1- pls don't wait for us for minor changes in the paper and how this modified section is relevant to the methodology and thematic analysis.
2- as mentioned earlier this section fits in the best case under discussion and has nothing to do with results. 
3- this section feels ad hoc, for example what re-examination means? where does it fit in the overall approach? and what's the methodology for the re-examination?
4- I don't have experience with thematic analysis, unfortunately I can't comment on this. 
 
Honestly, I'm now skeptical whether this project can achieve its goal, 
I recall in the last meeting Ashish Gehani mentioned that the meeting was fruitful and  Abdullah Sohail and Mohammad Huzaifa have a good plan based on the TSE paper that i shared, and they will post the plan soon. Nobody posted the plan and Abdullah Sohail is asking for a feedback based on very minor modification. Please let me know if I'm misunderstanding anything. 
 
I'd suggest Abdullah Sohail and Mohammad Huzaifa really think carefully what you want to achieve here. You have 2 great mentors Ashish Gehani and Sazzadur Rahaman, I also tried to help. We identified several potential problems and hypothesis approaches to address them. But the execution needs improvement, and this project can't be carried out as a very secondary project, we had many delays and skips. 
 
Please Abdullah Sohail and Mohammad Huzaifa remember, you ARE leading this work. As mentioned in my meeting with you, if you ask vague questions, then you'll get vague answers. It's mentioned several times, dig deep, don't be shallow. Before sharing something with us, do cross checking, ask yourselves, is this useful? does it bring any value? 
 
I also have 2 deadlines neurips and ccs. So I'll be available for a short time for our meeting. So pls come up with a real questions. 
 
 
 
have u tried this sbom tool https://github.com/trailofbits/it-depends, if i recall correctly, I shared this a long time ago
GitHub - trailofbits/it-depends: A tool to automatically build a dependency graph and Software Bill of Materials (SBOM) for packages and arbitrary source code repositories.
A tool to automatically build a dependency graph and Software Bill of Materials (SBOM) for packages and arbitrary source code repositories. - trailofbits/it-depends
 
Are we going to have a call today?
 
I'm away (PTI) but Mohammad Huzaifa and Abdullah Sohail should join.
 
As advised, we’re working on deeper analysis of the 4 sbom generation tools mentioned in the writeup, and are extending it to include the trailofbits tool that you sent. As of now, we may not have any questions to ask. Good luck with your submissions!
 
Additionally, when it comes to the analysis of SBOM quality assurance tools, this is present in the background of the writeup, where we have talked about all of the relevant quality assurance tools (schemas, sbomqs, jbomaudit). While the schemas have already been comprehensively analysed, we will extend the analysis of sbomqs and jbomaudit further in order to ensure that we go into the sufficient depth that you mentioned
 
Feel free to post your thoughts/questions. I do my best to answer questions promptly
 
Hello, I’ll need to skip today’s meeting being occupied with a paper submission. Also, I believe huzaifa won’t be able to take the meeting as well since he was admitted to the hospital. please keep him in prayers
 
Thanks for letting us know. So sorry to hear that  Mohammad Huzaifa is unwell. I wish his speedy recovery.
 
Sorry to hear that. Wishing Huzaifa a speedy recovery.
 
Mohammad Huzaifa I hope everything is going well and that you’re recovering quickly.
 
Abdullah Sohail: Please can you let us know how Huzaifa is doing?
 
Thankfully, I’ve managed to make a recovery and have been released from the hospital. I’m doing much better now, thank you very much for the kind words and well wishes!
 
Mohammad Huzaifa 
Thankfully, I’ve managed to make a recovery and have been released from the hospital. I’m doing much better now, thank you very much for the kind words and well wishes!

Glad to hear that! Take care.
 "

this was our task to be done:"As advised, we’re working on deeper analysis of the 4 sbom generation tools mentioned in the writeup, and are extending it to include the trailofbits tool that you sent. As of now, we may not have any questions to ask. Good luck with your submissions!
 
Additionally, when it comes to the analysis of SBOM quality assurance tools, this is present in the background of the writeup, where we have talked about all of the relevant quality assurance tools (schemas, sbomqs, jbomaudit). While the schemas have already been comprehensively analysed, we will extend the analysis of sbomqs and jbomaudit further in order to ensure that we go into the sufficient depth that you mentioned
 "

Show less
12 May, 17:20

Worked for 2m 22s
I’ve gone through both the professor chat and the SSC workspace, and I have the project state clear now.

What I understand from the chat:

Your advisors are not mainly asking for prettier writing. They want a deeper, method anchored contribution.
The core criticism is that 4.2.3 still reads like discussion unless each claim is tied to explicit spec evidence, a clear analytical method, and concrete examples.
They also want two follow ups beyond the writing:
inspect how actual SBOM generators populate fields
position your work against SBOM quality tools such as sbomqs, and possibly jbomaudit
Dr. Mohannad is especially pushing on execution quality, sharper questions, and a more concrete implementation facing analysis.
What is in this repo:

This repo is mostly the analysis and experiment workspace, not the paper source itself. I did not find any .tex or .bib files here.
The main CycloneDX experiment pieces are:
create_sboms.py
run_tests.py
3_test_sboms.py
1_collect_sboms.py
2_analyze_sboms.py
The repo already has generator level experimentation for syft, trivy, and cdxgen, with a commented out Microsoft path in create_sboms.py.
There is already a test case framework for the measurement study under cyclonedx/measurement/test_cases.
I did not find current repo level work on sbomqs, jbomaudit, or it-depends yet.
Important repo note:

The git tree is already dirty with user changes, especially under cyclonedx/measurement, plus untracked experiment folders. I have not touched any of that.
My read of the best next step:

The strongest next move is not more broad rewriting first.
It is a small implementation facing study of a few generators using the existing harness, focused on how they populate:
dependency graphs
supplier, timestamp, authors
scope
completeness related fields such as compositions
Right after that, add a short sbomqs positioning section explaining what it can check from artifacts and what it cannot check when population semantics are underspecified.
I’m fully oriented now and ready to help with the next concrete step. My recommendation is to do the generator population inspection first, because it directly answers the advisors’ biggest missing point.

12 May, 17:22
let;s look into generators, maybe cdxgen and trivy for now

trivy:https://github.com/aquasecurity/trivy
"Skip to content
aquasecurity
trivy
Repository navigation
Code
Issues
175
 (175)
Pull requests
82
 (82)
Agents
Discussions
Actions
Projects
Security and quality
2
 (2)
Insights
Owner avatar
trivy
Public
aquasecurity/trivy
Go to file
t
T
Name		
DmitriyLewen
DmitriyLewen
feat(seal): add vendor support for language file detection. (#10297)
b08bf6a
 · 
2 hours ago
.github
ci: remove secrets from run block (#10590)
last week
.vex
fix(vex): add CVE-2025-66564 as not_affected into Trivy VEX file (#9924)
5 months ago
brand
style: update band logos (#5968)
2 years ago
ci
chore: update the rpm download Update (#9202)
10 months ago
cmd/trivy
feat: add documentation URL for database lock errors (#9531)
8 months ago
contrib
chore: add client option to install script (#9962)
5 months ago
docs
feat(seal): add vendor support for language file detection. (#10297)
2 hours ago
e2e
test: add end-to-end testing framework with image scan and proxy tests (
10 months ago
examples
feat: replace TinyGo with standard Go for WebAssembly modules (#8496)
last year
helm/trivy
ci(helm): bump Trivy version to 0.70.0 for Trivy Helm Chart 0.22.0 (#…
last month
integration
chore(deps): replace xeipuuv/gojsonschema and invopop/jsonschema with…
3 weeks ago
internal
fix: pull instead of clone when test repo already exists (#10636)
4 days ago
magefiles
chore(deps): replace xeipuuv/gojsonschema and invopop/jsonschema with…
3 weeks ago
misc
chore: update reference links to Go Wiki (#9987)
5 months ago
pkg
feat(seal): add vendor support for language file detection. (#10297)
2 hours ago
rpc
fix(misconf): apply check aliases when filtering results via .trivyig…
3 months ago
schema
chore(deps): replace xeipuuv/gojsonschema and invopop/jsonschema with…
3 weeks ago
.dockerignore
SARIF: Tweak format for GitHub UI (#571)
6 years ago
.gitattributes
feat: Adding support for Windows testing (#3037)
4 years ago
.gitignore
feat(fs): use git commit hash as cache key for clean repositories (#8278
last year
.golangci.yaml
chore: bump golangci-lint to v2.10.0 (#10223)
3 months ago
.release-please-manifest.json
release: v0.70.0 [main] (#10105)
last month
CHANGELOG.md
release: v0.70.0 [main] (#10105)
last month
CONTRIBUTING.md
fix: update all documentation links (#9777)
6 months ago
Dockerfile
chore(deps): bump alpine to 3.23.4 (#10552)
last month
Dockerfile.canary
chore(deps): bump alpine to 3.23.4 (#10552)
last month
LICENSE
Change license to Apache 2.0
6 years ago
NOTICE
Change license to Apache 2.0
6 years ago
README.md
docs: convert README demonstration videos to mp4 (#10419)
3 weeks ago
SECURITY.md
docs: Fix typos and linguistic errors in documentation / hacktoberfest (
6 months ago
buf.gen.yaml
chore: migrate protoc setup from Docker to buf CLI (#9184)
10 months ago
buf.yaml
chore: migrate protoc setup from Docker to buf CLI (#9184)
10 months ago
go.mod
feat(seal): add vendor support for language file detection. (#10297)
2 hours ago
go.sum
feat(seal): add vendor support for language file detection. (#10297)
2 hours ago
goreleaser-canary.yml
refactor: migrate from go-json-experiment to encoding/json/v2 (#9422)
8 months ago
goreleaser.yml
fix: use Development category for GoReleaser discussions (#10530)
last month
mkdocs.yml
docs: migrate private registry documentation from GCR to GAR (#10208)
3 months ago
release-please-config.json
ci: introduce Release Please for automated release management (#6795)
2 years ago
zizmor.yml
ci: add zizmor to scan GitHub Actions workflows (#10322)
2 months ago
Repository files navigation
README
Code of conduct
Contributing
Apache-2.0 license
Security

GitHub Release Test Go Report Card License: Apache-2.0 GitHub Downloads Docker Pulls

📖 Documentation

Trivy (pronunciation) is a comprehensive and versatile security scanner. Trivy has scanners that look for security issues, and targets where it can find those issues.

Targets (what Trivy can scan):

Container Image
Filesystem
Git Repository (remote)
Virtual Machine Image
Kubernetes
Scanners (what Trivy can find there):

OS packages and software dependencies in use (SBOM)
Known vulnerabilities (CVEs)
IaC issues and misconfigurations
Sensitive information and secrets
Software licenses
Trivy supports most popular programming languages, operating systems, and platforms. For a complete list, see the Scanning Coverage page.

To learn more, go to the Trivy homepage for feature highlights, or to the Documentation site for detailed information.

Quick Start
Get Trivy
Trivy is available in most common distribution channels. The full list of installation options is available in the Installation page. Here are a few popular examples:

brew install trivy
docker run aquasec/trivy
Download binary from https://github.com/aquasecurity/trivy/releases/latest/
See Installation for more
Trivy is integrated with many popular platforms and applications. The complete list of integrations is available in the Ecosystem page. Here are a few popular examples:

GitHub Actions
Kubernetes operator
VS Code plugin
See Ecosystem for more
Canary builds
There are canary builds (Docker Hub, GitHub, ECR images and binaries) generated with every push to the main branch.

Please be aware: canary builds might have critical bugs, so they are not recommended for use in production.

General usage
trivy <target> [--scanners <scanner1,scanner2>] <subject>
Examples:

trivy image python:3.4-alpine
Result
trivy fs --scanners vuln,secret,misconfig myproject/
Result
trivy k8s --report summary cluster
Result
FAQ
How to pronounce the name "Trivy"?
tri is pronounced like trigger, vy is pronounced like envy.

Want more? Check out Aqua
If you liked Trivy, you will love Aqua which builds on top of Trivy to provide even more enhanced capabilities for a complete security management offering.
You can find a high level comparison table specific to Trivy users here. In addition check out the https://aquasec.com website for more information about our products and services. If you'd like to contact Aqua or request a demo, please use this form: https://www.aquasec.com/demo

Community
Trivy is an Aqua Security open source project.
Learn about our open source work and portfolio here.
Contact us about any matter by opening a GitHub Discussion here

Please ensure to abide by our Code of Conduct during all interactions.

About
Find vulnerabilities, misconfigurations, secrets, SBOM in containers, Kubernetes, code repositories, clouds and more

trivy.dev
Topics
go docker kubernetes golang security containers iac vulnerability infrastructure-as-code vulnerability-detection hacktoberfest vulnerability-scanners security-tools devsecops misconfiguration
Resources
 Readme
License
 Apache-2.0 license
Code of conduct
 Code of conduct
Contributing
 Contributing
Security policy
 Security policy
 Activity
 Custom properties
Stars
 35k stars
Watchers
 207 watching
Forks
 361 forks
Report repository
Releases 86
v0.70.0
Latest
last month
+ 85 releases
Deployments
500+
 github-pages 2 hours ago
+ more deployments
Packages
1
trivy
Used by 426
@cl-swe-bench
@verity-org
@Las-Ensenanzas-De-Liz
@accuknox
@c6ai
@DataDog
@gurevichdmitry
@altshiftab
+ 418
Contributors
526
@knqyf263
@DmitriyLewen
@dependabot[bot]
@nikpivkin
@simar7
@afdesk
@chen-keinan
@masahiro331
@itaysk
@liamg
@tomoyamachi
@aqua-bot
@rahul2393
@josedonizetti
+ 512 contributors
Languages
Go
98.7%
 
Other
1.3%
Footer
© 2026 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Community
Docs
Contact
Manage cookies
Do not share my personal information"

cdxgen:"logo
CycloneDX Generator (cdxgen)
Universal CycloneDX BOM workflows for developers, AppSec, and compliance teams.

Get Started · CLI Usage · cdx-audit · REPL

Generate and analyze
SBOM
,
CBOM
,
OBOM
,
SaaSBOM
,
CDXA
, and
VDR
documents from
local paths
,
containers
,
archives
,
git URLs
, and
package URLs
— then validate, sign, convert, and audit them in one toolchain.

What cdxgen helps you do
Generate BOMs across polyglot applications, containers, operating systems, and cryptographic inventory
Export CycloneDX JSON or SPDX 3.0.1 JSON-LD and integrate with CI/CD and Dependency-Track
Run as a CLI, library, server, container image, or standalone binary
Choose your path
Developers
Start fast from a local project, git repository, or purl with the CLI
Check ecosystem coverage in Supported Project Types
AppSec teams
Validate structure and compliance with cdx-validate
Analyze generated BOMs with BOM Audit
Prioritize upstream dependency review with cdx-audit
Compliance and platform teams
Convert BOMs to SPDX with cdx-convert
Sign and verify BOMs with cdx-sign and cdx-verify
Review Permissions and Configuring Allowlists for hardened environments
Start here
Getting Started
CLI Usage
Server Usage
Supported Project Types
Learn and go deeper
Advanced Usage
Threat Model
AI/ML Usage
Tutorials - Scanning Git URLs and purls with BOM Audit
Tutorials - Auditing container escape and privilege risks
Support (Enterprise & Community)

Search
cdxgen documentation
Home
CLI Usage
cdx-audit — Predictive supply-chain audit
cdx-convert — CycloneDX to SPDX
cdx-sign — Sign a CycloneDX BOM
cdx-validate — SCVS & CRA
cdx-verify — Verify BOM signatures
evinse — Evidence and SaaSBOM enrichment
REPL / cdxi
Server Usage
Getting Started - Development
Supported Project Types
Environment Variables
Advanced Usage
MCP Inventory
cdx: Custom Properties
BOM Audit
AI/ML Usage
Permissions
Configuring Allowlists
Threat Model
Tutorials - Java
Tutorials - JavaScript
Tutorials - Sign & Attach
Tutorials - Standards & Attestations
Tutorials - OWASP juice-shop
Tutorials - Multi-Signing and Signature Chaining for SBOMs
Tutorials - Validating SBOMs against SCVS and CRA
Tutorials - Scanning Git URLs and purls with BOM Audit
Tutorials - Auditing container escape and privilege risks
Tutorials - Auditing Cargo workspaces, caches, and native build surfaces
Tutorials - Cataloging and auditing MCP servers
Tutorials - Cataloging Electron ASAR archives
Tutorials - Generating OBOM
Trust enrichment BOM diff examples
macOS OBOM troubleshooting
Support (Enterprise & Community)
Getting Started
cdxgen is available as an npm package, container image, and single executable binaries. Begin your journey by selecting your use case.

Installation
npm install -g @cyclonedx/cdxgen
If you are a Homebrew user, you can also install cdxgen via:

brew install cdxgen
If you are a Winget user on windows, you can also install cdxgen via:

winget install cdxgen
Single Executable Application (SEA) Binaries
cdxgen is available as a standalone binary for Linux, macOS, and Windows. These binaries do not require Node.js or npm to be installed on the system, making them ideal for CI/CD environments, containerized scans, or quick local usage.

Binaries are available in the GitHub Releases page.

Available Variants:

Standard: (cdxgen-linux-amd64, etc.) The default standalone binary with bundled plugins and node runtime.
Slim: (-slim) Smaller binaries with the node runtime and without the binary plugins. Some project types that require plugins such as docker, os, and features such as evinse will not work.
Musl: (-musl) Linked against Musl libc, specifically for Alpine Linux.
Linux and macOS (Bash)
OS=linux
ARCH=amd64
BINARY_NAME=cdxgen-$OS-$ARCH

curl -LO "https://github.com/cdxgen/cdxgen/releases/latest/download/$BINARY_NAME"
curl -LO "https://github.com/cdxgen/cdxgen/releases/latest/download/$BINARY_NAME.sha256"

if command -v sha256sum >/dev/null; then
  sha256sum -c "$BINARY_NAME.sha256"
else
  shasum -a 256 -c "$BINARY_NAME.sha256"
fi

chmod +x "$BINARY_NAME"
./"$BINARY_NAME" --version
Windows (PowerShell)
$Arch = "amd64"
$BinaryName = "cdxgen-windows-$Arch.exe"
$BaseUrl = "https://github.com/cdxgen/cdxgen/releases/latest/download"

Invoke-WebRequest -Uri "$BaseUrl/$BinaryName" -OutFile $BinaryName
Invoke-WebRequest -Uri "$BaseUrl/$BinaryName.sha256" -OutFile "$BinaryName.sha256"

$ExpectedHash = (Get-Content "$BinaryName.sha256").Split(" ")[0].Trim()
$ActualHash = (Get-FileHash $BinaryName -Algorithm SHA256).Hash.ToLower()

if ($ExpectedHash -eq $ActualHash) {
    Write-Host "Hash verified successfully!" -ForegroundColor Green
    & .\$BinaryName --version
} else {
    Write-Error "Hash mismatch! Do not run the binary."
}
Note: The cdx-verify, cdx-sign, cdx-validate, and cdx-convert tools are also available as standalone binaries in the releases using the same naming convention (e.g., cdx-convert-linux-amd64).

Generate BOM for source code inputs
Minimal example.

cd <Path to source code>
cdxgen -o bom.json
For a java project. This would automatically detect maven, gradle or sbt and build bom accordingly

cdxgen -t java -o bom.json
To print the SBOM as a table pass -p argument.

cdxgen -t java -o bom.json -p
To recursively generate a single BOM for all languages pass -r argument.

cdxgen -r -o bom.json
Generate directly from a git URL:

cdxgen -t java -o bom.json --git-branch main https://github.com/HooliCorp/java-sec-code.git
Generate from a package URL (purl):

cdxgen -t js -o bom.json "pkg:npm/lodash@4.17.21"
Supported purl source types: npm, pypi, gem, cargo, pub, github, bitbucket, maven (version required), composer, and generic (with vcs_url or download_url qualifier).

Warning: For purl inputs, cdxgen resolves repository metadata from registries. This information can be inaccurate or malicious, so review resolved sources before trusting output.

To generate SBOM for an older specification version such as 1.4, pass the version using the --spec-version argument.

cdxgen -r -o bom.json --spec-version 1.4
To generate SBOM for C or Python, ensure Java >= 21 is installed.

# Install java >= 21
cdxgen -t c -o bom.json
Generate BOM for container images
docker type is automatically detected based on the presence of values such as sha256 or docker.io prefix etc in the path.

cdxgen odoo@sha256:4e1e147f0e6714e8f8c5806d2b484075b4076ca50490577cdf9162566086d15e -o bom.json
You can also pass -t docker for simple labels. Only the latest tag would be pulled if none was specified.

cdxgen ghcr.io/owasp-dep-scan/depscan:nightly -o bom.json -t docker
For offline or staged scans, point cdxgen at a locally reconstructed root filesystem directory. The container pipeline accepts -t docker, -t rootfs, or -t oci-dir for this mode.

cdxgen /tmp/remote_target -o /tmp/bom.json -t rootfs
With the packaged helpers installed, rootfs and container BOMs now gain repository trust-source components, deep keyring / CA-store cryptographic-asset components, native CycloneDX origin fields such as supplier, manufacturer, and authors for OS package trust metadata, plus additional package trust-state properties such as PackageArchitecture, PackageSource, and PackageStatus.

You can also pass the .tar file of a container image.

docker pull ghcr.io/owasp-dep-scan/depscan
docker save -o /tmp/slim.tar ghcr.io/owasp-dep-scan/depscan
podman save -q --format oci-archive -o /tmp/slim.tar ghcr.io/owasp-dep-scan/depscan
cdxgen /tmp/slim.tar -o /tmp/bom.json -t docker
Podman in rootless mode
Setup podman in either rootless or remote mode

On Linux, do not forget to start the podman socket which is required for API access.

systemctl --user enable --now podman.socket
systemctl --user start podman.socket
podman system service -t 0 &
Generate OBOM
You can use the obom command to generate an OBOM for a live system or a VM for compliance and vulnerability management purposes. Linux, Windows, and macOS are supported in this mode, though some macOS tables require elevated privileges and Full Disk Access.

# obom is an alias for cdxgen -t os
obom
# cdxgen -t os
This feature is powered by osquery, which is installed along with the binary plugins. cdxgen would opportunistically try to detect as many components, apps, and extensions as possible using the platform-specific default queries under data/queries*.json. With osquery 5.23.0, the default profiles now include Gatekeeper posture on macOS, Secure Boot certificate inventory on Linux, targeted Windows process-open-handle telemetry, and improved npm package discovery. The process would take several minutes and result in an SBOM file with thousands of components of various types such as operating-system, device-drivers, files, and data.

When trustinspector is available, live-host OBOM generation also enriches matching macOS and Windows components with code-signing / notarization / Authenticode properties and emits additional host-trust data components for Gatekeeper and WDAC posture. See Trust enrichment BOM diff examples for compact before/after excerpts.

For macOS-specific setup and permission caveats, see OBOM macOS troubleshooting.

For practical SOC/IR and compliance playbooks, see OBOM lessons. For container hardening and breakout-focused binary reviews, see Lesson 9.

Integrate with Dependency Track
Invoke cdxgen with the below arguments to automatically submit the BOM to your organization’s Dependency Track server.

      --type                   Project type. Please refer to https://cyclonedx.g
                               ithub.io/cdxgen/#/PROJECT_TYPES for supported lan
                               guages/platforms.
      --server-url             Dependency track url. Eg: https://deptrack.cyclon
                               edx.io
      --api-key                Dependency track api key
      --project-group          Dependency track project group
      --project-name           Dependency track project name. Default use the di
                               rectory name
      --project-version        Dependency track project version    [default: ""]
      --project-tag            Dependency track project tag. Multiple values all
                               owed.                                     [array]
      --project-id             Dependency track project id. Either provide the i
                               d or the project name and version together
      --parent-project-id      Dependency track parent project id. You must provide the id or both
                               parent project name and parent project version.
      --parent-project-name    Dependency track parent project name
      --parent-project-version Dependency track parent project version
Example
cdxgen -t java -o bom.json --server-url https://deptrack.server.com --api-key "token" --project-group ...
Supported Languages and Package Managers
See our Supported Project Types documentation

Advanced Usage
cdxgen supports advanced use cases as a library and in REPL mode.

Resolving Licenses
cdxgen can automatically query public registries such as maven, npm, or nuget to resolve the package licenses. This is a time-consuming operation and is disabled by default. To enable, set the environment variable FETCH_LICENSE to true, as shown.

export FETCH_LICENSE=true
SBOM Server
Invoke cdxgen with --server argument to run it in server mode. By default, it listens to port 9090, which can be customized with the arguments --server-host and --server-port.

cdxgen --server
Or use the container image.

docker run --rm -v /tmp:/tmp -p 9090:9090 -v $(pwd):/app:rw -t ghcr.io/cyclonedx/cdxgen -r /app --server --server-host 0.0.0.0
Use curl or your favourite tool to pass arguments to the /sbom route.

Scanning a local path
curl "http://127.0.0.1:9090/sbom?path=/Volumes/Work/sandbox/vulnerable-aws-koa-app&multiProject=true&type=js"
Scanning a git repo
curl "http://127.0.0.1:9090/sbom?url=https://github.com/HooliCorp/vulnerable-aws-koa-app.git&multiProject=true&type=js"
If you need to pass credentials to authenticate.

curl "http://127.0.0.1:9090/sbom?url=https://<access_token>repo.git&multiProject=true&type=js"
curl "http://127.0.0.1:9090/sbom?url=https://<username>:<password>repo.git&multiProject=true&type=js"
You can POST the arguments.

curl -H "Content-Type: application/json" http://localhost:9090/sbom -XPOST -d $'{"url": "https://github.com/HooliCorp/vulnerable-aws-koa-app.git", "type": "nodejs", "multiProject": "true"}'
Integration as Library
cdxgen is ESM only and could be imported and used with both deno and Node.js >= 20

Minimal example:

import { createBom, submitBom } from "npm:@cyclonedx/cdxgen@^9.9.0";
See the Deno Readme for detailed instructions.

import { createBom, submitBom } from "@cyclonedx/cdxgen";
// bomNSData would contain bomJson
const bomNSData = await createBom(filePath, options);
// Submission to dependency track server
const dbody = await submitBom(args, bomNSData.bomJson);
BOM Signing
cdxgen can sign the generated BOM json file to increase authenticity and non-repudiation capabilities. To enable this, set the following environment variables.

SBOM_SIGN_ALGORITHM: Algorithm. Example: RS512
SBOM_SIGN_PRIVATE_KEY: Location to the RSA private key
SBOM_SIGN_PUBLIC_KEY: Optional. Location to the RSA public key
To generate test public/private key pairs, you can run cdxgen by passing the argument --generate-key-and-sign. The generated json file would have an attribute called signature, which could be used for validation. jwt.io is a known site that could be used for such signature validation.

SBOM signing

Verifying the signature
Use the bundled cdx-verify command, which supports verifying a single signature added at the bom level.

npm install -g @cyclonedx/cdxgen
cdx-verify -i bom.json --public-key public.key
Verifying the signature (pnpm)
Use the bundled cdx-verify command, which supports verifying a single signature added at the BOM level.

You can run it directly using pnpm (no global install needed):

pnpm dlx @cyclonedx/cdxgen cdx-verify -i bom.json --public-key public.key
Custom verification tool (Node.js example)
There are many libraries available to validate JSON Web Tokens. Below is a javascript example.

import { readFileSync } from "node:fs";

import jws from "jws";

// npm install jws
const bomJsonFile = "bom.json";
const publicKeyFile = "public.key";
const bomJson = JSON.parse(readFileSync(bomJsonFile, "utf8"));
// Retrieve the signature
const bomSignature = bomJson.signature.value;
const validationResult = jws.verify(
  bomSignature,
  bomJson.signature.algorithm,
  readFileSync(publicKeyFile, "utf8"),
);
if (validationResult) {
  console.log("Signature is valid!");
} else {
  console.log("SBOM signature is invalid :(");
}
REPL Mode
cdxi is the interactive REPL for creating, importing, querying, and reviewing BOMs.

cdxi demo

Use it to:

generate or import a BOM with .create or .import
inspect trust and provenance with .trusted and .provenance
review audit annotations with .auditfindings, .auditactions, and .dispatchedges
inspect evidence with .occurrences, .callstack, .services, and .formulation
pivot through OBOM categories with .osinfocategories and built-in osquery commands such as .processes
See REPL.md for the full command reference.

Sample REPL usage
Start the REPL server.

cdxi
Below are some example commands to create an SBOM for a spring application and perform searches and queries.

.create /mnt/work/vuln-spring
.print
.search spring
.query components[name ~> /spring/ and scope = "required"]
.trusted
.provenance
.auditfindings
// Supplier names
.query $distinct(components.supplier.name)

# Check obom metadata for windows os
.query metadata.component[purl ~> /Windows/]

# check if docker is installed in the c drive
.query components[name ~> /Docker/ and properties.value ~> "C:"]

# check if docker is running, exposing a pipe
.query components[name ~> /docker/ and properties[value = "pipes_snapshot"]]

.sort name
.sort components^(>name)
.update | components[name ~> /spring/] | {'publisher': "foo"} |
REPL History
Repl history will persist under the $HOME/.config/.cdxgen directory. To override this location, use the environment variable CDXGEN_REPL_HISTORY.
""Skip to content
cdxgen
cdxgen
Repository navigation
Code
Issues
412
 (412)
Pull requests
15
 (15)
Agents
Discussions
Actions
Security and quality
2
 (2)
Insights
Owner avatar
cdxgen
Public
cdxgen/cdxgen
Go to file
t
T
Name		
prabhuCopilot
prabhu
and
Copilot
package visibility, cbom and obom improvements (#4002)
4d233a5
 · 
2 hours ago
.github
package visibility, cbom and obom improvements (#4002)
2 hours ago
.versions
Update Node.js to v24.15.0 (#3995)
last week
bin
package visibility, cbom and obom improvements (#4002)
2 hours ago
ci
package visibility, cbom and obom improvements (#4002)
2 hours ago
contrib
Dependency-Track BOM submit: configurable autoCreate/isLatest + s…
3 weeks ago
data
package visibility, cbom and obom improvements (#4002)
2 hours ago
docs
package visibility, cbom and obom improvements (#4002)
2 hours ago
lib
package visibility, cbom and obom improvements (#4002)
2 hours ago
plugins
Moved plugins binary invocation to cdxgen to simplify bundling
4 years ago
test
package visibility, cbom and obom improvements (#4002)
2 hours ago
tools_config
Update references of SBoM to SBOM (#610)
3 years ago
types
package visibility, cbom and obom improvements (#4002)
2 hours ago
.codacy.yml
Let's make things easy for Ruby - part 1 (#1545)
last year
.dockerignore
Trim non-runtime files from published npm artifacts, image context, a…
last week
.gitignore
chore: gitignore macos (#2405)
7 months ago
.npmignore
load images in self-hosted agents
last year
.nvmrc
Update Node.js to v24.15.0 (#3995)
last week
.pnpmfile.cjs
Removed the removal of transitive dependencies for @npmcli/query (#3101)
5 months ago
.pokurc.jsonc
feat: add VS Code extension support with deep BOM generation and capa…
last month
ADVANCED.md
package visibility, cbom and obom improvements (#4002)
2 hours ago
AGENTS.md
package visibility, cbom and obom improvements (#4002)
2 hours ago
AI-DECLARATION.md
Remove dependency on table (#3919)
3 weeks ago
LICENSE
Initial commit
9 years ago
README.md
package visibility, cbom and obom improvements (#4002)
2 hours ago
SECURITY.md
Remove dependency on table (#3919)
3 weeks ago
SKILL.md
package visibility, cbom and obom improvements (#4002)
2 hours ago
biome.json
package visibility, cbom and obom improvements (#4002)
2 hours ago
deno.json
package visibility, cbom and obom improvements (#4002)
2 hours ago
docker-compose.yml
Use node 22 via nvm in docker. Enable NODE_COMPILE_CACHE (#1036)
2 years ago
index.cjs
Adds support for commonjs and esbuild (#1712)
last year
jsr.json
types
last week
package.json
package visibility, cbom and obom improvements (#4002)
2 hours ago
pnpm-lock.yaml
package visibility, cbom and obom improvements (#4002)
2 hours ago
pnpm-workspace.yaml
WIP: pnpm v11 support (#3861)
last month
pyproject.toml
types
last week
renovate.json
GitHub workflows parsing improvements (#3796)
2 months ago
tsconfig.json
Add qualifiers only for os packages (#3577)
3 months ago
uv.lock
types
last week
Repository files navigation
README
Apache-2.0 license
Security
SBOM AI-DECLARATION: pair JSR NPM GitHub Releases NPM Downloads GitHub License GitHub Contributors SWH

CycloneDX Generator (cdxgen)


cdxgen is a CLI tool, library, REPL, and server to create, validate, sign, and verify software BOMs. It generates CycloneDX JSON BOMs and supports SPDX 3.0.1 JSON-LD export. CycloneDX is a full-stack BOM specification that is easily created, human and machine-readable, and simple to parse. The tool supports CycloneDX specification versions from 1.5 - 1.7.

Supported BOM formats:

Software (SBOM) - For many languages and container images.
Cryptography (CBOM) - For Java keystores and certificates, plus JavaScript and TypeScript source-level algorithm inventory.
Operations (OBOM) - For Linux container images and VMs running Linux or Windows operating systems.
Software-as-a-Service (SaaSBOM) - For Java, Python, JavaScript, TypeScript, and PHP projects.
Attestations (CDXA) - Generate SBOM with templates for multiple standards. Sign the BOM document at a granular level to improve authenticity.
Vulnerability Disclosure Report (VDR) - Use cdxgen with OWASP depscan to automate the generation of VDR at scale.
Supported output document formats:

CycloneDX JSON (primary native format)
SPDX 3.0.1 JSON-LD (cdxgen --format spdx or cdx-convert)
Choose your path
Persona	What cdxgen helps you do	First command	Read next
Developers	Generate a CycloneDX BOM from a local repo, git URL, purl, or container image	cdxgen -o bom.json .	CLI Usage, Supported Project Types
AppSec	Enrich BOMs with evidence, run BOM audit rules, and feed downstream security workflows	cdxgen -o bom.json --profile appsec --evidence --bom-audit .	BOM Audit, Threat Model
SOC analysts	Build OBOM inventories for live hosts and triage runtime posture issues	obom -o obom.json --deep --bom-audit --bom-audit-categories obom-runtime	OBOM lessons, Server Usage
Compliance teams	Validate BOM quality, check SCVS/CRA posture, and export SPDX deliverables	cdx-validate -i bom.json --benchmark scvs-l2,cra	cdx-validate, cdx-convert, Permissions
Role-based quick starts
For developers
Start with a local path, git URL, or purl and generate a BOM in one command.
Use Supported Project Types to confirm ecosystem coverage before wiring cdxgen into CI.
For AppSec
Use --profile appsec, --evidence, and --bom-audit when you want richer security context.
Combine generation with BOM Audit, cdx-validate, signing, and verification for a fuller secure-SBOM workflow.
For SOC analysts
Use obom for live-system and runtime inventory on Linux, Windows, and macOS hosts.
Focus on OBOM lessons when you need host triage, persistence review, Linux GTFOBins-backed runtime analysis, hardening drift review, or incident-response evidence.
For compliance and platform governance
Use cdx-validate to assess structural and compliance posture, then cdx-convert when SPDX output is required.
Review Permissions and hardened-environment guidance before adopting cdxgen in controlled pipelines.
Why cdxgen?
Most SBOM tools are like simple barcode scanners. For easy applications, they can parse a few package manifests and create a list of components only based on these files without any deep inspection. Further, a typical application might have several repos, components, and libraries with complex build requirements. Traditional techniques to generate an SBOM per language or package manifest either do not work in enterprise environments or don't provide the confidence required for both compliance and automated analysis. So we built cdxgen - the universal polyglot SBOM generator that is user-friendly, precise, and comprehensive!

Our philosophy:

Explainability: Don't list, but explain with evidence.
Precision: Try using multiple techniques to improve precision, even if it takes extra time.
Personas: Cater to the needs of a range of personas such as security researchers, compliance auditors, developers, and SOC.
Machine Learning: Optimize the generated data for Machine Learning (ML) purposes by considering the various model properties.
Safety: Execute external build tools and handle untrusted inputs defensively, with hardened defaults, a secure mode for sensitive environments, and a read-only --dry-run mode for review-first workflows.
Review-first dry runs
When you want to inspect what cdxgen would do before allowing side effects, use --dry-run.

cdxgen --dry-run -p -t js .
Dry-run mode keeps cdxgen read-only: it reads local files, blocks writes/exec/temp creation/cloning/submission, and prints an activity summary table for both beginners and power users. When available, the recorded activity data also captures archive extraction intent, command I/O volume, and followed symlink-resolution traces.

Documentation
Please visit our GPT app or the documentation site for detailed usage, tutorials, and support documentation.

Sections include:

Getting Started
CLI Usage
Server Usage
Hands-on Lessons
Container Escape & Privilege Lesson
Supported Project Types
Environment Variables
Advanced Usage
Permissions
Security Policy
Threat Model
Support (Enterprise & Community)
Usage
Installing
Install the npm package when you want the full multi-command CLI surface.

npm install -g @cyclonedx/cdxgen
Installing @cyclonedx/cdxgen exposes these commands:

Command	Purpose	Standalone GitHub release binary
cdxgen	Generate CycloneDX / SPDX BOMs from source, images, binaries, git URLs, or purls	yes
cdx-audit	Prioritize existing BOM dependencies for upstream supply-chain review using explainable risk signals	yes
cdx-convert	Convert CycloneDX JSON to SPDX 3.0.1 JSON-LD	yes
cdx-sign	Sign BOMs with JSF signatures	yes
cdx-validate	Validate BOMs and benchmark posture	yes
cdx-verify	Verify BOM signatures	yes
cdxi	Open the interactive REPL	no
evinse	Add evidence, reachability, and service context	no
cbom	Alias for CBOM-oriented cdxgen defaults	use cdxgen
obom	Alias for cdxgen -t os	use cdxgen
saasbom	Alias for SaaSBOM-oriented cdxgen defaults	use cdxgen
spdxgen	Alias for cdxgen --format spdx	use cdxgen
cdxgen-secure	Alias for hardened cdxgen defaults	use cdxgen
Standalone GitHub release binaries are published for cdxgen, cdxgen-slim, cdx-audit, cdx-convert, cdx-sign, cdx-validate, and cdx-verify.

cdx-audit is designed to accelerate upstream dependency review with explainable, evidence-backed risk prioritization. It complements provenance, reproducibility, and manual investigation rather than replacing them.

To run cdxgen without installing (hotloading), use the pnpm dlx command.

corepack pnpm dlx @cyclonedx/cdxgen --help
You can call any packaged command the same way:

corepack pnpm dlx --package=@cyclonedx/cdxgen cdx-audit --help
corepack pnpm dlx --package=@cyclonedx/cdxgen cdx-convert --help
corepack pnpm dlx --package=@cyclonedx/cdxgen cdx-validate --help
corepack pnpm dlx --package=@cyclonedx/cdxgen cdx-sign --help
corepack pnpm dlx --package=@cyclonedx/cdxgen cdx-verify --help
corepack pnpm dlx --package=@cyclonedx/cdxgen evinse --help
corepack pnpm dlx --package=@cyclonedx/cdxgen cdxi --help
If you are a Homebrew user, you can also install cdxgen via:

$ brew install cdxgen
If you are a Winget user on windows, you can also install cdxgen via:

winget install cdxgen
Standalone GitHub release binaries
If you want a single-file executable instead of an npm installation, download a published release asset and verify its hash before executing it.

Common asset names:

cdxgen-linux-amd64
cdxgen-linux-amd64-musl
cdxgen-darwin-arm64
cdxgen-windows-amd64.exe
cdx-audit-linux-amd64
cdx-audit-darwin-arm64
cdx-audit-windows-amd64.exe
cdx-convert-*, cdx-sign-*, cdx-validate-*, cdx-verify-*
Linux
VERSION="v12.3.1"
ASSET="cdx-audit-linux-amd64"
BASE_URL="https://github.com/cdxgen/cdxgen/releases/download/${VERSION}"

curl -fsSLO "${BASE_URL}/${ASSET}"
curl -fsSLO "${BASE_URL}/${ASSET}.sha256"
sha256sum -c "${ASSET}.sha256"
chmod +x "${ASSET}"
./"${ASSET}" --help
macOS
VERSION="v12.3.1"
ASSET="cdx-audit-darwin-arm64"
BASE_URL="https://github.com/cdxgen/cdxgen/releases/download/${VERSION}"

curl -fsSLO "${BASE_URL}/${ASSET}"
curl -fsSLO "${BASE_URL}/${ASSET}.sha256"
shasum -a 256 -c "${ASSET}.sha256"
chmod +x "${ASSET}"
./"${ASSET}" --help
Windows (PowerShell)
$Version = "v12.3.1"
$Asset = "cdx-audit-windows-amd64.exe"
$BaseUrl = "https://github.com/cdxgen/cdxgen/releases/download/$Version"

Invoke-WebRequest -Uri "$BaseUrl/$Asset" -OutFile $Asset
Invoke-WebRequest -Uri "$BaseUrl/$Asset.sha256" -OutFile "$Asset.sha256"
$Expected = (Get-Content "$Asset.sha256" | Select-Object -First 1).Trim().Split()[0]
$Actual = (Get-FileHash $Asset -Algorithm SHA256).Hash.ToLowerInvariant()
if ($Actual -ne $Expected.ToLowerInvariant()) {
  throw "SHA256 mismatch for $Asset"
}
.\$Asset --help
GitHub Actions with the GitHub CLI
permissions:
  contents: read

steps:
  - name: Download cdx-audit release binary
    env:
      GH_TOKEN: ${{ github.token }}
    run: |
      gh release download v12.3.1 \
        --repo cdxgen/cdxgen \
        --pattern 'cdx-audit-linux-amd64' \
        --pattern 'cdx-audit-linux-amd64.sha256'
      sha256sum -c cdx-audit-linux-amd64.sha256
      chmod +x cdx-audit-linux-amd64
      ./cdx-audit-linux-amd64 --help
Deno and bun runtime can be used with limited support.

deno install --allow-read --allow-env --allow-run --allow-sys=uid,systemMemoryInfo,gid,homedir --allow-write --allow-net -n cdxgen "npm:@cyclonedx/cdxgen/cdxgen"
You can also use the cdxgen container image with node, deno, or bun runtime versions.

The default version uses Node.js 23

docker run --rm -e CDXGEN_DEBUG_MODE=debug -v /tmp:/tmp -v $(pwd):/app:rw -t ghcr.io/cyclonedx/cdxgen:master -r /app -o /app/bom.json
To use the deno version, use ghcr.io/cyclonedx/cdxgen-deno as the image name.

docker run --rm -e CDXGEN_DEBUG_MODE=debug -v /tmp:/tmp -v $(pwd):/app:rw -t ghcr.io/cyclonedx/cdxgen-deno:master -r /app -o /app/bom.json
For the bun version, use ghcr.io/cyclonedx/cdxgen-bun as the image name.

docker run --rm -e CDXGEN_DEBUG_MODE=debug -v /tmp:/tmp -v $(pwd):/app:rw -t ghcr.io/cyclonedx/cdxgen-bun:master -r /app -o /app/bom.json
In deno applications, cdxgen could be directly imported without any conversion.

import { createBom, submitBom } from "npm:@cyclonedx/cdxgen@^12.2.1";
Common workflows
Goal	First command	Read next
Generate a BOM from the current repository	cdxgen -o bom.json .	CLI Usage
Generate a BOM from a git URL	cdxgen -o bom.json https://github.com/example/project.git	CLI Usage
Generate a BOM from a package URL	cdxgen -o bom.json "pkg:npm/lodash@4.17.21"	CLI Usage
Scan a container image	cdxgen ghcr.io/owasp-dep-scan/depscan:nightly -o bom.json -t docker	Server Usage
Audit a generated BOM for built-in supply-chain findings	cdxgen -o bom.json --bom-audit .	BOM Audit
Prioritize an existing BOM for upstream risk-driven review	cdx-audit --bom bom.json	cdx-audit
Validate a BOM against structural and compliance checks	cdx-validate -i bom.json	cdx-validate
Convert CycloneDX JSON to SPDX JSON-LD	cdx-convert -i bom.json -o bom.spdx.json	cdx-convert
Generate an OBOM for live-system triage	obom -o obom.json --deep --bom-audit --bom-audit-categories obom-runtime	OBOM lessons
Review an offline rootfs for hardening drift	cdxgen /absolute/path/to/rootfs -t rootfs -o bom.json --bom-audit --bom-audit-categories rootfs-hardening	BOM Audit
For the full option reference, use cdxgen --help or visit CLI Usage.

Companion commands also expose built-in help:

cbom --help
cdx-audit --help
cdx-validate --help
cdx-convert --help
cdx-sign --help
cdx-verify --help
cdxgen-secure --help
cdxi --help
evinse --help
obom --help
saasbom --help
spdxgen --help
Example
Minimal example.

cdxgen -o bom.json
The primary positional input can be:

a local filesystem path (default: current directory)
a git URL that cdxgen clones before scanning
a package URL (purl) that cdxgen resolves to source and then scans
Common source input examples:

# Local path
cdxgen -o bom.json .

# Git URL
cdxgen -t java -o bom.json --git-branch main https://github.com/HooliCorp/java-sec-code.git

# Package URL (purl)
cdxgen -t js -o bom.json "pkg:npm/lodash@4.17.21"
For a java project. cdxgen would automatically detect maven, gradle, or sbt and build bom accordingly

cdxgen -t java -o bom.json
To print the SBOM as a table pass -p argument.

cdxgen -t java -o bom.json -p
To recursively generate a single BOM for all languages pass -r argument.

cdxgen -r -o bom.json
To generate an SBOM directly from a git URL:

cdxgen -t java -o bom.json --git-branch main https://github.com/HooliCorp/java-sec-code.git
This works anywhere cdxgen expects its primary source input, so a git URL can be used in place of . or any other local path.

To generate an SBOM from a package URL (purl), cdxgen resolves registry metadata to a repository URL, clones it, and scans it:

cdxgen -t js -o bom.json "pkg:npm/lodash@4.17.21"
Supported purl source types: npm, pypi, gem, cargo, pub, github, bitbucket, maven (version required), composer, and generic (with vcs_url or download_url qualifier).

Warning: Repository URLs resolved from registries may be inaccurate or malicious. Review resolved sources before trusting generated output.

The default specification used by cdxgen is 1.7. To generate BOM for a different specification version, such as 1.5 or 1.6, pass the version number using the --spec-version argument.

# 1.6 is supported by most tools
cdxgen -r -o bom.json --spec-version 1.6
To generate SBOM for C or Python, ensure Java >= 21 is installed.

# Install java >= 21
cdxgen -t c -o bom.json
NOTE: cdxgen is known to freeze with Java 8 or 11, so ensure >= 21 is installed and JAVA_HOME environment variable is configured correctly. If in doubt, use the cdxgen container image.

Universal SBOM
By passing the type argument -t universal, cdxgen could be forced to opportunistically collect as many components and services as possible by scanning all package, container, and Kubernetes manifests. The resulting SBOM could have over a thousand components, thus requiring additional triaging before use with traditional SCA tools.

SBOM server
Invoke cdxgen with --server argument to run it in server mode. By default, it listens to port 9090, which can be customized with the arguments --server-host and --server-port.

cdxgen --server
Or use the container image.

docker run --rm -v /tmp:/tmp -p 9090:9090 -v $(pwd):/app:rw -t ghcr.io/cyclonedx/cdxgen -r /app --server --server-host 0.0.0.0
Use curl or your favorite tool to pass arguments to the /sbom route.

Server arguments
Arguments can be passed either via the query string or as a JSON body. Please refer to Server Usage

Health endpoint
Use the /health endpoint to check if the SBOM server is up and running.

curl "http://127.0.0.1:9090/health"
Scanning a local path
curl "http://127.0.0.1:9090/sbom?path=/Volumes/Work/sandbox/vulnerable-aws-koa-app&multiProject=true&type=js"
Scanning a git repo
curl "http://127.0.0.1:9090/sbom?url=https://github.com/HooliCorp/vulnerable-aws-koa-app.git&multiProject=true&type=js"
If you need to pass credentials to authenticate.

curl "http://127.0.0.1:9090/sbom?url=https://<access_token>repo.git&multiProject=true&type=js"
curl "http://127.0.0.1:9090/sbom?url=https://<username>:<password>repo.git&multiProject=true&type=js"
You can POST the arguments.

curl -H "Content-Type: application/json" http://localhost:9090/sbom -XPOST -d $'{"url": "https://github.com/HooliCorp/vulnerable-aws-koa-app.git", "type": "nodejs", "multiProject": "true"}'
Docker compose
git clone https://github.com/cdxgen/cdxgen.git
docker compose up
War file support
cdxgen can generate a BOM file from a given war file.

# cdxgen -t java app.war
cdxgen app.war
Resolving class names
Sometimes, it is necessary to resolve class names contained in jar files. By passing an optional argument --resolve-class, it is possible to get cdxgen to create a separate mapping file with the jar name (including the version) as the key and class names list as a value.

cdxgen -t java --resolve-class -o bom.json
This would create a bom.json.map file with the jar - class name mapping. Refer to these examples to learn about the structure.

Resolving licenses
cdxgen can automatically query public registries such as maven, npm, or nuget to resolve the package licenses. This is a time-consuming operation and is disabled by default. To enable, set the environment variable FETCH_LICENSE to true, as shown. Ensure that GITHUB_TOKEN is set or provided by built-in GITHUB_TOKEN in GitHub Actions, otherwise rate limiting might prevent license resolving.

export FETCH_LICENSE=true
Dependency Tree
cdxgen can retain the dependency tree under the dependencies attribute for a small number of supported package manifests. These are currently limited to:

package-lock.json
yarn.lock
pnpm-lock.yaml
Maven (pom.xml)
Gradle
Scala SBT
Python (requirements.txt, setup.py, pyproject.toml, poetry.lock)
.NET (packages.lock.json, project.assets.json, paket.lock, .nuspec/.nupkg)
Go (go.mod)
PHP (composer.lock)
Ruby (Gemfile.lock)
Rust (Cargo.lock)
Plugins
cdxgen could be extended with external binary plugins to support more SBOM use cases. These are now installed as an optional dependency.

sudo npm install -g @cdxgen/cdxgen-plugins-bin
Plugins (pnpm)
cdxgen can be extended with external binary plugins to support more SBOM use cases.
These are now installed as optional dependencies and can be used without a global install.

pnpm dlx @cdxgen/cdxgen-plugins-bin
Docker / OCI container support
docker type is automatically detected based on the presence of values such as sha256 or docker.io prefix etc in the path.

cdxgen odoo@sha256:4e1e147f0e6714e8f8c5806d2b484075b4076ca50490577cdf9162566086d15e -o /tmp/bom.json
You can also pass -t docker with repository names. Only the latest tag would be pulled if none was specified.

cdxgen shiftleft/scan-slim -o /tmp/bom.json -t docker
For offline or staged scans, point cdxgen at a locally reconstructed root filesystem directory. The container pipeline accepts -t docker, -t rootfs, or -t oci-dir for this mode.

cdxgen /tmp/remote_target -o /tmp/bom.json -t rootfs
With the packaged helpers installed, rootfs and container BOMs now gain repository trust-source components, deep keyring / CA-store cryptographic-asset components, native CycloneDX origin fields such as supplier, manufacturer, and authors for OS package trust metadata, plus additional package trust-state properties such as PackageArchitecture, PackageSource, and PackageStatus.

You can also pass the .tar file of a container image.

docker pull shiftleft/scan-slim
docker save -o /tmp/slim.tar shiftleft/scan-slim
podman save -q --format oci-archive -o /tmp/slim.tar shiftleft/scan-slim
cdxgen /tmp/slim.tar -o /tmp/bom.json -t docker
Podman in rootless mode
Setup podman in either rootless or remote mode

Do not forget to start the podman socket required for API access on Linux.

systemctl --user enable --now podman.socket
systemctl --user start podman.socket
podman system service -t 0 &
Generate OBOM for a live system
You can use the obom command to generate an OBOM for a live system or a VM for compliance and vulnerability management purposes. Linux, Windows, and macOS are supported in this mode, though some macOS tables require elevated privileges and Full Disk Access.

# obom is an alias for cdxgen -t os
obom
# cdxgen -t os
This feature is powered by osquery, which is installed along with the binary plugins. cdxgen would opportunistically try to detect as many components, apps, and extensions as possible using the platform-specific default queries under data/queries*.json. The Linux profile includes dedicated sysctl_hardening and mount_hardening snapshots, GTFOBins enrichment for privileged and network-active runtime rows, Secure Boot certificate inventory, and improved npm package discovery. When the optional trustinspector helper is available, OBOM collection is further enriched with:

macOS code-signing authority, team ID, and notarization assessment metadata for discovered application paths
Windows Authenticode signer/timestamp metadata for discovered executable paths
Windows WDAC active-policy inventory
batched path inspection so large host inventories keep their trust metadata instead of stopping at the first few hundred paths
Container and rootfs BOMs also summarize how many executable and shared-library file components were discovered outside OS package ownership. Look for cdx:container:unpackagedExecutableCount and cdx:container:unpackagedSharedLibraryCount in metadata, or use .unpackagedbins and .unpackagedlibs in cdxi for an interactive pivot.

The process would take several minutes and result in an SBOM file with thousands of components of various types, such as operating-system, device-drivers, files, and data.

For practical SOC/IR and compliance workflows, see the dedicated OBOM lessons. For macOS-specific setup and permission caveats, see OBOM macOS troubleshooting. For compact before/after examples of the new trust metadata, see Trust enrichment BOM diff examples.

Generate Cryptography Bill of Materials (CBOM)
Use the cbom alias to generate a CBOM. In addition to keystores and certificates, cdxgen can also derive cryptographic algorithm inventory from JavaScript and TypeScript source by following lightweight constant propagation through common node:crypto, WebCrypto, and JWT call sites.

cbom -t java
# cdxgen -t java --include-crypto -o bom.json .

# Add source-derived crypto algorithms for a JS or TS project
cdxgen --include-crypto -o bom.json /absolute/path/to/js-project
When reviewing the result in cdxi, use .cryptos for the full cryptographic asset view or .sourcecryptos to narrow the list to source-derived algorithm components only.

Generating SaaSBOM and component evidences
See evinse mode in the advanced documentation.

BOM signing
cdxgen features a best-in-class, native JSON Signature Format (JSF) implementation for BOM signing, providing robust authenticity and non-repudiation capabilities. Unlike basic signing tools, our implementation fully supports granular signatures (signing individual components, services, and annotations), parallel Multi-Signatures (signers), and sequential Signature Chains (chain).

To enable automatic signing during BOM generation, set the following environment variables:

SBOM_SIGN_ALGORITHM: JSF Algorithm. Examples: RS512, ES256, Ed25519, HS256
SBOM_SIGN_PRIVATE_KEY: Location of the private key (PEM format)
SBOM_SIGN_PUBLIC_KEY: Optional. Location of the public key
SBOM_SIGN_MODE: Optional. Signature mode (replace, signers, chain). Default is replace.
To quickly generate test public/private key pairs and sign your first BOM, you can run cdxgen with the --generate-key-and-sign argument.

Advanced Signing with cdx-sign
For complex supply chain orchestration, use the bundled cdx-sign CLI. This tool allows multiple entities (e.g., a Builder and an Auditor) to co-sign an existing BOM without modifying its original data.

# Append a parallel multi-signature (Auditor co-signing)
# Note: Granular component signing is disabled to preserve the Builder's original signature payload.
cdx-sign -i bom.json -k auditor_private.pem -a ES256 --key-id "auditor-qa" --mode signers --no-sign-components
Validating CycloneDX BOMs
Use the bundled cdx-validate command to validate CycloneDX BOMs against structural, deep, and compliance checks. Refer to this document for usage.

Verifying the signature
Use the bundled cdx-verify command to validate BOM signatures. By default, cdx-verify performs a strict deep verification, meaning it mathematically validates the top-level BOM signature and the signatures of every nested component, service, and annotation against the provided public key. Refer to this lesson for the usage of sign and verify commands.

npm install -g @cyclonedx/cdxgen

# Perform strict deep verification (default)
cdx-verify -i bom.json --public-key public.key

# Verify ONLY the top-level root signature (useful for verifying a multi-signer who didn't sign nested components)
cdx-verify -i bom.json --public-key auditor_public.key --no-deep
Verifying the signature (pnpm)
You can run the verification tools directly using pnpm (no global install needed):

pnpm dlx @cyclonedx/cdxgen cdx-verify -i bom.json --public-key public.key
You can also use pnpm to invoke the signing tool:

pnpm dlx @cyclonedx/cdxgen cdx-sign -i bom.json -k private.key
Automatic usage detection
For node.js projects, lock files are parsed initially, so the SBOM would include all dependencies, including dev ones. An AST parser powered by babel-parser is then used to detect packages that are imported and used by non-test code. Such imported packages would automatically set their scope property to required in the resulting SBOM. You can turn off this analysis by passing the argument --no-babel. Scope property would then be set based on the dev attribute in the lock file.

This attribute can be later used for various purposes. For example, dep-scan uses this attribute to prioritize vulnerabilities. Unfortunately, tools such as dependency track, do not include this feature and might over-report the CVEs.

With the argument --required-only, you can limit the SBOM only to include packages with the scope "required", commonly called production or non-dev dependencies. Combine with --no-babel to limit this list to only non-dev dependencies based on the dev attribute being false in the lock files.

For go, go mod why command is used to identify required packages. For php, composer lock file is parsed to distinguish required (packages) from optional (packages-dev).

Automatic services detection
cdxgen can automatically detect names of services from YAML manifests such as docker-compose, Kubernetes, or Skaffold manifests. These would be populated under the services attribute in the generated SBOM. With evinse, additional services could be detected by parsing common annotations from the source code.

Conversion to SPDX format
For direct conversion of an existing CycloneDX JSON BOM to SPDX JSON-LD, use the bundled cdx-convert command:

cdx-convert -i bom.json -o bom.spdx.json
cdx-convert currently supports CycloneDX 1.6 and 1.7 inputs and exports SPDX 3.0.1 JSON-LD.

Use cdxgen --format spdx (or --format cyclonedx,spdx) when generating BOMs. Use the CycloneDX CLI tool for advanced use cases such as diff and merging.

Including .NET Global Assembly Cache dependencies in the results
For dotnet and dotnet-framework, SBOM could include components without a version number. Often, these components begin with the prefix System..

Global Assembly Cache (GAC) dependencies (System Runtime dependencies) must be made available in the build output of the project for version detection. A simple way to have the dotnet build copy the GAC dependencies into the build directory is to place the file Directory.Build.props into the root of the project and ensure the contents include the following:

<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
<ItemDefinitionGroup>
  <Reference>
    <Private>True</Private>
  </Reference>
</ItemDefinitionGroup>
</Project>
Then, run cdxgen cli with the --deep argument.

License
Permission to modify and redistribute is granted under the terms of the Apache 2.0 license. See the LICENSE file for the full license.

Integration as library
cdxgen is ESM only and could be imported and used with both deno and Node.js >= 20

Minimal example:

import { createBom, submitBom } from "npm:@cyclonedx/cdxgen@^9.0.1";
See the Deno Readme for detailed instructions.

import { createBom, submitBom } from "@cyclonedx/cdxgen";
// bomNSData would contain bomJson
const bomNSData = await createBom(filePath, options);
// Submission to dependency track server
const dbody = await submitBom(args, bomNSData.bomJson);
Contributing
Please check out our open issues if you are interested in helping.

Codeberg Mirror
The project is mirrored on Codeberg. Users can clone the repository using the following URL:

git clone https://codeberg.org/cdxgen/cdxgen.git
The maintainers accept Pull Requests (PRs) against the Codeberg repository.

Note: The Codeberg repository is currently synced manually from GitHub.

Before raising a PR, please run the following commands.

corepack enable pnpm
pnpm install:frozen
# Generate types using jsdoc syntax
pnpm run gen-types
# Run biomejs formatter and linter with auto fix
pnpm run lint
# Run jest tests
pnpm test
Testing main branch
Use pnpm add -g command to quickly test the main branch.

corepack pnpm bin -g
corepack pnpm setup
corepack pnpm add -g https://github.com/cdxgen/cdxgen
cdxgen --help
Testing main branch (No Global Install)
To quickly test the latest main branch without installing globally, you can use pnpm in a local or temporary environment.

corepack enable
pnpm install --prefer-offline
pnpm dlx cdxgen --help
Sponsors
 
Some features are funded through NGI Zero Core, a fund established by NLnet with financial support from the European Commission's Next Generation Internet program. Learn more at the NLnet project page.

NLnet foundation logo NGI Zero Logo

cdxgen is an OWASP Foundation production project.



cdxgen badge
Copy the below block to your markdown files to show your ❤️ for cdxgen.

![SBOM](https://github.com/cdxgen/cdxgen)
About
Creates CycloneDX Bill of Materials (BOM) for your projects from source and container images. Supports many languages and package managers. Integrate in your CI/CD pipeline with automatic submission to Dependency Track server

cdxgen.github.io/cdxgen/
Topics
docker containers supply-chain owasp bom oci spdx sca software-bill-of-materials purl package-url sbom cyclonedx saasbom spdx-sbom cbom
Resources
 Readme
License
 Apache-2.0 license
Security policy
 Security policy
 Activity
 Custom properties
Stars
 961 stars
Watchers
 12 watching
Forks
 246 forks
Report repository
Releases 393
Release v12.3.3
Latest
last week
+ 392 releases
Sponsor this project
https://owasp.org/donate/?reponame=www-project-cdxgen&title=OWASP+cdxgen
Packages
127
cdxgen-python312
cdxgen-java11
cdxgen-python313
+ 124 packages
Contributors
114
@renovate[bot]
@prabhu
@malice00
@github-actions[bot]
@setchy
@Copilot
@aryan-rajoria
@cerrussell
@bandhan-majumder
@Copilot
@ajmalab
@marob
@Nikemare
@sebastianvoss
+ 100 contributors
Languages
JavaScript
95.8%
 
CMake
1.3%
 
Shell
1.0%
 
Python
0.9%
 
Ruby
0.4%
 
Dockerfile
0.2%
 
Other
0.4%
Footer
© 2026 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Community
Docs
Contact
Manage cookies
Do not share my personal information"

i have cloned both trivy and cdxgen into the SSC directory as well

Show less
12 May, 17:39

Worked for 9m 6s
I’ve read the whole advisor chat and inspected the SSC folder. No files edited.

Key Findings

trivy generates metadata.timestamp, but not metadata.supplier or metadata.authors. Supplier is only mapped at component level when package maintainer data exists. See marshal.go (line 92) and encode.go (line 470).

trivy builds dependency graphs from package DependsOn data and emits empty dependency entries for leaf nodes, but the code itself notes ambiguity between “no dependencies” and “graph unsupported”. This is strong evidence for the paper. See encode.go (line 221).

trivy does not populate CycloneDX scope. Instead, it filters dev dependencies by default unless --include-dev-deps is passed. See service.go (line 452).

cdxgen generates metadata.timestamp and metadata.authors, with default author OWASP Foundation, but leaves metadata.supplier undefined. See index.js (line 487) and index.js (line 537).

cdxgen has explicit implementation logic for scope. It can mark packages required, optional, or excluded depending on ecosystem evidence, source usage analysis, dependency tree propagation, and flags like --required-only. See utils.js (line 21904), index.js (line 1033), and utils.js (line 6264).

cdxgen handles completeness better than Trivy when filtering. If --required-only filters the SBOM, it automatically adds compositions.aggregate = incomplete unless disabled. See cdxgen.js (line 234) and postgen.js (line 965).

Useful Paper Angle
This gives us a concrete implementation claim:

trivy treats scope mostly as a pre-output filtering problem, while cdxgen treats scope as an SBOM field that can be inferred and propagated. Both can emit schema-valid CycloneDX SBOMs, but they encode different assumptions about dependency relevance, provenance, and completeness.

Also note: installed CLI versions are trivy 0.68.2 and cdxgen 12.0.0, while the cloned repos are newer snapshots. If we run experiments, we should record exact versions.

12 May, 17:48
give evidences from the cloned repos and give me more writeups in the sense i dont understand your summary pointers, i want proper motivation, what u did, how u did, what/how did u inspect, why it matters for us, what did u find out and why does it happen, and hows it important for us and what to tell advisors, like very detailed so that i can discuss w dr mohannad
12 May, 17:50
I inspected the cloned trivy and cdxgen repositories directly, not just their README/docs. The goal was to answer Dr. Mohannad’s concern: instead of saying “CycloneDX leaves fields optional” at a specification level, we need evidence showing how real generators actually populate those fields differently.

What I Did
I inspected the generator code paths that produce CycloneDX output for the fields your advisor specifically cared about:

Dependency graphs: how dependencies and dependsOn are created.
Provenance fields: metadata.timestamp, metadata.authors, metadata.supplier, component supplier.
Scope fields: how scope = required, optional, or missing is determined.
Completeness fields: whether tools use compositions to say the SBOM is complete or incomplete.
VEX and vulnerability context: whether vulnerability analysis is emitted or only consumed.
I also checked the existing experiment folder in your repo. You already have generated SBOMs for trivy, cdxgen, and syft under cyclonedx/sbom_testing (line 4), and your script runs trivy fs ... --format cyclonedx and cdxgen -o ... on five projects.

Repository Evidence
The cloned repo commits I inspected are:

trivy: b08bf6a0a
cdxgen: 4d233a5b
Your installed CLI versions are older:

trivy: 0.68.2
cdxgen: 12.0.0
That matters because if we report empirical output, we should report the CLI versions. If we report source-code analysis, we should report the cloned commit hashes.

Main Finding
The important result is this:

trivy and cdxgen both emit CycloneDX SBOMs, but they treat key CycloneDX concepts differently. This is exactly the implementation-level evidence we need. The inconsistency is not only because the tools are “buggy” or incomplete. It happens because CycloneDX allows many fields to be optional, and each generator makes different choices about how to infer, omit, filter, or enrich those fields.

Trivy
Trivy’s CycloneDX output is generated through a scanner-first pipeline. It scans packages, converts them into an internal BOM model, then marshals that internal BOM into CycloneDX.

The CycloneDX marshaler creates the metadata block here: marshal.go (line 92). It always sets metadata.timestamp, and it records Trivy itself under metadata.tools.components. However, this metadata block does not set metadata.supplier or metadata.authors.

That matters because CISA expects supplier, author, and timestamp as minimum elements. Trivy satisfies timestamp, but not metadata supplier or author. This supports the claim that a valid CycloneDX SBOM can still miss policy-relevant provenance fields.

For component supplier, Trivy maps internal package supplier data into CycloneDX here: marshal.go (line 119). The actual supplier conversion happens here: marshal.go (line 258). If supplier is empty, it returns nil. The supplier source is package maintainer data: encode.go (line 470).

So Trivy’s behavior is: metadata supplier is not populated, component supplier appears only when package maintainer metadata exists.

For dependency graphs, Trivy builds relationships from package DependsOn data. The key code is here: encode.go (line 221). It adds package-to-package relationships from pkg.DependsOn: encode.go (line 273). Then it adds empty dependency entries for packages with no dependencies: encode.go (line 282).

The most useful evidence is the TODO comment in Trivy’s own code: it says the tool should check whether the component actually has no dependencies or whether the dependency graph is unsupported. This is very important for your paper because it directly supports the “completeness ambiguity” point. An empty dependency entry can mean either “this package has no dependencies” or “the tool does not know the dependencies.”

For scope, Trivy does not appear to emit CycloneDX component scope. Its internal component model has supplier, licenses, PURL, files, and properties, but no scope field: bom.go (line 145). Instead, Trivy handles development dependencies before SBOM generation by filtering them out by default: service.go (line 452). The flag is --include-dev-deps, supported for npm, yarn, and gradle: package_flags.go (line 10).

So Trivy’s behavior is: it treats dev dependencies mainly as a filtering decision, not as CycloneDX scope metadata.

That matters because a consumer cannot inspect the SBOM and know whether omitted dev dependencies existed, unless the generation command is known. This is exactly the gap between “representation” and “population semantics.”

Trivy also supports VEX, but mainly as an input/filtering mechanism. It filters vulnerabilities based on VEX sources here: filter.go (line 51). It can parse CycloneDX VEX analysis here: cyclonedx.go (line 25). But the CycloneDX marshaler emits vulnerabilities as affected findings, not rich VEX-style analysis statements by default: marshal.go (line 427).

So Trivy can consume VEX, but its normal SBOM output should not be treated as a full VEX-rich CycloneDX document.

cdxgen
cdxgen is different. It is not only a scanner. It is a CycloneDX-first generator with enrichment, validation, signing, formulation, audit, and conversion features.

cdxgen creates authors here: index.js (line 487). The CLI default author is OWASP Foundation: cdxgen.js (line 337). It creates the metadata object here: index.js (line 537). It sets timestamp, tools, authors, and sets supplier: undefined.

So cdxgen’s behavior is: timestamp and authors are populated, but metadata supplier is still missing by default.

This matters because it shows that even a CycloneDX-native tool with strong SBOM features still does not necessarily satisfy CISA provenance expectations by default.

For dependency graphs, cdxgen assembles the final CycloneDX JSON here: index.js (line 1338). The final object includes components and dependencies: index.js (line 1375). It merges dependency arrays from different parsers using mergeDependencies: depsUtils.js (line 14).

This means cdxgen’s dependency graph depends heavily on parser-specific data. For some ecosystems it can produce a graph; for others it may emit few or no dependency edges. This matches your existing results: some cdxgen SBOMs had many components but zero dependency graph entries.

For scope, cdxgen is much more explicit than Trivy. It has many ecosystem-specific rules. It maps imported packages to required and non-imported packages to optional here: index.js (line 1033). For Python, it marks imported modules as required during deeper analysis: index.js (line 4525). For Go, it can use go mod why to detect required packages: index.js (line 4785). For Maven, it maps compile and runtime to required, test to optional, and provided to excluded: utils.js (line 6264).

cdxgen also recomputes scope from the dependency tree: utils.js (line 21904). If a package is required, its dependencies are marked required as well. If packages are not required and have no scope, they may become optional.

This is important because cdxgen is making an actual semantic judgment about runtime or production relevance. Trivy avoids this by filtering dev dependencies before output. cdxgen tries to encode this judgment inside the SBOM.

For completeness, cdxgen has a very useful mechanism. The --required-only flag keeps only required packages and says this will set compositions.aggregate to incomplete unless disabled: cdxgen.js (line 234). The actual post-processing code adds compositions with aggregate: incomplete: postgen.js (line 965).

This is a strong contrast with Trivy. cdxgen sometimes explicitly admits that a filtered SBOM is incomplete. Trivy filters dev dependencies by default, but I did not find equivalent automatic compositions.aggregate = incomplete behavior.

For formulation, cdxgen supports it, but it is off by default. The flag is here: cdxgen.js (line 406). The formulation section is applied during post-processing only if includeFormulation is enabled: postgen.js (line 71). This supports your earlier claim that build provenance exists in CycloneDX tooling, but remains opt-in.

Why This Happens
This happens because the CycloneDX standard gives tools a vocabulary, but it does not fully prescribe how tools must populate that vocabulary.

For example, CycloneDX has fields for authors, supplier, scope, dependencies, compositions, formulation, and vulnerability analysis. But the standard generally does not force every generator to populate them. So each tool chooses its own operational policy.

Trivy’s policy seems to be: scan accurately, filter dev dependencies by default, produce a clean vulnerability/SBOM output, and avoid making too many extra semantic claims.

cdxgen’s policy seems to be: generate a richer CycloneDX-native document, infer scope where possible, support evidence and formulation, and sometimes mark incompleteness when filtering changes the SBOM.

Neither approach is “wrong.” But they produce different SBOMs from the same project, and both can still be valid CycloneDX. That is the important research point.

Why This Matters For The Paper
This directly responds to Dr. Mohannad’s criticism that the previous section felt ad hoc.

Previously, the writeup mostly said: CycloneDX has optional fields, so tools may omit them.

Now we can say something stronger:

We inspected the implementation logic of two generators and found that generator behavior differs at the point where abstract CycloneDX fields must be populated. Trivy treats development dependencies as a pre-output filtering issue and does not emit scope, while cdxgen computes and propagates scope into the SBOM. Trivy emits empty dependency nodes but acknowledges ambiguity between true leaf nodes and unsupported graphs, while cdxgen merges parser-specific dependency graphs and can mark filtered SBOMs as incomplete through compositions. These differences show that SBOM inconsistency is not only a validation problem. It is also a population semantics problem.

That sentence is probably the core of what you should explain to Dr. Mohannad.

How To Frame This In Discussion
You can say:

“I agree the earlier Section 4.2.3 was too specification-level and looked ad hoc. I started looking at generator implementations directly. For now I inspected Trivy and cdxgen. The main finding is that the inconsistency is not only caused by missing schema validation. The tools make different implementation choices about how to populate the same CycloneDX concepts.”

Then explain:

“Trivy does not emit component scope. It filters dev dependencies before SBOM emission unless --include-dev-deps is passed. cdxgen, in contrast, computes scope inside the SBOM using ecosystem-specific rules, source/import analysis, dependency propagation, and flags like --required-only.”

Then explain:

“For dependency graphs, Trivy emits empty dependency entries for leaf nodes, but the source code itself has a TODO saying it should distinguish actual no-dependency cases from unsupported dependency graphs. That is direct evidence for the ambiguity around completeness. cdxgen merges parser-specific dependency graphs, but graph availability still depends on ecosystem and parser support.”

Then explain:

“For provenance, both tools generate timestamps, but neither sets metadata supplier by default. cdxgen sets authors by default to OWASP Foundation, while Trivy does not set metadata authors. So even mature tools can produce valid CycloneDX documents that miss CISA-relevant provenance fields.”

Message To Send Advisors
You can send this:

Hello Dr. Mohannad,

I started the implementation-level analysis of SBOM generators, beginning with Trivy and cdxgen. The main finding so far is that the inconsistency is not only a schema or specification issue, but also a population semantics issue.

For example, Trivy filters development dependencies before SBOM generation and does not appear to emit CycloneDX component scope, while cdxgen computes and propagates scope using ecosystem-specific rules, source/import analysis, and dependency graph information. For dependency graphs, Trivy emits empty dependency entries for components without dependencies, but its own source code notes the ambiguity between a true leaf node and an unsupported dependency graph. cdxgen can mark filtered SBOMs as incomplete through compositions when using required-only mode, but this behavior is tool-specific rather than guaranteed by CycloneDX.

I also checked provenance fields. Both tools generate timestamps, but neither sets metadata.supplier by default. cdxgen sets metadata.authors by default, while Trivy does not. This gives us concrete evidence that valid CycloneDX SBOMs can still differ in CISA-relevant provenance and completeness fields depending on generator implementation choices.

Next, I plan to extend this same inspection to the other generators and then compare these findings against sbomqs and jbomaudit to see which of these implementation-level issues quality tools can actually detect.
My Recommendation
For the next step, we should turn this into a small table for the paper:

Field	Trivy behavior	cdxgen behavior	Why it matters
metadata.timestamp	Populated	Populated	Both satisfy timestamp
metadata.authors	Not populated	Default author populated	CISA author differs by tool
metadata.supplier	Not populated	Undefined by default	CISA supplier gap remains
scope	Not emitted, dev deps filtered	Inferred and emitted in some paths	Different production semantics
dependencies	Built from DependsOn, empty nodes emitted	Merged from parser-specific dependency lists	Completeness depends on parser support
compositions	Not found as automatic completeness claim	Set to incomplete when filtered	Completeness claims are tool-specific
formulation	Not a normal SBOM output feature found here	Supported but opt-in	Build provenance remains optional
This would make the advisor discussion much more concrete and much less “narrative.”

12 May, 17:53
i can barely map out your text with the code youre referencing. a better way to explain everything would be to:
- explain me everything around both trivy and cdxgen repos, how theyre structured etc everything
- for all of your points, reiterate them in detail and give all code citaations directly in output instead of only citing/referencing them, and give code outputs in details and evertyhting explained since i dont know go
12 May, 20:14
I’ll make this more “walk me through the codebase like I’m new to it” instead of dropping conclusions. I’m going to pull the repo structure and the exact code blocks behind each claim, then I’ll translate the Go and JavaScript into plain English.

12 May, 20:24
i can barely map out your text with the code youre referencing. a better way to explain everything would be to:
- explain me everything around both trivy and cdxgen repos, how theyre structured etc everything
- for all of your points, reiterate them in detail and give all code citaations directly in output instead of only citing/referencing them, and give code outputs in details and evertyhting explained since i dont know go
12 May, 20:24

Worked for 7m 56s
Below is the detailed version you wanted. I’ll explain this like we are preparing you to discuss it with Dr. Mohannad, not like I’m just dumping repo links.

Big Picture
What we are trying to prove is not just “CycloneDX has optional fields.” That is too specification-level and your advisor already pushed back on that.

The better claim is:

Different SBOM generators make different implementation choices when they populate the same CycloneDX fields. These choices affect dependency graphs, provenance, scope, completeness, and VEX/vulnerability context. Therefore, SBOM inconsistency is partly a generator implementation problem, not only a schema/specification problem.

For now, I inspected two cloned repos:

trivy: /Users/abdullahsohail/LUMS/SSC/trivy

cdxgen: /Users/abdullahsohail/LUMS/SSC/cdxgen

The cloned commits were:

trivy: b08bf6a0a

cdxgen: 4d233a5b

Your installed CLI versions are older:

trivy --version: 0.68.2

cdxgen --version: 12.0.0

So if we write about source code, cite the commit hashes. If we write about generated output, cite the CLI versions.

How Trivy Is Structured
Trivy is written in Go. Its repo is much larger than just SBOM generation because Trivy scans vulnerabilities, secrets, IaC, containers, Kubernetes, filesystems, and more.

The important directories for us are:

trivy/cmd/trivy
CLI entrypoint.

trivy/pkg/flag
CLI flags such as --include-dev-deps.

trivy/pkg/scan
Scanning pipeline. This is where packages are filtered before output.

trivy/pkg/fanal
Low-level artifact analysis. This is where package evidence comes from.

trivy/pkg/sbom/core
Trivy's internal SBOM model.

trivy/pkg/sbom/io
Converts a scan report into Trivy's internal SBOM model.

trivy/pkg/sbom/cyclonedx
Converts Trivy's internal SBOM model into CycloneDX JSON.

trivy/pkg/result
Filters scan results, including VEX-based filtering.

trivy/pkg/vex
VEX support, including reading OpenVEX and CycloneDX VEX.
The main Trivy SBOM flow is:

scan target
-> produce Trivy report
-> encode report into Trivy internal core.BOM
-> marshal core.BOM into CycloneDX BOM
The most important files are:

/Users/abdullahsohail/LUMS/SSC/trivy/pkg/sbom/io/encode.go
This builds Trivy's internal SBOM graph from scan results.

/Users/abdullahsohail/LUMS/SSC/trivy/pkg/sbom/core/bom.go
This defines Trivy's internal component and relationship model.

/Users/abdullahsohail/LUMS/SSC/trivy/pkg/sbom/cyclonedx/marshal.go
This writes CycloneDX metadata, components, dependencies, and vulnerabilities.
In Go, a line like this:

func (m *Marshaler) Metadata(ctx context.Context) *cdx.Metadata
means:

func: defines a function.

(m *Marshaler): this function belongs to a Marshaler object.

Metadata: function name.

ctx context.Context: input argument.

*cdx.Metadata: returns a pointer to a CycloneDX metadata object.

So this is basically “method Metadata on the CycloneDX marshaler.”

Trivy Finding 1: Metadata Timestamp Is Present, But Metadata Supplier And Authors Are Missing
The exact CycloneDX marshaling function is here:

marshal.go (line 68)

Code excerpt:

68  // Marshal converts the Trivy component to the CycloneDX format
69  func (m *Marshaler) Marshal(ctx context.Context, bom *core.BOM) (*cdx.BOM, error) {
70      m.bom = bom
71      m.componentIDs = make(map[uuid.UUID]string, len(m.bom.Components()))
72  
73      cdxBOM := cdx.NewBOM()
74      cdxBOM.SerialNumber = uuid.New().URN()
75      cdxBOM.Metadata = m.Metadata(ctx)
76  
77      var err error
78      if cdxBOM.Metadata.Component, err = m.MarshalRoot(); err != nil {
79          return nil, xerrors.Errorf("failed to marshal component: %w", err)
80      }
81  
82      if cdxBOM.Components, err = m.marshalComponents(); err != nil {
83          return nil, xerrors.Errorf("failed to marshal components: %w", err)
84      }
85  
86      cdxBOM.Dependencies = m.marshalDependencies()
87      cdxBOM.Vulnerabilities = m.marshalVulnerabilities()
88  
89      return cdxBOM, nil
90  }
Plain English:

This function creates the CycloneDX BOM.

It sets:

serialNumber

metadata

metadata.component

components

dependencies

vulnerabilities

So this is the final CycloneDX output assembly point.

Now look at the metadata function:

marshal.go (line 92)

92  func (m *Marshaler) Metadata(ctx context.Context) *cdx.Metadata {
93      return &cdx.Metadata{
94          Timestamp: clock.Now(ctx).UTC().Format(timeLayout),
95          Tools: &cdx.ToolsChoice{
96              Components: &[]cdx.Component{
97                  {
98                      Type:         cdx.ComponentTypeApplication,
99                      Group:        ToolVendor,
100                     Name:         ToolName,
101                     Version:      m.appVersion,
102                     Manufacturer: &cdx.OrganizationalEntity{Name: ToolManufacturer},
103                 },
104             },
105         },
106     }
107 }
Plain English:

This returns the CycloneDX metadata object.

It includes:

Timestamp: current time.

Tools: Trivy as the tool that generated the SBOM.

Inside Tools, Trivy records:

tool type = application

tool group/vendor

tool name

tool version

tool manufacturer

But there is no:

Authors

Supplier

That means Trivy-generated CycloneDX SBOMs can include metadata.timestamp, but not metadata.authors or metadata.supplier.

Why this matters:

CISA minimum elements expect supplier, author, and timestamp. Trivy handles timestamp but does not set metadata supplier/authors in this code path. This is a concrete generator-level reason why valid CycloneDX output can still miss minimum provenance fields.

Trivy Finding 2: Component Supplier Comes From Package Maintainer, Not Metadata Supplier
Trivy does populate component-level supplier if it has package maintainer data.

Code excerpt:

marshal.go (line 119)

119 func (m *Marshaler) MarshalComponent(component *core.Component) (*cdx.Component, error) {
120     componentType, err := m.componentType(component.Type)
121     if err != nil {
122         return nil, xerrors.Errorf("failed to get cdx component type: %w", err)
123     }
124 
125     cdxComponent := &cdx.Component{
126         BOMRef:     component.PkgIdentifier.BOMRef,
127         Type:       componentType,
128         Name:       component.Name,
129         Group:      component.Group,
130         Version:    component.Version,
131         PackageURL: m.PackageURL(component.PkgIdentifier.PURL),
132         Supplier:   m.Supplier(component.Supplier),
133         Hashes:     m.Hashes(component.Files),
134         Licenses:   m.Licenses(component.Licenses),
135         Properties: m.Properties(component.Properties),
136     }
137     m.componentIDs[component.ID()] = cdxComponent.BOMRef
138 
139     return cdxComponent, nil
140 }
Plain English:

Every Trivy internal component is converted into a CycloneDX component.

The CycloneDX component gets:

BOM reference

type

name

group

version

PURL

supplier

hashes

licenses

properties

The supplier value comes from component.Supplier.

Now look at how supplier is converted:

marshal.go (line 258)

258 func (*Marshaler) Supplier(supplier string) *cdx.OrganizationalEntity {
259     if supplier == "" {
260         return nil
261     }
262     return &cdx.OrganizationalEntity{
263         Name: supplier,
264     }
265 }
Plain English:

If supplier is an empty string, Trivy emits no supplier.

If supplier exists, Trivy writes it as a CycloneDX organization with a name.

Where does this supplier value come from?

encode.go (line 470)

470 return &core.Component{
471     Type:       core.TypeLibrary,
472     Name:       name,
473     Group:      group,
474     Version:    version,
475     SrcName:    pkg.SrcName,
476     SrcVersion: utils.FormatSrcVersion(pkg),
477     SrcFile:    srcFile,
478     PkgIdentifier: ftypes.PkgIdentifier{
479         UID:    pkg.Identifier.UID,
480         PURL:   pkg.Identifier.PURL,
481         BOMRef: pkg.Identifier.BOMRef,
482     },
483     Supplier:   pkg.Maintainer,
484     Licenses:   pkg.Licenses,
485     Files:      files,
486     Properties: filterProperties(properties),
487 }
Plain English:

When Trivy creates its internal component, it sets:

Supplier: pkg.Maintainer

So Trivy’s component supplier is basically package maintainer metadata, if available.

Important distinction:

metadata.supplier tells us who supplied the SBOM/product.

component.supplier tells us who supplied an individual dependency/package.

Trivy may populate component supplier, but the metadata supplier is still absent.

Why this matters:

If a policy tool checks only metadata.supplier, Trivy may fail CISA-like provenance checks even if some individual components have supplier data.

Trivy Finding 3: Dependency Graph Is Built From Package DependsOn
The dependency graph starts in:

encode.go (line 182)

182 func (e *Encoder) encodeResult(root *core.Component, metadata types.Metadata, result types.Result) {
183     if slices.Contains(ftypes.AggregatingTypes, result.Type) {
184         // If a package is language-specific package that isn't associated with a lock file,
185         // it will be a dependency of a component under "metadata".
186         // e.g.
187         //   Container component (alpine:3.15) ----------------------- #1
188         //     -> Library component (npm package, express-4.17.3) ---- #2
189         //     -> Library component (python package, django-4.0.2) --- #2
190         //     -> etc.
191         // ref. https://cyclonedx.org/use-cases/#inventory
192 
193         // Dependency graph from #1 to #2
194         e.encodePackages(root, result)
195     } else if result.Class == types.ClassOSPkg || result.Class == types.ClassLangPkg {
196         // If a package is OS package, it will be a dependency of "Operating System" component.
197         // e.g.
198         //   Container component (alpine:3.15) --------------------- #1
199         //     -> Operating System Component (Alpine Linux 3.15) --- #2
200         //       -> Library component (bash-4.12) ------------------ #3
201         //       -> Library component (vim-8.2)   ------------------ #3
202         //       -> etc.
203         //
204         // Else if a package is language-specific package associated with a lock file,
205         // it will be a dependency of "Application" component.
206         // e.g.
207         //   Container component (alpine:3.15) ------------------------ #1
208         //     -> Application component (/app/package-lock.json) ------ #2
209         //       -> Library component (npm package, express-4.17.3) --- #3
210         //       -> Library component (npm package, lodash-4.17.21) --- #3
211         //       -> etc.
212 
213         // #2
214         appComponent := e.resultComponent(root, result, metadata.OS)
215 
216         // #3
217         e.encodePackages(appComponent, result)
218     }
219 }
Plain English:

Trivy distinguishes different scan result types.

If packages are general aggregated packages, it attaches them to the root component.

If packages are OS packages or language packages, it creates an intermediate component, such as:

container image

operating system component

application component

library dependencies

This is Trivy’s internal model before CycloneDX output.

Now the actual dependency edges are built here:

encode.go (line 221)

221 func (e *Encoder) encodePackages(parent *core.Component, result types.Result) {
222     // Get dependency parents first
223     parents := ftypes.Packages(result.Packages).ParentDeps()
224 
225     // Group vulnerabilities by package ID
226     vulns := make(map[string][]core.Vulnerability)
227     for _, vuln := range result.Vulnerabilities {
228         v := e.vulnerability(vuln)
229         vulns[vuln.PkgIdentifier.UID] = append(vulns[vuln.PkgIdentifier.UID], v)
230     }
231 
232     // UID => Package Component
233     components := make(map[string]*core.Component, len(result.Packages))
234     // PkgID => Package Component
235     dependencies := make(map[string]*core.Component, len(result.Packages))
236     var hasRoot bool
237     for i, pkg := range result.Packages {
238         pkgID := lo.Ternary(pkg.ID == "", fmt.Sprintf("%s@%s", pkg.Name, pkg.Version), pkg.ID)
239         result.Packages[i].ID = pkgID
240 
241         // Check if the project has a root dependency
242         // TODO: Ideally, all projects should have a root dependency.
243         if pkg.Relationship == ftypes.RelationshipRoot {
244             hasRoot = true
245         }
246 
247         // Convert packages to components
248         c := e.component(result, pkg)
249         components[pkg.Identifier.UID] = c
250 
251         // For dependencies: the key "pkgID" might be duplicated in aggregated packages,
252         // but it doesn't matter as they don't have "DependsOn".
253         dependencies[pkgID] = c
254 
255         // Add a component
256         e.bom.AddComponent(c)
257 
258         // Add vulnerabilities
259         if vv := vulns[pkg.Identifier.UID]; vv != nil {
260             e.bom.AddVulnerabilities(c, vv)
261         }
262     }
263 
264     // Build a dependency graph between packages
265     for _, pkg := range result.Packages {
266         c := components[pkg.Identifier.UID]
267 
268         // Add a relationship between the parent and the package if needed
269         if e.belongToParent(pkg, parents, hasRoot) {
270             e.bom.AddRelationship(parent, c, core.RelationshipContains)
271         }
272 
273         // Add relationships between the package and its dependencies
274         for _, dep := range pkg.DependsOn {
275             dependsOn, ok := dependencies[dep]
276             if !ok {
277                 continue
278             }
279             e.bom.AddRelationship(c, dependsOn, core.RelationshipDependsOn)
280         }
281 
282         // Components that do not have their own dependencies MUST be declared as empty elements within the graph.
283         // TODO: Should check if the component has actually no dependencies or the dependency graph is not supported.
284         if len(pkg.DependsOn) == 0 {
285             e.bom.AddRelationship(c, nil, "")
286         }
Plain English:

First loop:

Trivy converts each package into an internal component.

It stores those components in maps so it can find them later.

Second loop:

For each package, Trivy checks pkg.DependsOn.

For every dependency listed in pkg.DependsOn, it creates a relationship:

current package depends on dependency package.

If pkg.DependsOn is empty, Trivy adds an empty dependency entry.

The crucial line is the TODO:

// TODO: Should check if the component has actually no dependencies or the dependency graph is not supported.
This is extremely important.

It means Trivy’s own source code acknowledges an ambiguity:

Empty dependency list could mean “this package truly has no dependencies.”

Empty dependency list could also mean “the dependency graph was not supported or not discovered.”

Why this matters:

This is direct implementation evidence for your “completeness ambiguity” argument. CycloneDX allows an empty dependency entry, but the generator may not know whether it is representing a real leaf node or missing graph knowledge.

Trivy Finding 4: Internal Relationships Are Later Converted Into CycloneDX dependencies
After Trivy builds internal relationships, it converts them into CycloneDX dependencies.

marshal.go (line 167)

167 func (m *Marshaler) marshalDependencies() *[]cdx.Dependency {
168     var dependencies []cdx.Dependency
169     for key, rels := range m.bom.Relationships() {
170         ref, ok := m.componentIDs[key]
171         if !ok {
172             continue
173         }
174 
175         deps := lo.FilterMap(rels, func(rel core.Relationship, _ int) (string, bool) {
176             d, ok := m.componentIDs[rel.Dependency]
177             return d, ok
178         })
179         sort.Strings(deps)
180 
181         dependencies = append(dependencies, cdx.Dependency{
182             Ref:          ref,
183             Dependencies: &deps,
184         })
185     }
Plain English:

Trivy loops over all internal relationships.

For each component, it finds its CycloneDX bom-ref.

It collects the dependency bom-refs.

Then it emits a CycloneDX object like:

{
  "ref": "pkg:npm/foo@1.0.0",
  "dependsOn": ["pkg:npm/bar@2.0.0"]
}
In Go, Dependencies: &deps means “set CycloneDX dependsOn to the list named deps.”

Why this matters:

Trivy’s CycloneDX graph is downstream of its internal package relationship discovery. If pkg.DependsOn is incomplete, CycloneDX output will be incomplete too. The CycloneDX schema cannot tell whether the graph was complete.

Trivy Finding 5: Scope Is Not Emitted As CycloneDX scope
The internal Trivy component model is here:

bom.go (line 145)

145     // SPDX: package.licenseConcluded, package.licenseDeclared
146     Licenses []string
147 
148     // PkgIdentifier has PURL and BOMRef for the component
149     // PURL:
150     //   CycloneDX: component.purl
151     //   SPDX: package.externalRefs.referenceLocator
152     // BOMRef:
153     //   CycloneDX: component.bom-ref
154     //   SPDX: N/A
155     PkgIdentifier ftypes.PkgIdentifier
156 
157     // Supplier is the name of the supplier of the component
158     // CycloneDX: component.supplier
159     // SPDX: package.supplier
160     Supplier string
Plain English:

This is part of Trivy’s internal component structure.

It has:

licenses

PURL/BOM reference

supplier

But in the inspected section, there is no component Scope field.

Then, when Trivy creates CycloneDX components, it sets name, version, PURL, supplier, hashes, licenses, and properties:

marshal.go (line 125)

125     cdxComponent := &cdx.Component{
126         BOMRef:     component.PkgIdentifier.BOMRef,
127         Type:       componentType,
128         Name:       component.Name,
129         Group:      component.Group,
130         Version:    component.Version,
131         PackageURL: m.PackageURL(component.PkgIdentifier.PURL),
132         Supplier:   m.Supplier(component.Supplier),
133         Hashes:     m.Hashes(component.Files),
134         Licenses:   m.Licenses(component.Licenses),
135         Properties: m.Properties(component.Properties),
136     }
Again, no Scope.

Instead, Trivy handles development dependencies earlier by filtering them out.

service.go (line 452)

452 func excludePackages(target *types.ScanTarget, options types.ScanOptions) {
453     // Filter packages by relationship
454     filterPkgByRelationship(target, options)
455 
456     // By default, development packages are removed from the result
457     // '--include-dev-deps' option allows including them
458     excludeDevDeps(target.Applications, options.IncludeDevDeps)
459 }
And here is the filtering logic:

service.go (line 478)

478 // excludeDevDeps removes development dependencies from the list of applications
479 func excludeDevDeps(apps []ftypes.Application, include bool) {
480     if include {
481         return
482     }
483 
484     onceInfo := sync.OnceFunc(func() {
485         log.Info("Suppressing dependencies for development and testing. To display them, try the '--include-dev-deps' flag.")
486     })
487 
488     for i := range apps {
489         devDeps := set.New[string]()
490         apps[i].Packages = lo.Filter(apps[i].Packages, func(pkg ftypes.Package, _ int) bool {
491             if pkg.Dev {
492                 onceInfo()
493                 devDeps.Append(pkg.ID)
494             }
495             return !pkg.Dev
496         })
497 
498         // Remove development dependencies from dependencies of root and workspace packages
499         for j, pkg := range apps[i].Packages {
500             if pkg.Relationship != ftypes.RelationshipRoot && pkg.Relationship != ftypes.RelationshipWorkspace {
501                 continue
502             }
503             apps[i].Packages[j].DependsOn = lo.Filter(apps[i].Packages[j].DependsOn, func(dep string, _ int) bool {
504                 return !devDeps.Contains(dep)
505             })
Plain English:

By default, Trivy removes development dependencies before output.

If the user passes --include-dev-deps, then Trivy keeps them.

The flag definition says:

package_flags.go (line 10)

10  IncludeDevDepsFlag = Flag[bool]{
11      Name:          "include-dev-deps",
12      ConfigName:    "pkg.include-dev-deps",
13      Usage:         "include development dependencies in the report (supported: npm, yarn, gradle)",
14      TelemetrySafe: true,
15  }
Why this matters:

Trivy treats development dependency relevance as a generation-time filtering decision.

It does not preserve that decision as CycloneDX scope.

So a consumer who only sees the final SBOM cannot easily know whether dev dependencies were absent because they do not exist, or because Trivy filtered them.

This is exactly the “population semantics” issue.

How cdxgen Is Structured
cdxgen is written in JavaScript.

Important directories:

cdxgen/bin
CLI entrypoints. Main CLI file is bin/cdxgen.js.

cdxgen/lib/cli
Main BOM generation logic. Important file: lib/cli/index.js.

cdxgen/lib/helpers
Large helper library. This includes ecosystem parsers, PURL logic, scope logic, dependency utilities.

cdxgen/lib/stages/postgen
Post-generation processing. This is where cdxgen adds formulation, annotations, compositions, metadata enrichment, etc.

cdxgen/lib/validator
Validation and compliance checks.

cdxgen/lib/audit
cdx-audit logic.

cdxgen/lib/evinser
Evidence and enrichment logic.
The cdxgen flow is roughly:

read CLI options
-> detect project type
-> parse manifests / lockfiles / source evidence
-> create components and dependency arrays
-> build CycloneDX JSON
-> post-process BOM
-> optionally add formulation, annotations, compositions, signatures, validation, audit data
The important files are:

/Users/abdullahsohail/LUMS/SSC/cdxgen/bin/cdxgen.js
Defines CLI flags such as --author, --required-only, --include-formulation, --no-babel.

/Users/abdullahsohail/LUMS/SSC/cdxgen/lib/cli/index.js
Builds the actual CycloneDX JSON.

/Users/abdullahsohail/LUMS/SSC/cdxgen/lib/helpers/utils.js
Contains many ecosystem-specific parsers and scope rules.

/Users/abdullahsohail/LUMS/SSC/cdxgen/lib/helpers/depsUtils.js
Merges dependency graphs.

/Users/abdullahsohail/LUMS/SSC/cdxgen/lib/stages/postgen/postgen.js
Adds post-generation sections such as formulation and compositions.
cdxgen Finding 1: Metadata Timestamp And Authors Are Populated, But Supplier Is Undefined
The author option is defined in the CLI:

cdxgen.js (line 337)

337   .option("author", {
338     description:
339       "The person(s) who created the BOM. Set this value if you're intending the modify the BOM and claim authorship.",
340     default: "OWASP Foundation",
341   })
Plain English:

If the user does not provide an author, cdxgen uses OWASP Foundation.

Now look at how authors are inserted:

index.js (line 487)

487 const addAuthorsSection = (options) => {
488   const authors = [];
489   if (options.author) {
490     const oauthors = Array.isArray(options.author)
491       ? options.author
492       : [options.author];
493     for (const aauthor of oauthors) {
494       if (aauthor.trim().length < 2) {
495         continue;
496       }
497       authors.push({ name: aauthor });
498     }
499   }
500   return authors;
501 };
Plain English:

cdxgen checks options.author.

If it exists, it turns it into an array.

For every author string, it creates:

{ "name": "author name" }
So cdxgen actively populates metadata.authors.

Now look at the metadata object:

index.js (line 537)

537 function addMetadata(parentComponent = {}, options = {}, context = {}) {
538   // DO NOT fork this project to just change the vendor or author's name
539   // Try to contribute to this project by sending PR or filing issues
540   const tools = addToolsSection(options, context);
541   const authors = addAuthorsSection(options);
542   const lifecycles =
543     options.specVersion >= 1.5 ? addLifecyclesSection(options) : undefined;
544   const metadata = {
545     timestamp: getTimestamp(),
546     tools,
547     authors,
548     supplier: undefined,
549   };
550   if (lifecycles) {
551     metadata.lifecycles = lifecycles;
552   }
Plain English:

cdxgen creates metadata with:

timestamp

tools

authors

supplier: undefined

This is very clear evidence.

cdxgen populates timestamp and authors, but supplier is explicitly undefined by default.

Why this matters:

cdxgen is a CycloneDX-native generator, yet even it does not populate metadata.supplier by default. So the supplier gap is not just a Trivy issue.

This supports the paper claim that CISA-relevant provenance depends on generator policy, not just CycloneDX schema validity.

cdxgen Finding 2: It Builds The Final CycloneDX JSON In One Central Place
The final BOM construction is here:

index.js (line 1338)

1338 const buildBomNSData = (options, pkgInfo, ptype, context) => {
1339   // Many create*Bom call sites provide only a source directory (`src`) when
1340   // there is no single manifest/lock file to report, so activity records must
1341   // fall back to that directory to keep the target populated.
1342   const sourcePath =
1343     context?.srcDir || context?.src || options.path || options.filePath;
1344   const activityProjectType =
1345     context?.projectType ||
1346     (Array.isArray(options.projectType)
1347       ? options.projectType.length === 1
1348         ? options.projectType[0]
1349         : undefined
1350       : options.projectType);
1351   setActivityContext({
1352     packageType: ptype,
1353     sourcePath,
1354     ...(activityProjectType ? { projectType: activityProjectType } : {}),
1355   });
1356   const bomNSData = {
1357     bomJson: undefined,
1358     bomJsonFiles: undefined,
1359     nsMapping: undefined,
1360     dependencies: undefined,
1361     parentComponent: undefined,
1362   };
1363   const serialNum = `urn:uuid:${uuidv4()}`;
1364   let allImports = {};
1365   if (context?.allImports) {
1366     allImports = context.allImports;
1367   }
1368   const nsMapping = context.nsMapping || {};
1369   const dependencies = context.dependencies || [];
1370   const services = context.services || [];
1371   const parentComponent =
1372     determineParentComponent(options) || context.parentComponent;
1373   const metadata = addMetadata(parentComponent, options, context);
1374   const components = listComponents(options, allImports, pkgInfo, ptype);
Plain English:

This function receives package info and context.

It collects:

dependencies

services

parent component

metadata

components

Then it creates the CycloneDX JSON:

index.js (line 1375)

1375   if (components && (components.length || parentComponent)) {
1376     // CycloneDX Json Template
1377     const jsonTpl = {
1378       bomFormat: "CycloneDX",
1379       specVersion: `${options.specVersion || "1.7"}`,
1380       serialNumber: serialNum,
1381       version: 1,
1382       metadata: metadata,
1383       components,
1384       dependencies,
1385     };
1386     if (services.length) {
1387       jsonTpl.services = mergeServices([], services);
1388     }
1389     bomNSData.bomJson = jsonTpl;
Plain English:

The final SBOM includes:

bomFormat

specVersion

serialNumber

version

metadata

components

dependencies

services, if any

Why this matters:

cdxgen is assembling CycloneDX directly. It is not simply converting some other internal SBOM format. So its choices about authors, supplier, scope, dependencies, and compositions are intentional generator behavior.

cdxgen Finding 3: Dependency Graphs Are Merged From Many Parsers
cdxgen has many ecosystem-specific parsers. Instead of one graph source, it merges dependency arrays.

The merge function is here:

depsUtils.js (line 14)

14  export function mergeDependencies(
15    dependencies,
16    newDependencies,
17    parentComponent = {},
18  ) {
19    if (!parentComponent && DEBUG_MODE) {
20      console.log(
21        "Unable to determine parent component. Dependencies will be flattened.",
22      );
23    }
24    let providesFound = false;
25    const deps_map = {};
26    const provides_map = {};
27    const parentRef = parentComponent?.["bom-ref"]
28      ? parentComponent["bom-ref"]
29      : undefined;
30    const combinedDeps = dependencies.concat(newDependencies || []);
31    for (const adep of combinedDeps) {
32      if (!deps_map[adep.ref]) {
33        deps_map[adep.ref] = new Set();
34      }
35      if (!provides_map[adep.ref]) {
36        provides_map[adep.ref] = new Set();
37      }
38      if (adep["dependsOn"]) {
39        for (const eachDepends of adep["dependsOn"]) {
40          if (!eachDepends) {
41            continue;
42          }
43          if (parentRef) {
44            if (eachDepends.toLowerCase() !== parentRef.toLowerCase()) {
45              deps_map[adep.ref].add(eachDepends);
46            }
47          } else {
48            deps_map[adep.ref].add(eachDepends);
49          }
50        }
51      }
52      if (adep["provides"]) {
53        providesFound = true;
54        for (const eachProvides of adep["provides"]) {
55          // Add the entry unless it is the parent itself:
56          // when there is no parentRef every entry is kept (!parentRef is true),
57          // when parentRef exists only entries that differ from it are kept.
58          if (
59            !parentRef ||
60            eachProvides?.toLowerCase() !== parentRef?.toLowerCase()
61          ) {
62            provides_map[adep.ref].add(eachProvides);
63          }
64        }
65      }
66    }
67    const retlist = [];
68    for (const akey of Object.keys(deps_map)) {
69      if (providesFound) {
70        retlist.push({
71          ref: akey,
72          dependsOn: Array.from(deps_map[akey]).sort(),
73          provides: Array.from(provides_map[akey]).sort(),
74        });
75      } else {
76        retlist.push({
77          ref: akey,
78          dependsOn: Array.from(deps_map[akey]).sort(),
79        });
80      }
81    }
82    return retlist;
Plain English:

This takes existing dependencies and new dependencies.

It combines them.

It deduplicates them using JavaScript Set.

It removes self-references to the parent component.

Then it returns a clean dependency list.

Important line:

"Unable to determine parent component. Dependencies will be flattened."
This means cdxgen itself recognizes that dependency graph structure can degrade when parent context is missing.

Why this matters:

cdxgen’s graph quality depends on ecosystem parser quality and parent component detection. It is richer than simple schema validation, but still conditional.

cdxgen Finding 4: Scope Is Explicitly Computed
This is the biggest contrast with Trivy.

In cdxgen, scope can be computed when components are listed.

index.js (line 1033)

1033     let compScope = pkg.scope;
1034     if (allImports) {
1035       const impPkgs = Object.keys(allImports);
1036       if (
1037         impPkgs.includes(name) ||
1038         impPkgs.includes(`${group}/${name}`) ||
1039         impPkgs.includes(`@${group}/${name}`) ||
1040         impPkgs.includes(group) ||
1041         impPkgs.includes(`@${group}`)
1042       ) {
1043         compScope = "required";
1044       } else if (impPkgs.length && compScope !== "excluded") {
1045         compScope = "optional";
1046       }
1047     }
Plain English:

cdxgen starts with pkg.scope.

Then it checks imported packages.

If the package appears in imports, mark it required.

If imports exist but this package is not imported, mark it optional.

This is source-usage-based scope inference.

For Maven, cdxgen maps Maven dependency scopes into CycloneDX scope:

utils.js (line 6260)

6260         // Ignore test scope
6261         if (!includeMavenTestScope && componentScope === "test") {
6262           return;
6263         }
6264         let scope;
6265         if (["compile", "runtime"].includes(componentScope)) {
6266           scope = "required";
6267         } else if (componentScope === "test") {
6268           scope = "optional";
6269         } else if (componentScope === "provided") {
6270           scope = "excluded";
6271         }
Plain English:

Maven compile and runtime become CycloneDX required.

Maven test becomes CycloneDX optional.

Maven provided becomes CycloneDX excluded.

That is an explicit semantic mapping.

cdxgen also recomputes scope using the dependency tree:

utils.js (line 21896)

21896 /**
21897  * Re-compute and set the scope based on the dependency tree
21898  *
21899  * @param {Array} pkgList List of components
21900  * @param {Array} dependencies List of dependencies
21901  *
21902  * @returns {Array} Updated list
21903  */
21904 export function recomputeScope(pkgList, dependencies) {
21905   const requiredPkgs = {};
21906   if (!pkgList || !dependencies) {
21907     return pkgList;
21908   }
21909   for (const pkg of pkgList) {
21910     if (!pkg.scope || !pkg["bom-ref"]) {
21911       continue;
21912     }
21913     if (pkg.scope === "required") {
21914       requiredPkgs[pkg["bom-ref"]] = true;
21915     }
21916   }
21917   for (const adep of dependencies) {
21918     if (requiredPkgs[adep.ref]) {
21919       for (const ado of adep.dependsOn) {
21920         requiredPkgs[ado] = true;
21921       }
21922     }
21923   }
21924   // Prevent marking every component as optional
21925   if (!Object.keys(requiredPkgs).length) {
21926     return pkgList;
21927   }
21928   for (const pkg of pkgList) {
21929     if (requiredPkgs[pkg["bom-ref"]]) {
21930       pkg.scope = "required";
21931     } else if (!pkg.scope) {
21932       pkg.scope = "optional";
21933     }
21934   }
21935   return pkgList;
21936 }
Plain English:

First, cdxgen finds all packages already marked required.

Then it looks at the dependency graph.

If a required package depends on another package, it marks that dependency as required too.

Anything not required and missing scope can become optional.

This is important because scope is not just copied from a manifest. It is propagated through the dependency graph.

Why this matters:

Trivy filters dev dependencies before output.

cdxgen tries to encode production relevance into the SBOM via scope.

This is a major generator difference.

Both can emit valid CycloneDX, but the meaning of the resulting SBOM differs.

cdxgen Finding 5: cdxgen Can Mark Filtered SBOMs As Incomplete
The CLI option says this directly:

cdxgen.js (line 234)

234   .option("required-only", {
235     type: "boolean",
236     description:
237       "Include only the packages with required scope on the SBOM. Would set compositions.aggregate to incomplete unless --no-auto-compositions is passed.",
238   })
Plain English:

If the user asks for only required packages, cdxgen knows it is producing a partial SBOM.

So it says it will set compositions.aggregate to incomplete.

The actual code is here:

postgen.js (line 946)

946     for (const adep of bomJson.dependencies || []) {
947       if (retainedRefs.has(adep.ref)) {
948         const newdepson = (adep.dependsOn || []).filter((d) =>
949           retainedRefs.has(d),
950         );
951         const obj = {
952           ref: adep.ref,
953           dependsOn: newdepson,
954         };
955         // Filter provides array if needed
956         if (adep.provides?.length) {
957           obj.provides = adep.provides.filter((d) => retainedRefs.has(d));
958         }
959         newdependencies.push(obj);
960       }
961     }
962     bomJson.components = newcomponents;
963     bomJson.dependencies = newdependencies;
964     bomJson.services = newServices;
965     // We set the compositions.aggregate to incomplete by default
966     if (
967       options.specVersion >= 1.5 &&
968       options.autoCompositions &&
969       bomJson.metadata?.component
970     ) {
971       if (!bomJson.compositions) {
972         bomJson.compositions = [];
973       }
974       bomJson.compositions.push({
975         "bom-ref": bomJson.metadata.component["bom-ref"],
976         aggregate: options.only ? "incomplete_first_party_only" : "incomplete",
977       });
978     }
Plain English:

After filtering components, cdxgen also filters dependencies to keep only retained references.

Then it updates:

bomJson.components

bomJson.dependencies

bomJson.services

Then it adds:

{
  "bom-ref": "...",
  "aggregate": "incomplete"
}
inside compositions.

Why this matters:

This is a good implementation example of a tool using CycloneDX’s completeness mechanism properly.

But it is tool-specific behavior.

CycloneDX allows compositions, but does not force all tools to use it when output is partial.

So cdxgen may tell consumers “this is incomplete,” while another tool may silently omit parts without a completeness claim.

cdxgen Finding 6: Formulation Exists But Is Opt-In
The CLI flag is here:

cdxgen.js (line 406)

406   .option("include-formulation", {
407     type: "boolean",
408     default: false,
409     description:
410       "Generate formulation section with git metadata and build tools. Defaults to false.",
Plain English:

Formulation is disabled by default.

The post-processing code only adds formulation if this option is enabled:

postgen.js (line 71)

71  function applyFormulation(bomJson, options, filePath, formulationList) {
72    if (
73      !options.includeFormulation ||
74      options.specVersion < 1.5 ||
75      !bomJson ||
76      bomJson.formulation !== undefined
77    ) {
78      return bomJson;
79    }
80    const context = formulationList?.length ? { formulationList } : {};
81    setActivityContext({
82      bomMutation: "formulation",
83      capability: "bom-mutation",
84      projectType: "Formulation",
85      sourcePath: filePath || options.filePath || process.cwd(),
86    });
87    let formulationData;
88    try {
89      formulationData = addFormulationSection(filePath, options, context);
90    } finally {
91      resetActivityContext();
92    }
93    if (!formulationData) {
94      return bomJson;
95    }
96    bomJson.formulation = formulationData.formulation;
97    const formulationServices = formulationData.formulation.flatMap(
98      (entry) => entry?.services || [],
99    );
100   if (formulationServices.length) {
101     bomJson.services = mergeServices(
102       bomJson.services || [],
103       formulationServices,
104     );
105   }
106   if (formulationData.dependencies?.length) {
107     bomJson.dependencies = mergeDependencies(
108       bomJson.dependencies || [],
109       formulationData.dependencies,
110     );
111   }
112   return bomJson;
Plain English:

If includeFormulation is false, return the BOM unchanged.

If enabled, cdxgen adds formulation.

It can also merge formulation-related services and dependencies.

Why this matters:

This supports the point that build provenance is technically supported but not baseline. Even in cdxgen, the user must opt in.

How To Explain The Difference Between Trivy And cdxgen
The core comparison is:

Trivy is scan-first.

cdxgen is CycloneDX-generation-first.

Trivy’s output is shaped by what its scanners find and what it filters before output.

cdxgen’s output is shaped by parsers, enrichment logic, post-processing, and CycloneDX-specific features.

For provenance:

Trivy sets timestamp and tool metadata, but not metadata authors or supplier.

cdxgen sets timestamp and authors, but leaves supplier undefined.

For dependency graphs:

Trivy uses package DependsOn relationships and then emits CycloneDX dependencies.

cdxgen merges dependency arrays from multiple parser outputs.

For scope:

Trivy filters dev dependencies before output and does not emit CycloneDX scope in the inspected path.

cdxgen computes and propagates scope into the SBOM.

For completeness:

Trivy emits empty dependency nodes, but its own TODO admits ambiguity between true leaves and unsupported graphs.

cdxgen can mark filtered SBOMs as incomplete using compositions.

For formulation:

Trivy does not appear to produce formulation in normal CycloneDX SBOM output.

cdxgen supports formulation but leaves it disabled by default.

Why This Is Important For Your Paper
Your previous Section 4.2.3 was criticized because it sounded like discussion rather than results.

This implementation analysis gives you real results:

Result 1:
Generators differ in whether they populate CISA-relevant provenance fields. Trivy emits timestamp but not metadata authors or supplier. cdxgen emits timestamp and authors, but leaves supplier undefined.

Result 2:
Generators differ in how they represent production relevance. Trivy filters development dependencies before output, while cdxgen computes and emits scope using ecosystem-specific rules and dependency propagation.

Result 3:
Generators differ in how they communicate completeness. Trivy emits empty dependency entries but acknowledges ambiguity between true leaves and unsupported graphs. cdxgen can mark filtered SBOMs as incomplete through compositions.

Result 4:
Advanced CycloneDX features remain opt-in or tool-specific. cdxgen supports formulation but disables it by default; Trivy supports VEX filtering but does not make normal SBOM output a VEX-rich document.
This makes the argument much stronger:

The inconsistency is not just “tools fail to follow the spec.”

It is:

The specification leaves population choices open, and generators fill that gap differently.

What To Tell Dr. Mohannad
You can say this:

I inspected the implementation logic of Trivy and cdxgen directly. The main takeaway is that the inconsistency appears at the point where tools have to populate CycloneDX fields, not only at the schema validation level.

For provenance, Trivy sets metadata.timestamp and tool metadata but does not populate metadata.authors or metadata.supplier. cdxgen sets metadata.timestamp and metadata.authors by default, but still leaves metadata.supplier undefined. So both can produce valid CycloneDX output while differing on CISA-relevant provenance.

For scope, the tools differ more sharply. Trivy filters development dependencies before SBOM output unless --include-dev-deps is used, and I did not find CycloneDX component scope being emitted in the inspected path. cdxgen, by contrast, computes scope using import usage, ecosystem-specific mappings, and dependency graph propagation.

For completeness, Trivy emits empty dependency entries for packages without dependencies, but its own source code has a TODO noting the ambiguity between a true leaf node and an unsupported dependency graph. cdxgen can mark filtered SBOMs as incomplete using compositions.aggregate = incomplete when required-only filtering is used.

This gives us implementation-level evidence that SBOM inconsistency is partly caused by underspecified population semantics. The same CycloneDX concepts exist in the standard, but tools make different choices about when and how to populate them.
Possible Paper Paragraph
You can use this as a draft:

To move beyond schema-level analysis, we inspected the CycloneDX generation paths of Trivy and cdxgen. The inspection shows that tool inconsistency emerges at the point where generators must operationalize underspecified fields. Trivy constructs CycloneDX metadata with a timestamp and tool information, but does not populate metadata-level supplier or authors. Component supplier is populated only when package maintainer metadata is available. In contrast, cdxgen populates timestamp and authors by default, but leaves metadata.supplier undefined. The two tools also differ in their treatment of dependency relevance. Trivy removes development dependencies before output unless \texttt{--include-dev-deps} is enabled, whereas cdxgen computes component \texttt{scope} using ecosystem-specific rules, import analysis, and dependency graph propagation. Completeness is similarly tool-dependent: Trivy emits empty dependency entries for components with no listed dependencies, while its own implementation notes the ambiguity between actual leaf nodes and unsupported dependency graphs; cdxgen, when filtering to required components, can explicitly mark the BOM as incomplete through \texttt{compositions}. These findings suggest that CycloneDX inconsistency is not only a validation problem, but also a population semantics problem: tools make different implementation choices for fields that the specification can represent but does not fully operationalize.
My honest recommendation: discuss this with Dr. Mohannad as a concrete pivot. Instead of saying “we revised 4.2.3,” say “we started implementation-level tracing and found concrete divergence between Trivy and cdxgen.” That is much closer to what he asked for.

12 May, 20:32
can u give me the main top 3 features from both like the findings and hat i need to present to professors? also can u like generate slides maybe?
12 May, 21:55

Worked for 1m 19s
Using the Presentations skill because this is now professor-facing slide/narrative prep.

Main Message
The headline for professors should be:

We inspected Trivy and cdxgen at the implementation level and found that SBOM inconsistency comes from population semantics: both tools output valid CycloneDX, but they make different choices about what to populate, infer, filter, or leave unspecified.

Top 3 Findings To Present
1. Provenance fields are populated differently
Trivy:
metadata.timestamp is generated, but metadata.authors and metadata.supplier are not populated in the CycloneDX metadata block.

Evidence: marshal.go (line 92)

cdxgen:
metadata.timestamp and metadata.authors are populated, but metadata.supplier is explicitly left undefined.

Evidence: index.js (line 537)

Why it matters:
Both tools can produce valid CycloneDX, but both may still miss CISA-relevant provenance. This supports our argument that schema validity does not imply policy usefulness.

2. Dependency graph completeness is tool dependent
Trivy:
Builds dependency edges from package DependsOn, then emits empty dependency entries for packages with no listed dependencies. Its own TODO says it should distinguish true leaf nodes from unsupported dependency graphs.

Evidence: encode.go (line 273)

cdxgen:
Merges dependency graphs from ecosystem parsers. If parent context is missing, dependencies may be flattened.

Evidence: depsUtils.js (line 14)

Why it matters:
A missing or shallow dependency graph is not always a tool bug. It can result from parser support, missing parent context, or ambiguity in what an empty graph means.

3. Scope and completeness are handled very differently
Trivy:
Does not appear to emit CycloneDX scope in the inspected path. Instead, it filters dev dependencies before SBOM output unless --include-dev-deps is used.

Evidence: service.go (line 452)

cdxgen:
Computes scope using imports, ecosystem rules, and dependency graph propagation. It can also mark filtered SBOMs as incomplete using compositions.aggregate = incomplete.

Evidence: utils.js (line 21904) and postgen.js (line 965)

Why it matters:
This is the clearest implementation divergence. Trivy treats production relevance as filtering. cdxgen tries to encode production relevance inside the SBOM.

Suggested Slide Deck
Slide 1: Why We Looked At Generator Code
Title: From Specification Optionality To Generator Behavior

Main point:
We moved from asking “what does CycloneDX allow?” to “what do generators actually populate?”

Say:
“Dr. Mohannad’s feedback was that our previous analysis was too high-level. So we inspected generator implementation paths directly.”

Slide 2: Tools Inspected
Title: Two Generators, Two Design Philosophies

Table:

Tool	Design Style	What We Inspected
Trivy	Scanner-first	CycloneDX marshaler, dependency encoder, dev dependency filtering
cdxgen	CycloneDX-first	metadata builder, scope logic, dependency merge, post-generation completeness
Slide 3: Finding 1: Provenance Is Inconsistent
Title: Valid SBOMs Can Still Miss Provenance

Table:

Field	Trivy	cdxgen
metadata.timestamp	Yes	Yes
metadata.authors	No	Yes, default author
metadata.supplier	No	Undefined
Takeaway:
“Both tools are valid CycloneDX emitters, but neither fully satisfies provenance expectations by default.”

Slide 4: Finding 2: Dependency Graphs Depend On Tool Internals
Title: Dependency Completeness Is Not Just A Schema Question

Trivy:
Uses package DependsOn.

Important evidence:
Trivy TODO says it should distinguish true no-dependency cases from unsupported dependency graphs.

cdxgen:
Merges parser-specific dependency graphs.

Takeaway:
“CycloneDX can represent a graph, but generator-specific evidence decides whether a useful graph exists.”

Slide 5: Finding 3: Scope Is The Biggest Divergence
Title: Trivy Filters, cdxgen Infers

Table:

Question	Trivy	cdxgen
How are dev deps handled?	Filtered before output	Often represented through scope
Is scope emitted?	Not found in inspected path	Yes, in several ecosystem paths
Is incompleteness declared?	Not found automatically	Yes, for filtered required-only BOMs
Takeaway:
“Two valid CycloneDX SBOMs can encode very different assumptions about production relevance.”

Slide 6: What This Means For The Paper
Title: Our Stronger Claim

Use this exact line:

SBOM inconsistency is partly caused by underspecified population semantics. CycloneDX provides fields for provenance, scope, dependencies, and completeness, but generators decide differently when and how to populate them.

Slide 7: Next Step
Title: Extension Plan

Bullets:

Add Syft and Microsoft SBOM Tool to the same implementation tracing.
Add Trail of Bits it-depends because Dr. Mohannad specifically mentioned it.
Compare generator issues against sbomqs and jbomaudit.
Identify which issues quality tools can detect and which require external context.
What To Tell Professors

We inspected Trivy and cdxgen directly rather than only comparing their SBOM outputs. The key finding is that both tools output valid CycloneDX, but they operationalize important fields differently.

Trivy generates timestamp metadata but not metadata supplier or authors, filters dev dependencies before output, and builds dependency graphs from package DependsOn data. Its own code notes ambiguity between true leaf nodes and unsupported dependency graphs.

cdxgen generates timestamp and authors but leaves metadata supplier undefined, computes scope using ecosystem-specific rules and dependency propagation, and can mark filtered SBOMs as incomplete through compositions.

So our revised direction is to frame the problem as population semantics: CycloneDX can represent these concepts, but the specification does not fully determine how generators should populate them.
I can also generate an actual .pptx from this next, probably around 7 slides, clean and professor-meeting friendly.

12 May, 21:56
can u take this and make it more detailed for advisors to look into pls:"I’ll be running late to the meeting. I inspected the implementation logic of Trivy and cdxgen. the main takeaway I think from my work is that the inconsistency appears at the point where tools have to populate CycloneDX fields, not only at the schema validation level.

For provenance, Trivy sets metadata.timestamp and tool metadata but does not populate metadata.authors or metadata.supplier. cdxgen sets metadata.timestamp and metadata.authors by default, but still leaves metadata.supplier undefined. So both can produce valid CycloneDX output while differing on CISA-relevant provenance.

For scope, the tools differ more sharply. Trivy filters development dependencies before SBOM output unless --include-dev-deps is used, and I did not find CycloneDX component scope being emitted in the inspected path. cdxgen, by contrast, computes scope using import usage, ecosystem-specific mappings, and dependency graph propagation.

For completeness, Trivy emits empty dependency entries for packages without dependencies, but its own source code has a TODO noting the ambiguity between a true leaf node and an unsupported dependency graph. cdxgen can mark filtered SBOMs as incomplete using compositions.aggregate = incomplete when required-only filtering is used.

This gives us implementation-level evidence that SBOM inconsistency is partly caused by underspecified population semantics. The same CycloneDX concepts exist in the standard, but tools make different choices about when and how to populate them."

and write as if jit's human written

Show less
12 May, 21:58
I’ll be running a bit late to the meeting, but I wanted to share the update beforehand.

I started looking directly into the implementation logic of two SBOM generators, Trivy and cdxgen. The main takeaway so far is that the inconsistency does not only appear at the schema validation level. It also appears at the point where each tool has to decide how to populate CycloneDX fields.

For provenance, Trivy creates metadata.timestamp and records tool metadata, but I did not find it populating metadata.authors or metadata.supplier in the CycloneDX metadata block. cdxgen behaves differently: it creates metadata.timestamp and metadata.authors by default, but still leaves metadata.supplier undefined. So both tools can produce valid CycloneDX output, but they differ on fields that are relevant to the CISA minimum elements.

For dependency scope, the difference is stronger. Trivy seems to treat development dependencies mostly as a filtering decision before SBOM output. By default, it suppresses development dependencies unless --include-dev-deps is used, and I did not find CycloneDX component scope being emitted in the path I inspected. cdxgen, on the other hand, tries to compute scope inside the SBOM. It uses import usage, ecosystem-specific rules, and dependency graph propagation to decide whether components should be marked as required, optional, or excluded.

For dependency completeness, Trivy builds dependency entries from package DependsOn relationships. It also emits empty dependency entries for packages that do not have listed dependencies. However, its own source code has a TODO noting that the tool should distinguish between a component that truly has no dependencies and a component whose dependency graph is simply unsupported. cdxgen handles completeness differently. When it filters the SBOM using required-only mode, it can mark the result as incomplete using compositions.aggregate = incomplete.

I think this gives us a better implementation-level angle for the paper. The issue is not simply that CycloneDX allows optional fields, or that tools fail schema validation. Rather, CycloneDX provides concepts such as provenance, scope, dependency relationships, and completeness, but generator tools make different choices about how and when to populate them. This suggests that some SBOM inconsistencies are caused by underspecified population semantics, not just weak validation.

12 May, 21:59

Current working directory missing
This chat's working directory no longer exists



Outputs
cyclonedx_extractions.csv
cyclonedx_generator_consumer_coding.csv
cyclonedx_generator_consumer_codebook.csv

Sources

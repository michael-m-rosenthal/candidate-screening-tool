# Resume Intelligence Pipeline

An automated, multi-agent system designed to perform evidence-based audits of technical resumes against complex job requirements, while filtering out "ghost jobs" and internal-only postings. This pipeline leverages Large Language Models (LLMs) to bridge the gap between unstructured human-readable documents and structured career data.

## 🛠 Author’s Note on AI Collaboration
**Disclosed Use of Generative AI:** Much of the boilerplate logic, Pydantic schemas, and CLI argument parsing in this repository were generated in collaboration with Google Gemini (Gemini 3 Flash).
**Verification Statement:** The author of this repository is a proficient developer and has:
* Architected the logic flow and multi-agent interaction strategy.
* Thoroughly reviewed all AI-generated code for security, efficiency, and PEP 8 compliance.
* Vigorously tested the pipeline against real-world data to ensure functional reliability.

## 🛠 Pipeline Architecture
The system is decomposed into two distinct phases to ensure auditability, consistency, and scalability.

### Phase 0: Job Quality Screening
Filters out "compliance postings" or internal-only roles before you waste time applying.
* **agent0_1.py (Fraud Auditor)**: Checks the `posting.txt` for internal-hire red flags using a master JSON criteria.
* **agent0_2.py (Futility Summarizer)**: Generates the `screening_summary.md` verdict (GO/NO-GO).

### Phase 1: Candidate Evaluation
Audits a specific candidate against a validated job posting.
* **agent1_1.py (Requirement Extractor)**: Normalizes the `posting.txt` into a structured `questions.json` rubric.
* **agent1_2.py (Evidence Auditor)**: Cross-references `resume.md` against the rubric, assessing evidence strength (Strong/Moderate/Weak).
* **agent1_3.py (Executive Synthesizer)**: Aggregates audit data into the final `executive_summary.md` report.



## 📂 Directory Structure
The pipeline utilizes a decoupled directory strategy, allowing for a 1-to-many relationship between job postings and candidates.

```text
.
├── prompts/                    # System instructions & Master Question JSONs
├── postings/                   # Library of standardized job postings
│   └── senior-eng-vls/         # Job-specific folder
│       ├── posting.txt         # Input: Raw text of the job
│       ├── screening_report.json # Agent 0_1 Output
│       ├── screening_summary.md  # Agent 0_2 Output
│       └── questions.json      # Agent 1_1 Output
└── candidates/                 # Evaluation workspace
    └── alex-chen/              # Candidate-specific folder
        ├── resume.md           # Input: The candidate's resume
        ├── candidate_eval.json # Agent 1_2 Output
        └── executive_summary.md# Agent 1_3 Output

```

## 🚀 Usage

### 1. Initial Screening (Phase 0)

Check if the job is a legitimate opportunity. These scripts only require the posting directory.

```bash
python agent0_1.py ./postings/senior-eng-vls
python agent0_2.py ./postings/senior-eng-vls

```

### 2. Requirement Extraction (Phase 1 Start)

If the screening verdict is **GO**, generate the technical requirements rubric.

```bash
python agent1_1.py ./postings/senior-eng-vls

```

### 3. Candidate Audit (Phase 1 Finish)

Evaluate a specific candidate folder against the posting requirements.

```bash
# Cross-reference resume with requirements
python agent2.py ./postings/senior-eng-vls ./candidates/alex-chen

# Generate the final human-readable report
python agent1_3.py ./postings/senior-eng-vls ./candidates/alex-chen

```

## 🧠 Why This System?

Standard LLM interactions often suffer from "hallucinated fit." This pipeline enforces:

* **Evidence-Based Scoring:** Agent 1_2 must categorize evidence as Strong, Moderate, or Weak based on documented achievements.
* **Traceability:** Every "Yes/No" recommendation is backed by a specific justification found in the source text.
* **Gatekeeping:** Phase 0 prevents wasting resources on roles that are likely already filled internally.

## ⚙️ Installation & Setup

1. **Prerequisites**: Python 3.10+ and a Google Gemini API Key.
2. **Install Dependencies**:
```bash
pip install -U google-genai pydantic

```


3. **Configure API Access**:
```bash
export GOOGLE_API_KEY='your_api_key_here'

```



## ⚖️ Legal Disclaimer & License

This software is provided "as-is", without warranty of any kind. The author primarily uses this tool as a self-assessment utility to determine personal alignment with job requirements. Use of this tool for the screening of third-party candidates is strictly at the user's own risk regarding compliance with local labor laws (e.g., EEOC, GDPR).


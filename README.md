# Resume Intelligence Pipeline

An automated, multi-agent system designed to perform evidence-based audits of technical resumes against complex job requirements, while filtering out "ghost jobs" and internal-only postings. This pipeline leverages Large Language Models (LLMs) to bridge the gap between unstructured human-readable documents and structured career data.


## ⚠️ Project Context & Disclaimer

**This is a "clever poor-man's solution."** Large companies spend millions of dollars on enterprise-grade recruitment platforms that leverage massive LLM context windows to ingest entire resume stacks simultaneously. This project is **not** that.

Instead, this is a modular, agentic pipeline designed to:
* **Work within the constraints** of smaller, faster, and more cost-effective context windows.
* **Provide "White-Box" Transparency:** Every decision is backed by a specific evidence trace, unlike the "black-box" scoring of enterprise tools.
* **Empower the Individual:** Designed for developers who want to audit their own alignment or screen job quality without an enterprise subscription.

**If you require a monolithic, high-volume enterprise solution with a million-token context window, this project may not be for you.**

---

## 🛠 Author’s Note on AI Collaboration
**Disclosed Use of Generative AI:** Much of the boilerplate logic, Pydantic schemas, and CLI argument parsing in this repository were generated in collaboration with Google Gemini (Gemini 2.5 Flash).

**Verification Statement:** This is not "AI-slop." The architecture, logic flow, and multi-agent interaction strategies were manually designed to enforce a strict, evidence-based audit trail that enterprise black-boxes often lack. The author has:
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

### 1. Manual Execution

You can run agents individually for granular control:

**Phase 0: Screening**

```bash
python agent0_1.py ./postings/senior-eng-vls
python agent0_2.py ./postings/senior-eng-vls

```

**Phase 1: Evaluation**

```bash
python agent1_1.py ./postings/senior-eng-vls
python agent1_2.py ./postings/senior-eng-vls ./candidates/alex-chen
python agent1_3.py ./postings/senior-eng-vls ./candidates/alex-chen

```

### 2. Automation with Orchestrator

To process all job postings and all candidates in bulk, use the provided `orchestrate.sh` script.

**Setup Execute Permissions:**
Before running the script for the first time, you must grant it execution permissions:

```bash
chmod +x orchestrate.sh

```

**Run the Pipeline:**

```bash
./orchestrate.sh

```

The script will loop through every `posting.txt` in the `postings/` subdirectories and audit them against every `resume.md` found in the `candidates/` directory.

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
export GEMINI_API_KEY='your_api_key_here'

```



## ⚖️ Legal Disclaimer & License

This software is provided "as-is", without warranty of any kind. The author primarily uses this tool as a self-assessment utility to determine personal alignment with job requirements. Use of this tool for the screening of third-party candidates is strictly at the user's own risk regarding compliance with local labor laws (e.g., EEOC, GDPR).


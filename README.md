# Resume Intelligence Pipeline

## ⚠️ Project Context & Disclaimer

**This is a "clever poor-man's solution."** Large companies spend millions of dollars on enterprise-grade recruitment platforms that leverage massive LLM context windows to ingest entire resume stacks simultaneously. This project is **not** that.

Instead, this is a modular, agentic pipeline designed to:
* **Work within the constraints** of smaller, faster, and more cost-effective context windows.
* **Provide "White-Box" Transparency:** Every decision is backed by a specific evidence trace, unlike the "black-box" scoring of enterprise tools.
* **Empower the Individual:** Designed for developers who want to audit their own alignment or screen job quality without an enterprise subscription.

**If you require a monolithic, high-volume enterprise solution with a million-token context window, this project may not be for you.**

---

## 🛠 Author’s Note on AI Collaboration
**Disclosed Use of Generative AI:** Much of the boilerplate logic, Pydantic schemas, and CLI argument parsing in this repository were generated in collaboration with Google Gemini (Gemini 3 Flash).

**Verification Statement:** This is not "AI-slop." The architecture, logic flow, and multi-agent interaction strategies were manually designed to enforce a strict, evidence-based audit trail that enterprise black-boxes often lack. The author has:
* Architected the logic flow and multi-agent interaction strategy.
* Thoroughly reviewed all AI-generated code for security, efficiency, and PEP 8 compliance.
* Vigorously tested the pipeline against real-world data to ensure functional reliability.

## 🛠 Pipeline Architecture
The system is decomposed into phases to ensure auditability and scalability.

### Phase 0: Job Quality Screening
* **agent0_1.py (Fraud Auditor)**: Checks `posting.txt` for internal-hire red flags.
* **agent0_2.py (Futility Summarizer)**: Generates the `screening_summary.md` verdict.

### Phase 1: Candidate Evaluation (Standard)
* **agent1_1.py (Requirement Extractor)**: Normalizes `posting.txt` into `questions.json`.
* **agent1_2.py (Evidence Auditor)**: Cross-references `resume.md` against the rubric.
* **agent1_3.py (Executive Synthesizer)**: Aggregates data into `executive_summary.md`.

### Phase 2: Deep Alignment (Experience-Enhanced)
* **agent2_1.py (Experience Auditor)**: Performs a high-fidelity audit using both `resume.md` and `experiences.md` (STAR format). Output is saved to a sanitized, hierarchy-aware JSON in the candidate's `role_alignments/` folder.

## 📂 Directory Structure

```text
.
├── prompts/                    # System instructions & master rubrics
├── postings/                   # Library of job postings
│   └── vls/
│       └── eng/
│           └── senior-dev/     # Nested job folder
│               ├── posting.txt
│               └── questions.json
└── candidates/                 # Evaluation workspace
    └── alex-chen/              # Candidate-specific folder
        ├── resume.md           # Primary Resume
        ├── experiences.md      # STAR-formatted experiences
        └── role_alignments/    # Agent 2_1 unique outputs
            └── alex-chen_vls_eng_senior_dev_role_alignment.json

```

## 🚀 Usage

### 1. Automation with Orchestrator

To run the full suite across all postings and candidates:

```bash
chmod +x orchestrate.sh
./orchestrate.sh

```

### 2. Manual Experience Audit (Agent 2_1)

To run a deep alignment check for a specific role:

```bash
python agent2_1.py ./postings/vls/eng/senior-dev ./candidates/alex-chen

```

## ⚙️ Installation

1. **Prerequisites**: Python 3.10+ and a Google Gemini API Key.
2. **Install Dependencies**:
```bash
pip install -U google-genai pydantic

```


3. **Configure API Access**:
```bash
export GEMINI_API_KEY='your_api_key_here'

```



## ⚖️ License

This software is provided "as-is" for personal assessment. Use for third-party screening is at the user's own risk regarding labor law compliance.

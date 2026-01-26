# Resume Intelligence Pipeline

An automated, multi-agent system designed to perform evidence-based audits of technical resumes against complex job requirements. This pipeline leverages Large Language Models (LLMs) to bridge the gap between unstructured human-readable documents and structured career data.

## 🛠 Author’s Note on AI Collaboration

**Disclosed Use of Generative AI:** Much of the boilerplate logic, Pydantic schemas, and CLI argument parsing in this repository were generated in collaboration with **Google Gemini (Gemini 2.0 Flash)**.

**Verification Statement:** The author of this repository is a proficient Python developer and has:

* **Architected the logic flow** and multi-agent interaction strategy.
* **Thoroughly reviewed** all AI-generated code for security, efficiency, and PEP 8 compliance.
* **Vigorously tested** the pipeline against real-world data to ensure functional reliability.

The AI was utilized as a high-velocity pair-programmer to reduce boilerplate overhead, allowing the author to focus on the mathematical rigor and system design.

## 🛠 Pipeline Architecture

The system is decomposed into three specialized agents to ensure auditability, consistency, and scalability.

| Agent | Component | Purpose |
| :--- | :--- | :--- |
| **Agent 1** | **Requirement Extractor** | Normalizes a raw job posting into a structured JSON schema of core and preferred competencies. |
| **Agent 2** | **Evidence Auditor** | Cross-references a candidate's resume against the requirements, looking for specific proof and assessing evidence strength. |
| **Agent 3** | **Executive Synthesizer** | Aggregates the audit data into a high-level Markdown report with fit percentages and hiring recommendations. |

---

## 📂 Directory Structure

The pipeline utilizes a decoupled directory strategy, allowing for a 1-to-many relationship between job postings and candidates.

```text
.
├── prompts/                    # System instructions for Gemini Agents
├── postings/                   # Library of standardized job postings
│   └── senior-eng-vls/         # Specific job folder
│       ├── posting.txt         # Raw text of the job
│       └── questions.json      # Extracted requirements (Agent 1 Output)
└── candidates/                 # Evaluation workspace
    └── michael-r/              # Unique candidate folder
        ├── resume.md           # The candidate's resume
        ├── candidate_eval.json # Detailed audit log (Agent 2 Output)
        └── executive_summary.md# Final human-readable report (Agent 3 Output)

```

---

## 🚀 Usage

### 1. Extract Requirements (Agent 1)

Prepares the "rubric" for the evaluation based on the job posting.

### 2. Audit the Candidate (Agent 2)

Scans the candidate's resume for evidence.

```bash
python agent2_auditor.py ./postings/senior-eng-vls ./candidates/michael-r

```

### 3. Generate Executive Summary (Agent 3)

Synthesizes the findings into a final report.

```bash
python agent3_synthesizer.py ./postings/senior-eng-vls ./candidates/michael-r

```

---

## 🧠 Why This System?

Standard LLM interactions often suffer from "hallucinated fit," where the AI claims a candidate is a match without evidence. This pipeline enforces:

* **Evidence-Based Scoring:** Agent 2 must categorize evidence as `Strong`, `Moderate`, or `Weak` based on documented achievements.
* **Traceability:** Every "Yes/No" recommendation is backed by a specific justification found in the source text.
* **Context Preservation:** By maintaining a `posting.txt` context, the agents understand the difference between a "Senior" role at a startup vs. a legacy enterprise firm.

## ⚙️ Installation & Setup

### 1. Prerequisites

* Python 3.10 or higher.
* A Google Gemini API Key.

### 2. Install Dependencies

The pipeline requires the `google-genai` library and `pydantic` for structured data validation.

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install the required modules
pip install -U google-genai pydantic

```

### 3. Configure API Access

The agents are configured to initialize the `genai.Client()` using an environment variable.

```bash
# Add this to your .bashrc, .zshrc, or export it in your current session
export GOOGLE_API_KEY='your_api_key_here'

```


## ⚖️ Legal Disclaimer & License

### 1. Personal Use Disclosure

The author primarily uses this tool as a **self-assessment utility** to determine personal alignment with specific job requirements before initiating a formal application. It is designed to evaluate technical "fit" and reduce the noise in the career search process.

### 2. No Liability & "As-Is" Clause

This software is provided **"as-is"**, without warranty of any kind, express or implied. In no event shall the author be held liable for any claim, damages, or other liability arising from the use of this software.

### 3. Ethical Use & Compliance Warning

**The use of this tool for the screening or automated rejection of third-party candidates is strictly at the user's own risk.**

* Users are solely responsible for ensuring that their implementation complies with local, state, and federal labor laws (e.g., **EEOC**, **GDPR**, and the **AI Act**).
* This tool is not intended to, and should not be used to, screen candidates based on protected characteristics including, but not limited to, **age, gender, race, religion, or disability status**.
* The author disclaims all responsibility for any discriminatory outcomes resulting from the misuse of these scripts or the underlying LLM models.


# Resume Intelligence Pipeline

An automated, multi-agent system designed to perform evidence-based audits of technical resumes against complex job requirements. This pipeline leverages Large Language Models (LLMs) to bridge the gap between unstructured human-readable documents and structured career data.

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

---

### Why we use `google-genai`

Unlike the older `google-generativeai` library, the newer `google-genai` SDK (used in your scripts) provides native support for **Pydantic models** in the `response_schema`. This is what allows **Agent 2** to return a strictly formatted list of evaluations that your code can parse immediately into a JSON file without manual string cleaning.

### Next Step

Now that your environment is ready, would you like me to provide the **questions.json** for the VLS directory so you can perform a test run of the full pipeline?
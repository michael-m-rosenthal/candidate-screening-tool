import sys
import os
import json
import argparse
import re
from google import genai
from pydantic import BaseModel, Field
from typing import Literal

class Evaluation(BaseModel):
    question: str
    requirement: str
    priority: Literal["Core", "Preferred"]
    answer: Literal["Yes", "No"]
    evidence_strength: Literal["Strong", "Moderate", "Weak", "None"]
    justification: str

def main():
    parser = argparse.ArgumentParser(description="Agent 2_1: Experience-Enhanced Evaluator")
    parser.add_argument("posting_directory", help="Directory containing posting.txt")
    parser.add_argument("candidate_directory", help="Directory containing resume.md and experiences.md")
    args = parser.parse_args()

    # Absolute paths
    base_posting_dir = os.path.normpath(os.path.abspath(args.posting_directory))
    base_candidate_dir = os.path.normpath(os.path.abspath(args.candidate_directory))
    postings_root = os.path.abspath("postings")

    # --- SANITIZED UNIQUE FILENAME LOGIC ---
    try:
        rel_job_path = os.path.relpath(base_posting_dir, postings_root)
    except ValueError:
        rel_job_path = os.path.basename(base_posting_dir)
    
    # Replace all non-alphanumeric characters (including slashes) with underscores
    # Example: 'VLS/Dept-Name/Senior Eng!' -> 'vls_dept_name_senior_eng_'
    job_slug = re.sub(r'[^a-zA-Z0-9]', '_', rel_job_path).lower()
    
    # Setup the output directory: candidate_dir/role_alignments/
    alignment_dir = os.path.join(base_candidate_dir, "role_alignments")
    os.makedirs(alignment_dir, exist_ok=True)

    candidate_name = os.path.basename(base_candidate_dir).lower()
    final_filename = f"{candidate_name}_{job_slug}_role_alignment.json"
    final_path = os.path.join(alignment_dir, final_filename)
    # ---------------------------------------

    # --- SKIP LOGIC ---
    if os.path.exists(final_path):
        print(f"Agent 2_1: Skip - {final_path} already exists.")
        return 
    # ------------------

    client = genai.Client()
    
    # File paths
    questions_path = os.path.join(base_posting_dir, "questions.json")
    posting_path = os.path.join(base_posting_dir, "posting.txt")
    resume_path = os.path.join(base_candidate_dir, "resume.md")
    experiences_path = os.path.join(base_candidate_dir, "experiences.md")
    prompt_path = "prompts/candidate-evaluator-prompt.txt"

    # Validation
    for p in [questions_path, posting_path, resume_path, experiences_path, prompt_path]:
        if not os.path.exists(p):
            print(f"Error: Required file not found: {p}")
            sys.exit(1)

    # Load All Inputs
    with open(questions_path, "r") as f: questions_json = f.read()
    with open(resume_path, "r") as f: resume_text = f.read()
    with open(experiences_path, "r") as f: experiences_text = f.read()
    with open(posting_path, "r") as f: posting_text = f.read()
    with open(prompt_path, "r") as f: prompt_template = f.read()

    print(f"Agent 2_1: Auditing alignment for {job_slug}...")

    full_request = (
        f"{prompt_template}\n\n"
        f"### REQUIREMENTS:\n{questions_json}\n\n"
        f"### RESUME:\n{resume_text}\n\n"
        f"### DETAILED STAR EXPERIENCES:\n{experiences_text}\n\n"
        f"### POSTING CONTEXT:\n{posting_text}"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            #model="gemini-3-flash-preview",
            contents=full_request,
            config={
                'response_mime_type': 'application/json', 
                'response_schema': list[Evaluation]
            }
        )
        
        with open(final_path, "w") as f:
            json.dump(json.loads(response.text), f, indent=4)

        print(f"Success! Alignment saved: {final_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
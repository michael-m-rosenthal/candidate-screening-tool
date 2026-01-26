import sys
import os
import json
import argparse
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
    parser = argparse.ArgumentParser(description="Agent 2: Candidate Evaluator")
    parser.add_argument("posting_directory", help="Directory containing posting.txt and questions.json")
    parser.add_argument(
        "candidate_directory", 
        nargs='?', 
        help="Optional: Directory containing resume.md (defaults to posting_directory)"
    )
    args = parser.parse_args()

    # Fallback logic for optional directory
    candidate_dir = args.candidate_directory if args.candidate_directory else args.posting_directory
    
    # Absolute paths for reliability
    base_posting_dir = os.path.abspath(args.posting_directory)
    base_candidate_dir = os.path.abspath(candidate_dir)

    client = genai.Client()
    
    # Define file paths
    questions_path = os.path.join(base_posting_dir, "questions.json")
    posting_path = os.path.join(base_posting_dir, "posting.txt")
    resume_path = os.path.join(base_candidate_dir, "resume.md")
    prompt_path = "prompts/candidate-evaluator-prompt.txt"

    # Validation: Ensure required files exist
    for p in [questions_path, posting_path, resume_path, prompt_path]:
        if not os.path.exists(p):
            print(f"Error: Required file not found: {p}")
            sys.exit(1)

    # Load All Inputs
    with open(questions_path, "r") as f: questions_json = f.read()
    with open(resume_path, "r") as f: resume_text = f.read()
    with open(posting_path, "r") as f: posting_text = f.read()
    with open(prompt_path, "r") as f: prompt_template = f.read()

    print(f"Agent 1_2: Auditing resume at {resume_path} against {base_posting_dir}...")

    full_request = (
        f"{prompt_template}\n\n"
        f"### REQUIREMENTS:\n{questions_json}\n\n"
        f"### RESUME:\n{resume_text}\n\n"
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

        # Output to the candidate directory
        final_path = os.path.join(base_candidate_dir, "candidate_evaluation.json")
        with open(final_path, "w") as f:
            json.dump(json.loads(response.text), f, indent=4)

        print(f"Success! Evaluation complete: {final_path}")

    except Exception as e:
        print(f"Error during API generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
import sys
import os
import json
import argparse
from google import genai
from pydantic import BaseModel, Field
from typing import Literal

# The schema for the AI's response per question
class ScreeningResult(BaseModel):
    category: str
    question: str
    answer: Literal["Yes", "No"]
    evidence: str = Field(description="Direct quote or specific observation from the posting.")
    risk_level: str

def main():
    parser = argparse.ArgumentParser(description="Screen a job posting for red flags.")
    parser.add_argument("posting_directory")
    args = parser.parse_args()

    # Path Setup
    posting_path = os.path.join(args.posting_directory, "posting.txt")
    base_dir = os.path.dirname(posting_path)
    output_path = os.path.join(base_dir, "screening_report.json")

    # --- SKIP LOGIC ---
    if os.path.exists(output_path):
        print(f"Agent 0_1: Skip - {output_path} already exists.")
        return 
    # ------------------

    client = genai.Client()

    # Assume prompts directory is in the current working directory
    prompts_dir = os.path.join(os.getcwd(), "prompts")
    master_questions_path = os.path.join(prompts_dir, "screening_questions_master.json")
    prompt_template_path = os.path.join(prompts_dir, "job-screening-prompt.txt")

    # Load All Inputs
    try:
        with open(master_questions_path, "r") as f:
            master_questions = f.read()
        with open(prompt_template_path, "r") as f:
            prompt_template = f.read()
        with open(posting_path, "r") as f:
            posting_content = f.read()
    except FileNotFoundError as e:
        print(f"Error: Required file not found: {e}")
        sys.exit(1)

    print(f"Agent 0_1: Screening {posting_path} using master criteria...")

    # Construct the request with the JSON questions injected
    full_request = (
        f"{prompt_template}\n\n"
        f"### MASTER SCREENING QUESTIONS (JSON):\n{master_questions}\n\n"
        f"### JOB POSTING TO ANALYZE:\n{posting_content}"
    )

    try:
        response = client.models.generate_content(
            #model="gemini-2.5-flash",
            model="gemini-3-flash-preview",
            contents=full_request,
            config={
                'response_mime_type': 'application/json',
                'response_schema': list[ScreeningResult]
            }
        )
        
        results = json.loads(response.text)
        
        # Save output in the SAME directory as the posting.txt
        with open(output_path, "w") as f:
            json.dump(results, f, indent=4)

        # Quick summary for the console
        red_flags = len([q for q in results if q['answer'] == 'Yes'])
        print(f"Success! {red_flags} potential red flags identified.")
        print(f"Report written to: {output_path}")

    except Exception as e:
        print(f"Error during API call: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
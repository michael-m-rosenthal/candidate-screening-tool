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
    parser = argparse.ArgumentParser()
    parser.add_argument("posting_directory")
    args = parser.parse_args()

    client = genai.Client()
    directory = os.path.dirname(args.posting_directory)
    questions_path = os.path.join(directory, "questions.json")
    posting_path = os.path.join(directory, "posting.txt")
    resume_path = os.path.join(directory, "resume.md")

    # Load All Inputs
    with open(questions_path, "r") as f: questions_json = f.read()
    with open(resume_path, "r") as f: resume_text = f.read()
    with open(posting_path, "r") as f: posting_text = f.read()
    with open("prompts/candidate-evaluator-prompt.txt", "r") as f: prompt_template = f.read()

    print(f"Agent 2: Auditing resume {resume_path}...")

    full_request = (
        f"{prompt_template}\n\n"
        f"### REQUIREMENTS:\n{questions_json}\n\n"
        f"### RESUME:\n{resume_text}\n\n"
        f"### POSTING CONTEXT:\n{posting_text}"
    )

    response = client.models.generate_content(
        #model="gemini-2.5-flash",
        model="gemini-3-flash-preview",
        contents=full_request,
        config={'response_mime_type': 'application/json', 'response_schema': list[Evaluation]}
    )

    final_path = os.path.join(directory, "candidate_evaluation.json")
    with open(final_path, "w") as f:
        json.dump(json.loads(response.text), f, indent=4)

    print(f"Success! Evaluation complete: {final_path}")

if __name__ == "__main__":
    main()
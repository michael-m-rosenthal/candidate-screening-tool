import sys
import os
import json
import argparse
from google import genai
from pydantic import BaseModel, Field
from typing import Literal

class BinaryRequirement(BaseModel):
    question: str = Field(description="Yes/No question for the skill.")
    requirement: str = Field(description="Original snippet from the job posting.")
    priority: Literal["Core", "Preferred"]
    answer: str = "No"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("posting_directory")
    args = parser.parse_args()

    client = genai.Client()
    #questions_path = os.path.join(directory, "questions.json")
    posting_path = os.path.join(args.posting_directory, "posting.txt")

    # Define output path for the skip check
    output_directory = os.path.dirname(os.path.abspath(posting_path))
    output_path = os.path.join(output_directory, "questions.json")

    # --- SKIP LOGIC ---
    if os.path.exists(output_path):
        print(f"Agent 1_1: Skip - {output_path} already exists.")
        return 
    # ------------------

    with open("prompts/job-requirement-analyzer-prompt.txt", "r") as f:
        prompt = f.read()
    with open(posting_path, "r") as f:
        posting = f.read()

    print(f"Agent 1: Extracting requirements from {posting_path}...")
    
    response = client.models.generate_content(
        #model="gemini-2.5-flash",
        model="gemini-3-flash-preview",
        contents=f"{prompt}\n\n[JOB POSTING]:\n{posting}",
        config={'response_mime_type': 'application/json', 'response_schema': list[BinaryRequirement]}
    )

    with open(output_path, "w") as f:
        json.dump(json.loads(response.text), f, indent=4)

    print(f"Success! Created: {output_path}")

if __name__ == "__main__":
    main()
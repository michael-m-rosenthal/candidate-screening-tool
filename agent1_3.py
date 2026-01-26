import sys
import os
import json
import argparse
from google import genai
from pydantic import BaseModel, Field
from typing import Literal

# Schema for the Agent 3 result
class FitnessSummary(BaseModel):
    fit_percentage: float
    recommendation: Literal["Strong Fit", "Potential Fit", "Not a Match"]
    markdown_content: str = Field(description="The full executive summary in Markdown format.")

def main():
    parser = argparse.ArgumentParser(description="Agent 3: Synthesize Executive Summary")
    parser.add_argument("posting_directory", help="Directory containing the job posting details")
    parser.add_argument(
        "candidate_directory", 
        nargs='?', 
        help="Optional: Directory containing candidate evaluation data (defaults to posting_directory)"
    )
    args = parser.parse_args()

    # If candidate_directory is not provided, use posting_directory
    candidate_dir = args.candidate_directory if args.candidate_directory else args.posting_directory

    client = genai.Client()
    
    # Using abspath for reliability
    base_posting_dir = os.path.abspath(args.posting_directory)
    base_candidate_dir = os.path.abspath(candidate_dir)
    
    # The evaluation data (input) comes from the candidate directory
    evaluation_path = os.path.join(base_candidate_dir, "candidate_evaluation.json")
    prompt_path = "prompts/executive-summary-prompt.txt"

    # Load Inputs
    if not os.path.exists(evaluation_path):
        print(f"Error: {evaluation_path} not found. Ensure Agent 2 has run.")
        sys.exit(1)

    with open(evaluation_path, "r") as f: 
        eval_data = f.read()
    
    if not os.path.exists(prompt_path):
        print(f"Error: Prompt template not found at {prompt_path}")
        sys.exit(1)
        
    with open(prompt_path, "r") as f: 
        prompt_template = f.read()

    print(f"Agent 1_3: Synthesizing Markdown summary...")
    print(f"  Postings:  {base_posting_dir}")
    print(f"  Candidate: {base_candidate_dir}")

    full_request = (
        f"{prompt_template}\n\n"
        f"### CANDIDATE EVALUATION DATA:\n{eval_data}"
    )

    try:
        # Note: Using the model version specified in your snippet
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            #model="gemini-3-flash-preview",
            contents=full_request,
            config={
                'response_mime_type': 'application/json', 
                'response_schema': FitnessSummary
            }
        )
        
        # Parse result
        result = json.loads(response.text)
        
        # Save as Markdown file in the candidate directory
        output_path = os.path.join(base_candidate_dir, "executive_summary.md")
        with open(output_path, "w") as f:
            f.write(result['markdown_content'])

        print(f"Success! Executive summary written to: {output_path}")
        print(f"Result: {result['recommendation']} ({result['fit_percentage']}%)")

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
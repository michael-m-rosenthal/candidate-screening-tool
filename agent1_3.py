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
    parser = argparse.ArgumentParser(description="Agent 1_3: Synthesize Executive Summary")
    parser.add_argument("posting_directory", help="Directory containing the job posting details")
    parser.add_argument(
        "candidate_directory", 
        help="Directory containing the candidate's original resume/context"
    )
    args = parser.parse_args()

    client = genai.Client()
    
    # Using abspath for reliability
    base_posting_dir = os.path.abspath(args.posting_directory)
    base_candidate_dir = os.path.abspath(args.candidate_directory)
    
    # Get candidate name from the folder name
    candidate_name = os.path.basename(base_candidate_dir)

    # Input logic: Look in posting_dir/evaluations/candidate_name_evaluation.json
    evaluation_path = os.path.join(base_posting_dir, "evaluations", f"{candidate_name}_evaluation.json")
    prompt_path = "prompts/executive-summary-prompt.txt"

    # Load Inputs
    if not os.path.exists(evaluation_path):
        print(f"Error: {evaluation_path} not found. Ensure Agent 1_2 has run.")
        sys.exit(1)

    with open(evaluation_path, "r") as f: 
        eval_data = f.read()
    
    if not os.path.exists(prompt_path):
        print(f"Error: Prompt template not found at {prompt_path}")
        sys.exit(1)
        
    with open(prompt_path, "r") as f: 
        prompt_template = f.read()

    print(f"Agent 1_3: Synthesizing Markdown summary for {candidate_name}...")

    full_request = (
        f"{prompt_template}\n\n"
        f"### CANDIDATE EVALUATION DATA:\n{eval_data}"
    )

    try:
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
        
        # Setup the output sub-directory within the posting directory
        summary_output_dir = os.path.join(base_posting_dir, "summaries")
        os.makedirs(summary_output_dir, exist_ok=True)

        # Save as Markdown file in the summaries directory with unique name
        final_filename = f"{candidate_name}_summary.md"
        output_path = os.path.join(summary_output_dir, final_filename)
        
        with open(output_path, "w") as f:
            f.write(result['markdown_content'])

        print(f"Success! Executive summary written to: {output_path}")
        print(f"Result: {result['recommendation']} ({result['fit_percentage']}%)")

        # List all summaries alphabetically
        all_summaries = sorted([f for f in os.listdir(summary_output_dir) if f.endswith("_summary.md")])
        print(f"All summaries in {summary_output_dir}: {all_summaries}")

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
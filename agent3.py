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
    parser = argparse.ArgumentParser()
    parser.add_argument("posting_directory")
    args = parser.parse_args()

    client = genai.Client()
    
    # Using abspath for reliability
    base_dir = os.path.abspath(args.posting_directory)
    evaluation_path = os.path.join(base_dir, "candidate_evaluation.json")
    prompt_path = "prompts/executive-summary-prompt.txt"

    # Load Inputs
    if not os.path.exists(evaluation_path):
        print(f"Error: {evaluation_path} not found. Ensure Agent 2 has run.")
        sys.exit(1)

    with open(evaluation_path, "r") as f: 
        eval_data = f.read()
    with open(prompt_path, "r") as f: 
        prompt_template = f.read()

    print(f"Agent 3: Synthesizing Markdown summary for {base_dir}...")

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
        
        # Save as Markdown file
        output_path = os.path.join(base_dir, "executive_summary.md")
        with open(output_path, "w") as f:
            f.write(result['markdown_content'])

        print(f"Success! Executive summary written to: {output_path}")
        print(f"Result: {result['recommendation']} ({result['fit_percentage']}%)")

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
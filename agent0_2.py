import sys
import os
import json
import argparse
from google import genai
from pydantic import BaseModel, Field
from typing import Literal

class ScreeningSummary(BaseModel):
    futility_score: float
    verdict: Literal["GO", "CAUTION", "NO-GO"]
    markdown_content: str = Field(description="The full summary in Markdown format.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("posting_directory")
    args = parser.parse_args()

    client = genai.Client()

    # Path Setup
    posting_path = os.path.join(args.posting_directory, "posting.txt")
    base_dir = os.path.dirname(posting_path)
    report_path = os.path.join(base_dir, "screening_report.json")
    
    prompts_dir = os.path.join(os.getcwd(), "prompts")
    prompt_template_path = os.path.join(prompts_dir, "screening-summary-prompt.txt")

    if not os.path.exists(report_path):
        print(f"Error: {report_path} not found. Run Agent 0 first.")
        sys.exit(1)

    with open(report_path, "r") as f:
        report_data = f.read()
    with open(prompt_template_path, "r") as f:
        prompt_template = f.read()

    print(f"Agent 0.5: Summarizing screening for {base_dir}...")

    full_request = (
        f"{prompt_template}\n\n"
        f"### SCREENING DATA:\n{report_data}"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        #model="gemini-3-flash-preview",
        contents=full_request,
        config={
            'response_mime_type': 'application/json',
            'response_schema': ScreeningSummary
        }
    )
    
    result = json.loads(response.text)
    output_path = os.path.join(base_dir, "screening_summary.md")
    with open(output_path, "w") as f:
        f.write(result['markdown_content'])

    print(f"Success! Markdown verdict saved to: {output_path}")

if __name__ == "__main__":
    main()
import sys
import os
import json
import argparse
from google import genai
from pydantic import BaseModel, Field

# Schema for the product profile
class ProductProfile(BaseModel):
    product_name: str
    target_audience: str
    core_problem_solved: str
    technical_stack_mentioned: list[str]
    product_maturity: str = Field(description="e.g., MVP, Scaling, Legacy, R&D")
    markdown_summary: str = Field(description="A concise 2-paragraph description of the product.")

def main():
    parser = argparse.ArgumentParser(description="Agent 0_3: Product Profiler")
    parser.add_argument("posting_directory")
    args = parser.parse_args()

    # Path Setup
    base_dir = os.path.abspath(args.posting_directory)
    posting_path = os.path.join(base_dir, "posting.txt")
    context_path = os.path.join(base_dir, "product_info.txt") # Optional user-provided context
    output_path = os.path.join(base_dir, "product_profile.json")

    # --- SKIP LOGIC ---
    if os.path.exists(output_path):
        print(f"Agent 0_3: Skip - {output_path} already exists.")
        return 
    # ------------------

    client = genai.Client()

    # Load All Inputs
    try:
        with open(posting_path, "r") as f:
            posting_content = f.read()
        
        # Check for optional manual context
        extra_context = ""
        if os.path.exists(context_path):
            with open(context_path, "r") as f:
                extra_context = f.read()
                print(f"Agent 0_3: Found additional product context at {context_path}")

        with open("prompts/product-profiler-prompt.txt", "r") as f:
            prompt_template = f.read()
    except FileNotFoundError as e:
        print(f"Error: Required file not found: {e}")
        sys.exit(1)

    print(f"Agent 0_3: Profiling product for {base_dir}...")

    full_request = (
        f"{prompt_template}\n\n"
        f"### JOB POSTING:\n{posting_content}\n\n"
        f"### USER-PROVIDED PRODUCT CONTEXT:\n{extra_context if extra_context else 'No additional context provided.'}\n\n"
        "INSTRUCTION: Use ONLY the provided Job Posting and Product Context. If details are missing, state 'Not specified' rather than hallucinating."
    )

    try:
        response = client.models.generate_content(
            #model="gemini-2.5-flash",
            model="gemini-3-flash-preview",
            contents=full_request,
            config={
                'response_mime_type': 'application/json',
                'response_schema': ProductProfile
            }
        )
        
        result = json.loads(response.text)
        
        with open(output_path, "w") as f:
            json.dump(result, f, indent=4)

        print(f"Success! Product profile saved to: {output_path}")

    except Exception as e:
        print(f"Error during API call: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
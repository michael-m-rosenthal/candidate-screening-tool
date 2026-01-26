#!/bin/bash

# Ensure we have the necessary API Key
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY is not set."
    echo "Please run: export GEMINI_API_KEY='your_api_key_here'"
    exit 1
fi

echo "🚀 Starting Resume Intelligence Pipeline..."

# 1. Find all Job Postings
# Logic: Look for any 'posting.txt' file. Its parent directory is the root.
find postings -name "posting.txt" -print0 | while IFS= read -r -d '' posting_path; do
    job_dir=$(dirname "$posting_path")
    echo "------------------------------------------------"
    echo "📂 Processing Job: $job_dir"
    echo "------------------------------------------------"
    
    # Phase 0: Screening
    python3 agent0_1.py "$job_dir"
    python3 agent0_2.py "$job_dir"

    # Phase 1: Requirement Extraction
    python3 agent1_1.py "$job_dir"

    # 2. Iterate through all Candidates for this job
    find candidates -name "resume.md" -print0 | while IFS= read -r -d '' resume_path; do
        candidate_dir=$(dirname "$resume_path")
        candidate_name=$(basename "$candidate_dir")
        
        echo "  🔍 Auditing Candidate: $candidate_name"

        # Phase 1: Audit & Executive Summary
        python3 agent1_2.py "$job_dir" "$candidate_dir"
        python3 agent1_3.py "$job_dir" "$candidate_dir"
    done
done

echo "✅ Pipeline Complete."
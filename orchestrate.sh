#!/bin/bash

# Traverse: postings / company / job / posting.txt
for posting in postings/*/*/posting.txt; do
    job_dir=$(dirname "$posting")
    echo "Processing Job: $job_dir"

    # Phase 0 & Agent 1.1
    python agent0_1.py "$job_dir"
    python agent0_2.py "$job_dir"
    python agent1_1.py "$job_dir"

    # Traverse: candidates / candidate_dir / resume.md
    for resume in candidates/*/resume.md; do
        candidate_dir=$(dirname "$resume")
        echo "  - Auditing: $(basename "$candidate_dir")"

        # Phase 1: Audit & Summary
        python agent2.py "$job_dir" "$candidate_dir"
        python agent1_3.py "$job_dir" "$candidate_dir"
    done
done
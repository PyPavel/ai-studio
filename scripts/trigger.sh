#!/bin/bash
# trigger.sh — On-demand trigger for any studio agent
# Usage: ./scripts/trigger.sh <analyst|rnd|pm|senior|junior>

set -e

STUDIO_DIR=$(cd "$(dirname "$0")/.." && pwd)
STUDIO_NAME=$(grep "name:" "$STUDIO_DIR/config/studio.yaml" | head -1 | cut -d'"' -f2)

if [ $# -ne 1 ]; then
    echo "Usage: $0 <agent_role>"
    echo "Available roles: analyst, rnd, pm, senior, junior"
    exit 1
fi

ROLE=$1
JOB_NAME="$STUDIO_NAME ${ROLE^}"

echo "Looking for job: '$JOB_NAME'..."

# Find the job ID using hermes cron list
JOB_ID=$(hermes cron list --json | python3 -c "
import sys, json
target = sys.argv[1].lower()
data = json.load(sys.stdin)
for job in data.get('jobs', []):
    if job.get('name', '').lower() == target:
        print(job['job_id'])
        break
" "$JOB_NAME")

if [ -z "$JOB_ID" ]; then
    echo "Error: Could not find job ID for '$JOB_NAME'."
    echo "Make sure you have run scripts/setup.py first."
    exit 1
fi

echo "Triggering job $JOB_ID ($JOB_NAME)..."
hermes cron run "$JOB_ID"
echo "Job triggered successfully."

#!/bin/bash
# setup_studio.sh — Bootstrap a new AI Studio from config

set -e

STUDIO_DIR=$(pwd)
CONFIG_FILE="$STUDIO_DIR/config/studio.yaml"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: config/studio.yaml not found. Copy config/studio.yaml.example and edit it."
    exit 1
fi

# Ensure directories exist
mkdir -p data/reports/analyst

# 1. Update paths in config (hacky but works)
# We add data_dir and project_dir to config dynamically
echo "paths:" >> "$CONFIG_FILE"
echo "  data_dir: \"$STUDIO_DIR/data\"" >> "$CONFIG_FILE"
echo "  project_dir: \"$STUDIO_DIR\"" >> "$CONFIG_FILE"

# 2. Render data templates
echo "Bootstrapping data files..."
python3 scripts/render_prompts.py analyst "$CONFIG_FILE" data/reports/analyst/init_report.md
sed -e "s/\${STUDIO_NAME}/$(grep 'name:' "$CONFIG_FILE" | head -1 | cut -d' ' -f2- | tr -d '"')/g" \
    -e "s/\${DOMAINS}/$(grep -A 10 'domains:' "$CONFIG_FILE" | grep '-' | cut -d' ' -f4- | tr '\n' ',' | sed 's/,$//')/g" \
    templates/data/user_directives.md.tpl > data/user_directives.md

sed -e "s/\${PROJECT_NAME}/$(grep 'name:' "$CONFIG_FILE" | head -2 | tail -1 | cut -d' ' -f2- | tr -d '"')/g" \
    -e "s/\${PROJECT_DESCRIPTION}/$(grep -A 1 'description:' "$CONFIG_FILE" | tail -1 | cut -d' ' -f2- | tr -d '"')/g" \
    templates/data/studio_memory.md.tpl > data/studio_memory.md

cp templates/data/product_requirements.md.tpl data/product_requirements.md
touch data/sprint_results.md

# 3. Generate and install cron jobs
echo "Installing agent cron jobs..."

install_agent() {
    ROLE=$1
    NAME=$2
    SCHEDULE=$3
    SKILLS=$4
    PROMPT_FILE="data/rendered_prompt_$ROLE.md"

    # Render prompt
    python3 scripts/render_prompts.py "$ROLE" "$CONFIG_FILE" "$PROMPT_FILE"
    
    # Create/Update cron job
    # We use 'hermes cron' (cli interface to cronjob tool)
    hermes cron create \
        --name "$NAME" \
        --schedule "$SCHEDULE" \
        --prompt "$(cat "$PROMPT_FILE")" \
        --skills "$SKILLS" \
        --deliver all \
        --enabled-toolsets terminal,web,file,search,skills
}

# Read config values using python (simpler than bash/grep)
PY_CMD="import yaml; cfg=yaml.safe_load(open('$CONFIG_FILE'));"

ANALYST_SCHED=$(python3 -c "$PY_CMD print(cfg['schedule']['analyst'])")
RND_SCHED=$(python3 -c "$PY_CMD print(cfg['schedule']['rnd'])")
PM_SCHED=$(python3 -c "$PY_CMD print(cfg['schedule']['pm'])")
SENIOR_SCHED=$(python3 -c "$PY_CMD print(cfg['schedule']['senior'])")
JUNIOR_SCHED=$(python3 -c "$PY_CMD print(cfg['schedule']['junior'])")

ANALYST_SKILLS=$(python3 -c "$PY_CMD print(','.join(cfg['skills']['analyst']))")
RND_SKILLS=$(python3 -c "$PY_CMD print(','.join(cfg['skills']['rnd']))")
PM_SKILLS=$(python3 -c "$PY_CMD print(','.join(cfg['skills']['pm']))")
SENIOR_SKILLS=$(python3 -c "$PY_CMD print(','.join(cfg['skills']['senior']))")
JUNIOR_SKILLS=$(python3 -c "$PY_CMD print(','.join(cfg['skills']['junior']))")

STUDIO_NAME=$(python3 -c "$PY_CMD print(cfg['studio']['name'])")

install_agent analyst "$STUDIO_NAME Analyst" "$ANALYST_SCHED" "$ANALYST_SKILLS"
install_agent rnd "$STUDIO_NAME R&D" "$RND_SCHED" "$RND_SKILLS"
install_agent pm "$STUDIO_NAME PM" "$PM_SCHED" "$PM_SKILLS"
install_agent senior "$STUDIO_NAME Senior" "$SENIOR_SCHED" "$SENIOR_SKILLS"
install_agent junior "$STUDIO_NAME Junior" "$JUNIOR_SCHED" "$JUNIOR_SKILLS"

echo "Setup complete! Studio '$STUDIO_NAME' is active."
echo "Check data/user_directives.md to start giving orders."

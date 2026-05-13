#!/usr/bin/env python3
"""
Bootstrap an AI Studio from config/studio.yaml
Usage: python3 scripts/setup.py
"""
import yaml
import subprocess
import sys
import os
from pathlib import Path

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True).strip()

STUDIO_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = STUDIO_DIR / "config" / "studio.yaml"
DATA_DIR = STUDIO_DIR / "data"

def load_config():
    with open(CONFIG_FILE) as f:
        cfg = yaml.safe_load(f)
    # Inject paths
    cfg["paths"] = {
        "data_dir": str(DATA_DIR),
        "project_dir": str(STUDIO_DIR),
        "studio_dir": str(STUDIO_DIR),
    }
    return cfg

def render_template(template_path, cfg, output_path):
    with open(template_path) as f:
        content = f.read()

    studio = cfg.get("studio", {})
    project = cfg.get("project", {})
    data_dir = cfg["paths"]["data_dir"]
    project_dir = cfg["paths"]["project_dir"]

    health_checks = "\n".join(f"   - {h['name']}: {h['url']}" for h in cfg.get("health", []))
    domains = " | ".join(project.get("domains", ["studio"]))
    research_domains = "\n".join(f"- {d}" for d in project.get("domains", []))

    content = content.replace("${STUDIO_NAME}", studio.get("name", "AI Studio"))
    content = content.replace("${PROJECT_NAME}", project.get("name", "Untitled"))
    content = content.replace("${PROJECT_DESCRIPTION}", project.get("description", ""))
    content = content.replace("${DOMAINS}", domains)
    content = content.replace("${DATA_DIR}", data_dir)
    content = content.replace("${PROJECT_DIR}", project_dir)
    content = content.replace("${HEALTH_CHECKS}", health_checks)
    content = content.replace("${RESEARCH_DOMAINS}", research_domains)

    with open(output_path, "w") as f:
        f.write(content)
    print(f"  ✓ {output_path}")

def bootstrap_data(cfg):
    print("Bootstrapping data files...")
    DATA_DIR.mkdir(exist_ok=True)
    (DATA_DIR / "reports" / "analyst").mkdir(parents=True, exist_ok=True)

    # Render templates
    render_template(STUDIO_DIR / "templates" / "data" / "user_directives.md.tpl", cfg, DATA_DIR / "user_directives.md")
    render_template(STUDIO_DIR / "templates" / "data" / "studio_memory.md.tpl", cfg, DATA_DIR / "studio_memory.md")
    render_template(STUDIO_DIR / "templates" / "data" / "product_requirements.md.tpl", cfg, DATA_DIR / "product_requirements.md")

    # Touch sprint_results
    (DATA_DIR / "sprint_results.md").touch()
    print(f"  ✓ data/ directory ready")

def create_cron_job(role, cfg):
    studio_name = cfg["studio"]["name"]
    job_name = f"{studio_name} {role.capitalize()}"
    schedule = cfg["schedule"][role]
    skills = cfg["skills"][role]

    # Render prompt to temp file
    prompt_file = DATA_DIR / f"rendered_prompt_{role}.md"
    render_template(STUDIO_DIR / "templates" / "prompts" / f"{role}.md", cfg, prompt_file)

    with open(prompt_file) as f:
        prompt = f.read()

    # Build skills string
    skills_str = ",".join(skills)

    # Check if job exists already
    try:
        list_output = subprocess.check_output("hermes cron list --json 2>/dev/null || true", shell=True, text=True)
        jobs = yaml.safe_load(list_output) if list_output.strip() else {"jobs": []}
        existing = [j for j in jobs.get("jobs", []) if j.get("name") == job_name]
        if existing:
            print(f"  ↳ Updating existing job: {job_name}")
            job_id = existing[0]["job_id"]
            subprocess.run(f'hermes cron update --id "{job_id}" --prompt """{prompt}""" --skills "{skills_str}"', shell=True, check=False)
            return
    except Exception:
        pass

    # Create new job
    print(f"  ✓ Creating cron job: {job_name} @ {schedule}")
    try:
        subprocess.run(
            f'hermes cron create --name "{job_name}" --schedule "{schedule}" '
            f'--prompt """{prompt}""" --skills "{skills_str}" --deliver all --enabled-toolsets terminal,web,file,search,skills',
            shell=True, check=False
        )
    except Exception as e:
        print(f"  ⚠ Failed to create cron job (may require manual setup): {e}")

def install_cron_jobs(cfg):
    print("Installing agent cron jobs...")
    for role in ["analyst", "rnd", "pm", "senior", "junior"]:
        create_cron_job(role, cfg)

def main():
    if not CONFIG_FILE.exists():
        print(f"Error: {CONFIG_FILE} not found. Copy from config/studio.yaml.example and edit.")
        sys.exit(1)

    cfg = load_config()
    studio_name = cfg["studio"]["name"]
    print(f"")
    print(f"  ┌{'─' * (len(studio_name) + 28)}┐")
    print(f"  │ AI Studio Factory: {studio_name} │")
    print(f"  └{'─' * (len(studio_name) + 28)}┘")
    print(f"")

    bootstrap_data(cfg)
    install_cron_jobs(cfg)

    print(f"")
    print(f"  ✅ Studio '{studio_name}' is bootstrapped and active!")
    print(f"")
    print(f"  Next steps:")
    print(f"    1. Write directives to: {DATA_DIR}/user_directives.md")
    print(f"    2. Run agents manually: hermes cron run <job_id>")
    print(f"    3. Check reports in: {DATA_DIR}/reports/")
    print(f"")

if __name__ == "__main__":
    main()

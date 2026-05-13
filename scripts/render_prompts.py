#!/usr/bin/env python3
"""
Renders prompt templates with studio config values.
Usage: python3 render_prompts.py <role> <config.yaml> <output.md>
"""
import sys
import yaml
from string import Template

def render(role: str, config_path: str) -> str:
    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    studio = cfg.get("studio", {})
    project = cfg.get("project", {})
    data_dir = cfg.get("paths", {}).get("data_dir", "./data")
    project_dir = cfg.get("paths", {}).get("project_dir", ".")

    health_checks = []
    for h in cfg.get("health", []):
        health_checks.append(f"   - {h['name']}: {h['url']}")
    health_checks_str = "\n".join(health_checks)

    domains = ", ".join(project.get("domains", ["studio"]))
    research_domains = "\n".join(f"- {d}" for d in project.get("domains", []))

    with open(f"templates/prompts/{role}.md") as f:
        tpl = f.read()

    # Basic substitution
    result = tpl.replace("${STUDIO_NAME}", studio.get("name", "AI Studio"))
    result = result.replace("${PROJECT_NAME}", project.get("name", "Untitled Project"))
    result = result.replace("${PROJECT_DESCRIPTION}", project.get("description", ""))
    result = result.replace("${DOMAINS}", domains)
    result = result.replace("${DATA_DIR}", data_dir)
    result = result.replace("${PROJECT_DIR}", project_dir)
    result = result.replace("${HEALTH_CHECKS}", health_checks_str)
    result = result.replace("${RESEARCH_DOMAINS}", research_domains)

    return result

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 render_prompts.py <role> <config.yaml> <output.md>")
        sys.exit(1)

    role = sys.argv[1]
    config = sys.argv[2]
    output = sys.argv[3]

    rendered = render(role, config)
    with open(output, "w") as f:
        f.write(rendered)
    print(f"Rendered {role} prompt to {output}")

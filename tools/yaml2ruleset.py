import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import sys

# Load the YAML file
with open("RuleSet.yaml") as f:
    config = yaml.safe_load(f)

# Set up the Jinja2 environment to load templates from the current directory
env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True, undefined=StrictUndefined)

# Load the template
template = env.get_template("yaml2ruleset.j2")

#print(config)
#sys.exit()

# Render the template with YAML data
ruleset_output = template.render(config).strip()

# Write to output file
with open("output.ruleset", "w") as f:
    f.write(ruleset_output.strip() + "\n")

print("RuleSet generated in output.ruleset")
from jinja2 import Template
import os
import sys
import subprocess

# Define a Jinja2 template for a PBS submission script
pbs_template = """
#!/bin/bash
#PBS -N {{ job_name }}
#PBS -l nodes={{ num_nodes }}:ppn={{ ppn }}
#PBS -l walltime={{ walltime }}
#PBS -o {{ output_file }}
#PBS -e {{ error_file }}
#PBS -q {{ queue }}
#PBS -A {{ account }}
#PBS -M {{ email }}
#PBS -m {{ email_type }}
{{ additional_directives }}
{{ command }}
"""

slurm_template = """
#!/bin/bash
#SBATCH --job-name={{ job_name }}
#SBATCH --nodes={{ num_nodes }}
#SBATCH --ntasks-per-node={{ ppn }}
#SBATCH --time={{ walltime }}
#SBATCH --output={{ output_file }}
#SBATCH --error={{ error_file }}
#SBATCH -A {{ account }}
#SBATCH --mail-user={{ email }}
#SBATCH --mail-type={{ email_type }}
{{ additional_directives }}
{{ command }}
"""

default_inputs: dict = {
    "mail_user": "MAIL",
    "account": "ACCOUNT",
    "queue": "QUEUE",
    "email_type": "EMAIL_TYPE",
    "walltime": "WALLTIME",
    "num_nodes": "NODES",
    "ppn": "PPN",
    "job_name": "JOB_NAME",
    "output_file": "OUTPUT_FILE",
    "error_file": "ERROR_FILE",
    "command": "COMMAND",
    "additional_directives": "ADDITIONAL_DIRECTIVES",
}


def get_group_names():
    try:
        # Run the 'id -Gn' command and capture its output
        result = subprocess.run(
            ["id", "-Gn"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        # Split the output by spaces and return the group names as a list
        group_names = result.stdout.strip().split()

        # Print the group names
        print("Group Names:", group_names)

        return group_names

    except subprocess.CalledProcessError:
        print("Error: Unable to get group names.")
        return []


def create_template(template, template_variables):
    """Creates a template from a template string"""
    template = Template(template)
    return template.render(template_variables)


def check_env_for_default_inputs() -> dict:
    """Checks to see if the user env has default inputs"""

    default_inputs_found = {}

    for key, value in default_inputs.items():
        if value in os.environ:
            default_inputs_found[key] = os.environ[value]

    return default_inputs_found


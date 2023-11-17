from jinja2 import Template
import os
import subprocess

pbs_template = """
#!/bin/bash
#PBS -l nodes={{ nodes }}:ppn={{ ppn }}
#PBS -l walltime={{ walltime }}
#PBS -q {{ queue }}
{% if job_name %}#PBS -N {{ job_name }}{% endif %}
{% if account %}#PBS -A {{ account }}{% endif %}
{% if mail %}#PBS -M {{ mail }}{% endif %}
{% if email_type %}#PBS -m {{ email_type }}{% endif %}
{{ directives }}
"""

slurm_template = """
#!/bin/bash
#SBATCH --nodes={{ nodes }}
#SBATCH --ntasks-per-node={{ ppn }}
#SBATCH --time={{ walltime }}
{% if job_name %}#SBATCH --job-name={{ job_name }}{% endif %}
{% if account %}#PBS -A {{ account }}{% endif %}
{% if mail %}#SBATCH --mail-user={{ mail }}{% endif %}
{% if email_type %}}#SBATCH --mail-type={{ email_type }}{% endif %}
{{ directives }}
"""

default_inputs: dict = {
    "mail": "MAIL",
    "account": "ACCOUNT",
    "queue": "QUEUE",
    "email_type": "EMAIL_TYPE",
    "walltime": "WALLTIME",
    "nodes": "NODES",
    "ppn": "PPN",
    "job_name": "JOB_NAME",
    "directives": "DIRECTIVES",
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


def create_submission_file(args):
    """Creates a submission file with user supplied inputs"""
    # Get the default inputs from the environment
    default_inputs_found = check_env_for_default_inputs()

    # Create a dictionary of template variables
    template_variables = {
        "job_name": args.job_name,
        "nodes": args.nodes,
        "ppn": args.ppn,
        "walltime": args.walltime,
        "queue": args.queue,
        "account": args.account,
        "email": args.mail,
        "email_type": args.email_type,
        "directives": args.directives,
    }

    # Check if variables are missing - if so, use the default inputs
    for key, value in template_variables.items():
        if value is None:
            if key in default_inputs_found:
                template_variables[key] = default_inputs_found[key]

    # Create the submission script
    if args.pbs:
        submission_script = create_template(pbs_template, template_variables)
    elif args.slurm:
        submission_script = create_template(slurm_template, template_variables)
    else:
        print("Error: No scheduler specified.")
        return None

    return submission_script


def run(args):
    # Create the submission script
    submission_script = create_submission_file(args)

    if not args.output:
        print(submission_script)

    else:
        with open(args.output, "w") as f:
            f.write(submission_script)

    return None

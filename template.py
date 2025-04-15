import argparse
import logging
import os
from pathlib import Path

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s")

# File content templates for some common files
FILE_TEMPLATES = {
    "setup.py": (
        "from setuptools import setup, find_packages\n\n"
        "setup(\n"
        "    name='{}',\n"
        "    version='0.1',\n"
        "    packages=find_packages(),\n"
        "    install_requires=[],\n"
        ")\n"
    ),
    "requirements.txt": "# Add your project dependencies here\n",
    "config/config.yaml": "# YAML configuration for your project\n",
    "dvc.yaml": "# DVC configuration file\n",
    "params.yaml": "# Parameters for the project\n",
}


def create_project_structure(project_name, dry_run=False, overwrite=False):
    """
    Creates the file and directory structure for the project.

    Args:
        project_name (str): The main project folder name.
        dry_run (bool): If True, no files or directories are written; only logs the actions.
        overwrite (bool): If True, existing files will be overwritten with template content.
    """
    # Define the list of file paths to create
    list_of_files = [
        ".github/workflows/.gitkeep",
        f"src/{project_name}/__init__.py",
        f"src/{project_name}/components/__init__.py",
        f"src/{project_name}/utils/__init__.py",
        f"src/{project_name}/config/__init__.py",
        f"src/{project_name}/config/configuration.py",
        f"src/{project_name}/pipeline/__init__.py",
        f"src/{project_name}/entity/__init__.py",
        f"src/{project_name}/constants/__init__.py",
        "config/config.yaml",
        "dvc.yaml",
        "params.yaml",
        "requirements.txt",
        "setup.py",
        "research/trials.ipynb",
        "templates/index.html",
    ]

    for filepath in list_of_files:
        path_obj = Path(filepath)
        filedir, filename = os.path.split(path_obj)

        # Create directory if needed
        if filedir:
            dir_path = Path(filedir)
            if dry_run:
                logging.info(f"[Dry Run] Would create directory: {dir_path}")
            else:
                try:
                    os.makedirs(dir_path, exist_ok=True)
                    logging.info(f"Created directory: {dir_path} for file: {filename}")
                except OSError as err:
                    logging.error(f"Failed to create directory {dir_path}: {err}")

        # Decide what to write into the file (empty or template content)
        file_relative = str(path_obj)
        content = ""
        if file_relative in FILE_TEMPLATES:
            # If the file is setup.py, insert the project name into the template.
            if file_relative == "setup.py":
                content = FILE_TEMPLATES[file_relative].format(project_name)
            else:
                content = FILE_TEMPLATES[file_relative]

        # Write file content conditionally
        if dry_run:
            logging.info(
                f"[Dry Run] Would create/overwrite file: {path_obj} with content: {'provided template' if content else 'empty file'}"
            )
        else:
            # Overwrite if file doesn't exist or if file is empty or if overwrite flag is True.
            if (
                not os.path.exists(path_obj)
                or os.path.getsize(path_obj) == 0
                or overwrite
            ):
                try:
                    with open(path_obj, "w") as f:
                        f.write(content)
                    action = (
                        "Overwritten"
                        if overwrite and os.path.exists(path_obj)
                        else "Created"
                    )
                    logging.info(
                        f"{action} file: {path_obj}{' with template content' if content else ''}"
                    )
                except OSError as err:
                    logging.error(f"Failed to write file {path_obj}: {err}")
            else:
                logging.info(f"File already exists and is non-empty: {path_obj}")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Setup a standardized project structure for a machine learning/deep learning project."
    )
    parser.add_argument(
        "-p",
        "--project_name",
        type=str,
        default="cnnClassifier",
        help="Name of the project",
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Simulate the file creation without making changes",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files even if not empty",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    create_project_structure(
        args.project_name, dry_run=args.dry_run, overwrite=args.overwrite
    )

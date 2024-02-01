#!/bin/python3
import os
import subprocess
import sys


def prefix_output(file, process):
    """
    Prefix each line of output with the filename.
    """
    for line in process.stdout:
        print(f"[{file}] {line.decode().strip()}")


def verify_in_repo_root() -> None:
    """
    Verifies that the script is being executed from within the repository
    root. Exits with non-zero code if that's not the case.
    """
    # Determine the script's directory and the parent directory (which should
    # be <repo root>)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, '..'))

    # Check if the current working directory is the repo root
    if os.getcwd() != repo_root:
        print("The script must be run from the repo root. Please cd into " +
              "the repo root directory and then type: " +
              f"./quality-checks/{os.path.basename(__file__)}.")
        sys.exit(1)


def main() -> None:
    """
    Script entrypoint.
    """
    verify_in_repo_root()

    quality_checks_dir = './quality-checks/'
    failed_scripts = []

    # Iterate over every file in the quality-checks directory
    for file in os.listdir(quality_checks_dir):
        filepath = os.path.join(quality_checks_dir, file)

        # Exclude README.md and run_all.sh
        if file in ["README.md", "run_all.py"]:
            continue

        # Check if the file is executable
        if os.access(filepath, os.X_OK):
            print(f"Executing: {file}")
            with subprocess.Popen(filepath,
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT) as process:
                prefix_output(file, process)
                process.wait()  # Wait for the process to complete

                # Check the exit status of the script
                if process.returncode != 0:
                    print(f"Script {file} failed with exit status " +
                          f"{process.returncode}.")
                    failed_scripts.append(file)
            print()

    # Exit with a non-zero status if any script failed
    if failed_scripts:
        print('The following scripts failed:')
        for fs in failed_scripts:
            print(f'- {fs}')
        sys.exit(1)


if __name__ == "__main__":
    main()
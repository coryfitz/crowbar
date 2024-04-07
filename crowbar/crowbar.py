import argparse
import os
import subprocess
import sys
import venv

def parse_arguments():
    parser = argparse.ArgumentParser(description='Crowbar Package Installer')
    parser.add_argument('command', help='Command to run (e.g., install)')
    parser.add_argument('package_name', help='Name of the package to install')
    return parser.parse_args()

def create_venv_if_not_exists():
    venv_path = 'venv'
    if not os.path.isdir(venv_path):
        print("Creating virtual environment...")
        venv.create(venv_path, with_pip=True)
    return venv_path

def activate_venv_and_install_package(venv_path, package_name):
    # Note: Directly use the venv's pip to install packages, as activating a venv doesn't carry over to the user's shell.
    pip_path = os.path.join(venv_path, 'bin', 'pip')  # Adjust this path for Windows compatibility if necessary
    subprocess.run([pip_path, 'install', package_name])

def main():
    args = parse_arguments()
    if args.command == 'install':
        print(f"Installing {args.package_name}...")
        venv_path = create_venv_if_not_exists()
        activate_venv_and_install_package(venv_path, args.package_name)
    else:
        print("Unknown command.")
        sys.exit(1)

if __name__ == "__main__":
    main()

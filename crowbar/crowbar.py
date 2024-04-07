import argparse
import os
import subprocess
import sys
import venv

def parse_arguments():
    parser = argparse.ArgumentParser(description='Crowbar Package Installer and Script Runner')
    subparsers = parser.add_subparsers(dest='command')

    # Parser for the install command
    install_parser = subparsers.add_parser('install', help='Install a package')
    install_parser.add_argument('package_name', help='Name of the package to install')

    # Parser for the run command
    run_parser = subparsers.add_parser('run', help='Run a Python script')
    run_parser.add_argument('file_name', help='Name of the Python file to run')

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

def run_python_script(venv_path, script_name):
    if not os.path.isfile(script_name):
        print(f"Error: The file {script_name} does not exist.")
        sys.exit(1)
    
    python_executable = os.path.join(venv_path, 'bin', 'python')  # Adjust for Windows if necessary
    subprocess.run([python_executable, script_name])


def main():
    args = parse_arguments()
    
    # Common functionality: Ensure venv exists for both install and run commands
    venv_path = create_venv_if_not_exists()
    
    if args.command == 'install':
        print(f"Installing {args.package_name}...")
        activate_venv_and_install_package(venv_path, args.package_name)
    elif args.command == 'run':
        print(f"Running {args.file_name}...")
        run_python_script(venv_path, args.file_name)
    else:
        print("Unknown command.")
        sys.exit(1)


if __name__ == "__main__":
    main()

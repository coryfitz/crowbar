import argparse
import os
import subprocess
import sys
import venv

def get_venv_bin_path(venv_path):
    """Return the path to the virtual environment's bin/Scripts directory."""
    if os.name == 'nt':  # Windows
        return os.path.join(venv_path, 'Scripts')
    else:  # Unix-like
        return os.path.join(venv_path, 'bin')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Crowbar Package Manager')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Parser for the install command
    install_parser = subparsers.add_parser('install', help='Install packages')
    # Make package_name optional for the install command
    install_parser.add_argument('package_name', nargs='?', default=None, help='Name of the package to install (optional). If omitted, installs from requirements.txt')

    # Parser for the uninstall command
    uninstall_parser = subparsers.add_parser('uninstall', help='Uninstall a package')
    uninstall_parser.add_argument('package_name', help='Name of the package to uninstall')

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

def uninstall_package(venv_path, package_name):
    pip_path = os.path.join(venv_path, 'bin', 'pip')  # Adjust this path for Windows compatibility if necessary
    subprocess.run([pip_path, 'uninstall', package_name, '-y'])  # The '-y' flag auto-confirms uninstallation

def run_python_script(venv_path, script_name):
    if not os.path.isfile(script_name):
        print(f"Error: The file {script_name} does not exist.")
        sys.exit(1)
    
    python_executable = os.path.join(venv_path, 'bin', 'python')  # Adjust for Windows if necessary
    subprocess.run([python_executable, script_name])

def update_requirements(venv_path):
    pip_path = os.path.join(get_venv_bin_path(venv_path), 'pip')
    try:
        # Ensure we're using the correct pip by specifying the full path
        freeze_output = subprocess.check_output([pip_path, 'freeze'], text=True)
        with open("requirements.txt", "w") as req_file:
            req_file.write(freeze_output)
    except subprocess.CalledProcessError as e:
        print(f"Error updating requirements.txt: {e}")

def install_packages(venv_path, package_name=None):
    pip_path = os.path.join(get_venv_bin_path(venv_path), 'pip')
    if package_name:
        # Install a specific package
        subprocess.run([pip_path, 'install', package_name])
    else:
        # Install from requirements.txt
        requirements_path = os.path.join(os.getcwd(), 'requirements.txt')
        if os.path.exists(requirements_path):
            subprocess.run([pip_path, 'install', '-r', requirements_path])
        else:
            print("requirements.txt not found.")

def main():
    args = parse_arguments()
    
    venv_path = create_venv_if_not_exists()
    
    if args.command == 'install':
        if args.package_name:
            print(f"Installing {args.package_name}...")
            install_packages(venv_path, args.package_name)
            update_requirements(venv_path)  # Update requirements after installing a specific package
        else:
            print("Installing packages from requirements.txt...")
            install_packages(venv_path)
            # No call to update_requirements here, as we're installing from it
    elif args.command == 'uninstall':
        print(f"Uninstalling {args.package_name}...")
        uninstall_package(venv_path, args.package_name)
        update_requirements(venv_path)  # Update requirements after uninstallation
    elif args.command == 'run':
        print(f"Running {args.file_name}...")
        run_python_script(venv_path, args.file_name)
    else:
        print("Unknown command.")
        sys.exit(1)

if __name__ == "__main__":
    main()
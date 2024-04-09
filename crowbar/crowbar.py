import argparse
import os
import subprocess
import sys

def is_conda_environment():
    return 'CONDA_DEFAULT_ENV' in os.environ or 'CONDA_PREFIX' in os.environ

def get_conda_executable():
    """Attempts to find the 'conda' command in known directories or in the system path."""
    conda_executable = 'conda'  # Default to using conda in path
    # Specified by Conda on activation
    if 'CONDA_EXE' in os.environ:
        conda_executable = os.environ['CONDA_EXE']
    elif 'CONDA_PREFIX' in os.environ:
        # Construct a path to conda based on the active environment
        conda_executable = os.path.join(os.environ['CONDA_PREFIX'], 'condabin', 'conda')
    return conda_executable

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

def create_conda_environment(env_name):
        conda_prefix = os.environ['CONDA_PREFIX']
        # Construct the command to create a new Conda environment
        command = f"{os.path.join(conda_prefix, 'condabin', 'conda')} create --name {env_name} --yes"
        subprocess.run(command, shell=True)

def create_env_if_not_exists():
    env_name = 'conda_env' if is_conda_environment() else 'venv'
    
    if is_conda_environment():
        # Check if the Conda environment already exists
        conda_executable = get_conda_executable()
        check_env = subprocess.run([conda_executable, 'env', 'list'], capture_output=True, text=True)
        if env_name not in check_env.stdout:
            print(f"Creating Conda environment named {env_name}...")
            subprocess.run([conda_executable, 'create', '--name', env_name, '--yes'], check=True)
        else:
            print(f"Conda environment named {env_name} already exists.")
    else:
        if not os.path.isdir(env_name):
            print(f"Creating environment named {env_name}...")
            subprocess.run([sys.executable, '-m', 'venv', env_name], check=True)
        else:
            print(f"Environment named {env_name} already exists.")
    
    return env_name

def uninstall_package(env_name, package_name):
    if is_conda_environment():
        conda_executable = get_conda_executable()
        # Uninstall a package with Conda
        print(f"Uninstalling {package_name} from Conda environment {env_name}...")
        subprocess.run([conda_executable, 'remove', '--name', env_name, package_name, '--yes'], check=True)
    else:
        pip_path = os.path.join(env_name, 'Scripts', 'pip') if os.name == 'nt' else os.path.join(env_name, 'bin', 'pip')
        # Uninstall a package with pip
        print(f"Uninstalling {package_name} from environment {env_name}...")
        subprocess.run([pip_path, 'uninstall', package_name, '-y'], check=True)  # The '-y' flag auto-confirms uninstallation

def run_python_script(env_name, script_name):
    if not os.path.isfile(script_name):
        print(f"Error: The file {script_name} does not exist.")
        sys.exit(1)
    
    # Determine the correct path for the Python executable
    if os.name == 'nt':  # Windows
        # Adjusting for both Conda and venv paths on Windows
        python_executable = os.path.join(env_name, 'Scripts', 'python.exe')
    else:  # Unix-like (Linux, macOS)
        python_executable = os.path.join(env_name, 'bin', 'python')
    
    # Check if the executable exists
    if not os.path.exists(python_executable):
        print(f"Error: Python executable not found at {python_executable}.")
        sys.exit(1)
    
    print(f"Running {script_name} using {python_executable}...")
    subprocess.run([python_executable, script_name])

def install_packages(env_name, package_name=None):
    if is_conda_environment():
        conda_executable = get_conda_executable()
        if package_name:
            subprocess.run([conda_executable, 'install', '--name', env_name, package_name, '--yes'], check=True)
        else:
            requirements_path = os.path.join(os.getcwd(), 'requirements.txt')
            if os.path.exists(requirements_path):
                subprocess.run([conda_executable, 'install', '--name', env_name, '--file', requirements_path, '--yes'], check=True)
            else:
                print("requirements.txt not found.")
    else:
        pip_path = os.path.join(env_name, 'Scripts', 'pip') if os.name == 'nt' else os.path.join(env_name, 'bin', 'pip')
        if package_name:
            subprocess.run([pip_path, 'install', package_name], check=True)
        else:
            requirements_path = os.path.join(os.getcwd(), 'requirements.txt')
            if os.path.exists(requirements_path):
                subprocess.run([pip_path, 'install', '-r', requirements_path], check=True)
            else:
                print("requirements.txt not found.")

def update_requirements(env_name):
    if is_conda_environment():
        conda_executable = get_conda_executable()
        # Using conda list to export the package list, which is not directly equivalent to pip freeze
        subprocess.run([conda_executable, 'list', '--name', env_name, '--export'], stdout=open('requirements.txt', 'w'), check=True)
    else:
        pip_path = os.path.join(env_name, 'Scripts', 'pip') if os.name == 'nt' else os.path.join(env_name, 'bin', 'pip')
        subprocess.run([pip_path, 'freeze'], stdout=open('requirements.txt', 'w'), check=True)

def main():
    args = parse_arguments()
    
    venv_path = create_env_if_not_exists()
    
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
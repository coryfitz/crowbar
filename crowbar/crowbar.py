import argparse
import os
import subprocess
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description='Crowbar Package Manager')
    parser.add_argument('-g', '--global', dest='global_run', action='store_true', help='Operate on the global Python environment instead of a virtual environment')
    parser.add_argument('command', nargs='?', help='Command to run (install, uninstall, run, or external commands)')
    parser.add_argument('remainder', nargs=argparse.REMAINDER, help='Arguments for commands')
    return parser.parse_args()

def create_env_if_not_exists():
    env_name = 'venv'
    if not os.path.isdir(env_name):
        print(f"Creating environment named {env_name}...")
        subprocess.run([sys.executable, '-m', 'venv', env_name], check=True)
    return env_name

def run_external_command(env_name, command, args, global_run):
    if global_run:
        subprocess.run([command] + args)
    else:
        command_path = os.path.join(env_name, 'Scripts' if os.name == 'nt' else 'bin', command)
        if os.path.exists(command_path):
            # This is for executables in the venv
            subprocess.run([command_path] + args)
        elif command.endswith('.py'):
            # This is for Python scripts
            python_executable = os.path.join(env_name, 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(env_name, 'bin', 'python')
            script_path = os.path.join(os.getcwd(), command)
            if os.path.exists(script_path):
                subprocess.run([python_executable, command] + args)
            else:
                print(f"Error: The file {script_path} does not exist.")
                sys.exit(1)
        else:
            print(f"Command {command} not found.")
            sys.exit(1)

def install_packages(env_name, packages, global_install):
    pip_path = 'pip' if global_install else os.path.join(env_name, 'Scripts' if os.name == 'nt' else 'bin', 'pip')
    subprocess.run([pip_path, 'install'] + packages, check=True)
    if not global_install:
        update_requirements(env_name)

def uninstall_packages(env_name, packages, global_uninstall):
    pip_path = 'pip' if global_uninstall else os.path.join(env_name, 'Scripts' if os.name == 'nt' else 'bin', 'pip')
    subprocess.run([pip_path, 'uninstall', '-y'] + packages, check=True)
    if not global_uninstall:
        update_requirements(env_name)

def update_requirements(env_name):
    pip_path = os.path.join(env_name, 'Scripts' if os.name == 'nt' else 'bin', 'pip')
    subprocess.run([pip_path, 'freeze'], stdout=open('requirements.txt', 'w'), check=True)

def main():
    args = parse_arguments()

    if args.global_run:
        print("Global operations are enabled.")
        if args.command == 'install':
            install_packages(None, args.remainder, True)
        elif args.command == 'uninstall':
            uninstall_packages(None, args.remainder, True)
    else:
        env_name = create_env_if_not_exists()
        if args.command == 'install':
            install_packages(env_name, args.remainder, False)
        elif args.command == 'uninstall':
            uninstall_packages(env_name, args.remainder, False)
        elif args.command == 'run':
            run_external_command(env_name, args.remainder[0], args.remainder[1:], False)
        elif args.command:
            run_external_command(env_name, args.command, args.remainder, False)

if __name__ == "__main__":
    main()

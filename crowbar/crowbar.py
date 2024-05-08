import argparse
import os
import subprocess
import sys
import toml
import appdirs

def parse_arguments():
    parser = argparse.ArgumentParser(description='Crowbar Package Manager')
    parser.add_argument('-g', '--global', dest='global_run', action='store_true', help='Operate on the global Python environment instead of a virtual environment')
    parser.add_argument('command', nargs='?', help='Command to run (install, uninstall, run, name, or external commands)')
    parser.add_argument('remainder', nargs=argparse.REMAINDER, help='Arguments for commands')
    return parser.parse_args()

def load_config():
    config_dir = appdirs.user_data_dir(appname='crowbar', appauthor=False)
    config_path = os.path.join(config_dir, 'cbconfig.toml')
    if not os.path.exists(config_path):
        return {'env_name': 'venv', 'gitignore': True}
    with open(config_path, 'r') as config_file:
        return toml.load(config_file)

def save_config(config):
    config_dir = appdirs.user_data_dir(appname='crowbar', appauthor=False)
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, 'cbconfig.toml')
    with open(config_path, 'w') as config_file:
        toml.dump(config, config_file)

def find_virtual_environment_directory():
    original_dir = os.getcwd()
    try:
        while True:
            current_dir = os.getcwd()
            config = load_config()
            env_name = config.get('env_name', 'venv')
            if os.path.isdir(env_name):
                return current_dir
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                return None
            os.chdir(parent_dir)
    finally:
        os.chdir(original_dir)

def check_current_directory():
    config = load_config()
    env_name = config.get('env_name', 'venv')
    return os.path.isdir(env_name)

def update_gitignore(dir_name):
    current_dir = os.getcwd()
    gitignore_path = os.path.join(current_dir, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r+') as file:
            contents = file.read()
            if dir_name not in contents.splitlines():
                file.write(f'\n{dir_name}')
                print(f"Added '{dir_name}' to {gitignore_path}")
    else:
        with open(gitignore_path, 'w') as file:
            file.write(f'{dir_name}\n')
            print(f"Created .gitignore and added '{dir_name}'")

def create_env_if_not_exists(env_name, gitignore_status):
    if not os.path.isdir(env_name):
        print(f"Creating environment named {env_name}.")
        subprocess.run([sys.executable, '-m', 'venv', env_name], check=True)
        if gitignore_status:
            update_gitignore(env_name)

def run_external_command(env_directory, env_name, command, args, global_run):
    env_path = os.path.join(env_directory, env_name)
    if global_run:
        subprocess.run([command] + args)
    else:
        command_path = os.path.join(env_path, 'Scripts' if os.name == 'nt' else 'bin', command)
        if os.path.exists(command_path):
            subprocess.run([command_path] + args)
        else:
            python_executable = os.path.join(env_name, 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(env_path, 'bin', 'python')
            if command.endswith('.py'):
                subprocess.run([python_executable, command] + args)
            else:
                print(f"Command {command} not found.")
                sys.exit(1)

def install_packages(env_directory, env_name, packages, global_install):
    env_path = os.path.join(env_directory, env_name)
    pip_path = 'pip' if global_install else os.path.join(env_path, 'Scripts' if os.name == 'nt' else 'bin', 'pip')
    if packages:
        subprocess.run([pip_path, 'install'] + packages, check=True)
    else:
        requirements_path = os.path.join(env_directory, 'requirements.txt')
        if os.path.exists(requirements_path):
            subprocess.run([pip_path, 'install', '-r', requirements_path], check=True)
        else:
            print("No packages specified and requirements.txt not found.")
    if not global_install:
        update_requirements(env_directory, env_name)

def uninstall_packages(env_directory, env_name, packages, global_uninstall):
    env_path = os.path.join(env_directory, env_name)
    pip_path = 'pip' if global_uninstall else os.path.join(env_path, 'Scripts' if os.name == 'nt' else 'bin', 'pip')
    subprocess.run([pip_path, 'uninstall', '-y'] + packages, check=True)
    if not global_uninstall:
        update_requirements(env_directory, env_name)

def update_requirements(env_directory, env_name):
    env_path = os.path.join(env_directory, env_name)
    pip_path = os.path.join(env_path, 'Scripts' if os.name == 'nt' else 'bin', 'pip')
    requirements_file_path = os.path.join(env_directory, 'requirements.txt')
    with open(requirements_file_path, 'w') as requirements_file:
        subprocess.run([pip_path, 'freeze'], stdout=requirements_file, check=True)

def show_gitignore(config):
    gitignore_status = config.get('gitignore')
    if gitignore_status:
        print('Gitignore status: on')
    else:
        print('Gitignore status: off')

def show_name(config):
    env_name = config.get('env_name')
    print(f'Environment name: {env_name}')

def main():
    args = parse_arguments()

    if args.command == 'name' and args.remainder:
        new_name = args.remainder[0]
        config = load_config()
        config['env_name'] = new_name
        save_config(config)
        print(f'Default environment name changed to {new_name}')
        return
    
    if args.command == 'show' and args.remainder[0] == 'name':
        config = load_config()
        show_name(config)
        return
    
    if args.command == 'gitignore' and args.remainder[0] == 'on':
        config = load_config()
        config['gitignore'] = True
        save_config(config)
        print('Crowbar will create a .gitignore file when it creates a new environment folder')
        return
    
    if args.command == 'gitignore' and args.remainder[0] == 'off':
        config = load_config()
        config['gitignore'] = False
        save_config(config)
        print('Crowbar will not create a .gitignore file when it creates a new environment folder')
        return
    
    elif args.command == 'check' and args.remainder[0] == 'env':
        directory = find_virtual_environment_directory()
        config = load_config()
        env_name = config.get('env_name', 'venv') 
        if directory == None:
            print('There is no environment folder found. Crowbar will install one in your current directory.')
        else:
            print(f"Crowbar found {env_name} at {directory}. If this is not the environment folder you would like to use, 'cb create env' will allow you to install one manually if it does not already exist.")
        return
    
    elif args.command == 'show' and args.remainder[0] == 'gitignore':
        config = load_config()
        show_gitignore(config)
        return
    
    elif args.command == 'show' and args.remainder[0] == 'config':
        config = load_config()
        show_gitignore(config)
        show_name(config)
        return
    
    elif args.command == 'create' and args.remainder[0] == 'env':
        env_exists = check_current_directory()
        config = load_config()
        env_name = config.get('env_name', 'venv')
        gitignore_status = config.get('gitignore', True)
        if not env_exists:
            create_env_if_not_exists(env_name, gitignore_status)
        else:
            print(f'An environment folder already exists in the current directory.')
        return

    env_directory = find_virtual_environment_directory()
    config = load_config()
    env_name = config.get('env_name', 'venv')    
    gitignore_status = config.get('gitignore', True)

    # To avoid creating a venv if cwd is in a subdirectory
    if args.command == 'install' and not args.remainder:
        to_reset = False
        if env_directory is None:
            env_directory = os.getcwd()
            to_reset = True
        requirements_path = os.path.join(env_directory, 'requirements.txt')
        if not os.path.exists(requirements_path):
            print("No packages specified and requirements.txt not found.")
            sys.exit(1)
        if to_reset:
            env_directory = None

    existing_commands = ['install', 'uninstall', 'run']

    if env_directory is None:
        if args.command in existing_commands:
            create_env_if_not_exists(env_name, gitignore_status)
            env_directory = os.getcwd()
        else:
            print("Unknown command.")
            sys.exit(1)
    else:
        if not args.global_run:
            print(f"Using environment {env_name} at {env_directory}")
        else:
            print('**global environment**')

    if args.command == 'install':
        install_packages(env_directory, env_name, args.remainder, args.global_run)
    elif args.command == 'uninstall':
        uninstall_packages(env_directory, env_name, args.remainder, args.global_run)
    elif args.command == 'run':
        run_external_command(env_directory, env_name, args.remainder[0], args.remainder[1:], args.global_run)
    elif args.command:
        run_external_command(env_directory, env_name, args.command, args.remainder, args.global_run)
    else:
        print("Unknown command.")
        sys.exit(1)

if __name__ == "__main__":
    main()

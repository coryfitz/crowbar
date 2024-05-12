# crowbar

<br>

## what is it?

Crowbar is a tool for managing your dependencies in Python projects. Inspired by tools like NPM in the JavaScript ecosystem, it installs your dependencies with your project and frees you from the need to think about virtual environments or keep track of your dependencies yourself.

<br>

## who is it for?

Crowbar is for any Python developer, but it works especially well with someone who uses the vanilla path of dependency management (pip, venv, requirements.txt) and wants to automate some of this workflow.

It's probably not for you if you're deeply embedded in an alternate ecosystem like Conda.

<br>

## how do I use it?

I'll walk you through the steps of starting a Django project, so you can get a feel for the crowbar mental model.

First, install crowbar:

```
pip install crowbar-package-manager
```

Create and/or enter your project directory and then use crowbar to install Django:

```
crowbar install django
```

Note: any instance of ```crowbar``` can be replaced with ```cb```

```crowbar install <package name>``` uses pip to install your package to a virtual environment folder (named venv by default), records it to requirements.txt, and creates a .gitignore file with venv listed.

Start a new Django project:

```
crowbar django-admin startproject project_name .
```
Notice that we didn't need to activate a virtual environment - using ```crowbar``` before your command means that it runs using the dependencies in your venv folder automatically.

Run the Django development server:

```
crowbar manage.py runserver
```

You can also use ```crowbar``` to run a Python file, so in this case you don't put ```python``` before ```manage.py```


<br>

## how does it work?

Crowbar uese pip and venv under the hood. It essentially runs the same commands that you would, but automates the process.

It is worth explaining how crowbar finds the nearest environment folder. It does this by looking for an environment folder at the current directory and progressively looking in higher directories until it finds an environment folder or reaches the root directory. The name of the environment folder it looks for can be changed by the user, but defaults to venv.

The benefit of this search is that you can run crowbar commands from anywhere within your project as long as your dependencies are stored in the main directory of your project.

There is a potential problem though if you have an environment folder in a directory above your current directory. For example, if you have a venv folder on your desktop and then you create a project on your desktop named my_project, enter that directory and type ```crowbar install pandas```, pandas will be installed in the venv folder on your desktop.

If you are concerned that this might be a problem for you, you can simply run ```crowbar check env``` to see if crowbar can detect any environment folders at your current directory or above and, if you find any that you want to avoid installing packages to, you can run ```crowbar create env``` to force crowbar to create a new environment folder in your current directory.

## commands

Note: any instance of ```crowbar``` can be replaced with ```cb```


```
crowbar install <package_name> <package_name>
```
-Checks to see if there is an environment folder based on the name you've set (venv is the default) in the current directory or in directories above
-Creates a virtual environment called venv if it does not exist<br>
-Installs a package (or packages) from pypi into venv<br>
-Updates requirements.txt and creates one if it does not exist

```
crowbar uninstall <package_name> <package_name>
```
-Uninstalls a package (or packages) from venv
-Updates requirements.txt

```
crowbar install
```
-Installs all packages listed in requirements.txt

```
crowbar <file_name>.py
```
-Runs a python file using the contents of the local venv

```
crowbar show name
```
-Lists the current name of the environment folder that crowbar creates (venv is the default)

```
crowbar name <environment name>
```
-Changes the name of the environment folder that crowbar creates (venv is the default)

```
crowbar check env
```
-Checks to see if there is an environment folder based on the name you've set (venv is the default) in the current directory or in directories above

```
crowbar create env
```
-Creates an environment folder in the current directory based on the name you've set (venv is the default)

```
crowbar show gitignore
```
-Indicates whether Crowbar is set to create a .gitignore file when it creates an environment folder (default is to create .gitignore)

```
crowbar gitignore on
```
-Instructs Crowbar to create a .gitignore file when it creates an environment folder and add the name of that folder to the .gitignore file (this is the default)

```
crowbar gitignore off
```
-Instructs Crowbar not to create a .gitignore file when it creates an environment folder

```
crowbar show config
```
-Lists all current configurable settings (environment folder name and gitignore on/off)

Warning – you may have pip muscle memory which may cause you to accidentally install globally. Use crowbar/cb and not pip if you are not in an active virtual environment.

<br>

### global flag

```
crowbar --global install <package_name>
```
```
cb -g uninstall <package_name>
```
-installs or uninstalls a package globally

<br>

### running package commands

With the crowbar command you can run any commands installed in the virtual environment.

Example - starting a new Django project:

```
cb django-admin startproject project_name .
```

Running the Django development server:

```
cb manage.py runserver
```

<br>

### package managers other than pip

Crowbar does not support Conda. Crowbar has plans to support UV eventually.
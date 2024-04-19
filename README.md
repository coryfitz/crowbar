## crowbar

Note: any instance of ```crowbar``` can be replaced with ```cb```


```
crowbar install <package_name> <package_name>
```
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
crowbar run <file_name>.py
```
-Runs a python file using the contents of the local venv

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
cb django-admin startproject django_project .
```

Use ```crowbar run``` to run any commands surfaced by files within your Python program.

Example - running the Django development server:

```
cb run manage.py runserver
```

<br>

### package managers other than pip

Crowbar does not support Conda. Crowbar has plans to support UV eventually.
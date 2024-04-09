## crowbar

Note: any instance of ```crowbar``` can be replaced with ```cb```


```
crowbar install <package_name>
```
-Creates a virtual environment called venv if it does not exist<br>
-Installs a package from pypi into venv<br>
-Updates requirements.txt and creates one if it does not exist

```
crowbar uninstall <package_name>
```
-Uninstalls a package from venv
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

### conda support

Crowbar supports python and will create an environment called conda_env instead of venv if it detects that it is within a conda environment.
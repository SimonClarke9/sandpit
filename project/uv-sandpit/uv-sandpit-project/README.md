# UV Environment Manager 
A utility for Pakaging Software , projects ready  to deploy

## Setup
```bash
# Link to install UV in a bash shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Usage

### First Project
```bash
uv init my-first-project
```
From the current working directory creates these artifacts:
- my-first-project sub directory in this folder:
    -   .python-version
    -   main.py
    -   pyproject.toml
    -   README.md

```bash
cd my-first-project
uv venv my-first-project
```
Creates the virtual enviroment for the project
Adds these artifacts:
-   Lib folder
-   Scripts folder  for activating | deactivating venv
-   .gitignore - git  ignore configuration file 
-   CACHEDIR.TAG
-   pyvenv.cfg

```bash
# activate  venv
source ./uv-sandpit-project/Scripts/activate

# deactivate
deactivate
```

### Add Dependencies
create a requirement.txt file in the root folder for your project.
Add depedencies into the file on a new line
```txt
pandas
```
now load those dependencies into the project
```bash
# activate venv
source ./uv-sandpit-project/Scripts/activate

# uv install dependencies
uv pip install -r ./../requirments.txt
```
or

```bash
uv add numpy
```
Installs the numpy libary into the venv and inserts to pyproject.toml under dependencies.
```bash
uv remove numpy
```
Removes numpy from the dependencies list and the deinstalls the library.

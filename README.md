# Masking User Private Information 🙈

Pivony Text anonymization is a tool to hide users potential identification information including: <br>
1. Emails
2. Phone numbers
3. Location information
4. Names

This tool is only supporting Turkish language 🇹🇷
<br>
If you are running on Windows this guide is meant for you.

## Installation for Windows Users

1- First step is to install python 
from this [link](https://www.python.org/downloads/release/python-3104/) <br> To check your installation open your command Prompt and run this:
```bash
python -V
```
The expected output is the installed python version
<br>
2- Install virtual environment:
```bash
#install virtual env with
pip install virtualenv
```
3- Create a virtual environment 
open your commant Prompt again
```bash
#navigate to the project folder
cd folder_path/
#create a virtual env with name <env_name>
python -m venv env_name
```
4- Activate the virtual environment by:
```bash
.\env_name\Scripts\activate
```
5- Install all requirements
```bash
pip install -r requirements.txt
```
## Quick tour
To process any file you need to know:
1. File type accepted is "csv"
2. You need to place 1 or more files inside input_files/
3. Your text column should be "Verbatim"
### RUN
To immediately use the script run this
<br>
```bash
cd code/
python main.py
```

## Outputs
The script output is the files generated: <br> Files will have same name and contain the same original columns except for the text column that will be renamed as "Masked" and text will be replaced with the masked version. <br>
all private information will be converted to `*****`

## Licence
Copyright (c) 2022, Pivony All rights reserved.

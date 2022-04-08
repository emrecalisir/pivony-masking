# Masking User Private Information 🙈

Pivony Text anonymization is a tool to hide users potential identification information including: <br>
1. Emails
2. Phone numbers
3. Location information
4. Names

This tool is only supporting Turkish language 🇹🇷

## Install Requirements
### With pip
You should install requirements in a [virtual environment](https://docs.python.org/3/library/venv.html). If you're unfamiliar with Python virtual environments, check out the [user guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
First, create a virtual environment with the version of Python you're going to use and activate it.

Then, you will need to install packages from `requirements.txt`
<br>
```bash
# install requirements
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
# Change directory
cd code/
# run script run.sh
./run.sh
```
<br>
## Outputs
The script output is the files generated: <br> Files will have same name and contain the same original columns except for the text column that will be renamed as "Masked" and text will be replaced with the masked version. <br>
all private information will be converted to `*****`

## Licence
Copyright (c) 2022, Pivony All rights reserved.

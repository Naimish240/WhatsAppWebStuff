#!/bin/sh

# Create Virtual Environment
python3 -m venv env 
# Activate Virtual Environment
source env/bin/activate

# Install dependancies
pip install -r requirements.txt
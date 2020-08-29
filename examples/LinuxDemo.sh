#!/bin/sh
# Run in folder where the environment 'env' is declared
# Activates the virtual environment
source env/bin/activate

# Loads the files from the folder "Data", default ISD
# python sendMessage.py -f "Data/CSVs.csv" -t "Data/message.txt"

# Loads the files from the folder Data/
# python sendMessage.py -f "Data/CSVs.csv" -t "Data/message.txt" -i "+91"
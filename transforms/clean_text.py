"""

"""
# Libraries
import os
import mysql.connector
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src import utils, transforms

# Directories                                                                      
DIR_ROOT = utils.get_root_directory()                                              
DIR_CONFIG = os.path.join(DIR_ROOT, 'configurations')                              
DIR_TEXT_RAW = os.path.join(DIR_ROOT, 'data', 'text', 'raw')                    
DIR_TEXT_CLEAN = os.path.join(DIR_ROOT, 'data', 'text', 'clean')

# File Name List
files_local = os.listdir(DIR_TEXT_RAW)

# Test File
for file in files_local:
    print(f"Cleaning file => {file}")
    path = os.path.join(DIR_TEXT_RAW, file)
    os.path.exists(path)

    with open(path, 'r') as f:
        text = f.read()

    # Clean Text
    clean_text = transforms.CleanText().transform(text=text)

    print(f"\tWriting file => {file} to {DIR_TEXT_CLEAN}")
    path = os.path.join(DIR_TEXT_CLEAN, file)
    
    with open(path, 'w') as f:
        f.write(clean_text)
    print("\tWritten successfully \n")


print("Script finished")






















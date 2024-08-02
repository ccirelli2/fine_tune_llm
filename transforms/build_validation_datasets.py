"""
Edgar financial relational data is saved by quarter in archives and various
tab delimited files.  This code iterates the archives and extracts the specific
file, processes and concatentates them into single csv files.  Then writes
them to the output directory.
"""
import os
import chardet
import pandas as pd
from src.transforms import ConcatArchives

# Directories
DIR_DATA="/Users/temp-admin/repositories/fine_tune_llm/data/validation/raw"
DIR_OUTPUT = DIR_DATA.replace("/raw", "/clean")

# Archive Names
archives = os.listdir(DIR_DATA)
file_names = ['tag.txt', 'pre.txt', 'sub.txt', 'num.txt']

# Open Files
if __name__ == "__main__":
    
    concat_archives = ConcatArchives(
        input_dir=DIR_DATA,
        output_dir=DIR_OUTPUT,
        target_files=file_names
    ).transform()
    
    






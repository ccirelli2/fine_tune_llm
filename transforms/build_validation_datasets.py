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
        archive_dir=DIR_DATA,
        target_files=file_names
    ).transform()
    
    






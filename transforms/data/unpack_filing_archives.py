"""
Filing archives contain filing text.

They are located in zip archives that are themselves located in a sub directory
of data/archives.

This code iterates through the sub directories, extracts the desired text files
and writes them to a new raw directory.
"""
import os
import gzip 
import shutil
from dotenv import load_dotenv
from src import queries, utils, connections

# Directories
load_dotenv()
DIR_ROOT = os.getenv("DIR_ROOT")                                                   
DIR_CONFIG = os.getenv("DIR_CONFIG")                                               
DIR_DATA = os.getenv("DIR_DATA")
DIR_DATA_TEXT = os.getenv("DIR_DATA_TEXT")
DIR_INPUT = os.path.join(DIR_DATA, 'archives')
DIR_OUTPUT = os.path.join(DIR_DATA_TEXT, 'raw')


def unzip_gz(file_path, output_path):
    with gzip.open(file_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def unzip_all_gz_in_directory(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for file_name in files:
            if file_name.endswith('.gz'):
                file_path = os.path.join(root, file_name)
                output_path = os.path.join(output_dir, file_name[:-3])  # Remove .gz extension
                unzip_gz(file_path, output_path)
                print(f"Unzipped {file_path} to {output_path}")

# Example usage
unzip_all_gz_in_directory(DIR_INPUT, DIR_OUTPUT)



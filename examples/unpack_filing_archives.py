"""
Unpack filing archives from gzip to text
"""
import os
import gzip 
import shutil
from src import queries, utils, connections
# Directories
DIR_ROOT = utils.get_root_directory()
DIR_CONFIG = os.path.join(DIR_ROOT, 'master')
DIR_INPUT = os.path.join(DIR_ROOT, 'data', 'archives')
DIR_OUTPUT = os.path.join(DIR_ROOT, 'data', 'unzipped')


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



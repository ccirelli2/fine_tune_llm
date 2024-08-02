"""

"""
# Libraries
import os
import asyncio
import mysql.connector
import pandas as pd
import chardet
from src import utils, transforms
from src.transforms import CleanTextAsync

# Directories                                                                      
DIR_ROOT = utils.get_root_directory()                                              
DIR_CONFIG = os.path.join(DIR_ROOT, 'configurations')                              
DIR_TEXT_RAW = os.path.join(DIR_ROOT, 'data', 'text', 'raw')                    
DIR_TEXT_CLEAN = os.path.join(DIR_ROOT, 'data', 'text', 'clean')

# Clean Text
async def main():
    cleaner = CleanTextAsync(max_concurrent_files=50)
    await cleaner.process_files(DIR_TEXT_RAW, DIR_TEXT_CLEAN)

asyncio.run(main())
























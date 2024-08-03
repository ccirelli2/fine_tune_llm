"""

"""
# Libraries
import os
import asyncio
import mysql.connector
import pandas as pd
import chardet
from dotenv import load_dotenv
from src import utils, transforms
from src.transforms import CleanTextAsync

# Directories                 
load_dotenv()
DIR_ROOT = os.getenv("DIR_ROOT")
DIR_CONFIG = os.getenv("DIR_CONFIG")
DIR_DATA = os.getenv("DIR_DATA_TEXT")
DIR_TEXT_RAW = os.path.join(DIR_DATA_TEXT, 'raw')                    
DIR_TEXT_CLEAN = os.path.join(DIR_DATA_TEXT, 'clean')

# Clean Text
async def main():
    cleaner = CleanTextAsync(max_concurrent_files=50)
    await cleaner.process_files(DIR_TEXT_RAW, DIR_TEXT_CLEAN)

asyncio.run(main())
























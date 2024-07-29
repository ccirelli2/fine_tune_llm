"""
"""
import os
import re
import pandas as pd
from src import queries, utils, connections

# Directories
DIR_ROOT = utils.get_root_directory()
DIR_CONFIG = os.path.join(DIR_ROOT, 'master')
DIR_TEXT_RAW = os.path.join(DIR_ROOT, 'data', 'text', 'raw')
DIR_TEXT_CLEAN = os.path.join(DIR_ROOT, 'data', 'text', 'clean')

# Get List of Files
files = os.listdir(DIR_TEXT_RAW)

# Load Files

patterns = {
        "CIK": "CENTRAL INDEX KEY:.*\n",
        "FILING_TYPE": "CONFORMED SUBMISSION TYPE:.*\n",
        "FILING_DATE": "FILED AS OF DATE:.*\n",
        "COMPANY_NAME": "COMPANY CONFORMED NAME:.*\n",
        "CIK": "CENTRAL INDEX KEY:.*\n",
        "IRS_NUMBER": "IRS NUMBER:.*\n",
}

# Patterns
class FilingIndex:
    def __init__(self, directory: str, patterns: dict, filenames: list = []):
        self.directory = directory
        self.filenames = filenames 
        self.patterns = patterns
        self.filing_df = pd.DataFrame({})
        self.struct = {}
        
        if not filenames:
            print("Filenames not provided.  Taking from directory")
            self.filenames = os.listdir(directory)
        print("Total Files => {}".format(len(self.filenames)))
        print(f"{__class__} instantiated successfully")

    def _open_file(self, filename):
        """
        """
        path = os.path.join(self.directory, filename)
        with open(path, 'r') as f:
            text = f.read()
        return text

    def _match_patterns(self, text):
        """
        """
        pattern_match = {key: None for key, value in self.patterns.items()}

        for key, value in self.patterns.items():
            search = re.search(value, text)
            if search:
                match = search.group()
                pattern_match[key] = match.split(":")[-1].strip()
            else:
                pattern_match[key] = 'not-found'

        return pattern_match

    def _create_struct(self):
        """
        """
        print("Creating Struct File")
        self.struct = {key: [] for key, value in self.patterns.items()}
        self.struct.update({'filename': [], 'id': []})
        print(f"Finished. Result => {self.struct}\n\n")
        return self

    def _create_dataframe(self):
        """
        """
        print("Creating Filings DataFrame")
        return pd.DataFrame(self.struct)
    
    def _extract_patterns(self):
        
        for i in range(len(self.filenames)):
            name = self.filenames[i]
            print(f"Finding matches for filename => {name}")
            text = self._open_file(name)
            matches = self._match_patterns(text)
            # Populate Struct
            self.struct['id'].append(i)
            self.struct['filename'].append(name)
            for key, value in matches.items():
                self.struct[key].append(value)
        return self

    def transform(self):
        self._create_struct()
        self._extract_patterns()
        return self._create_dataframe()





if __name__ == "__main__":
    indexer = FilingIndex(
        directory=DIR_TEXT_RAW,
        patterns=patterns
        )

    filings_df = indexer.transform()
    print(filings_df.head())

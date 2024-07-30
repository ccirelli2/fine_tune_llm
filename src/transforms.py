"""
"""
import os
import re
import pandas as pd
from bs4 import BeautifulSoup


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
        self.struct.update({'FILE_NAME': [], 'ID': []})
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
            self.struct['ID'].append(i)
            self.struct['FILE_NAME'].append(name)
            for key, value in matches.items():
                self.struct[key].append(value)
        return self

    def transform(self):
        self._create_struct()
        self._extract_patterns()
        return self._create_dataframe()


class CleanText:
    """TODO: Parameterize parser, bs4 and re tags.
    """
    def __init__(self):
        self.bs4_tags = ['img', 'table', 'canvas', 'graphic', 'link']
        self.re_tags = ["GRAPHIC", "EXCEL", "ZIP"]
        self.parser = 'lxml'
        self.text_clean = ""
        print(f"{__class__} instantiated successfully")

    
    def _strip_bs4_tags(self, text):
        """                                                                            
        Function to remove html from underlying text using the BeautifulSoup library.
        """             
        print(f"Stripping html tags => {self.bs4_tags}")

        # Parse HTML                                                            
        soup = BeautifulSoup(text, self.parser)                            
        # Remove all images                                                     
        for tag in self.bs4_tags:
            for element in soup.find_all(tag):                                        
                element.decompose()  # acts on soup obj.                                
        
        self.text_clean = soup.get_text(separator="\n", strip=True)                 
        return self

    def _strip_re_tags(self):
        """
         
        """
        print(f"Stripping re tags {self.re_tags}")
        pattern = re.compile(r'(<TYPE>(GRAPHIC|EXCEL|ZIP).*?<TEXT>\s*begin)(.*?)(end)', re.DOTALL)
        self.text_clean = pattern.sub(r'\1\nend', self.text_clean)
        return self

    def transform(self, text):
        self._strip_bs4_tags(text)
        self._strip_re_tags()
        return self.text_clean





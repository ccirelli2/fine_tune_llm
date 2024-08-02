"""
Noisy text to inspect

"""
import os
import re
import pandas as pd
import chardet
import asyncio
import aiofiles
from bs4 import BeautifulSoup


# Patterns
class FilingIndex:
    """
    Create Filing Index dataframe.
    
    Data is generated from headers in each edgar filings.
    Essentially, a regex statement is used to extract certain standard key value
    pairs that appear in every filings.
    These data attributes constitute the metadata for each file.

    Patterns (example):
    """
    def __init__(self, directory: str, patterns: dict = {}, filenames: list = []):
        self.directory = directory
        self.filenames = filenames 
        self.patterns = patterns
        self.filing_df = pd.DataFrame({})
        self.struct = {}
        
        if not filenames:
            print("Filenames not provided.  Taking from directory")
            self.filenames = os.listdir(directory)
        print("Total Files => {}".format(len(self.filenames)))
        
        if not patterns:
            patterns = {
                "CIK": "CENTRAL INDEX KEY:.*\n",                                           
                "FILING_TYPE": "CONFORMED SUBMISSION TYPE:.*\n",                           
                "FILING_DATE": "FILED AS OF DATE:.*\n",                                    
                "COMPANY_NAME": "COMPANY CONFORMED NAME:.*\n",                             
                "CIK": "CENTRAL INDEX KEY:.*\n",                                           
                "IRS_NUMBER": "IRS NUMBER:.*\n",   
            }
        print(f"Metadata fields to generate from filings => {patterns.keys()}")
        print(f"{__class__} instantiated successfully")

    def _open_file(self, filename):
        """TODO: add dynamic encoding identification
        """
        try:
            path = os.path.join(self.directory, filename)
            with open(path, 'r') as f:
                text = f.read()
        except Exception as e:
            print("Opening file caused error => {}".format(e))
            text = ""
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
        self.bs4_tags = ['img', 'table', 'canvas', 'graphic', 'link', 'a']
        self.re_tags = ["GRAPHIC", "EXCEL", "ZIP"]
        self.parser = 'lxml'
        self.text = ""
        print(f"{__class__} instantiated successfully")

    
    def _strip_bs4_tags(self, text):
        """                                                                            
        Function to remove html from underlying text using the BeautifulSoup library.
        """             
        print(f"\tStripping html tags => {self.bs4_tags}")

        # Parse HTML                                                            
        soup = BeautifulSoup(text, self.parser)                            
        # Remove all images                                                     
        for tag in self.bs4_tags:
            for element in soup.find_all(tag):                                        
                element.decompose()  # acts on soup obj.                                
        
        self.text = soup.get_text(separator="\n", strip=True)                 
        return self

    def _strip_doctype_tags(self):
        """
         
        """
        print(f"\tStripping re tags {self.re_tags}")
        pattern = re.compile('<TYPE>GRAPHIC|EXCEL|ZIP|XML|XBRL.*</DOCUMENT>')
        self.text = re.sub(pattern, '', self.text)
        return self

    def _strip_xbrl_tags(self):
        print(f"\tStripping XBRL tags")
        pattern = re.compile(r'<XBRL.*</XBRL>|XBRL DOCUMENT.*/DOCUMENT', re.DOTALL)
        self.text = re.sub(pattern, '', self.text)
        return self

    def _get_file_encoding(self, path):                                            
        with open(path, 'rb') as f:                                                
            raw_data = f.read(100_000)                                               
        encoding = chardet.detect(raw_data)['encoding']                            
        return encoding                                                            

    def _write_file(self, path, txt_obj: str):
        """
        """
        print(f"Writing {path}")
        with open(path, 'w') as f:
            f.write(txt_obj)
            print("Successful")
        return self

    def transform(self, text):
        self._strip_bs4_tags(text)
        self._strip_doctype_tags()
        self._strip_xbrl_tags()
        return self.text

    def transform_from_directory(self, input_dir, output_dir):
        """
        Assumes files are of type .txt
        """
        # Get Files From Directory
        files = os.listdir(input_dir)
        txt_files = [i for i in files if i.endswith('.txt')]
        print(f"\tTotals Files Found in Directory => {len(txt_files)}")

        # Iterate Files in Directory
        for tf in txt_files:
            path = os.path.join(input_dir, tf)
            encoding = self._get_file_encoding(path)
            
            # Open & Clean Text
            with open(path, mode='r', encoding=encoding) as f:
                print(f"\t Cleaning text file => {tf}")
                try:
                    text = f.read()
                    text = self.transform(text)
                except Exception as e:
                    print(f"ERROR: => {e}")
                    text = "text clearning resulted in an error"
                # Write Text to Output Directory
                path = os.path.join(output_dir, tf)
                self._write_file(path, text)

        pass


class CleanTextAsync:
    """Class to clean text documents asynchronously."""

    def __init__(self, max_concurrent_files=10):
        self.bs4_tags = ['img', 'table', 'canvas', 'graphic', 'link', 'a']
        self.re_tags = ["GRAPHIC", "EXCEL", "ZIP"]
        self.parser = 'lxml'
        self.text = ""
        self.semaphore = asyncio.Semaphore(max_concurrent_files)

        print(f"{__class__} instantiated successfully")

    def _strip_bs4_tags(self, text):
        """Remove HTML from underlying text using BeautifulSoup."""
        print(f"\tStripping HTML tags => {self.bs4_tags}")

        # Parse HTML
        soup = BeautifulSoup(text, self.parser)
        # Remove specified tags
        for tag in self.bs4_tags:
            for element in soup.find_all(tag):
                element.decompose()

        self.text = soup.get_text(separator="\n", strip=True)
        return self

    def _strip_doctype_tags(self):
        """Strip DOCTYPE tags."""
        print(f"\tStripping RE tags {self.re_tags}")
        pattern = re.compile('<TYPE>GRAPHIC|EXCEL|ZIP|XML|XBRL.*</DOCUMENT>')
        self.text = re.sub(pattern, '', self.text)
        return self

    def _strip_xbrl_tags(self):
        """Strip XBRL tags."""
        print(f"\tStripping XBRL tags")
        pattern = re.compile(r'<XBRL.*</XBRL>|XBRL DOCUMENT.*/DOCUMENT', re.DOTALL)
        self.text = re.sub(pattern, '', self.text)
        return self

    async def _get_file_encoding(self, path):
        async with aiofiles.open(path, 'rb') as f:
            raw_data = await f.read(100_000)
        encoding = chardet.detect(raw_data)['encoding']
        return encoding

    async def _read_file(self, path):
        encoding = await self._get_file_encoding(path)
        try:
            async with aiofiles.open(path, 'r', encoding=encoding) as f:
                return await f.read()
        except Exception as e:
            print("Reading file {} generated error => {}".format(path, e))
            return "error"

    async def _write_file(self, path, txt_obj):
        """Write cleaned text to a file."""
        print(f"Writing {path}")
        async with aiofiles.open(path, 'w') as f:
            await f.write(txt_obj)
            print("Successful")

    async def process_file(self, path, output_dir):
        """Process a single file and write cleaned text to output directory."""
        async with self.semaphore:
            text = await self._read_file(path)
            self._strip_bs4_tags(text)
            self._strip_doctype_tags()
            self._strip_xbrl_tags()
            cleaned_text = self.text
            output_path = f"{output_dir}/{path.split('/')[-1]}"
            await self._write_file(output_path, cleaned_text)

    async def process_files(self, source_dir, output_dir):
        """Process all files in source_dir asynchronously."""
        import glob
        paths = glob.glob(f"{source_dir}/*.txt")
        tasks = [self.process_file(path, output_dir) for path in paths]
        await asyncio.gather(*tasks)


class ConcatArchives:                                                              
    """
    Concat tab separated files located in various archives or sub directories.

    Args:
        input_dir: directory where archives or sub-folders are located.
        output_dir: output directory where to write concatenated files.
        target_files: a list of file names located in archives.

    Return:
        files written to output directory.
    """                                                                            
    def __init__(self, input_dir: str, output_dir: str, target_files: list):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.target_files = target_files                                           
        self.concat_df = pd.DataFrame({})                                          
        assert os.path.exists(self.input_dir)                                    
        print(f"{__class__} instantiated succesffully")                            
                                                                                   
    def _create_directory(self):
        if not os.path.exists(self.output_dir):
            print("\tCreating output directory => {}".format(self.output_dir))         
        return self                                                                
                                                                                   
    def _get_file_encoding(self, path):                                            
        with open(path, 'rb') as f:                                                
            raw_data = f.read(10000)                                               
        encoding = chardet.detect(raw_data)['encoding']                            
        return encoding                                                            
                                                                                   
    def _concat_archive_file_by_name(self, target_file: str):                      
        """
        TODO: Technically these are not archives but sub directories.
            Maybe we should change to deal with zip files directly.
        :target_file: file name within archives to extract and concat
        """                                                                        
        print(f"\tConcatanating files for => {target_file}")                       
                                                                                   
        archives = os.listdir(self.input_dir)                                    
                                                                                   
        frames = []                                                                
                                                                                   
        for a in archives:                                                         
            path = os.path.join(self.input_dir, a, target_file)                  
            if os.path.exists(path):                                               
                try:                                                               
                    encoding = self._get_file_encoding(path)                       
                    frames.append(pd.read_csv(path, delimiter='\t', encoding=encoding))
                except Exception as e:                                             
                    print("Reading file {} generated error {}".format(target_file, e)) 
            else:                                                                  
                print("Path => {path} does not exists")                            
        if frames:                                                                 
            self.concat_df = pd.concat(frames)                                     
        return self

    def _write_dataframe(self, target_file: str):                                  
        print("\tWriting concatenated file {} to {}".format(
            target_file, self.output_dir)
        )
                                                                                   
        self._create_directory()                                            
        output_filename = target_file.replace('.txt', '.csv')                   
        path = os.path.join(self.output_dir, output_filename)                   
        self.concat_df.to_csv(path)                                             
        print("\tWritten successfully")                                         
        return self                                                             
                                                                                
    def transform(self):                                                        
        print("\tRunning transform for all files => {}".format(self.target_files))
        for file in self.target_files:                                          
            self._concat_archive_file_by_name(file)                             
            self._write_dataframe(file)                                         
        print("Transform completed")  


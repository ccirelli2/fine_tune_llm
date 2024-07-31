"""
Noisy text to inspect

    filename1.pdf
    begin 644 filename1
    M)5!$1BTQ+C4*)>+CS],*,2 P(&]B:@H\/"]#;VQO
    7!E+UA/8FIE8W0O5VED=&@@,30R."],96YG=&@@,S8U+T)I='-097)#
    M;VUP;VYE;G0@.#X^
    GI]?5504-$1$1$1$1$+N;M[>WIZ>GAX6&_WS<"Q:]?O^[O
    M[^.KQW.(\K]__VZJBLJ1,EY>7M0Q1$1$1$1$1&3"Q\<'QA6_?__&K *98K_?
    MQY;8?A/O#TPX@I>7%X21/%;\C7_3)..&IR8B(B(B(B(B_S1O;V^/CX_5*"(^
    MQY;GY^?M2@6B1/]YSL>!EY<7O%&R ?O]_N'A(;9??E8B(B(B(B(B\H^#5P@N
    M(=@\/#P\;+%YB +89F1$B_P<-7Q\?-S?WZ=72)2,HZ2;2=4TL.*H-<>^T8#'
    MQ\=T5&''V*A'B8B(B(B(B,C_A]?75T)NHCQ@X;#=3>/CXR-V2>&"9"+H%?%W
    M.8@2J68\/S_'O_O]'AT#[2)VP
    !?#0T2=<91L)!J("H:(B(B(B(C(#^;]
    M_?WY^3G5@/O[^SY")I$HTG B"@\=-V(OZOG]^_=R$$.B
    MGI[8]_'QD:](J)HJ1]0PE% :$0/CD"_I(!$1$1$1$1'Y0WQ\?*1[R*]?O_#=
    M2-6"H!-1($->D/LC_DW]H:^0;Z,\3B($QXB-B ^Q$5L+CI@UH&/4.MD2Q:))
    M%(Y*>G4BJN444GA1P1 1$1$1$1'Y ;#DQVB!+![5T +) N.*:@(1GY>B/P2]
    M]47:9CP^/J8Z42N/FM-X(ZTILL(:^"+M-U(M09T@7FAC&8)9"#$Z5#!$1$1$
    M1$1$_EUBR1\+_[2UZ(-%O+^_IQD#7T7Y3/-!F=0??O_^W>Q>_4K2CJ*6B?HS
    MWB9*17R;TD3U#4%4P>XB;3 R: :6&+4\T3!2P6A"@(J(B(B(B(C(WP_!,%GX
    M-ZI%>HN0G!0)@BWO[^\I%V29S%O:6#ADN,[8Z_[
    TEXT-EXTRACT
    2

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

    def transform(self, text):
        self._strip_bs4_tags(text)
        self._strip_doctype_tags()
        self._strip_xbrl_tags()
        return self.text





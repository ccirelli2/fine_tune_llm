import os
import chardet
import pandas as pd

# Directories
DIR_DATA="/Users/temp-admin/repositories/fine_tune_llm/data/validation/raw"
DIR_OUTPUT = DIR_DATA.replace("/raw", "/clean")

# Archive Names
archives = os.listdir(DIR_DATA)
file_names = ['tag.txt', 'pre.txt', 'sub.txt', 'num.txt']

# Open Files
class ConcatArchives:
    """
    """
    def __init__(self, archive_dir: str, target_files: list, archive_dir_suffix: str = "/raw"):
        self.archive_dir = archive_dir
        self.archive_dir_suffix = archive_dir_suffix
        self.target_files = target_files
        self.output_dir = archive_dir.replace(archive_dir_suffix, "/clean")
        self.concat_df = pd.DataFrame({})
        assert os.path.exists(self.archive_dir)
        print(f"{__class__} instantiated succesffully")

    def _create_directory(self):
        print("\tCreating output directory => {}".format(self.output_dir))
        return self

    def _get_file_encoding(self, path):
        with open(path, 'rb') as f:
            raw_data = f.read(10000)
        encoding = chardet.detect(raw_data)['encoding']
        return encoding

    def _concat_archive_file_by_name(self, target_file: str):
        """
        """
        print(f"\tConcatanating files for => {target_file}")
        
        archives = os.listdir(self.archive_dir)

        frames = []
        
        for a in archives:
            path = os.path.join(self.archive_dir, a, target_file)
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
        print("\tWriting concatenated file {} to {}".format(target_file, self.output_dir))
        
        if not os.path.exists(self.output_dir):
            self._create_directory()

        self.concat_df.to_csv(os.path.join(self.output_dir, target_file))
        
        print("\tWritten successfully")
        return self

    def transform(self):
        print("\tRunning transform for all files => {}".format(self.target_files))
        for file in self.target_files:
            self._concat_archive_file_by_name(file)
            self._write_dataframe(file)
        print("Transform completed")




if __name__ == "__main__":
    
    concat_archives = ConcatArchives(
        archive_dir=DIR_DATA,
        target_files=file_names
    ).transform()
    
    






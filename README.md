# fine_tune_llm
Fine tune llm.  Validate via rag pipeline. 

# Transformation Pipeline (see: fine_tune_llm/transforms)
- create-base-sql-tables:
    script to programatically build the required mysql tables.
- unpack-filing-archives:
    the edgar filings that were copied from arc.insight
    reside in gzip archives.  This code extracts them into a single txt
    directory for downstream preprocessing.
- unpack-validation-archives:
    the edgar financial-statement data used for validation reside in archives
    within which are a set of N unique files.  This code goes into each archive
    extracts the file & saves it to the validation/raw directory.
- clean-text: this code takes as input the raw-text files, cleans them of
    html and other noisy text and then writes them to a clean files directory.
- build-filing-index-table:
    This code takes as input the files in the clean-text directory.
    For each file it searches for a set of 6 metadata variables.
    It then upserts the file name + metadata variables to mysql, effectively
    creating a filing index table of all filings.
    metadata fields: cik, filing type, filing date, company name, cik, irs num.
- build-filing-chunk-table:
    Takes as input the directory w/ clean text files.
    Chunks each filing and uploads chunks to a mysql table.
    Chunk table relates to filing-index table via foreign key.
- create-collection:
    Code that creates that chromadb edgar-filing collection from
    i.) the filing-index table used for metadata
    ii.) the filing-chunk table.
    iii.) embeddings of chunked text.
- build-validation-mysql-tables:
    Code that automates building the validation mysql tables.
- build-validation-datasets
    Code that automates the insertion of validation data into the validation
    mysql tables. 


# TOOD
- Add log handler & log file.  Replace print with logs.
- Change hardcoded directory & paths to config


# References

### Filing Definitions
Accession Number: uniuqe ID given to each filing.
    It combines the CIK id

### Validation Dataset
- https://www.sec.gov/about/dera_financial-statement-data-set
- data dictionary: https://www.sec.gov/files/aqfs.pdf


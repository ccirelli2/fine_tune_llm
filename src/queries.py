"""
Project service queries (ex: mysql, chromadb
"""
import pandas as pd

def command_create_mysql_filings_index_table():
    sql = """
        CREATE TABLE filing_index (
            id varchar(250) NOT NULL,
            file_name varchar(255),
            file_type varchar(255),
            file_date varchar(255),
            company_name varchar (255),
            cik varchar(255),
            irs_number varchar(255),
        PRIMARY KEY (id)
        );
    """
    return sql

def command_create_mysql_rag_queries_table():
    sql = """
        CREATE TABLE rag_query (
            id INT AUTO_INCREMENT,
            query_name varchar(250),
            query_category varchar(250),
            query_string varchar(500),
            query_attributes varchar(500),
        PRIMARY KEY (id)
    );
    """
    return sql

def command_create_mysql_rag_prompt_table():
    sql = """
        CREATE TABLE rag_prompt (
            id INT AUTO_INCREMENT,
            prompt_name varchar(250),
            prompt_category varchar(250),
            prompt_string varchar(500),
            prompt_attributes varchar(500),
            prompt_version varchar(250),
        PRIMARY KEY (id)
    );"""
    return sql

def command_create_mysql_chunk_table():
    sql = """
    
    CREATE TABLE filing_chunks (
        id              varchar(250) NOT NULL,
        text            LONGTEXT,
        character_count varchar(250),
        token_count     varchar(250),
        foreign_id      varchar(250) NOT NULL,
    PRIMARY KEY (id)
    );
    """
    return sql


def command_create_mysql_validation_num_table():
    sql = """
    
    CREATE TABLE validation_num (
        id          INT AUTO_INCREMENT,
        adsh        varchar(250),
        tag         varchar(250),
        version     varchar(250),
        coreg       varchar(250),
        ddate       varchar(250),
        qtrs        varchar(250),
        uom         varchar(250),
        value       varchar(250),
        footnote    LONGTEXT,
    PRIMARY KEY (id)
    );
    """
    return sql


def command_create_mysql_validation_pre_table():
    sql = """
    
    CREATE TABLE validation_pre ( 
        id          INT AUTO_INCREMENT,
        adsh        varchar(250),
        report      varchar(250),
        line        varchar(250),
        stmt        varchar(250),
        inpth       varchar(250),
        rfile       varchar(250),
        tag         varchar(250),
        version     varchar(250),
        plabel      LONGTEXT,
        negating    varchar(250),
    PRIMARY KEY (id)
    );
    """
    return sql

def command_create_mysql_validation_sub_table():
    sql = """
    
    CREATE TABLE validation_sub (
        id INT AUTO_INCREMENT,
        adsh VARCHAR(250),
        cik VARCHAR(250),
        name VARCHAR(250),
        sic VARCHAR(250),
        countryba VARCHAR(250),
        stprba VARCHAR(250),
        cityba VARCHAR(250),
        zipba VARCHAR(250),
        bas1 VARCHAR(250),
        bas2 VARCHAR(250),
        baph VARCHAR(250),
        countryma VARCHAR(250),
        stprma VARCHAR(250),
        cityma VARCHAR(250),
        zipma VARCHAR(250),
        mas1 VARCHAR(250),
        mas2 VARCHAR(250),
        countryinc VARCHAR(250),
        stprinc VARCHAR(250),
        ein VARCHAR(250),
        former VARCHAR(250),
        changed VARCHAR(250),
        afs VARCHAR(250),
        wksi VARCHAR(250),
        fye VARCHAR(250),
        form VARCHAR(250),
        period VARCHAR(250),
        fy VARCHAR(250),
        fp VARCHAR(250),
        filed VARCHAR(250),
        accepted VARCHAR(250),
        prevrpt VARCHAR(250),
        detail VARCHAR(250),
        instance VARCHAR(250),
        nciks VARCHAR(250),
        aciks VARCHAR(250),
    PRIMARY KEY (id)
    );
    """
    return sql


def command_create_mysql_validation_tag_table():
    sql = """
    
    CREATE TABLE validation_tag (
        id          INT AUTO_INCREMENT,
        tag         VARCHAR(250),
        version     VARCHAR(250),
        custom      VARCHAR(250),
        abstract    VARCHAR(250),
        datatype    VARCHAR(250),
        iord        VARCHAR(250),
        crdr        VARCHAR(250),
        tlabel      LONGTEXT,
        doc         LONGTEXT,
    PRIMARY KEY (id)
    );
    """
    return sql


def command_create_mysql_experiments_table():
    """
    Args:
        id:
        name:
        description:
        author:
    """
    sql = """
    CREATE TABLE experiments (
        id              varchar(250),
        name            varchar(250),
        description     LONGTEXT,
        author          varchar(250),
        created         TIMESTAMP,
    PRIMARY KEY (id)
    );
    """
    return sql


def command_create_mysql_trials_table():
    """
    Args
        id: the primary key for the trials.  Each trial is unique.
        name: the name associated with the trials.
        description: description of trial.  Should include objective of test.
        outcome: the expected outcome of the trials.
        author: name of individual {last-name, first-name}
        experiment_id: used to link trials to experiments.
    """
    sql = """
    CREATE TABLE trials (
        trial_id                  varchar(250),,
        name                varchar(250),
        description         LONGTEXT,
        outcome             LONGTEXT,
        author              LONGTEXT,
        created             TIMESTAMP,
        experiment_id       varchar(250),
    PRIMARY KEY (id)
    );
    """
    return sql


def command_create_mysql_trial_parameters_table():
    """
    Key value pairs associated with the parameters and values of a trial.
    The objective is to have a table that captures the environment used to
    validate a model.
    
    Examples:
        model name, description, checkpoint, source
        validation data source
        validation data config (ex: decisions related to chunk size, etc.)
        model temperature
        model fine tuning config (ex: decisions related to fine tuning).
        query, prompt, version numbers.
    
    Args:
        id:
        name: parameter name
        value: parameter value
        category: category of field.  Optional.
        datatype: parameter data type (used for data conversion)
        trial_id: foreign key to link back to trial table.
    """
    sql = """
    CREATE TABLE trial_parameters (
        id              INT AUTO_INCREMENT,
        name            varchar(250),
        value           varchar(250),
        category        varchar(250),
        datatype        varchar(250),
        trial_id        varchar(250),
    PRIMARY KEY (id)
    );
    """
    return sql


def command_create_mysql_models_table():
    """
    List of models and metadata from which to select for experiments and 
    trials.
    """
    sql = """
    CREATE TABLE models (
        id              varchar(250),
        name            varchar(250),
        checkpoint      varchar(250),
        version_no      varchar(250),
        description     varchar(250),
        source          varchar(250),
        created         varchar(250),
    PRIMARY KEY (id)
    );
    """
    return sql


def command_create_mysql_trial_extraction_table():
    """
    Capture output from extractions
    """
    sql = """
        CREATE TABLE trial_extractions(                                            
            call_id varchar(250),                                                  
            trial_id varchar(250),                                                 
            cik varchar(250),                                                      
            company_name varchar(250),                                             
            financial_metric_name_requested varchar(250),                          
            financial_metric_year_requested INT,                                   
            financial_metric_name_extracted varchar(250),                          
            financial_metric_value_extracted varchar(250),                         
            units varchar(250),
            chunk_used LONGTEXT,
            llm_logic LONGTEXT,                                                    
            pay_load LONGTEXT,                                                 
        PRIMARY KEY (call_id)    
    );
    """
    return sql


def command_create_mysql_trial_results_table():
    """
    """
    sql = """
    CREATE TABLE trial_results (
        id                      varchar(250),
        gt_variable_name        varchar(250),
        gt_variable_value       varchar(250),
        gt_variable_dtype       varchar(250),
        extracted_value         varchar(250),
        is_absolute_match       boolean,
        is_fuzzy_match          boolean,
        fuzzy_match_threshold   float,
        gt_id                   INT,
        trial_id                INT,
        created                 TIMESTAMP,
    PRIMARY KEY (id)

    );
    """
    return sql


def insert_into_filing_index_table(client, values: tuple):
    """
    """
    sql = """
    INSERT INTO
        filing_index
        (id, file_name, file_type, file_date, company_name, cik, irs_number)
    VALUES
        (%s, %s, %s, %s, %s, %s, %s);
    """             
    print("Inserting row => {}".format(values))
    try:
        print("\tExecuting insertion to table => filing_index")
        cursor = client.cursor()
        cursor.execute(sql, values)
        client.commit()
        print("\tSuccess")
        
    except Exception as e:
        print(f"\tInsertion command generated error => {e}")
    
    return None


def insert_into_validation_num(client, values: tuple):
    """
    """
    sql = """                                                                      
        INSERT INTO validation_num                                                     
            (adsh, tag, version, coreg, ddate, qtrs, uom, value, footnote)                 
        VALUES                                                                         
            (%s, %s, %s, %s, %s, %s, %s, %s, %s);                                          
    """    
    print("Inserting row => {}".format(values))
    try:
        print("\tExecuting insertion to table => filing_index")
        cursor = client.cursor()
        cursor.execute(sql, values)
        client.commit()
        print("\tSuccess")
        
    except Exception as e:
        print(f"\tInsertion command generated error => {e}")
    
    return None


def insert_into_validation_pre(client, values: tuple):
    """
    """
    sql = """                                                                   
    INSERT INTO validation_pre                                                  
        (adsh, report, line, stmt, inpth, rfile, tag, version, plabel, negating)    
    VALUES                                                                      
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);                                   
    """        

    print("Inserting row => {}".format(values))
    try:
        print("\tExecuting insertion to table => filing_index")
        cursor = client.cursor()
        cursor.execute(sql, values)
        client.commit()
        print("\tSuccess")
        
    except Exception as e:
        print(f"\tInsertion command generated error => {e}")
    
    return None


def insert_into_validation_sub(client, values: tuple):
    """
    """
                                                                                    
    sql = """
    INSERT INTO validation_sub                                                  
        (adsh, cik, name, sic, countryba, stprba, cityba, zipba, bas1, bas2, baph,  
        countryma, stprma, cityma, zipma, mas1, mas2, countryinc, stprinc, ein,     
        former, changed, afs, wksi,fye, fye, form, period, fy, fp, filed, accepted, 
        prevrpt, detail, instance, nciks, aciks)                                    
                                                                                
    VALUES                                                                      
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,                                    
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,                                    
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,                                    
        %s, %s, %s, %s, %s, %s, %s, %s);
    """  

    print("Inserting row => {}".format(values))
    try:
        print("\tExecuting insertion to table => filing_index")
        cursor = client.cursor()
        cursor.execute(sql, values)
        client.commit()
        print("\tSuccess")
        
    except Exception as e:
        print(f"\tInsertion command generated error => {e}")
    
    return None


def insert_into_validation_tag(client, values: tuple):
    """
    """
    sql = """
    INSERT INTO validation_tag
        (tag, version, custom, abstract, datatype, iord, crdr, tlabel, doc)
    VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s);                                        
    """

    print("Inserting row => {}".format(values))
    try:
        print("\tExecuting insertion to table => filing_index")
        cursor = client.cursor()
        cursor.execute(sql, values)
        client.commit()
        print("\tSuccess")
        
    except Exception as e:
        print(f"\tInsertion command generated error => {e}")
    
    return None



def get_filing_index_join_chunks():
    """
    TODO: Change name to query_
    """
    query = """
        SELECT
            fi.id,
            fi.file_name,
            fi.file_type,
            fi.file_date,
            fi.company_name,
            fi.cik,
            fi.irs_number,
            fc.id AS chunk_id,
            fc.chunk,
            fc.character_count,
            fc.token_count
    
        FROM filing_index AS fi
        INNER JOIN filing_chunks fc ON fi.file_name = fc.foreign_id;
    """
    return query


def query_get_current_experiments(client):
    """
    """
    sql = """
    SELECT *
    FROM experiments;
    """
    df = pd.DataFrame({})
    status = False
    error = "None"

    try:
        df = pd.read_sql(sql, client) 
        status = True
    except Exception as e:
        df = pd.DataFrame({})
        error = e
    return df, status, error


def insert_into_experiments(client, values: tuple):
    """
    """
    sql = """
    INSERT INTO experiments
        (id, name, description, author, created)
    VALUES
        (%s, %s, %s, %s, %s);                                        
    """
    status = False
    error = "None"
    try:
        print("\tExecuting insertion")
        cursor = client.cursor()
        cursor.execute(sql, values)
        client.commit()
        status = True 
    except Exception as e:
        status = False
        error = e
    return status, error


def query_get_current_trials(client):
    """
    """
    sql = """
    SELECT *
    FROM trials;
    """
    df = pd.DataFrame({})
    status = False
    error = "None"

    try:
        df = pd.read_sql(sql, client) 
        status = True
    except Exception as e:
        df = pd.DataFrame({})
        error = e
    return df, status, error


def insert_into_trials(client, values: tuple):
    """
    """
    sql = """
    INSERT INTO trials
        (trial_id, name, description, outcome, author, experiment_id, created)
    VALUES
        (%s, %s, %s, %s, %s, %s, %s);
    """
    status = False
    error = "None"
    try:
        print("\tExecuting insertion")
        cursor = client.cursor()
        cursor.execute(sql, values)
        client.commit()
        status = True
    except Exception as e:
        status = False
        error = e
    return status, error


def get_filing_index_companies(client):
    """
    Return unique set of company names from filing_index table. 
    """
    sql = """
    SELECT DISTINCT company_name, cik
    FROM filing_index;
    """
    df = pd.DataFrame({})
    status = False
    error = "None"

    try:
        df = pd.read_sql(sql, client) 
        status = True
    except Exception as e:
        df = pd.DataFrame({})
        error = e
    return df, status, error


def insert_into_trial_parameters_table(client, df: pd.DataFrame):
    """
    """
    table = "trial_parameters"
    status = False
    error = "None"
    try:
        print(f"Inserting {df.shape[0]} rows into {table}")
        df.to_sql(table, con=client, if_exists='append', index=False)
        print("Insertion successfull")
        status = True
    except Exception as e:
        error = e
        print(f"Insertion failed with exception => {e}")
    return status, error


def query_get_all_records_from_models(client):
    sql = """
        SELECT * FROM models;
    """
    df = pd.DataFrame({})
    status = False
    error = "None"

    try:
        df = pd.read_sql(sql, client) 
        status = True
    except Exception as e:
        df = pd.DataFrame({})
        error = e
    return df, status, error

# TODO: Change name to a more generic retrieval function
class ExtractTrialData:
    def __init__(self, client):
        self.client = client
        self.query = ""
        self.data = pd.DataFrame({})
        self.status = False
        self.error = "None"
        print(f"{__class__} instantiated correctly")

    def _create_base_query(self, table_name, trial_id: str):
        print("\tBuilding base query using table {} and trial-id {}".format(
            table_name, trial_id)
        )
        if trial_id:
            self.query = """
                SELECT *
                FROM {}
                WHERE trial_id = '{}';
            """.format(table_name, trial_id)
        
        else:
            self.query = "SELECT * FROM {}".format(table_name)
        return self

    def _execute_query(self):
        """
        """
        print("\tExecuting query")
        try:
            self.data = pd.read_sql(self.query, self.client) 
            self.status = True
            print("\t\tQuery successfull")
        except Exception as e:
            self.error = e
            print(f"\t\tQuery failed with error => {e}")
        return self

    def fetch_data(self, table_name: str, trial_id: str = None):
        """
        """
        self._create_base_query(table_name, trial_id)
        self._execute_query()
        return self.data


def insert_into_trial_extraction_table(client, values):
    """
    """
    status = False
    error = "None"

    sql = """
        INSERT INTO trial_extractions (
            call_id,
            trial_id,
            cik,
            company_name,
            financial_metric_name_requested,
            financial_metric_year_requested,
            financial_metric_name_extracted,
            financial_metric_value_extracted,
            units,
            chunk_used,
            llm_logic,
            pay_load
            )
        VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        );
    """
    print("Inserting row => {}".format(values))
    try:
        print("\tExecuting insertion to table => filing_index")
        cursor = client.cursor()
        cursor.execute(sql, values)
        client.commit()
        print("\tSuccess")
        status = True
        
    except Exception as e:
        print(f"\tInsertion command generated error => {e}")
        error = e
    return status, error



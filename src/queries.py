"""
Project service queries (ex: mysql, chromadb
"""

# Create MySql Tables
# index table schema
# text table schema
# chunk table schema
# embeddings table schema


def query_create_mysql_filings_index_table():
    query = """
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
    return query


def create_mysql_chunk_table():
    sql = """
    
    CREATE TABLE filing_chunks (
        id varchar(250) NOT NULL,
        text LONGTEXT,
        character_count varchar(250),
        token_count varchar(250),
        foreign_id varchar(250) NOT NULL,
    PRIMARY KEY (id)
    );
    """
    return slq


def create_mysql_valiation_num_table():
    sql = """
    
    CREATE TABLE validation_num (
        adsh varchar(250) NOT NULL,
        tag varchar(250),
        version varchar(250),
        coreg varchar(250),
        ddate varchar(250),
        qtrs varchar(250),
        uom varchar(250),
        value varchar(250),
        footnote varchar(500),
    PRIMARY KEY (adsh)
    );
    """
    return sql


def create_mysql_validation_pre_table():
    sql = """
    
    CREATE TABLE validation_pre ( 
        adsh varchar(250) NOT NULL,
        report varchar(250),
        line varchar(250),
        stmt varchar(250),
        inpth varchar(250),
        rfile varchar(250),
        tag varchar(250),
        version varchar(250),
        plabel varchar(250),
        negating varchar(250)
        PRIMARY KEY (adsh)
    );
    """
    return sql

def create_mysql_validation_sub_table():
    sql = """
    
    CREATE TABLE validation_sub (
        adsh VARCHAR(250) NOT NULL,
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
    PRIMARY KEY (adsh)
    );
    """
    return sql


def create_mysql_validation_tag_table():
    sql = """
    
    CREATE TABLE validation_tag (
        tag VARCHAR(250) NOT NULL,
        version VARCHAR(250),
        custom VARCHAR(250),
        abstract VARCHAR(250),
        datatype VARCHAR(250),
        iord VARCHAR(250),
        crdr VARCHAR(250),
        tlabel VARCHAR(250),
        doc VARCHAR(250),
    PRIMARY KEY (tag)
    );
    """
    return sql

def insert_into_filing_index_table(client, values: tuple):
    """
    """
    sql = """                                                                                              
        INSERT INTO filing_index (id, file_name, file_type, file_date, company_name, cik, irs_number)
        VALUES (%s, %s, %s, %s, %s, %s, %s)                                        
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






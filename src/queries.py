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
    
    CREATE TABLE filing_chunks
        id varchar(250) NOT NULL,
        text LONGTEXT,
        character_count varchar(250),
        token_count varchar(250),
        foreign_id varchar(250) NOT NULL,
        PRIMARY KEY (id)
    """
    return slq


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






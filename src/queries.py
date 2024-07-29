"""
Project service queries (ex: mysql, chromadb
"""

# Create MySql Tables
# index table schema
# text table schema
# chunk table schema
# embeddings table schema


create_mysql_filings_index_table = """
    CREATE TABLE filings (
        id int NOT NULL AUTO_INCREMENT,
        file_name varchar(255) NOT NULL,
        cik varchar(255) NOT NULL,
        created TIMESTAMP,
        PRIMARY KEY (id)
    );
"""


import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """ iterates on copy statements in sql_quries.py to load data of files in AWS S3 bucket to staging tables in AWS redsihft
           
    Args:
        curr (obj): object of curser class
        conn (obj): connection object
        
    Returns:
        no return values
    """    
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
""" iterates on insert statements in sql_quries.py to select data from staging tables and insert them into star schema tables
           
    Args:
        curr (obj): object of curser class
        conn (obj): connection object
        
    Returns:
        no return values
 """       
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Establishes connection to the redshift cluster using configtration data in dwh.cfg and gets
      cursor to it.
    - loads data from S3 bucket files into redshift  
    - inserts loaded data from staging tables into star schema tables
    - Finally, closes the connection.
           
    Args:
        no Args
        
    Returns:
        no return values
 """  
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

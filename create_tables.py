import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """ iterates on drop statements in sql_quries.py to drop created tables
           
    Args:
        curr (obj): object of curser class
        conn (obj): connection object
        
    Returns:
        no return values
    """  
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """ iterates on insert statements in sql_quries.py to create staging and star schema tables on redshift cluster
           
    Args:
        curr (obj): object of curser class
        conn (obj): connection object
        
    Returns:
        no return values
 """   
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Establishes connection to the redshift cluster using configtration data in dwh.cfg and gets
      cursor to it.
    - drops created tables  
    - creates staging and star schema tables
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

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

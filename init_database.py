import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE employees (
            employee_id CHAR(9) PRIMARY KEY,
            employee_name VARCHAR(50) NOT NULL,
            title VARCHAR(20) NOT NULL,
            phone VARCHAR(11) NOT NULL, 
            birthdate DATE NOT NULL
        )
        """,
        """ CREATE TABLE attendance (
                employee_id CHAR(9),
                date DATE NOT NULL,
                time TIME NOT NULL,
                PRIMARY KEY (date, time),
                FOREIGN KEY (employee_id)
                    REFERENCES employees (employee_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('The database was initialized.')


if __name__ == '__main__':
    create_tables()
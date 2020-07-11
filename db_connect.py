#from employees import Employee


# SQL queries:


def employees_count(cur):  # returns number of records in employee table
    sql = '''SELECT COUNT(*) FROM employees;'''
    cur.execute(sql)
    return cur.fetchone()


def check_id_exist(cur, e_id):  # returns 1 if finds ID, else returns 0
    sql = '''SELECT COUNT(1) FROM employees WHERE employee_id=%s'''
    cur.execute(sql, (e_id,))
    return cur.fetchone()[0]


def add_employee(cur, employee):
    sql = '''INSERT INTO employees VALUES (%s,%s,%s,%s,%s)'''
    cur.execute(sql, (employee.id, employee.name, employee.title, employee.phone, employee.birthday,))

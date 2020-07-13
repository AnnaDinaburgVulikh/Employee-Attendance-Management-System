# SQL queries:


def employees_count(cur):  # returns number of records in employee table
    sql = '''SELECT COUNT(*) FROM employees;'''
    cur.execute(sql)
    return cur.fetchone()


def check_id_exist(cur, emp_id):  # returns 1 if finds ID, else returns 0
    sql = '''SELECT COUNT(1) FROM employees WHERE employee_id = %s'''
    cur.execute(sql, (emp_id,))
    return cur.fetchone()[0]


def add_employee(cur, employee):  # adds employee to the database
    sql = '''INSERT INTO employees VALUES (%s,%s,%s,%s,%s)'''
    cur.execute(sql, (employee.id, employee.name, employee.title, employee.phone, employee.birthday,))


def delete_employee(cur, emp_id):  # deletes employee to the database
    sql = '''DELETE FROM employees WHERE employee_id = %s'''
    cur.execute(sql, (emp_id,))


def employee_name(cur, emp_id):  # returns the name of the employee
    sql = '''SELECT employee_name FROM employees WHERE employee_id = %s'''
    cur.execute(sql, (emp_id,))
    return cur.fetchone()


def add_attendance(cur, emp_id, date, time):  # registers the attendance time and date of the employee
    sql = '''INSERT INTO attendance VALUES (%s,%s,%s)'''
    cur.execute(sql, (emp_id, date, time,))


def attendance_by_id(cur, e_id):  # generates a list of tuples with the attendance log of the employee
    sql = '''SELECT date, time, attendance.employee_id, employee_name FROM attendance 
    INNER JOIN employees ON attendance.employee_id = employees.employee_id 
    WHERE attendance.employee_id = %s ORDER BY date, time'''
    cur.execute(sql, (e_id,))
    return cur.fetchall()


def attendance_by_date(cur, start_date, end_date):
    # generates a list of tuples with the attendance log of the employee that arrived between dates
    sql = '''SELECT date, time, attendance.employee_id, employee_name FROM attendance 
    INNER JOIN employees ON attendance.employee_id = employees.employee_id 
    WHERE date BETWEEN %s AND %s ORDER BY date, time'''
    cur.execute(sql, (start_date, end_date,))
    return cur.fetchall()


def attendance_after_hour(cur, hour, start_date):
    # generates a list of tuples with the attendance log of the employees that arrived after hour
    sql = '''SELECT date, time, attendance.employee_id, employee_name FROM attendance 
    INNER JOIN employees ON attendance.employee_id = employees.employee_id 
    WHERE time >= %s AND date >= %s ORDER BY date, time'''
    cur.execute(sql, (hour, start_date,))
    return cur.fetchall()

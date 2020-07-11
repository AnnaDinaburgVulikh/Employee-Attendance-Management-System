
# SQL queries:

count_employees = '''SELECT COUNT(*) FROM employees;'''
id_exists = '''SELECT COUNT(1) FROM employees WHERE employee_id=%s'''
add_employee = '''INSERT INTO employees VALUES (%s,%s,%s,%s,%s)'''
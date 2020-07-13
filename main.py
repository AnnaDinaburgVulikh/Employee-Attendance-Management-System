from employees import Employee
from config import config
import attendances
import psycopg2
import db_connect


def main():  # makes the program work
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        conn.set_session(autocommit=True)  # turns on the auto commit function
        cur = conn.cursor()
        print('Welcome to Employee Attendance Management system!')
        num = db_connect.employees_count(cur)
        print('The company has %d employees.' % num)
        print('What would you like to do today?')
        choice = 1
        while choice != 0:
            try:
                choice = int(input('''\nPlease choose from the menu:
    1 - Add employee manually
    2 - Add employees from file
    3 - Delete employee manually
    4 - Delete employees from file
    5 - Mark attendance
    6 - Generate attendance report of an employee
    7 - Print an attendance report for a chosen month for all employees (active only)
    8 - Print an attendance report for all employees who were late (choose arrival time limit)
    9 - Print an attendance report by dates
    0 - Exit the program
    Enter your choice: '''))
                if not 0 <= choice <= 9:
                    raise ValueError
            except ValueError:
                print('Please enter an integer number according to the list. ')
            else:
                if choice == 1:
                    Employee.add_employee_manually(cur)
                elif choice == 2:
                    Employee.add_employee_from_file(cur)
                elif choice == 3:
                    Employee.delete_employee_manually(cur)
                elif choice == 4:
                    Employee.delete_employee_from_file(cur)
                elif choice == 5:
                    attendances.mark_attendance(cur)
                elif choice == 6:
                    attendances.attendance_report_by_id(cur)
                elif choice == 7:
                    attendances.report_by_month(cur)
                elif choice == 8:
                    attendances.report_by_hour(cur)
                elif choice == 9:
                    attendances.report_by_dates(cur)
                else:
                    print('See you next time.')
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Have a nice day.')


main()

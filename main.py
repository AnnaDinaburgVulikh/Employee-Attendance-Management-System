from employees import Employee
from attendances import Attendance


def main():  # makes the program work
    employee_dic, num = Employee.load_employee_dic(Employee.path_employee)
    print('Welcome to Employee Attendance Managment system!')
    print('The company has %d employees.' % num)
    print('What would you like to do today?')
    choice = 1
    while choice != 0:
        try:
            choice = int(input('''    1 - Add employee manually
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
                employee_dic = Employee.add_employee_manually(employee_dic)
            elif choice == 2:
                employee_dic = Employee.add_employee_from_file(employee_dic)
            elif choice == 3:
                employee_dic = Employee.delete_employee_manually(employee_dic)
            elif choice == 4:
                employee_dic = Employee.delete_employee_from_file(employee_dic)
            elif choice == 5:
                Attendance.mark_attendance(employee_dic)
            elif 6 <= choice <= 9:
                attend_list = Attendance.load_attendance_list()
                if choice == 6:
                    Attendance.attendance_report_by_id(attend_list, employee_dic)
                elif choice == 7:
                    Attendance.report_by_month(attend_list)
                elif choice == 8:
                    Attendance.report_by_hour(attend_list)
                else: #choice is 9
                    Attendance.report_by_dates(attend_list)
            else:
                print('See you next time.')

main()
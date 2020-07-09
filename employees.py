import re
import csv
import datetime
import os
from attendances import Attendance


class Employee:
    path_employee = 'employees.csv'

    def __init__(self, emp_id: str, name: str, phone: str, birthday):
        self.id = str(emp_id)
        self.name = name
        self.phone = str(phone)
        if type(birthday) is str:
            # year, month, day = str(birthday).split('-')
            # birthday = datetime.date(int(year), int(month), int(day))
            birthday = datetime.datetime.strptime(birthday, "%Y-%m-%d").date()
        self.birthday = birthday

        self._age = None
        self._age_last_recalculated = None

        self._recalculate_age()

    def _recalculate_age(self):
        today = datetime.date.today()
        age = today.year - self.birthday.year
        if today < datetime.date(today.year, self.birthday.month, self.birthday.day):
            age -= 1
        self._age = age
        self._age_last_recalculated = today

    def age(self):
        if datetime.date.today() > self._age_last_recalculated:
            self._recalculate_age()
        return self._age

    def __str__(self):
        return f"ID Number: {self.id}\nName: {self.name}\nPhone: {self.phone}\nAge: {self._age}"

    # Functions related to Employee

    @staticmethod
    def load_employee_dic(user_path=None):
        # Used before the class instance is formed or used as a helper for adding employees from file
        while True:
            try:  # Should check if the file exists.
                if user_path is None:
                    user_path = input("Enter the path of your file: ")
                if user_path == '-1':
                    Employee.update_employee_file({})
                    user_path = Employee.path_employee
                assert os.path.exists(user_path)
                if user_path != Employee.path_employee:
                    Employee.path_employee = user_path
            except AssertionError:
                print("I did not find the file at: " + str(user_path))
                user_path = None
            else:
                with open(user_path, mode='r') as csv_file:
                    dic = {}
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    if csv_reader is None:
                        print('The file was empty')
                        return dic, 0
                    line_count = 0
                    for row in csv_reader:
                        if line_count != 0:
                            if len(row) == 4:
                                dic[row[0]] = Employee(row[0], row[1], row[2], row[3])
                            else:
                                print(f'The data in row {line_count} is partially missing.')
                                return None, None
                        line_count += 1
                    return dic, (line_count - 1)

    @staticmethod
    def update_employee_file(dic):
        with open(Employee.path_employee, mode='w', newline='') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',')
            employee_writer.writerow(['employee id', 'name', 'phone', 'birthday'])
            for employee in dic.values():
                employee_writer.writerow([employee.id, employee.name, employee.phone, employee.birthday])

    @staticmethod
    def enter_name():  # part of add_employee_manually
        """Lets the user enter a name, and checks it's a string of chars only."""
        while True:
            try:
                name = str(input('Please enter your name (example: john smith): '))
                while not re.match("[a-zA-Z]+[ ]?[a-zA-Z]*$", name):
                    if name == '':
                        print('You didn\'t enter a name.')
                    elif '  ' in name:
                        print('Only one space allowed.')
                    else:
                        print('The name should consist of letters only.')
                    name = str(input('Please enter your name (example: john smith): '))
            except ValueError:
                print('The name should consist of letters only.')
            else:
                return name

    @staticmethod
    def enter_phone():  # part of add_employee_manually
        phone = input("Please enter a phone number(0xx-xxxxxxx): ")
        while not re.match('0\d\d?-?\d{7}', phone):
            print("Error! Make sure you follow the template and enter numbers only.")
            phone = input("Please enter a phone number(0xx-xxxxxxx): ")
        return phone

    @staticmethod
    def enter_birthday():  # part of add_employee_manually
        age = 0
        while True:
            try:
                day, month, year = input('Please enter a birthday(dd-mm-yyyy):').split('-')
                birthday = datetime.date(int(year), int(month), int(day))
                age = datetime.date.today().year - int(year)
                assert 15 <= age <= 99
            except ValueError:
                print('Please enter valid integer numbers.')
            except AssertionError:
                print('Please check the birth day. your employee is %d years old' % age)
            else:
                return birthday
        pass

    @staticmethod
    def add_employee_manually(employee_dic):
        e_id = Attendance.enter_id()
        if e_id in employee_dic:
            print("The employee id %s is already listed." % e_id)
            return employee_dic
        else:
            name = Employee.enter_name()
            phone = Employee.enter_phone()
            birthday = Employee.enter_birthday()
            employee_dic[e_id] = Employee(e_id, name, phone, birthday)
            Employee.update_employee_file(employee_dic)
            print("Added an employee with id %s." % e_id)
            return employee_dic

    @staticmethod
    def add_employee_from_file(dic):
        # Runs the load dictionary to load the new rows and if the file is proper adds the value to main employee file
        new_dic, num = Employee.load_employee_dic()
        if num is not None and num > 0:
            dic.update(new_dic)
            Employee.update_employee_file(dic)
            print('Employees were added.')
        return dic

    @staticmethod
    def delete_employee_manually(dic):
        # The function allows to delete an employee by ID
        e_id = ''
        while True:
            try:
                e_id = str(input('Please enter employee ID (123456789) to delete or -1 to exit: '))
                if e_id == '-1':
                    return dic
                if not e_id.isalnum() or len(e_id) != 9:
                    raise ValueError
                assert dic[e_id]
            except ValueError:
                print('The ID should be an integer of 9 digits.')
            except KeyError or AssertionError:
                print(f'There is no employee with ID {e_id}. Please try again.')
            else:
                dic.pop(e_id)
                Employee.update_employee_file(dic)
                print("Deleted an employee with id %s." % e_id)
                return dic

    @staticmethod
    def load_employees_dic_to_delete():
        # Helper function, reads the IDs and makes sure that the IDs are valid
        user_path = ''
        while True:
            try:  # Should check if the file exists.
                user_path = input("Enter the path of your file: ")
                assert os.path.exists(user_path)
            except AssertionError:
                print("I did not find the file at: " + str(user_path))
            else:
                with open(user_path, mode='r') as csv_file:
                    delete_ids_array = []
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    if csv_reader is None:
                        print('The file was empty')
                        return delete_ids_array, 0
                    line_count = 0
                    for row in csv_reader:
                        if line_count != 0:
                            if len(row) == 1:
                                e_id = str(row[0])
                                if e_id.isalnum() and len(e_id) == 9:
                                    delete_ids_array.append(e_id)
                                else:
                                    print(f'The data in row {line_count} is partially missing.')
                                    return None, None
                            else:
                                print(f'There is extra data in row {line_count}.')
                                return None, None
                        line_count += 1
                    return delete_ids_array, (line_count - 1)

    @staticmethod
    def delete_employee_from_file(dic):
        # Deletes the employees by ID from file and reflects how many were deleted.
        # Also prompt about the IDs that didn't exist in our employee file.
        del_arr, num = Employee.load_employees_dic_to_delete()
        if num is not None and num > 0:
            non_exist = []
            for e_id in del_arr:
                exist = dic.pop(e_id, 'no')
                if exist == 'no':
                    non_exist.append(e_id)
            if len(non_exist) == len(del_arr):
                print('There were no employees with those IDs in our company.')
            elif len(non_exist) == 0:
                print(f'Number of employees deleted: {len(del_arr)}.')
            else:
                print(f'Number of employees deleted: {len(del_arr) - len(non_exist)}')
                print(f'The following employees didn\'t exist in our company: {" ,".join(non_exist)}')
        return dic

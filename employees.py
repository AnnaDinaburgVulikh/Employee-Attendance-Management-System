import re
import csv
import datetime
import os
import GUI
import attendances
import db_connect
from tkinter import *
from tkinter import messagebox


class Employee:
    TITLES = ('Manager', 'Senior', 'Junior')

    def __init__(self, emp_id: str, name: str, title: str, phone: str, birthday):
        self.id = str(emp_id)
        self.name = name
        self.title = title
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
        # Used as a helper for adding employees from file
        while True:
            try:  # Should check if the file exists.
                if user_path is None:
                    user_path = input("Enter the path of your file: ")
                assert os.path.exists(user_path)
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
                                dic[row[0]] = Employee(row[0], row[1], 'Junior', row[2], row[3])
                            elif len(row) == 5:
                                dic[row[0]] = Employee(row[0], row[1], row[2], row[3], row[4])
                            else:
                                print(f'The data in row {line_count} is partially missing.')
                                return None, None
                        line_count += 1
                    return dic, (line_count - 1)

    @staticmethod
    def check_id(cur=None, e_id=None):  # enter_id()
        message = ""
        correct = 0  # a flag for right input
        color = ""
        if e_id is None or len(e_id) == 0:
            message = "Please enter ID to proceed."
            color = "black"
        elif not e_id.isdecimal() or (len(e_id) != 9):
            message = "The ID should be an integer of 9 digits."
            color = "red"
        elif cur is not None:  # 9 digit ID
            if db_connect.check_id_exist(cur, e_id):
                message = "Employee name is %s." % db_connect.employee_name(cur, e_id)
                color = "blue"
            else:
                message = "Let's add the employee"
                color = "green"
                correct = 1
        return correct, message, color

    @staticmethod
    def check_name(name):  # part of add_employee_manually
        """Recieves the user input name, and checks it's a string of chars only."""
        message = ""
        correct = 0
        if not re.match("^[A-Za-z][A-Za-z'\-]+([ ][A-Za-z][A-Za-z'\-]+)*$", name):
            if name == '':
                message = "Please enter Employee Name to proceed."
            elif '  ' in name:
                message = 'Only one consecutive space allowed.'
            else:
                message = 'The name should consist of letters only\n and include 2 consecutive letters at least.'
        else:
            correct = 1
        return correct, message

    @staticmethod
    def check_phone(phone: str):  # part of add_employee_manually
        message = ""
        correct = 0     # a flag for right input
        if not re.match('0[1-9]{1,2}-?[1-9]{7}$', phone):
            if phone == "":
                message = "Please enter Phone to proceed."
            else:
                message = "Make sure you follow the template(0xx-xxxxxxx)\n and enter numbers only."
        else:
            correct = 1
        return correct, message

    @staticmethod
    def check_birthday(birthday:datetime):  # part of add_employee_manually
        age = datetime.date.today().year - birthday.year
        message = ""
        if not (15 <= age <= 99):
            message = 'Please check the date. your employee is %d years old' % age
            correct = 0
        else:
            correct = 1
        return correct, message

    @staticmethod
    def add_employee_from_file(cur):
        # Runs the load dictionary to load the new rows and if the file is proper adds the values to the DB
        new_dic, num = Employee.load_employee_dic()
        count = 0
        if num is not None and num > 0:
            for employee in new_dic.values():
                if not db_connect.check_id_exist(cur, employee.id):
                    db_connect.add_employee(cur, employee)
                    count += 1
            print(f'{count} employees were added.')
            print(f'{num - count} employees already existed in the database.')
        return

    @staticmethod
    def delete_employee_manually(cur, e_id=None):
        # The function allows to delete an employee by ID
        messagebox.askokcancel("Delete Employee", "You are going to loose all the information about employee %s.\n"
                                                  "Do you want to proceed?" % e_id)
        db_connect.delete_employee(cur, e_id)
        messagebox.showinfo("Delete Employee", "Employee with ID %s was deleted." % e_id)

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
    def delete_employee_from_file(cur):
        # Deletes the employees by ID from the database and reflects how many were deleted.
        # Also prompt about the IDs that didn't exist in our employee file.
        del_arr, num = Employee.load_employees_dic_to_delete()
        if num is not None and num > 0:
            non_exist = []
            for e_id in del_arr:
                if db_connect.check_id_exist(cur, e_id):
                    db_connect.delete_employee(cur, e_id)
                else:
                    non_exist.append(e_id)
            if len(non_exist) == num:
                print('There were no employees with those IDs in our company.')
            elif len(non_exist) == 0:
                print(f'Number of employees deleted: {num}.')
            else:
                print(f'Number of employees deleted: {num - len(non_exist)}')
                print(f'The following employees didn\'t exist in our company: {" ,".join(non_exist)}')
        return

import re
import csv
import datetime
import os
import GUI
import attendances
import db_connect
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog


class Employee:
    TITLES = ('Manager', 'Senior', 'Junior')

    def __init__(self, emp_id: str, name: str, title: str, phone: str, birthday):
        self.id = str(emp_id)
        self.name = name
        if title == 'm':
            self.title = Employee.TITLES[0]
        elif title == 's':
            self.title = Employee.TITLES[1]
        else:
            self.title = Employee.TITLES[2]
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
                                dic[row[0]] = Employee(row[0], row[1], 'j', row[2], row[3])
                            elif len(row) == 5:
                                dic[row[0]] = Employee(row[0], row[1], row[2], row[3], row[4])
                            else:
                                print(f'The data in row {line_count} is partially missing.')
                                return None, None
                        line_count += 1
                    return dic, (line_count - 1)

    @staticmethod
    def enter_name():  # part of add_employee_manually
        """Lets the user enter a name, and checks it's a string of chars only."""
        while True:
            try:
                name = simpledialog.askstring('Enter name', 'Please enter your name (example: John Smith): ')
                while not re.match("^[A-Za-z][A-Za-z'\-]+([ ][A-Za-z][A-Za-z'\-]+)*", name):
                    if name == '' or name == ' ':
                        messagebox.showwarning('Error entering name', 'You didn\'t enter a name.')
                    elif '  ' in name:
                        messagebox.showwarning('Error entering name', 'Only one space allowed.')
                    else:
                        messagebox.showwarning('Error entering name', 'The name should consist of letters only and '
                                                                      'include 2 consecutive letters at least.')
                    name = simpledialog.askstring('Enter name', 'Please enter your name (example: John Smith): ')
            except ValueError:
                messagebox.showwarning('Error entering name', 'The name should consist of letters only and include 2 '
                                                              'consecutive letters at least.')
            else:
                return name

    @staticmethod
    def enter_phone():  # part of add_employee_manually
        phone = simpledialog.askstring('Enter phone number', "Please enter a phone number(0xx-xxxxxxx): ")
        while not re.match('0[1-9]{1,2}-?[1-9]{7}', phone):
            messagebox.showwarning('Error entering phone ',
                                   "Error! Make sure you follow the template and enter numbers only.")
            phone = simpledialog.askstring('Enter phone number', "Please enter a phone number(0xx-xxxxxxx): ")
        return phone

    @staticmethod
    def enter_birthday():  # part of add_employee_manually
        age = 0
        while True:
            try:
                day, month, year = simpledialog.askstring('Enter Birthday', 'Please enter a birthday(dd-mm-yyyy):').split('-')
                birthday = datetime.date(int(year), int(month), int(day))
                age = datetime.date.today().year - int(year)
                assert 15 <= age <= 99
            except ValueError:
                messagebox.showwarning('Error entering birthday', 'Please enter valid integer numbers.')
            except AssertionError:
                messagebox.showwarning('Error entering birthday', 'Please check the birth day. your employee is %d years old' % age)
            else:
                return birthday
        pass

    @staticmethod
    def enter_title():  # part of add_employee_manually
        title = simpledialog.askstring('Enter title', "Please enter employee title('m' for Manager, 's' for Senior, 'j' for Junior): ")
        while not re.match('[msj]', title):
            messagebox.showwarning('Error entering title', "Error! Make sure to choose from the allowed characters.")
            title = simpledialog.askstring('Enter title', "Please enter employee title('m' for Manager, 's' for Senior, 'j' for Junior): ")
        return title

    @staticmethod
    def add_employee_manually(cur, e_id=None):
        # e_id = attendances.enter_id(e_id)
        # if e_id is None:
        #     return
        # if db_connect.check_id_exist(cur, e_id):
        #     messagebox.showwarning("Error Message", "The employee id %s is already listed." % e_id)
        #     return
        # else:
            #global emp_label
        GUI.Add_emp_top_window(cur, e_id)
        #emp_label = Label(top, text=("We are adding employee %s:" % e_id), font=16, anchor=CENTER).grid(row=0, columnspan=2,padx=5,pady=5)
        # ?????
        # name = Employee.enter_name()
        # title = Employee.enter_title()
        # phone = Employee.enter_phone()
        # birthday = Employee.enter_birthday()
        # # db_connect.add_employee(cur, Employee(e_id, name, title, phone, birthday))
        #messagebox.showinfo("Employee added", "Added an employee with id %s." % e_id)
        # top.destroy()
        return

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
    def delete_employee_manually(cur):
        # The function allows to delete an employee by ID
        e_id = ''
        while True:
            try:
                e_id = str(input('Please enter employee ID (123456789) to delete or -1 to exit: '))
                if e_id == '-1':
                    return
                if not e_id.isalnum() or len(e_id) != 9:
                    raise ValueError
                assert db_connect.check_id_exist(cur, e_id) == 1
            except ValueError:
                print('The ID should be an integer of 9 digits.')
            except KeyError or AssertionError:
                print(f'There is no employee with ID {e_id}. Please try again.')
            else:
                db_connect.delete_employee(cur, e_id)
                print("Deleted an employee with id %s." % e_id)
                return

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

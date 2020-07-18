from tkinter import *
from employees import Employee
import attendances
import db_connect


class CreateMenu:
    def __init__(self, master=None, cur=None):
        self.menu_base = Menu(master)
        self.cur = cur
        master.config(menu=self.menu_base)
        self.file_menu = Menu(self.menu_base)
        self.set_file_menu()
        self.report_menu = Menu(self.menu_base)
        self.set_report_menu()

    def set_file_menu(self):
        self.menu_base.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Add employee', command=self.add_emp)
        self.file_menu.add_command(label='Add employees from file', command=self.add_emp_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Delete employee', command=self.del_emp)
        self.file_menu.add_command(label='Delete employees from file', command=self.del_emp_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Mark attendance', command=self.mark_att)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.file_menu.quit)

    def set_report_menu(self):
        self.menu_base.add_cascade(label='Reports', menu=self.report_menu)
        self.report_menu.add_command(label='Attendance for employee', command=self.att_id_report)
        self.report_menu.add_separator()
        self.report_menu.add_command(label='Attendance by month', command=self.att_by_month)
        self.report_menu.add_command(label='Attendance by dates', command=self.att_by_date)
        self.report_menu.add_separator()
        self.report_menu.add_command(label='Late attendance by date and hour', command=self.att_by_hour)

    def add_emp(self, e_id=None):
        Employee.add_employee_manually(self.cur, e_id)

    def add_emp_file(self):
        Employee.add_employee_from_file(self.cur)

    def del_emp(self, e_id=None):
        Employee.delete_employee_manually(self.cur, e_id)

    def del_emp_file(self):
        Employee.add_employee_from_file(self.cur)

    def mark_att(self, e_id=None):
        attendances.mark_attendance(self.cur, e_id)

    def att_id_report(self, e_id=None):
        attendances.attendance_report_by_id(self.cur, e_id)

    def att_by_month(self):
        attendances.report_by_month(self.cur)

    def att_by_date(self):
        attendances.report_by_dates(self.cur)

    def att_by_hour(self):
        attendances.report_by_hour(self.cur)


class CreateFrames:
    def __init__(self, master, cur):
        self.top_frame = Frame(master, relief=SUNKEN, width=600, height=100, pady=3)
        self.center_frame = Frame(master, width=600, height=400, padx=3, pady=3)
        self.left_frame = Frame(self.center_frame, bg="lightblue", width=300, height=500, padx=3, pady=3)
        self.right_frame = Frame(self.center_frame, bg="lightgray", width=300, height=500, padx=3, pady=3)
        self.cur = cur

        self.top_frame.grid(row=0, sticky=NS)
        self.center_frame.grid(row=1, sticky=NSEW)
        self.left_frame.grid(row=0, column=0, sticky=NS)
        self.right_frame.grid(row=0, column=1, sticky=NS)

        self.top_frame_widgets()
        self.left_frame_widgets()
        self.right_frame_widgets()

    def top_frame_widgets(self):
        main_title = Label(self.top_frame, text="Employee Attendance Management System", font=20, anchor=CENTER)
        company_employees = self.update_emp_num()
        label_emp_num = Label(self.top_frame, text=company_employees)

        main_title.grid(row=0, columnspan=3, sticky=EW, padx=10)
        label_emp_num.grid(row=1, columnspan=3, sticky=EW)

    def update_emp_num(self):
        num = db_connect.employees_count(self.cur)
        return 'The company has %d employees.' % num

    def left_frame_widgets(self):
        main_title = Label(self.left_frame, text="Employees", bg="lightblue", font=18, anchor=CENTER)
        entry_label = Label(self.left_frame, text="Please enter ID to proceed:", bg="lightblue")
        self.e_id = StringVar()
        entry_id = Entry(self.left_frame, textvariable=self.e_id)
        add_button = Button(self.left_frame, text="Add employee", command=self.add_emp)
        del_button = Button(self.left_frame, text="Delete employee", command=self.del_emp)
        mark_button = Button(self.left_frame, text="Add employee", command=self.mark_att)
        # if not attendances.enter_id(e_id):
        #     pass

        main_title.grid(row=0, columnspan=3, sticky=EW, padx=60, pady=10)
        entry_label.grid(row=1, columnspan=3, sticky=EW, pady=5)
        entry_id.grid(row=2, columnspan=3, sticky=EW, padx=60, pady=5)
        add_button.grid(row=3, column=0, sticky=E, padx=2, pady=5)
        del_button.grid(row=3, column=1, sticky=E, padx=2, pady=5)
        mark_button.grid(row=3, column=2, sticky=E, padx=2, pady=5)

    def right_frame_widgets(self):
        Label(self.right_frame, text="Reports", bg="lightgray", font=18, anchor=CENTER).grid(row=0, columnspan=2, sticky=EW, padx=60)

    def add_emp(self):
        Employee.add_employee_manually(self.cur, str(self.e_id.get()))

    def add_emp_file(self):
        Employee.add_employee_from_file(self.cur)

    def del_emp(self):
        Employee.delete_employee_manually(self.cur, self.e_id.get())

    def del_emp_file(self):
        Employee.add_employee_from_file(self.cur)

    def mark_att(self):
        attendances.mark_attendance(self.cur, self.e_id.get())

    def att_id_report(self):
        attendances.attendance_report_by_id(self.cur, self.e_id.get())

    def att_by_month(self):
        attendances.report_by_month(self.cur)

    def att_by_date(self):
        attendances.report_by_dates(self.cur)

    def att_by_hour(self):
        attendances.report_by_hour(self.cur)


def do_nothing():
    print('Nothing...')






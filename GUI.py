import datetime
from tkinter import *
from employees import Employee
import attendances
import db_connect
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
from tkinter import ttk
from tkinter import simpledialog



class CreateMenu:
    def __init__(self, master=None, cur=None):
        self.master = master
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
        self.file_menu.add_command(label='Exit', command=self.master.destroy)

    def set_report_menu(self):
        self.menu_base.add_cascade(label='Reports', menu=self.report_menu)
        self.report_menu.add_command(label='Attendance for employee', command=self.att_id_report)
        self.report_menu.add_separator()
        self.report_menu.add_command(label='Attendance by month', command=self.att_by_month)
        self.report_menu.add_command(label='Attendance by dates', command=self.att_by_date)
        self.report_menu.add_separator()
        self.report_menu.add_command(label='Late attendance by date and hour', command=self.att_by_hour)

    def add_emp(self):  # Done
        Add_emp_top_window(self.cur)

    def add_emp_file(self):
        add_or_del_emp_file(self.cur, 1)

    def check_entered_id(self, e_id):
        id_exists, message, color = Employee.check_id(self.cur, e_id)
        if color == "blue":
            id_exists = 1
        elif color == "green":
            id_exists = 0
            message = "There is no employee with ID %s" % e_id
        elif color == "black":
            message = "You didn't enter an ID."
        return id_exists, message

    def del_emp(self):
        e_id = simpledialog.askstring("Delete Employee", "Please enter employee ID:")
        correct, message = self.check_entered_id(e_id)
        if correct == 1:
            Employee.delete_employee_manually(self.cur, e_id)
        messagebox.showinfo("Delete Employee", message)

    def del_emp_file(self):
        add_or_del_emp_file(self.cur, 0)

    def mark_att(self):  # Done
        e_id = simpledialog.askstring("Mark Attendance", "Please enter employee ID:")
        correct, message = self.check_entered_id(e_id)
        if correct == 1:
            attendances.mark_attendance(self.cur, e_id)
        else:
            messagebox.showinfo("Mark Attendance", message)

    def att_id_report(self, e_id=None):
        e_id = simpledialog.askstring("Attendance Report", "Please enter employee ID:")
        correct, message = self.check_entered_id(e_id)
        if correct == 1:
            attendances.attendance_report_by_id(self.cur, e_id)
        else:
            messagebox.showinfo("Attendance Report", message)

    def att_by_month(self):
        month = simpledialog.askstring("Attendance report by month", "Please enter a month (1-12):")
        test = month_check(month)
        if test:
            attendances.report_by_month(self.cur, int(month))
        else:
            messagebox.showwarning("Attendance report by month", "You should choose a month using 1-12 numbers.")

    def att_by_date(self):
        attendances.report_by_dates(self.cur)

    def att_by_hour(self):
        attendances.report_by_hour(self.cur)


class CreateFrames:
    def __init__(self, master, cur):
        self.master = master
        self.top_frame = Frame(master, relief=SUNKEN, width=600, height=100, pady=3)
        self.center_frame = Frame(master, width=600, height=400, padx=3, pady=3)
        self.left_frame = Frame(self.center_frame, bg="lightblue", width=300, height=500, padx=3, pady=3)
        self.right_frame = Frame(self.center_frame, bg="lightgray", width=300, height=500, padx=3, pady=3)
        self.bottom_frame = Frame(master, relief=SUNKEN, width=600, height=100, pady=3)
        self.cur = cur

        self.top_frame.grid(row=0, sticky=NS)
        self.center_frame.grid(row=1, sticky=NSEW)
        self.left_frame.grid(row=0, column=0, sticky=NS)
        self.right_frame.grid(row=0, column=1, sticky=NS)
        self.bottom_frame.grid(row=2, sticky=NS)

        self.top_frame_widgets()
        self.left_frame_widgets()
        self.right_frame_widgets()
        self.bottom_frame_widgets()

        self.master.bind('<FocusIn>', self.del_entry)

    def top_frame_widgets(self):
        main_title = Label(self.top_frame, text="Employee Attendance Management System", font=20, anchor=CENTER)
        self.company_employees = StringVar()
        self.update_emp_num()
        label_emp_num = Label(self.top_frame, textvariable=self.company_employees)

        main_title.grid(row=0, columnspan=3, sticky=EW, padx=10)
        label_emp_num.grid(row=1, columnspan=3, sticky=EW)

        self.master.bind('<FocusIn>', self.update_emp_num)

    def update_emp_num(self, event=None):
        self.emp_num = db_connect.employees_count(self.cur)
        self.company_employees.set('The company has %d employees.' % self.emp_num)
        return

    def left_frame_widgets(self):
        main_title = Label(self.left_frame, text="Employee management", bg="lightblue", font=18, anchor=CENTER)
        self.e_id = StringVar()
        self.entry_id = Entry(self.left_frame, textvariable=self.e_id)
        self.prompt_id = Label(self.left_frame, text="Please enter ID to proceed.", bg="lightblue")
        self.add_button = Button(self.left_frame, text="  Add employee  ", command=self.add_emp, state=DISABLED)
        self.del_button = Button(self.left_frame, text="Delete employee", command=self.del_emp, state=DISABLED)
        self.mark_button = Button(self.left_frame, text="Mark attendance", command=self.mark_att, state=DISABLED)
        self.report_button = Button(self.left_frame, text=" Generate report ", command=self.att_id_report, state=DISABLED)

        self.entry_id.bind('<KeyRelease>', self.id_input_prompt)

        main_title.grid(row=0, columnspan=2, sticky=EW, padx=45, pady=10)
        self.entry_id.grid(row=2, columnspan=2, sticky=EW, padx=60, pady=5)
        self.prompt_id.grid(row=3, columnspan=2, sticky=EW)
        self.add_button.grid(row=4, column=0, sticky=E, padx=5, pady=5)
        self.del_button.grid(row=5, column=0, sticky=E, padx=5, pady=5)
        self.mark_button.grid(row=4, column=1, sticky=W, padx=5, pady=5)
        self.report_button.grid(row=5, column=1, sticky=W, padx=5, pady=5)

    def right_frame_widgets(self):
        title = Label(self.right_frame, text="Multiple Employees", bg="lightgray", font=18, anchor=CENTER)
        entry_label1 = Label(self.right_frame, text="You can add/delete multiple employees\n by providing a file.\n "
                                                    "Please choose the desired action:", bg="lightgray")
        add_button = Button(self.right_frame, text="  Add employees  ", command=self.add_emp_file)
        del_button = Button(self.right_frame, text="Delete employees", command=self.del_emp_file)

        title.grid(row=0, columnspan=2, sticky=EW, padx=60, pady=10)
        entry_label1.grid(row=1, columnspan=2, sticky=EW)
        add_button.grid(row=3, columnspan=2, sticky=EW, padx=60, pady=5)
        del_button.grid(row=4, columnspan=2, sticky=EW, padx=60, pady=5)

    def bottom_frame_widgets(self):
        title = Label(self.bottom_frame, text="Attendance Reports", font=18, anchor=CENTER)
        clear_button = Button(self.bottom_frame, text="Clear", command=self.del_entry)
        entry_label_month = Label(self.bottom_frame, text="Please enter \na month (1-12): ")
        self.month = StringVar()
        self.entry_month = Entry(self.bottom_frame, textvariable=self.month)
        self.month_button = Button(self.bottom_frame, text="Generate monthly\n report ", command=self.att_by_month, state=DISABLED)
        line_label = Label(self.bottom_frame, text="--------------------------------------------------------------")
        self.entry_label_start_date = Label(self.bottom_frame, text="Please enter \nstart date: ")
        self.start_date = DateEntry(self.bottom_frame, date_pattern='d/m/y')
        self.prompt_start_date = Label(self.bottom_frame, text="")
        entry_label_end_date = Label(self.bottom_frame, text="End date: ")
        self.end_date = DateEntry(self.bottom_frame, date_pattern='d/m/y')
        self.dates_button = Button(self.bottom_frame, text="Generate report\n by dates", command=self.att_by_date, state=DISABLED)
        or_label = Label(self.bottom_frame, text="  or        ")
        entry_label_hour = Label(self.bottom_frame, text="Hour:\n(hh:mm)")
        self.hour = StringVar()
        self.entry_hour = Entry(self.bottom_frame, textvariable=self.hour)
        self.hour_button = Button(self.bottom_frame, text="Generate report by\n hour and date", command=self.att_by_hour, state=DISABLED)
        self.prompt_reports = Label(self.bottom_frame, text="")


        self.entry_month.bind('<KeyRelease>', self.month_prompt)
        self.start_date.bind('<<DateEntrySelected>>', self.start_date_input_prompt)
        self.start_date.bind('<FocusOut>', self.start_date_input_prompt)
        self.end_date.bind('<<DateEntrySelected>>', self.end_date_input_prompt)
        self.end_date.bind('<FocusOut>', self.end_date_input_prompt)
        self.entry_hour.bind('<KeyRelease>', self.hour_prompt)


        self.generate_report = [0,0,0]

        title.grid(row=0, column=1, columnspan=3, sticky=EW, padx=40, pady=10)
        clear_button.grid(row=0, column=4, sticky=EW, padx=5, pady=10)
        entry_label_month.grid(row=1, column=1, columnspan=1, sticky=E, padx=5, pady=5)
        self.entry_month.grid(row=1, column=2, columnspan=1, sticky=W, padx=5, pady=5)
        self.month_button.grid(row=1, column=3, sticky=EW, padx=5, pady=5)
        line_label.grid(row=2, columnspan=5, sticky=EW, padx=30, pady=10)
        self.entry_label_start_date.grid(row=3, column=1, sticky=E, padx=5, pady=5)
        self.start_date.grid(row=3, column=2, sticky=EW, padx=5, pady=10)
        self.prompt_start_date.grid(row=3, column=3, sticky=W, padx=5, pady=5)
        entry_label_end_date.grid(row=4, column=1, sticky=E, padx=5, pady=5)
        self.end_date.grid(row=4, column=2, sticky=EW, padx=5, pady=5)
        self.dates_button.grid(row=4, column=3, sticky=EW, padx=5, pady=5)
        or_label.grid(row=5, column=1, sticky=E, padx=0, pady=8)
        self.prompt_reports.grid(row=5, column=2, padx=0, pady=0, sticky=EW)
        entry_label_hour.grid(row=6, column=1, sticky=E, padx=5, pady=5)
        self.entry_hour.grid(row=6, column=2, sticky=W, padx=5, pady=5)
        self.hour_button.grid(row=6, column=3, sticky=EW, padx=5, pady=5)

    def del_entry(self, event=None):  # Clears the entry after pressing one of the functions
        self.entry_id.delete(0, END)
        self.id_input_prompt()
        self.entry_month.delete(0, END)
        self.month_prompt()
        if event is None:
            self.start_date.set_date(datetime.datetime.now().date())
            self.end_date.set_date(datetime.datetime.now().date())
            self.generate_report = [0,0,0]
            self.check_report()
            self.prompt_reports.destroy()
            self.entry_hour.delete(0, END)

    def id_input_prompt(self, event=None):
        self.prompt_id.destroy()
        self.add_button['state'] = DISABLED
        self.del_button['state'] = DISABLED
        self.mark_button['state'] = DISABLED
        self.report_button['state'] = DISABLED
        new_id, message, color = Employee.check_id(self.cur, self.e_id.get())
        self.prompt_id = Label(self.left_frame, text=message, fg=color, bg="lightblue")
        self.prompt_id.grid(row=3, columnspan=2, sticky=EW, padx=0, pady=0)
        if color == "blue":   # There is an employee with this ID
            self.del_button['state'] = NORMAL
            self.mark_button['state'] = NORMAL
            self.report_button['state'] = NORMAL
        elif color == "green":  # There is no employee with this ID
            self.add_button['state'] = NORMAL

    def add_emp(self):   # Done
        Add_emp_top_window(self.cur, str(self.e_id.get()))

    def add_emp_file(self):
        add_or_del_emp_file(self.cur, 1)

    def del_emp(self):
        Employee.delete_employee_manually(self.cur, self.e_id.get())

    def del_emp_file(self):
        add_or_del_emp_file(self.cur, 0)

    def mark_att(self):   # Done
        attendances.mark_attendance(self.cur, self.e_id.get())

    def att_id_report(self):
        attendances.attendance_report_by_id(self.cur, self.e_id.get())

    def month_prompt(self, event=None):
        test = month_check(self.month.get())
        if test:
            self.month_button['state'] = NORMAL
        else:
            self.month_button['state'] = DISABLED

    def att_by_month(self):
        attendances.report_by_month(self.cur, int(self.month.get()))

    def start_date_input_prompt(self, event=None):
        self.prompt_start_date.destroy()
        message = ""
        if self.start_date.get_date() <= datetime.datetime.now().date():
            self.generate_report[0] = 1
        else:
            self.generate_report[0] = 0
            message = "Make sure you \nchoose past date."
        self.prompt_start_date = Label(self.bottom_frame, text=message, fg="red")
        self.prompt_start_date.grid(row=3, column=3, sticky=W, padx=5)
        self.check_report()

    def end_date_input_prompt(self, event=None):
        self.prompt_reports.destroy()
        message = ""
        if self.start_date.get_date() <= self.end_date.get_date() <= datetime.datetime.now().date():
            self.generate_report[1] = 1
        else:
            self.generate_report[1] = 0
            message = "Make sure you choose a past date \ngreater than start date."
        self.prompt_reports = Label(self.bottom_frame, text=message, fg="red")
        self.prompt_reports.grid(row=5, column=2, columnspan=2, sticky=W, padx=5)
        self.check_report()

    def check_report(self):
        if self.generate_report[0] == 1:
            if self.generate_report[1] == 1:
                self.dates_button['state'] = NORMAL
            if self.generate_report[2] == 1:
                self.hour_button['state'] = NORMAL
        else:
            self.dates_button['state'] = DISABLED
            self.hour_button['state'] = DISABLED

    def att_by_date(self):
        attendances.report_by_dates(self.cur, self.start_date.get(), self.end_date.get())
        self.start_date.delete(0, END)
        self.end_date.delete(0, END)

    def hour_prompt(self, event=None):
        self.prompt_reports.destroy()
        test, message = hour_check(self.hour.get())
        self.generate_report[2] = test
        if len(message) > 2:
            self.prompt_reports = Label(self.bottom_frame, text=message, fg="red")
            self.prompt_reports.grid(row=5, column=2, columnspan=2, sticky=W, padx=5)
        self.check_report()

    def att_by_hour(self):
        attendances.report_by_hour(self.cur, self.start_date.get(), self.hour.get())


class Add_emp_top_window:  # Class for top window used for adding an employee
    def __init__(self, cur, e_id=None):
        self.top = Toplevel()
        w = 600
        h = 570
        sw = (self.top.winfo_screenwidth() - w) / 2
        sh = (self.top.winfo_screenheight() - h) / 2
        self.top.geometry('%dx%d+%d+%d' % (w, h, sw, sh))
        self.top_frame = Frame(self.top, width=300, height=500, padx=3, pady=3)
        self.top.title('Adding an employee')

        self.e_id = StringVar()
        self.name = StringVar()
        self.title = StringVar()
        self.phone = StringVar()
        self.birthday = datetime
        self.add_new = [0, 0, 0, 0, 0]

        if e_id is not None:
            self.e_id.set(e_id)
        self.cur = cur

        self.top_window_widgets()

        self.top.mainloop()

    def top_window_widgets(self):
        main_title = Label(self.top_frame, text="Adding a new Employee", font=18, anchor=CENTER)
        label1 = Label(self.top_frame, text="Enter Data:", font=10, bg="lightblue", anchor=W)
        label2 = Label(self.top_frame, text="Annotations:", font=10, bg="lightblue", width=20, anchor=W)

        entry_id = Entry(self.top_frame, textvariable=self.e_id)
        if len(self.e_id.get()) == 9:
            self.prompt_id = Label(self.top_frame, fg="green", text="Let's add the employee")
            self.add_new[0] = 1
        else:
            self.prompt_id = Label(self.top_frame, text="Please enter ID to proceed.")

        entry_name = Entry(self.top_frame, textvariable=self.name)
        self.prompt_name = Label(self.top_frame, text="Please enter Employee Name to proceed.")

        self.title = StringVar()
        self.title.set("")
        drop_title = ttk.Combobox(self.top_frame, value=Employee.TITLES, textvariable=self.title, state="readonly")
        self.prompt_title = Label(self.top_frame, text="Please choose Title to proceed.")

        self.entry_birthday = DateEntry(self.top_frame, date_pattern='d/m/y')
        self.prompt_birthday = Label(self.top_frame, text="Please enter Birth Date to proceed.")

        entry_phone = Entry(self.top_frame, textvariable=self.phone)
        self.prompt_phone = Label(self.top_frame, text="Please enter Phone to proceed.")

        self.add_button = Button(self.top_frame, text=" Add employee ", command=self.add_emp, state=DISABLED)
        self.cancel_button = Button(self.top_frame, text="   Cancel   ", command=self.top.destroy)

        entry_id.bind('<KeyRelease>', self.id_input_prompt)
        entry_name.bind('<KeyRelease>', self.name_input_prompt)
        drop_title.bind('<<ComboboxSelected>>', self.title_input_prompt)
        self.entry_birthday.bind('<<DateEntrySelected>>', self.birthday_input_prompt)
        self.entry_birthday.bind('<FocusOut>', self.birthday_input_prompt)
        entry_phone.bind('<KeyRelease>', self.phone_input_prompt)

        self.top_frame.grid(row=0, sticky=NS)
        main_title.grid(row=0, columnspan=2, sticky=EW, padx=45, pady=10)
        label1.grid(row=1, sticky=W, pady=5)
        label2.grid(row=1, column=1, sticky=W, pady=5)

        entry_id.grid(row=2, sticky=EW, padx=20, pady=5)
        self.prompt_id.grid(row=2, column=1, sticky=W)
        entry_name.grid(row=3, sticky=EW, padx=20, pady=5)
        self.prompt_name.grid(row=3, column=1, sticky=W)
        drop_title.grid(row=4, sticky=EW, padx=20, pady=5)
        self.prompt_title.grid(row=4, column=1, sticky=W)
        self.entry_birthday.grid(row=5, sticky=EW, padx=20, pady=5)
        self.prompt_birthday.grid(row=5, column=1, sticky=W)
        entry_phone.grid(row=6, sticky=EW, padx=20, pady=5)
        self.prompt_phone.grid(row=6, column=1, sticky=W)
        self.add_button.grid(row=7, column=0, sticky=E, padx=5, pady=10)
        self.cancel_button.grid(row=7, column=1, sticky=W, padx=5, pady=10)

    def add_emp(self):
        db_connect.add_employee(self.cur, Employee(self.e_id.get(), self.name.get(), self.title.get(),
                                                   self.phone.get(), self.birthday))
        messagebox.showinfo("Employee added", "Added an employee with ID %s." % self.e_id.get())
        self.top.destroy()

    def can_add_amp(self):
        if sum(self.add_new) == 5:
            self.add_button['state'] = NORMAL
        else:
            self.add_button['state'] = DISABLED

    def id_input_prompt(self, event):
        self.prompt_id.destroy()
        self.add_new[0], message, color = Employee.check_id(self.cur, self.e_id.get())
        self.prompt_id = Label(self.top_frame, text=message, fg=color)
        self.prompt_id.grid(row=2, column=1, sticky=W)
        self.can_add_amp()

    def name_input_prompt(self, event):
        self.prompt_name.destroy()
        self.add_new[1], message = Employee.check_name(self.name.get())
        self.prompt_name = Label(self.top_frame, fg="red", text=message)
        self.prompt_name.grid(row=3, column=1, sticky=W)
        self.can_add_amp()

    def title_input_prompt(self, event):
        if self.title.get() is not "":
            self.add_new[2] = 1
            self.prompt_title.destroy()
        self.can_add_amp()

    def birthday_input_prompt(self, event):
        self.birthday = self.entry_birthday.get_date()
        self.add_new[3], message = Employee.check_birthday(self.birthday)
        if self.birthday is not None:
            self.prompt_birthday.destroy()
            self.prompt_birthday = Label(self.top_frame, fg="red", text=message)
            self.prompt_birthday.grid(row=5, column=1, sticky=W)
        self.can_add_amp()

    def phone_input_prompt(self, event):
        self.prompt_phone.destroy()
        self.add_new[4], message = Employee.check_phone(self.phone.get())
        self.prompt_phone = Label(self.top_frame, fg="red", text=message)
        self.prompt_phone.grid(row=6, column=1, sticky=W)
        self.can_add_amp()


def add_or_del_emp_file(cur, add_emp):
    file_path = filedialog.askopenfilename()
    if len(file_path) > 1:
        if add_emp == 1:
            Employee.add_employee_from_file(cur, file_path)
        else:
            Employee.delete_employee_from_file(cur, file_path)
    else:
        if add_emp == 1:
            title = "Add Employees by File"
        else:
            title = "Delete Employees by File"
        messagebox.showwarning(title, "No file was selected.")


def month_check(month_input):
    legal_month = 0
    if month_input.isdecimal():
        if 1 <= int(month_input) <= 12:
            legal_month = 1
    return legal_month


def hour_check(hour_input):
    legal_time = 0
    message = ""
    if len(hour_input) > 0:
        try:
            hour = datetime.datetime.strptime(hour_input, "%H:%M").time()
            assert datetime.time(6, 0) <= hour <= datetime.time(19, 00)
        except ValueError:
            message = 'The time should be in the format HH:MM.'
        except AssertionError:
            message = 'Please enter a valid work time,\n between 6am and 7pm.'
        else:
            legal_time = 1
    return legal_time, message



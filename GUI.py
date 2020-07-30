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
        Employee.add_employee_from_file(self.cur)

    def check_entered_id(self, e_id):
        correct, message, color = Employee.check_id(self.cur, e_id)
        if color == "blue":
            correct = 1
        elif color == "green":
            correct = 0
            message = "There is no employee with ID %s" % e_id
        elif color == "black":
            message = "You didn't enter an ID."
        return correct, message

    def del_emp(self):
        e_id = simpledialog.askstring("Delete Employee", "Please enter employee ID:")
        correct, message = self.check_entered_id(e_id)
        if correct == 1:
            Employee.delete_employee_manually(self.cur, e_id)
        messagebox.showinfo("Delete Employee", message)

    def del_emp_file(self):
        Employee.add_employee_from_file(self.cur)

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
        attendances.report_by_month(self.cur)

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
        self.left_frame.bind('<FocusIn>', self.del_id_entry)

        main_title.grid(row=0, columnspan=2, sticky=EW, padx=45, pady=10)
        self.entry_id.grid(row=2, columnspan=2, sticky=EW, padx=60, pady=5)
        self.prompt_id.grid(row=3, columnspan=2, sticky=EW)
        self.add_button.grid(row=4, column=0, sticky=E, padx=5, pady=5)
        self.del_button.grid(row=5, column=0, sticky=E, padx=5, pady=5)
        self.mark_button.grid(row=4, column=1, sticky=W, padx=5, pady=5)
        self.report_button.grid(row=5, column=1, sticky=W, padx=5, pady=5)

    def right_frame_widgets(self):
        title = Label(self.right_frame, text="Multiple Employees", bg="lightgray", font=18, anchor=CENTER)
        entry_label1 = Label(self.right_frame, text="Please enter file path to proceed:", bg="lightgray")
        self.file_path = StringVar()
        entry_path = Entry(self.right_frame, textvariable=self.file_path)
        add_button = Button(self.right_frame, text="  Add employees  ", command=self.add_emp_file)
        del_button = Button(self.right_frame, text="Delete employees", command=self.del_emp_file)

        title.grid(row=0, columnspan=2, sticky=EW, padx=60, pady=10)
        entry_label1.grid(row=1, columnspan=2, sticky=EW, pady=5)
        entry_path.grid(row=2, columnspan=2, sticky=EW, padx=60, pady=5)
        add_button.grid(row=3, columnspan=2, sticky=EW, padx=60, pady=5)
        del_button.grid(row=4, columnspan=2, sticky=EW, padx=60, pady=5)

    def bottom_frame_widgets(self):
        title = Label(self.bottom_frame, text="Attendance Reports", font=18, anchor=CENTER)
        entry_label_month = Label(self.bottom_frame, text="Please enter month: ")
        self.month = StringVar()
        entry_month = Entry(self.bottom_frame, textvariable=self.month)
        month_button = Button(self.bottom_frame, text="Generate monthly\n report ", command=self.att_by_month)
        line_label = Label(self.bottom_frame, text="--------------------------------------------------------------")
        entry_label_start_date = Label(self.bottom_frame, text="Please enter start date: ")
        self.start_date = StringVar()
        entry_start_date = Entry(self.bottom_frame, textvariable=self.start_date)
        entry_label_end_date = Label(self.bottom_frame, text="End date: ")
        self.end_date = StringVar()
        entry_end_date = Entry(self.bottom_frame, textvariable=self.end_date)
        dates_button = Button(self.bottom_frame, text="Generate report\n by dates", command=self.att_by_date)
        or_label = Label(self.bottom_frame, text="  or      ")
        entry_label_hour = Label(self.bottom_frame, text="Hour: ")
        self.hour = StringVar()
        entry_hour = Entry(self.bottom_frame, textvariable=self.hour)
        hour_button = Button(self.bottom_frame, text="Generate report by\n hour and date", command=self.att_by_hour)

        title.grid(row=0, columnspan=3, sticky=EW, padx=40, pady=10)
        entry_label_month.grid(row=1, columnspan=1, sticky=E, padx=5, pady=5)
        entry_month.grid(row=1, column=1, columnspan=1, sticky=W, padx=5, pady=5)
        month_button.grid(row=1, column=2, sticky=EW, padx=5, pady=5)
        line_label.grid(row=2, columnspan=3, sticky=EW, padx=30, pady=10)
        entry_label_start_date.grid(row=3, sticky=E, padx=5, pady=5)
        entry_start_date.grid(row=3, column=1, sticky=W, padx=5, pady=5)
        entry_label_end_date.grid(row=4, column=0, sticky=E, padx=5, pady=5)
        entry_end_date.grid(row=4, column=1, sticky=W, padx=5, pady=5)
        dates_button.grid(row=4, column=2, sticky=EW, padx=5, pady=5)
        or_label.grid(row=5, column=0, sticky=E, padx=0, pady=0)
        entry_label_hour.grid(row=6, column=0, sticky=E, padx=5, pady=5)
        entry_hour.grid(row=6, column=1, sticky=W, padx=5, pady=5)
        hour_button.grid(row=6, column=2, sticky=EW, padx=5, pady=5)

    def del_id_entry(self, event):  # Clears the entry after pressing one of the functions
        self.entry_id.delete(0, END)
        self.id_input_prompt()

    def id_input_prompt(self, event=None):
        self.prompt_id.destroy()
        self.add_button['state'] = DISABLED
        self.del_button['state'] = DISABLED
        self.mark_button['state'] = DISABLED
        self.report_button['state'] = DISABLED
        correct, message, color = Employee.check_id(self.cur, self.e_id.get())
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
        #filedialog.LoadFileDialog()
        Employee.add_employee_from_file(self.cur)

    def del_emp(self):
        Employee.delete_employee_manually(self.cur, self.e_id.get())

    def del_emp_file(self):
        Employee.add_employee_from_file(self.cur)

    def mark_att(self):   # Done
        attendances.mark_attendance(self.cur, self.e_id.get())

    def att_id_report(self):
        attendances.attendance_report_by_id(self.cur, self.e_id.get())

    def att_by_month(self):
        attendances.report_by_month(self.cur)

    def att_by_date(self):
        attendances.report_by_dates(self.cur)

    def att_by_hour(self):
        attendances.report_by_hour(self.cur)


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

        self.entry_birthday = DateEntry(self.top_frame, date_pattern='m/d/y')
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







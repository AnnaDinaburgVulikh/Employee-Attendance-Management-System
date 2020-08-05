import csv
import datetime
import db_connect
import calendar
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog


def mark_attendance(cur, e_id=None):
    now = datetime.datetime.now()
    date = now.date()
    time = now.time()
    db_connect.add_attendance(cur, e_id, date, time)
    messagebox.showinfo("Mark Attendance", "Marked an attendance for ID %s." % e_id)


def attendance_report_by_id(cur, e_id=None):
    report = db_connect.attendance_by_id(cur, e_id)
    if len(report) == 0:
        messagebox.showinfo('Attendance Report', f'No attendance was registered for employee {e_id}.')
    else:
        create_report_file(f'Attendance report for employee {e_id}.csv', report)
        messagebox.showinfo('Attendance Report', f'Check your library for the report (Employee ID {e_id}).')


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


def report_by_month(cur, month: int):
    now = datetime.datetime.now()
    cur_month = now.month
    cur_year = now.year
    if month > cur_month:
        cur_year -= 1
    start_date = datetime.date(cur_year, month, 1)
    end_date = datetime.date(cur_year, month, calendar.monthrange(cur_year, month)[1])
    report = db_connect.attendance_by_date(cur, start_date, end_date)
    if len(report) == 0:
        messagebox.showinfo("Attendance report by month", f'No attendance was registered for {month}-{cur_year}.')
    else:
        create_report_file(f'Attendance report for {month}-{cur_year}.csv', report)
        messagebox.showinfo("Attendance report by month", 'Check your library for the report.')


def report_by_hour(cur, start_date: datetime, hour=None):
    hour = datetime.datetime.strptime(hour, "%H:%M").time()
    report = db_connect.attendance_after_hour(cur, hour, start_date)
    hour = hour.strftime("%H.%M")
    if len(report) == 0:
        messagebox.showinfo("Attendance report by hour", f'No attendance was registered after {hour} from {start_date}.')
    else:
        create_report_file(f'Attendance report after {hour} from {start_date}.csv', report)
        messagebox.showinfo("Attendance report by hour", f'Check your library for the report.')


def report_by_dates(cur, start_date: datetime, end_date: datetime):
    report = db_connect.attendance_by_date(cur, start_date, end_date)
    if len(report) == 0:
        messagebox.showinfo("Attendance report between dates", f'No attendance was registered between {start_date} and {end_date}.')
    else:
        create_report_file(f'Attendance report between {start_date} and {end_date}.csv', report)
        messagebox.showinfo("Attendance report between dates", f'Check your library for the report.')


def create_report_file(path, lst):  # A helper function, creates the report files - attendance and reports
    with open(path, mode='w', newline='') as attend_file:
        attend_writer = csv.writer(attend_file, delimiter=',')
        attend_writer.writerow(['Date', 'Time', 'employee id', 'name'])
        for attendance in lst:
            attend_writer.writerow(
                [attendance[0], attendance[1].strftime("%H:%M:%S"), attendance[2], attendance[3]])

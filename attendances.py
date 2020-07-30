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


def report_by_month(cur, month=None):
    now = datetime.datetime.now()
    cur_month = now.month
    cur_year = now.year
    while month is None:
        try:
            month = int(input('Please enter the month for the report or -1 for current month: '))
            if month == -1:
                month = cur_month
            elif not 1 <= month <= 12:
                raise ValueError
            else:
                if month > cur_month:
                    cur_year -= 1
        except ValueError:
            print('The month should be an number between 1 and 12.')
            month = None
    start_date = datetime.date(cur_year, month, 1)
    end_date = datetime.date(cur_year, month, calendar.monthrange(cur_year, month)[1])
    report = db_connect.attendance_by_date(cur, start_date, end_date)
    if len(report) == 0:
        print(f'No attendance was registered for {month}-{cur_year}.')
    else:
        create_report_file(f'Attendance report for {month}-{cur_year}.csv', report)
        print(f'Check your library for the report.')


def report_by_hour(cur, hour=None):
    while hour is None:
        try:
            time = input('Please enter the hour for the report (HH:MM) : ')
            hour = datetime.datetime.strptime(time, "%H:%M").time()
            assert datetime.time(6, 0) <= hour <= datetime.time(19, 00)
        except ValueError:
            print('The time should be int the format HH:MM.')
            hour = None
        except AssertionError:
            print('Please enter a valid work time, between 6am and 7pm.')
            hour = None
    print('Lets enter start date for the report (end date is today): ')
    start_date = enter_date()
    report = db_connect.attendance_after_hour(cur, hour, start_date)
    hour = hour.strftime("%H.%M")
    if len(report) == 0:
        print(f'No attendance was registered after {hour} from {start_date}.')
    else:
        create_report_file(f'Attendance report after {hour} from {start_date}.csv', report)
        print(f'Check your library for the report.')


def enter_date():
    while True:
        try:
            day, month, year = input('Please enter a date(dd-mm-yyyy): ').split('-')
            date = datetime.date(int(year), int(month), int(day))
            assert date < datetime.datetime.now().date()
        except ValueError:
            print('Please enter valid integer numbers.')
        except AssertionError:
            print('Only past dates are valid.')
        else:
            return date


def report_by_dates(cur, start_date=None, end_date=None):
    if start_date is None:
        print('Lets enter start date: ')
        start_date = enter_date()
    if (end_date is not None) and end_date < start_date:
        print(f'End date should be later than {start_date}.')
    if end_date is None:
        print('Lets enter end date: ')
    while end_date is None or end_date < start_date:
        try:
            end_date = enter_date()
            assert start_date <= end_date
        except AssertionError:
            print(f'End date should be later than {start_date}.')
        else:
            report = db_connect.attendance_by_date(cur, start_date, end_date)
            if len(report) == 0:
                print(f'No attendance was registered between {start_date} and {end_date}.')
            else:
                create_report_file(f'Attendance report between {start_date} and {end_date}.csv', report)
                print(f'Check your library for the report.')


def create_report_file(path, lst):  # A helper function, creates the report files - attendance and reports
    with open(path, mode='w', newline='') as attend_file:
        attend_writer = csv.writer(attend_file, delimiter=',')
        attend_writer.writerow(['Date', 'Time', 'employee id', 'name'])
        for attendance in lst:
            attend_writer.writerow(
                [attendance[0], attendance[1].strftime("%H:%M:%S"), attendance[2], attendance[3]])

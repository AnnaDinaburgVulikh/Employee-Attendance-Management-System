import csv
import datetime
import os


class Attendance:
    path_attendance = 'attendance_log.csv'

    def __init__(self, emp_id: str, name: str, date=None, time=None):
        self.id = str(emp_id)
        self.name = name
        if date is None or time is None:
            now = datetime.datetime.now()
            self.date = now.date()
            self.time = now.time()
        else:
            self.date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            self.time = datetime.datetime.strptime(time, "%H:%M:%S").time()

    def __str__(self):
        return f'{self.name}, ID num: {self.id} arrived at {self.time} on {self.date}'

    @staticmethod
    def load_attendance_list(user_path=None):
        # Used before the class instance is formed or used as a helper for adding employees from file
        if user_path is None:
            user_path = Attendance.path_attendance
        while True:
            try:  # Should check if the file exists.
                if user_path is None:
                    user_path = input("Enter the path of your file or -1 to create one: ")
                if user_path == '-1':
                    create_report_file(Attendance.path_attendance, [])
                    user_path = Attendance.path_attendance
                assert os.path.exists(user_path)
                if user_path != Attendance.path_attendance:
                    Attendance.path_attendance = user_path
            except AssertionError:
                print("I did not find the file at: " + str(user_path))
                user_path = None
            else:
                with open(user_path, mode='r') as csv_file:
                    lst = []
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    if csv_reader is None:
                        print('The file was empty')
                        return lst
                    line_count = 0
                    for row in csv_reader:
                        if line_count != 0:
                            if len(row) == 4:
                                lst.append(Attendance(row[2], row[3], row[0], row[1]))
                            else:
                                print(f'The data in row {line_count} is partially missing.')
                                return None
                        line_count += 1
                    return lst

    @staticmethod
    def enter_id(e_id=None):
        while True:
            try:
                if e_id is None:
                    e_id = str(input('Please enter employee ID (123456789): '))
                if not e_id.isalnum() or len(e_id) != 9:
                    raise ValueError
            except ValueError:
                print('The ID should be an integer of 9 digits.')
                e_id = None
            else:
                return e_id

    @staticmethod
    def mark_attendance(employee_dic: dict, e_id=None):
        e_id = Attendance.enter_id(e_id)
        if e_id in employee_dic:
            attend_list = Attendance.load_attendance_list(Attendance.path_attendance)
            attend_list.append(Attendance(e_id, employee_dic[e_id].name))
            create_report_file(Attendance.path_attendance, attend_list)
            print("Marked an attendance for id %s." % e_id)
        else:
            print('There is no employee with this ID in our company.')

    @staticmethod
    def attendance_report_by_id(attend_list, employee_dic):
        e_id = Attendance.enter_id()
        if e_id in employee_dic:
            report = []
            for attend in attend_list:
                if attend.id == e_id:
                    report.append(attend)
            if len(report) == 0:
                print(f'No attendance was registered for employee {e_id}.')
            else:
                create_report_file(f'Attendance report for employee {e_id}.csv', report)
                print(f'Check your library for the report.')
        else:
            print('There is no employee with this ID in our company.')

    @staticmethod
    def report_by_month(attend_list, month=None):
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
        report = []
        for attend in attend_list:
            if attend.date.month == month and attend.date.year == cur_year:
                report.append(attend)
        if len(report) == 0:
            print(f'No attendance was registered for {month}:{cur_year}.')
        else:
            create_report_file(f'Attendance report for {month}:{cur_year}.csv', report)
            print(f'Check your library for the report.')

    @staticmethod
    def report_by_hour(attend_list, hour=None):
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
        start_date = Attendance.enter_date()
        report = []
        for attend in attend_list:
            if hour <= attend.time and attend.date >= start_date:
                report.append(attend)
        hour = hour.strftime("%H.%M")
        if len(report) == 0:
            print(f'No attendance was registered after {hour} from {start_date}.')
        else:
            create_report_file(f'Attendance report after {hour} from {start_date}.csv', report)
            print(f'Check your library for the report.')

    @staticmethod
    def enter_date():
        while True:
            try:
                day, month, year = input('Please enter a date(dd-mm-yyyy): ').split('-')
                date = datetime.date(int(year), int(month), int(day))
                assert date > datetime.datetime.now()
            except ValueError:
                print('Please enter valid integer numbers.')
            except AssertionError:
                print('Only past dates are valid.')
            else:
                return date

    @staticmethod
    def report_by_dates(attend_list, start_date=None, end_date=None):
        if start_date is None:
            print('Lets enter start date: ')
            start_date = Attendance.enter_date()
        if (end_date is not None) and end_date < start_date:
            print(f'End date should be later than {start_date}.')
        if end_date is None:
            print('Lets enter end date: ')
        while end_date is None or end_date < start_date:
            try:
                end_date = Attendance.enter_date()
                assert start_date <= end_date
            except AssertionError:
                print(f'End date should be later than {start_date}.')
            else:
                report = []
                for attend in attend_list:
                    if start_date <= attend.date <= end_date:
                        report.append(attend)
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
                [attendance.date, attendance.time.strftime("%H:%M:%S"), attendance.id, attendance.name])
